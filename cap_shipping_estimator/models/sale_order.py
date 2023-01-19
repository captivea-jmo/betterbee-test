from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _find_delivery_carrier(self, category):
        if category.parent_id:
            categ = category.parent_id
            if categ.delivery_carrier_ids:
                return categ
            else:
                return self._find_delivery_carrier(categ)
        return False        

    def action_open_delivery_wizard(self):
        select_carriers = self.env['delivery.carrier']
        # carriers = self.env['delivery.carrier'].search(
        #     ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])
        # available_carrier = carriers.available_carriers(
        #     self.partner_shipping_id) if self.partner_id else carriers
        common_ship = []
        for category in self.order_line.mapped('product_id.categ_id').filtered(lambda cat: cat.name != 'Deliveries'):
            if category.delivery_carrier_ids:
                common_ship.append(category.delivery_carrier_ids.ids)
            else:
                categ = self._find_delivery_carrier(category)
                if categ:
                    common_ship.append(categ.delivery_carrier_ids.ids)

        elements_in_all = list(set.intersection(*map(set, common_ship)))
        available_carrier = self.env['delivery.carrier'].search([('id', 'in', elements_in_all)])
        for carrier in available_carrier:
            select_carriers |= carrier
            _logger.info("######### Carrier Name -->  %r #########", carrier.name)
            vals = carrier.rate_shipment(self)
            if vals.get('success'):
                carrier.delivery_cost = vals['carrier_price']
        view_id = self.env.ref('delivery.choose_delivery_carrier_view_form').id
        if self.env.context.get('carrier_recompute'):
            name = _('Update shipping cost')
            carrier = self.carrier_id
        else:
            name = _('Add a shipping method')
            carrier = (
                    self.with_company(self.company_id).partner_shipping_id.property_delivery_carrier_id
                    or self.with_company(
                self.company_id).partner_shipping_id.commercial_partner_id.property_delivery_carrier_id
                 or available_carrier and available_carrier[0]
            )

        select_carriers = select_carriers.sorted(lambda line: line.delivery_cost).filtered(
            lambda line: line.delivery_cost >= 0)
        if not select_carriers:
            raise UserError("Please select at least one common delivery method on the products category of every product.")
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'choose.delivery.carrier',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_carrier_id': carrier.id,
                'default_select_carrier_ids': [(6, 0, select_carriers.ids)]
            }
        }

    def _get_delivery_methods(self):
        address = self.partner_shipping_id
        select_carriers = self.env['delivery.carrier']

        # searching on website_published will also search for available website (_search method on computed field)
        common_ship = []
        for category in self.order_line.mapped('product_id.categ_id').filtered(lambda cat: cat.name != 'Deliveries'):
            if category.delivery_carrier_ids:
                common_ship.append(category.delivery_carrier_ids.ids)
            else:
                categ = self._find_delivery_carrier(category)
                if categ:
                    common_ship.append(categ.delivery_carrier_ids.ids)
                    
        elements_in_all = []
        if common_ship != []:
            elements_in_all = list(set.intersection(*map(set, common_ship)))

        available_carrier = self.env['delivery.carrier'].search([
            ('id', 'in', elements_in_all), ('website_published', '=', True)]).available_carriers(address)
        for carrier in available_carrier:
            select_carriers |= carrier

            if self._context.get('rate'):
                vals = carrier.rate_shipment(self)
                if vals.get('success'):
                    if carrier.delivery_cost != vals['carrier_price']:
                        carrier.delivery_cost = vals['carrier_price']

        select_carriers = available_carrier.sorted(lambda line: line.delivery_cost).filtered(
            lambda line: line.delivery_cost >= 0)
        return select_carriers
