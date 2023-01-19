# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class WebsiteCookie(models.Model):
    _name = 'website.cookie.notice'
    _description = "EU GDPR Cookie Notice"
    _rec_name = 'popup_title'

    popup_title = fields.Char(string="Title", default="Cookies Information", required=True, translate=True)
    # popup style
    popup_position = fields.Selection(
        [('bottom-left', "Bottom Left"), ('bottom-right', "Bottom Right"), ('bottom-panel', "Bottom Wide"),
         ('top-left', "Top Left"), ('top-right', "Top Right"), ('top-panel', "Top Wide")], default='bottom-left',
        string="Popup Position", required=True)

    distance = fields.Integer(string="Distance (px)", default=20)
    box_style = fields.Selection([('classic', "Classic"), ('modern', "Modern")], default="classic", string="Box Style",
                                 required=True)
    box_shape = fields.Selection([('rounded', "Rounded"), ('squared', "Squared")], default="rounded",
                                 string="Box Shape",
                                 required=True)
    background_color = fields.Char(string="Background Color", default="#fff584", required=True)
    text_color = fields.Char(string="Text Color", default="#542d04", required=True)
    button_shape = fields.Selection([('rounded', "Rounded"), ('squared', "Squared")], default="rounded",
                                    string="Button Shape",
                                    required=True)
    button_color = fields.Char(string="Button Color", default="#e1e1e1", required=True)
    button_size = fields.Selection([('normal', "Normal"), ('large', "Large")], default="normal",
                                   string="Button Size",
                                   required=True)
    box_skin = fields.Selection(
        [('skin-default-theme', "Custom"), ('skin-dark-theme', "Dark"), ('skin-light-theme', "Light")],
        default="skin-dark-theme",
        string="Theme",
        required=True)
    gear_icon_position = fields.Selection(
        [('top-left', "Top Left"), ('top-center', "Top Center"), ('top-right', "Top Right"),
         ('bottom-left', "Bottom Left"), ('bottom-center', "Bottom Center"), ('bottom-right', "Bottom Right"),
         ('center-left', "Center Left"), ('center-right', "Center Right")],
        default="bottom-left", string="Gear Icon Position",
        required=True)
    gear_icon_color = fields.Char(string="Gear Icon Color", default="#6a8ee7", required=True)

    # popup options
    gear_display = fields.Boolean(string="Is Gear Icon Always on Display ?", default=False)
    popup_text = fields.Text(string="Popup Text", default="Lorem Ipsum popup text", required=True, translate=True)
    accept_button_text = fields.Char(string="Accept Button Text", default="Accept", required=True, translate=True)
    reject_button_text = fields.Char(string="Reject Button Text", default="Reject", required=True, translate=True)
    read_button_text = fields.Char(string="Read Button Text", default="Read More", required=True, translate=True)
    read_more_link = fields.Char(string="Read More Link", default="#")
    advenced_button_text = fields.Char(string="Advanced Button Text", default="Change Settings", required=True, translate=True)
    accepted_text = fields.Char(string="Accepted Text", default="This website will:", required=True, translate=True)
    declined_text = fields.Char(string="Declined Text", default="This website won't:", required=True, translate=True)
    save_btn = fields.Char(string="Save Button Text", default="Save & Close", required=True, translate=True)

    setting_popup_title = fields.Char(string="Settings Popup Title", default="Privacy settings", required=True,
                                      translate=True)
    setting_popup_description = fields.Html(string="Settings Popup Description", required=True,
                                            translate=True)
    group_slider_title = fields.Char(string="Group Slider Title",
                                     default="With the slider, you can enable or disable different types of cookies:",
                                     required=True, translate=True)

    cookies_expire_time = fields.Integer(string="Cookie Expiry (days)", default=30)
    cookies_path = fields.Char(string="Cookie Path", default='/', required=True)
    cookies_groups_design = fields.Selection(
        [('skin-1', "Style 1"), ('skin-2', "Style 2"), ('skin-3', "Style 3")],
        default="skin-1",
        string="Cookie Group Styles",
        required=True)
    cookie_popup_close_color = fields.Char(string="Settings Popup Close Color", default="#ffffff", required=True)
    close_popup_text = fields.Char(string="Close Popup Text", default="X", required=True, translate=True)
    default_group_id = fields.Many2one('cookie.popup.group', string="Default Required Cookie Group", required=True)
    cookie_group_ids = fields.Many2many('cookie.popup.group', string="Cookie Group")


class CookiePopupGroup(models.Model):
    _name = 'cookie.popup.group'
    _description = 'Cookie Popup Group'

    code = fields.Char(string="Group Code", required=True,
                       default="-", readonly=True, copy=False)
    name = fields.Char(string="Title", required=True, translate=True)
    fa_icon = fields.Char(string="Fontawesome Icon", required=True)
    cookie_popup_group_info_ids = fields.One2many('cookie.popup.group.info', 'cookie_popup_group_id',
                                                  string="Highlight Points", required=True)

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default["code"] = self.env["ir.sequence"].next_by_code("cookie.popup.group")
        return super(CookiePopupGroup, self).copy(default)

    @api.model
    def create(self, vals):
        if vals.get("code", "-") == "-":
            vals["code"] = self.env["ir.sequence"].next_by_code(
                "cookie.popup.group")
        return super(CookiePopupGroup, self).create(vals)


class CookiePopupGroupInformation(models.Model):
    _name = 'cookie.popup.group.info'
    _description = "Cookie Popup Group Information"

    name = fields.Char(string="Highlight Point", required=True, translate=True)
    cookie_popup_group_id = fields.Many2one('cookie.popup.group')
