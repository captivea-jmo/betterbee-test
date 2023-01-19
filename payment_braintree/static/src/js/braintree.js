odoo.define('payment_braintree.payment_braintree', function(require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');

    var qweb = core.qweb;
    var _t = core._t;

    if ($.blockUI) {
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
        $.blockUI.defaults.baseZ = 1050;
    }

    var BraintreePaymentForm = Widget.extend({
        _removeInputName: ['tx_url', 'acquirer_id', 'merchant_account_id', 'enable3ds', 'givenName', 'surname', 'phoneNumber', 'streetAddress', 'locality', 'region', 'postalCode', 'countryCodeAlpha2', 'paypalEnabled'],
        init: function() {
            this.dropin = undefined;
            this.$form = $('form[provider="braintree"]');
            this.$payBtn = undefined;
            this.merchant_account_id = $('input[data-provider="braintree"]').data('merchant_account_id');;
            this.formData = {};
            this.priceText = $('.showPrice').text().trim();
            this._initBlockUI(_t("Loading Braintree JS..."));
            this.start();
        },
        start: function() {
            var self = this;
            self._formOperations();
            var braintree_js = "https://js.braintreegateway.com/web/dropin/1.20.3/js/dropin.min.js";
            if (self.formData.brtVersion==='old') {
                braintree_js = "https://js.braintreegateway.com/js/braintree-2.32.1.min.js";
            }
            return ajax.loadJS(braintree_js).then(function() {
                self._initBlockUI(_t("Initializing Payment..."));
                self._getAuthorizationToken();
            });
        },
        _formOperations: function() {
            this.formData = this._getFormData();
            for (var i = 0; i < this._removeInputName.length; i++) {
                this.$form.find("input[name='"+this._removeInputName[i]+"']").remove();
            }
            this.$form.find('.showPrice').remove();
            this.$form.attr("action", this.formData.tx_url);
        },
        _getAuthorizationToken: function() {
            var self = this;
            self._initBlockUI(_t("Getting Authorization Token..."));
            ajax.jsonRpc('/payment/braintree/get_authorization', 'call', {
                'merchant_account_id': self.merchant_account_id,
                'acquirer_id': self.formData.acquirer_id,
            }).then(function (result) {
                if (result.status) {
                    self._renderDropinUi(result.token);
                } else {
                    self._showErrorMessage(_t('Braintree Error'), result.message);
                }
            });
        },
        _renderDropinUi: function(token) {
            var self = this;
            self._initBlockUI(_t("Processing..."));
            var enable3ds = this.formData.enable3ds;
            var paypalEnabled = this.formData.paypalEnabled;
            if (enable3ds === 'True') {
                enable3ds = true;
            } else {
                enable3ds = false;
            }

            if (paypalEnabled === 'True') {
                paypalEnabled = true;
            } else {
                paypalEnabled = false;
            }
            return ajax.loadXML('/payment_braintree/static/src/xml/braintree.xml', qweb).then(function() {
                var $modal_html = $(qweb.render('payment_braintree.dropin_ui', {
                    'brt_version': self.formData.brtVersion,
                }));
                $modal_html.appendTo($('body')).modal({keyboard: false, backdrop: 'static'});
                $("#braintree_dropin_modal").on('hidden.bs.modal', function () {
                    self._dropinTeardown();
                });

                self.$payBtn = $('#braintree-pay-btn');
                if (self.formData.brtVersion==='old') {
                    self._oldDropinUi(token, enable3ds);
                } else {
                    self._setupDropinUi(token, enable3ds, paypalEnabled).then(function(instance) {
                        self.dropin = instance;
                        self._bindPayNowEvent();
                        self._enablePayNow();
                        self._revokeBlockUI();
                    }).catch(function (err) {
                        console.log('component error:', err);
                    });
                }
            });
        },
        _setupDropinUi: function(token, enable3ds, paypalEnabled) {
            var dropin_create_data = {
                authorization: token,
                container: '#braintree-dropin-ui',
                threeDSecure: enable3ds,
            }
            if (paypalEnabled) {
                dropin_create_data = $.extend(dropin_create_data, {
                    paypal: {
                        flow: 'checkout',
                        buttonStyle: {
                          color: 'blue',
                          shape: 'rect',
                          size: 'medium'
                        }
                    }
                }); 
            }
            return braintree.dropin.create(dropin_create_data);
        },
        _oldDropinUi: function(token, enable3ds) {
            var self = this;
            var client = new braintree.api.Client({
                clientToken: token
            });

            braintree.setup(token, "dropin", {
                container: 'braintree-dropin-ui',
                onError: function(result) {
                    self._showErrorMessage(_t('Braintree Error!'), result.message);
                    return false;
                },
                onReady: function(integration) {
                    self._enablePayNow();
                    self._revokeBlockUI();
                },
                onPaymentMethodReceived: function (obj) {
                    self._disablePayNow();
                    if (enable3ds) {
                        if (obj.type === 'CreditCard') {
                            client.verify3DS({
                                amount: self.formData.amount,
                                creditCard: obj.nonce,
                            }, function (err, response) {
                                if (!err) {
                                    self._appendAndSubmitForm(response);
                                } else {
                                    self._enablePayNow();
                                    self._showErrorMessage(_t('Braintree Error'), err.message);
                                    return false;
                                }
                            });
                        } else {
                            self._appendAndSubmitForm(obj);
                        }
                    } else {
                        self._appendAndSubmitForm(obj);
                    }
                },
            });
        },
        _enablePayNow: function() {
            this.$payBtn.html(qweb.render('payment_braintree.enable_text', {'price_text': this.priceText}));
            this.$payBtn.removeClass('disabled').removeAttr("disabled");
        },
        _disablePayNow: function() {
            this.$payBtn.html(qweb.render('payment_braintree.disable_text', {'price_text': this.priceText}));
            this.$payBtn.addClass('disabled').prop("disabled", "disabled");
        },
        _bindPayNowEvent: function() {
            var self = this;
            this.$payBtn.on('click', function(ev) {
                self._disablePayNow();
                self.dropin.requestPaymentMethod({
                    threeDSecure: {
                        amount: self.formData.amount,
                        email: self.formData.email,
                        billingAddress: {
                            givenName: self.formData.givenName,
                            surname: self.formData.surname,
                            phoneNumber: self.formData.phoneNumber.replace(/[\(\)\s\-]/g, ''),
                            streetAddress: self.formData.streetAddress,
                            locality: self.formData.locality,
                            region: self.formData.region,
                            postalCode: self.formData.postalCode,
                            countryCodeAlpha2: self.formData.countryCodeAlpha2
                        }
                    }
                }, function(err, payload) {
                    if (err) {
                        console.log('tokenization error:');
                        console.log(err);
                        self.dropin.clearSelectedPaymentMethod();
                        self._enablePayNow();
                        return;
                    }

                    if (payload.liabilityShiftPossible && !payload.liabilityShifted) {
                        console.log('Liability did not shift', payload);
                        self._dropinTeardown();
                        self._showErrorMessage(_t('3DS Error'), _t('3D authentication failed, Liability did not shift.'));
                        return;
                    }

                    console.log('verification success:', payload);
                    self._appendAndSubmitForm(payload);
                });
            });
        },
        _appendAndSubmitForm: function(payload) {
            this.$form.append(qweb.render('payment_braintree.payload_data', {
                'payload': payload,
                'merchant_account_id': this.merchant_account_id
            }));
            this.$form.submit();
        },
        _dropinTeardown: function() {
            this.dropin.teardown(function(err) {
                if (err) {
                    console.error('An error occurred during teardown:', err);
                }
                $('#braintree_dropin_modal').remove();
            });
        },
        _showErrorMessage: function(title, message) {
            this._revokeBlockUI();
            return new Dialog(null, {
                title: _t('Error: ') + _.str.escapeHTML(title),
                size: 'medium',
                $content: "<p>" + (_.str.escapeHTML(message) || "") + "</p>" ,
                buttons: [
                {text: _t('Ok'), close: true}]}).open();
        },
        _getFormData: function() {
            var data = {}
            this.$form.find('input').each(function() {
                data[$(this).attr('name')] = $(this).val();
            });
            return data
        },
        _initBlockUI: function(message) {
            if ($.blockUI) {
                if (message) {
                    $.blockUI({
                        'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                                '    <br />' + message +
                                '</h2>'
                    });
                } else {
                    $.blockUI({
                        'message': '',
                    });
                }
            }
            $("#o_payment_form_pay").attr('disabled', 'disabled');
        },
        
        _revokeBlockUI: function() {
            if ($.blockUI) {
                $.unblockUI();
            }
            $("#o_payment_form_pay").removeAttr('disabled');
        },
    });

    new BraintreePaymentForm();
});
