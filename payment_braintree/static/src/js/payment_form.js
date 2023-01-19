odoo.define('payment_braintree.payment_form', function (require) {
    "use strict";

    var core = require('web.core');
    var PaymentForm = require('payment.payment_form');
    var ajax = require('web.ajax');

    var _t = core._t;

    PaymentForm.include({
        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
            });
            this.braintree_checked = false;
            this.braintree_available = false;
        },
        updateNewPaymentDisplayStatus: function () {
            var self = this;
            var sup = this._super.apply(this, arguments);
            var $payBtn = $('#o_payment_form_pay');
            var $checkedRadio = this.$('input[type="radio"]:checked');

            if ($checkedRadio.length !== 1) {
                return;
            }
            var provider = $checkedRadio.data('provider');
            if (provider === 'braintree' && (!this.braintree_available)) {
                $payBtn.hide();
            } else {
                $payBtn.show();
            }
            if (provider === 'braintree' && (!this.braintree_checked)) {
                self.braintree_checked = true;
                var $parentDiv = $checkedRadio.parent().parent();
                $parentDiv.addClass('check_availability_loader')
                .append('<i class="fa fa-spinner fa-spin fa-2x"/>');
                ajax.jsonRpc('/payment/braintree/check_availability', 'call', {
                    'acquirer_id': $checkedRadio.data('acquirer-id'),
                    'currency_id': self.getParameterByName('currency_id')
                }).then(function (data) {
                    if (data.status) {
                        $checkedRadio.attr('data-merchant_account_id', data.merchant_account_id);
                        self.braintree_available = true;
                        $payBtn.show();
                    } else {
                        $parentDiv.addClass('braintree_disabled');
                        self.displayError(_t('Braintree Payment Error'), data.message)
                    }
                    $parentDiv.removeClass('check_availability_loader')
                    .find('.fa-spinner')
                    .remove();
                    return sup;
                });
            } else {
                return sup;
            }
        },
        payEvent: function (ev) {
            ev.preventDefault();
            var $checkedRadio = this.$('input[type="radio"]:checked');
            var provider = $checkedRadio.data('provider');
            if (provider !== 'braintree') {
                return this._super.apply(this, arguments);
            }
            if (provider === 'braintree' && this.braintree_available) {
                $checkedRadio.parent().parent().addClass('braintree_disabled');
                return this._super.apply(this, arguments);
            }
            this.displayError(_t('Braintree Payment Error'), _t('Braintree not available for this order.'))
            return;
        },
        getParameterByName: function(name, url) {
            if (!url) url = window.location.href;
            name = name.replace(/[\[\]]/g, '\\$&');
            var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
                results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, ' '));
        }
    });
});
