# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShGdprDataCategory(models.Model):
    _name = "sh.gdpr.data.category"
    _description = "GDPR Category"
    _order = "id desc"

    def default_website(self):
        company_id = self.env.company.id

        if self._context.get("default_company_id"):
            company_id = self._context.get("default_company_id")

        domain = [("company_id", "=", company_id)]
        return self.env["website"].search(domain, limit=1)

    name = fields.Char("Title", required=True)
    image_img = fields.Image(readonly=False)
    active = fields.Boolean("Active")
    description = fields.Text("Short Description")
    redirect_url = fields.Char("Redirect Url")
    type = fields.Selection([
        ("user", "User"),
        ("address", "Address")
    ], "Type")
    website_id = fields.Many2one("website", default=default_website)
    company_id = fields.Many2one(
        "res.company", string="Company",
        default=lambda self: self.env.company)
