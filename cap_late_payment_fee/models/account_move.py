from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    fee_applied = fields.Boolean(string="Fee applied", default=False)


    def lateFee(self):
        for record in self:
            wasPosted = False
            if record.fee_applied == False:
                if record.state == 'posted':
                    record['state'] = 'draft'
                    wasPosted = True

                late_fee_price = record['amount_untaxed']*record['partner_id']['late_fee_price']
                product = record.env['product.template'].search([('name','=','Late fee')])

                # line = record.env['account.move.line'].create({
                #     'product_id':product.id,
                #     'quantity':1,
                #     'price_unit':late_fee_price,
                #     'account_id':record.env['account.account'].search([('name', '=', 'Product Sales')], limit=1).id,
                #     'move_id':record.id,
                #     'currency_id':record.env['res.currency'].search([('name','=','USD')]).id
                #
                # })

                record.write({'line_ids': [
                            (0, None, {
                                'name': 'Late payment fee ',
                                'account_id': record.env['account.account'].search([('name', '=', 'Product Sales')], limit=1).id,
                                'debit': 0.0,
                                'credit': late_fee_price,
                                'exclude_from_invoice_tab': True,
                            }),
                            (0,None, {
                                'name': 'Late payment receivables',
                                'product_id':product.id,
                                'quantity': 1,
                                'account_id': record.env['account.account'].search([('name', '=', 'Account Receivable')], limit=1).id,
                                'credit': 0.0,
                                'debit': late_fee_price
                            })
                        ]
                })

                for line in record.invoice_line_ids:
                    if line.product_id.name == "Late fee":
                        if line.price_unit < 0:
                            line['price_unit'] = (line.price_unit)*-1

                record['fee_applied'] = True
                if wasPosted:
                    record['state'] = 'posted'
