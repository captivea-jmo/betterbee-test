// odoo.define('my_cart_popup.website_sale', function (require) {
    odoo.define('my_cart_popup.website_cart_popup', function (require) {
        "use strict";
        console.log("pop test")
    //     var base = require('web_editor.base');
        var ajax = require('web.ajax');
        var core = require('web.core');
    //     var utils = require('web.utils');
    //     var _t = core._t;
        var $cart_li_a = $('#top_menu a[href$="/shop/cart"]');
        $cart_li_a.attr({'data-original-title': 'My Cart'})
        .on('click', function(e) {
            e.preventDefault();
            $(this).popover('show');
        });
    
    
        $(function(){
            $('.tis_add_to_cart').each(function () {
            var oe_website_sale = this;
            $(oe_website_sale).on('click', function (event) {
                if (!event.isDefaultPrevented() && !$(this).is(".disabled")) {
                    event.preventDefault();
                    var $btn = $(this);
                    var $cart_li_a = $('#top_menu a[href$="/shop/cart"]');
                    var $form = $btn.closest('form');
                    var pid = $form.find('.product_id').val() || $form.find('input[name="product_id"]:first').val();
                    var qty = $form.find('.quantity').val();
                    var no_variant_attributes=[];
                    var custom_attribute_values=[];
                    var len = $form.find('.no_variant').length;
                    var custom_len = $form.find('.variant_custom_value').length;
                    if(len>0){
                        for (var i = 0; i < len; i++) {
                            var key='key_'+i
                            var obj = {}
                            if ($form.find('.no_variant')[i].tagName === 'SELECT'){
                                 obj= {
                                          custom_product_template_attribute_value_id : $form.find('.no_variant')[i].options[$form.find('.no_variant')[i].selectedIndex].getAttribute("data-value_id"),
                                          attribute_value_name : $form.find('.no_variant')[i].options[$form.find('.no_variant')[i].selectedIndex].getAttribute("data-value_name"),
                                          value : $form.find('.no_variant')[i].options[$form.find('.no_variant')[i].selectedIndex].getAttribute("value"),
                                          attribute_name : $form.find('.no_variant')[i].options[$form.find('.no_variant')[i].selectedIndex].getAttribute("data-attribute_name")
                                      };
                                 no_variant_attributes.push(obj)
                            }
                            else{
                                    if ($form.find('.no_variant')[i].type === 'radio' && $form.find('.no_variant')[i].checked){
                                            console.log("$form.getElementsByClassName.tagName", $form.find('.no_variant')[i].checked)
                                           obj= {
                                                    custom_product_template_attribute_value_id : $form.find('.no_variant')[i].getAttribute("data-value_id"),
                                                    attribute_value_name : $form.find('.no_variant')[i].getAttribute("data-value_name"),
                                                    value : $form.find('.no_variant')[i].getAttribute("value"),
                                                    attribute_name : $form.find('.no_variant')[i].getAttribute("data-attribute_name")
                                                };
                                          no_variant_attributes.push(obj)
                                    }
                            }
                        }
                     }
                     if(custom_len>0){
                            for (var j = 0; j < custom_len; j++) {
                                var cus_key='cus_key_'+j
                                var custom_obj = {
                                    custom_product_template_attribute_value_id : parseInt($form.find('.variant_custom_value')[j].getAttribute("data-custom_product_template_attribute_value_id"), 10),
                                    attribute_value_name : $form.find('.variant_custom_value')[j].getAttribute("data-attribute_value_name"),
                                    custom_value : $form.find('.variant_custom_value')[j].value,
                                }
                                custom_attribute_values.push(custom_obj)
                            }
                     }
                    if(!pid){
                        return false;
                    }
                    var loading = '<span class="fa fa-cog fa-spin v_loading"/>';
                    $btn.prepend('<span class="fa fa-cog fa-spin v_loading"/>');
                    console.log("_popoverRPC")
                    ajax.jsonRpc("/shop/cart/update_json_popup", 'call', {
                            'product_id': parseInt(pid, 10),
                            'add_qty': parseInt(qty) || 1,
                            'no_varient': no_variant_attributes || [],
                            'custom_attribute': custom_attribute_values || [],
                        }).then(function (data) {
    
                            $cart_li_a.find('.my_cart_quantity').text(data.cart_quantity);
                              if(parseInt(data.cart_quantity)==1)
                                    {
                                     setTimeout(function() {
                                        location.reload();
                                    }, 2000);
                                    }
                            console.log("_popoverRPC")
                            var _popoverRPC = $.get("/shop/cart", {'type': 'popover'})
                                .then(function (data) {
                                    $cart_li_a.parents('#my_cart').removeClass('hidden');
                                    $cart_li_a.data("bs.popover").config.content =  data;
                                    $cart_li_a.length=$cart_li_a.length;
                                    $cart_li_a.popover("show");
                                    $(this).find(loading);
                                    $btn.find('.v_loading').remove();
                                    $(".popover").on("mouseleave", function () {
                                        console.log("Set mouseleave")
                                        $cart_li_a.trigger('mouseleave');
                                    });
                                    setTimeout(function() {
                                        console.log("Set timeout")
                                        $cart_li_a.popover("hide");
                                    }, 2000);
                                });
                        });
                }
                if ($(this).hasClass('a-submit-disable')){
                    $(this).addClass("disabled");
                }
                if ($(this).hasClass('a-submit-loading')){
                    var loading = '<span class="fa fa-cog fa-spin"/>';
                    var fa_span = $(this).find('span[class*="fa"]');
                    if (fa_span.length){
                        fa_span.replaceWith(loading);
                    }
                    else{
                        $(this).append(loading);
                    }
                }
        return false;
    
            });
            });
    
        });
    
    });