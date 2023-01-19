odoo.define('cap_website_products_attributes_design.VariantMixin', function (require) {
'use strict';

var VariantMixin = require('sale.VariantMixin');
var core = require('web.core');
var publicWidget = require('web.public.widget');

publicWidget.registry.VariantButtons = publicWidget.Widget.extend(VariantMixin, {
    selector: '#product_detail',

    events: _.extend({}, VariantMixin.events || {}, {
        'click .attribute-selector': 'onClickVariantChange',
        'hover #zoom_custom': 'onHoverImage',
        'change [data-attribute_exclusions]': 'onChangeVariant',
    }),

    onChangeVariant: function (ev) {
        var $parent = $(ev.target).closest('.js_product');
        var $newel = $("#product_detail").find("a[data-attribute_value='" + parseInt(ev.target.value) + "']")
        if ($newel.length > 0){
            $($newel).parent().parent().find("a.attribute-selector.selected").removeClass('selected')
            $($newel).addClass('selected')
        }
        if (!$parent.data('uniqueId')) {
            $parent.data('uniqueId', _.uniqueId());
        }
        this._throttledGetCombinationInfo($parent.data('uniqueId'))(ev);
    },

    onClickVariantChange: function (ev) {
        $(ev.target).parent().parent().find("a.attribute-selector.selected").removeClass('selected')
        $(ev.target).addClass('selected')
        var value = parseInt($(ev.target).attr('data-attribute_value'))
        var data = $(this.target).find("input[value='" + value + "']");
        if (data.length > 0){
            data[0].checked = true
            if ($(data).parent()[0].tagName == 'LABEL'){
                $(this.target).find("label.css_attribute_color.active").removeClass('active')
                $(data).parent().addClass('active')
            }
        }else{
            $(this.target).find("option[value='" + value + "']").prop("selected", true);
        }
    },

    onHoverImage: function (ev) {
        $("#zoom_custom").addClass('transition');
    }, function() {
            $("#zoom_custom").removeClass('transition');
    },


});

publicWidget.registry.WebsiteSale.include({
    _updateProductImage: function ($productContainer, displayImage, productId, productTemplateId, newCarousel, isCombinationPossible) {
        var $carousel = $productContainer.find('.carousel');
        var self = this

        $productContainer.find('.carousel').each(function () {
            var $el = $(this);
            if (window.location.search.indexOf('enable_editor') === -1) {
                var $newCarousel = $(newCarousel);
                $el.after($newCarousel);
                $el.remove();
                $el = $newCarousel;
                $el.carousel(0);
                self._startZoom();
                self.trigger_up('widgets_start_request', {$target: $el});
            }
            $el.toggleClass('css_not_available', !isCombinationPossible);
        });
    },
})

});
