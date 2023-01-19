# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShWebsiteGdprCancelReasonWizard(models.TransientModel):
    _name = "sh.website.gdpr.cancel.reason.wizard"
    _description = "Request Reason Wizard"

    cancel_reason = fields.Text("Reason")

    def submit_reason(self):
        context = self.env.context or {}
        if context and context.get("active_ids", False):
            active_ids = context.get("active_ids")
            law_request = self.env["sh.gdpr.data.request"].browse(active_ids)
            if law_request:
                law_request.write({
                    "cancel_reason": self.cancel_reason,
                    "state": "cancel",
                })
