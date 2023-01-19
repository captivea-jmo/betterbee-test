
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

class Menu(models.Model):

	_inherit = "website.menu"

	def _set_website_mega_menus_content(self, vals={}):
		self.ensure_one()
		IrDefault = self.env['ir.default']
		self_wk_mega_menu_id =  self.env['wk.mega.menu'].browse(vals.get('wk_mega_menu_id',False)) if vals else ''

		template_id = self.wk_mega_menu_id.wk_mega_menu_template or self_wk_mega_menu_id.wk_mega_menu_template
		values = {
			'url' : 'none',
			'categories' : self.website_id.get_public_categories(self),
			'website_id' : self.website_id or self.env['website'].browse(vals.get('website_id', False)),
			'new_window' : self.new_window or vals.get('new_window',False),
		}

		if self.wk_mega_menu_id or self_wk_mega_menu_id:
			wk_mega_menu_id = self.wk_mega_menu_id or self_wk_mega_menu_id
			values.update({
				'header_bg_color' : wk_mega_menu_id.mega_menu_header_bg,
				'header_color' : wk_mega_menu_id.mega_menu_header_color,
				'body_bg' : wk_mega_menu_id.mega_menu_body_bg,
				'body_color' : wk_mega_menu_id.mega_menu_body_color,
				'body_hover_color' : wk_mega_menu_id.mega_menu_body_hover_color,
				'root_color' : wk_mega_menu_id.root_categ_color,
				'carousel_products' : self.featured_products_id.product_ids,
				'carousel_heading' : self.featured_products_id.name,
			})

		if self.is_wk_mega_menu or vals.get('is_wk_mega_menu', False) and self.wk_mega_menu_id or self_wk_mega_menu_id:
			default_content = self.env['ir.ui.view']._render_template(
			'website_mega_menus.'+template_id, values)
			self.website_mega_menus_content = default_content.decode()
			vals['website_mega_menus_content'] = default_content.decode()
		else:
			self.website_mega_menus_content = False
			vals['website_mega_menus_content'] = False
		return vals

	is_wk_mega_menu = fields.Boolean(
		string="Mega Menu",
		help="Show the categories as a mega menu on this menu",
		inverse=_set_website_mega_menus_content,
	)
	root_category = fields.Many2one(
		comodel_name="product.public.category",
		string="Root Category",
		help="If any root category is not selected then all the categories will be displayed.",
		inverse=_set_website_mega_menus_content,
	)
	categories_displayed = fields.Selection(
		[('all','ALL'),
		('selected','Selected')],
		default="all",
		string='Categories To Display',
		inverse=_set_website_mega_menus_content
	)
	selected_categories = fields.Many2many(
		'product.public.category','menu_id','category_id','rel',
		string="Select Categories",
	)
	bg_image = fields.Binary(
		string="Background Image",
		help="Image to be displayed on the background of the mega menu"
	)
	top_menu_icon = fields.Binary(
		string="Top Menu Icon",
		help="Icon to be displayed on the top menu of mega menu"
	)
	website_mega_menus_content = fields.Html(translate=html_translate, sanitize=False)

	wk_mega_menu_id = fields.Many2one(
	'wk.mega.menu',
	string="Wk Mega Menu",
	help="Select a mega menu setting you want to use",
	inverse=_set_website_mega_menus_content,
	)

	featured_products_id = fields.Many2one(
    'wk.mega.menu.featured.products',
    string="Product Carousel",
    help="Select a Product Carousel",
	inverse=_set_website_mega_menus_content,
    )

	def create_url(self):
		if self.root_category:
			self.url = "/shop/category/%s" % slug(self.root_category)
		return True


class Website(models.Model):
	_inherit = 'website'

	@api.model
	def get_public_categories(self, vals):
		categs = []
		if vals.categories_displayed == 'selected' and vals.selected_categories:
			categs = vals.selected_categories
		else:
			if vals.root_category:
				categs = request.env['product.public.category'].sudo().search([('parent_id', '=', vals.root_category.id)],order="sequence asc")
			else:
				categs = request.env['product.public.category'].sudo().search([('parent_id', '=', False)], order="sequence asc")
		return categs

	def create_fly_out_menu(self):
		mega_menu = self.env['website.menu'].search([('is_wk_mega_menu', '=', True),('website_id','=',request.website.id)])
		return mega_menu
