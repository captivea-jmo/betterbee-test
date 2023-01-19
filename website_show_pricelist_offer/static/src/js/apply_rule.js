odoo.define('website_show_pricelist_offer', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteSale.include({
        start: function () {
            var def = this._super.apply(this, arguments);
            setTimeout(function () {
                var product_id = $('input[name="product_id"]').val()
                var product_qty = $('input[name="add_qty"]').val()
                $(".variant_offer").each(function () {
                    if (product_id && product_qty) {
                        if ((parseInt($(this).data('product_id')) == product_id) && (parseFloat($(this).data('quantity')) <= parseFloat(product_qty))) {
                            $(this).prop("checked", true);
                            return false;
                        }
                        else {
                            $(this).prop("checked", false);
                        }
                    }
                });
            }, 500);
            return def;
        },

        _checkExclusions: function ($parent, combination) {
            var def = this._super.apply(this, arguments);
            setTimeout(function () {
                var product_id = $('input[name="product_id"]').val()
                var product_qty = $('input[name="add_qty"]').val()
                $(".variant_offer").each(function () {
                    if (product_id && product_qty) {
                        if ((parseInt($(this).data('product_id')) == product_id) && (parseFloat($(this).data('quantity')) <= parseFloat(product_qty))) {
                            $(this).prop("checked", true);
                            console.log("TR", $($(this).closest("tr")))
                            return false;
                        }
                        else {
                            $(this).prop("checked", false);
                        }
                    }
                });
            }, 500);
            return def;
        },
    });

    $(function () {
        $(".variant_offer").click(function () {
            if ($(this).is(':checked')) {
                var rule = $(this).data('rule')
                var attr = rule.attribute_values.join()
                if (rule) {
                    window.location.href = '/shop/' + rule.product_tmpl_id + '?add_qty=' + parseInt(rule.qty) + '#attr=' + attr
                }
            }
        });
        $("#clear_selection").click(function () {
            $("#collapse1").removeClass("show")
            $("#accordion_link").addClass("collapsed")
            $("#accordion_link").attr("aria-expanded","false")
            $("input[name='add_qty']").val(1)
        })
    });
});