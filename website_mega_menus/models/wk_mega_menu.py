# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError


class WkMegaMenu(models.Model):
    _name = "wk.mega.menu"

    name = fields.Char('Name')
    menu_ids = fields.One2many(
    'website.menu',
    'wk_mega_menu_id',
    string="Menus"
    )

    wk_mega_menu_template = fields.Selection(
	[('mega_menu_snippet_1','Template 1'),
	('mega_menu_snippet_2','Template 2'),
	('mega_menu_snippet_3','Template 3'),
	('mega_menu_snippet_4','Template 4'),
	('mega_menu_snippet_5','Template 5'),
	('mega_menu_snippet_6','Template 6'),
	('mega_menu_snippet_7','Template 7'),
	('mega_menu_snippet_8','Template 8'),
	('mega_menu_snippet_9','Template 9'),
    ],
	default="mega_menu_snippet_1",
	help="Select Template to use for this mega menu",
    required=True,
    string="Template")

    mega_menu_open_action = fields.Selection(
    [('wk_click','On mouse click'),
    ('wk_hover','On mouse hover')],
    default="wk_click",
    help="Specify action to open mega menu",
    string="Mega menu open action"
    )

    mega_menu_open_animation = fields.Selection(
    [('sweep_left','Sweep Left'),
    ('sweep_right','Sweep Right'),
    ('sweep_down','Sweep Down'),
    ('sweep_up','Sweep Up'),
    ('scroll_down','Scroll Down'),
    ('scroll_up','Scroll Up')],
    default="sweep_down",
    help="Select mega menu opening animation",
    string="Mega menu opening animation"
    )

    mega_menu_height = fields.Integer(
    string="Mega menu height",
    default=0,
    help="Set height for mega menu, set 0 for default height"
    )

    mega_menu_width = fields.Selection(
    [('container','Container'),
    ('100_percent', '100%')],
    default="container",
    help="set width for mega menu",
    string="Mega menu width"
    )

    mega_menu_header_color = fields.Char(
        string="Header Text Color",
        help="Background color to be displayed on the Mega menu header"
	)
    mega_menu_header_bg = fields.Char(
        string="Header Background Color",
        help="Text color to be displayed on the Mega menu header"
	)
    mega_menu_body_bg = fields.Char(
        string="Body Background Color",
        help="Background color to be displayed on the Mega menu body"
	)
    mega_menu_body_color = fields.Char(
        string="Body Text Color",
        help="Text color to be displayed on the Mega menu body"
	)
    root_categ_color = fields.Char(
        string="Root Category Text Color",
        help="Text color to be displayed on the Mega menu root category"
	)
    mega_menu_body_hover_color = fields.Char(
        string="Child Category Text Color",
        help="Text color to be displayed on the Mega menu child category"
    )

    def unlink(self):
        mega_menu = self.env['website.menu'].search([('wk_mega_menu_id','in',self.ids)])
        if mega_menu:
            raise ValidationError("This record is being used by a menu item")
        else:
            return super(WkMegaMenu, self).unlink()
