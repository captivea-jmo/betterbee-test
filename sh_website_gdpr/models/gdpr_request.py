# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import base64


class ShGdprDataCategory(models.Model):
    _name = "sh.gdpr.data.request"
    _description = "GDPR Category"
    _order = "id desc"

    name = fields.Char("Name", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Customer", required=True)
    data_categ_id = fields.Many2one(
        "sh.gdpr.data.category", string="Data Category", required=True)
    attachment = fields.Binary(string="Attachments", attachment=True)
    request_type = fields.Selection([
        ("download", "Download"),
        ("delete", "Delete")
    ], "Request Type", required=True)
    state = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ], string="Status", default="pending", readonly=True
    )
    website_id = fields.Many2one("website", related="data_categ_id.website_id")
    data_wiped = fields.Boolean("Data Wiped")
    cancel_reason = fields.Text("Cancel Reason")
    company_id = fields.Many2one(
        "res.company", "Company", readonly=True,
        required=True, index=True, default=lambda self: self.env.company)

    def done_btn(self):
        if(
            self.request_type == "download" and
            self.website_id.is_enable_email and
            self.website_id.is_customer
        ):
            url = ""
            base_url = self.env["ir.config_parameter"].sudo(
            ).get_param("web.base.url")
            url = base_url + "/my/gdpr_request"
            ctx = {
                "customer_url": url,
            }
            template__download_id = self.env["ir.model.data"].get_object(
                "sh_website_gdpr", "email_template_download_success")
            _ = self.env["mail.template"].browse(template__download_id.id).with_context(
                ctx).send_mail(self.id, notif_layout="mail.mail_notification_light", force_send=True)

        elif(
            self.request_type == "delete" and
            self.website_id.is_enable_email and
            self.website_id.is_customer
        ):
            url = ""
            base_url = self.env["ir.config_parameter"].sudo(
            ).get_param("web.base.url")
            url = base_url + "/my/gdpr_request"
            ctx = {
                "customer_url": url,
            }
            template__download_id = self.env["ir.model.data"].get_object(
                "sh_website_gdpr", "email_template_delete_success")
            _ = self.env["mail.template"].browse(template__download_id.id).with_context(
                ctx).send_mail(
                    self.id,
                    notif_layout="mail.mail_notification_light",
                    force_send=True)
        self.write({"state": "done"})

    def data_btn(self):
        content, content_type = self.env.ref(
            "sh_website_gdpr.action_report_gdpr_data_download")._render_qweb_pdf(self.id)
        pdf_data = base64.b64encode(content)
        self.attachment = pdf_data

    def wipe_btn(self):
        if self:
            if self.data_categ_id.type == "user":
                if self.partner_id:
                    wipe = self.partner_id.write({
                        "phone": False,
                        "company_name": False,
                        "email": False,
                        "vat": False,
                    })
                    if wipe:
                        self.data_wiped = True
            if self.data_categ_id.type == "address":
                if self.partner_id:
                    wipe = self.partner_id.write({
                        "street": False,
                        "street2": False,
                        "city": False,
                        "zip": False,
                        "state_id": False,
                        "country_id": False,
                    })
                    if wipe:
                        self.data_wiped = True
