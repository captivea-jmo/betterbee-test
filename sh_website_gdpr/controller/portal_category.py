# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import json


class CategoryPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CategoryPortal, self)._prepare_portal_layout_values()
        category_obj = request.env['sh.gdpr.data.category']
        categories_domain = [('active', '=', True)] + \
            request.website.website_domain()
        categories = category_obj.sudo().search(categories_domain)
        category_count = category_obj.sudo().search_count(categories_domain)
        values['category_count'] = category_count
        values['categories'] = categories
        return values

    @http.route(['/my/category', '/my/category/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_category(self, page=1, **kw):
        Category_sudo = request.env['sh.gdpr.data.category'].sudo()
        values = self._prepare_portal_layout_values()
        domain = [('active', '=', True)] + request.website.website_domain()
        category_count = Category_sudo.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/category",
            total=category_count,
            page=page,
            step=self._items_per_page,
        )
        categories = Category_sudo.search(
            domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'categories': categories,
            'page_name': 'category',
            'default_url': '/my/category',
            'category_count': category_count,
            'pager': pager,
        })
        return request.render("sh_website_gdpr.category_my_category", values)

    @http.route(['/create-request-download'], type='http', auth="public", method="post", website=True, csrf=False)
    def create_request_download(self, **post):
        dic = {}
        category_id = request.env['sh.gdpr.data.category'].sudo().browse(
            int(post.get('category_id')))
        request_obj = request.env['sh.gdpr.data.request']
        if category_id:

            search_req = request_obj.search([

                ('partner_id', '=', request.env.user.partner_id.id),
                ('data_categ_id', '=', category_id.id),
                ('request_type', '=', 'download'),
            ])

            if search_req:
                dic.update({
                    'error': 'Your request already has been submitted.'
                })
            else:
                request_vals = {}
                request_vals.update({
                    'name': category_id.name,
                    'partner_id': request.env.user.partner_id.id,
                    'data_categ_id': category_id.id,
                    'request_type': 'download',
                    'state': 'pending',
                })
                request_id = request_obj.sudo().create(request_vals)
                dic.update({
                    'success': 1,
                    'success_msg': 'Your request for download has been submitted.'
                })
                emails = []
                if request_id.website_id.is_enable_email and request_id.website_id.user_ids:
                    for user in request_id.website_id.user_ids:
                        if user.partner_id and user.partner_id.email:
                            emails.append(user.partner_id.email)
                    email_values = {
                        'email_to': ','.join(emails)
                    }
                    url = ''
                    base_url = request.env['ir.config_parameter'].sudo(
                    ).get_param('web.base.url')
                    url = base_url + "/web#id=" + \
                        str(request_id.id) + \
                        "&&model=sh.gdpr.data.request&view_type=form"
                    ctx = {
                        "customer_url": url,
                    }
                    template_id = request.env['ir.model.data'].get_object(
                        'sh_website_gdpr', 'email_template_download_responsible_person')
                    _ = request.env['mail.template'].sudo().browse(template_id.id).with_context(ctx).send_mail(
                        request_id.id, email_values=email_values, notif_layout='mail.mail_notification_light', force_send=True)
                if request_id.website_id.is_enable_email and request_id.website_id.is_customer:
                    template_download_id = request.env['ir.model.data'].sudo().get_object(
                        'sh_website_gdpr', 'email_template_download_customer')
                    url = ''
                    base_url = request.env['ir.config_parameter'].sudo(
                    ).get_param('web.base.url')
                    url = base_url + '/my/gdpr_request'
                    ctx = {
                        "customer_url": url,
                    }
                    _ = request.env['mail.template'].sudo().browse(template_download_id.id).with_context(
                        ctx).send_mail(request_id.id, notif_layout='mail.mail_notification_light', force_send=True)
        return json.dumps(dic)

    @http.route(['/create-request-delete'], type='http', auth="public", method="post", website=True, csrf=False)
    def create_request_delete(self, **post):
        dic = {}
        category_id = request.env['sh.gdpr.data.category'].sudo().browse(
            int(post.get('category_id')))
        request_obj = request.env['sh.gdpr.data.request']

        if category_id:
            domain = [
                ('partner_id', '=', request.env.user.partner_id.id),
                ('data_categ_id', '=', category_id.id),
                ('request_type', '=', 'delete'),
            ]
            search_req = request_obj.search(domain, limit=1)
            if search_req:
                dic.update({
                    'msg': 'Your request already has been submitted.',
                    'hide_i_am_sure_btn': True,
                })
                return json.dumps(dic)
            else:
                if post.get("do_delete", 0) == '1':
                    request_vals = {}
                    request_vals.update({
                        'name': category_id.name,
                        'partner_id': request.env.user.partner_id.id,
                        'data_categ_id': category_id.id,
                        'request_type': 'delete',
                        'state': 'pending',
                    })

                    request_id = request_obj.sudo().create(request_vals)

                    dic.update({
                        'success': 1,
                        'msg': 'Your request for delete has been submitted.',
                        'hide_i_am_sure_btn': True,
                    })
                    emails = []

                    if request_id.website_id.is_enable_email and request_id.website_id.user_ids:
                        for user in request_id.website_id.user_ids:
                            if user.partner_id and user.partner_id.email:
                                emails.append(user.partner_id.email)
                        email_values = {
                            'email_to': ','.join(emails)
                        }
                        url = ''
                        base_url = request.env['ir.config_parameter'].sudo(
                        ).get_param('web.base.url')
                        url = base_url + "/web#id=" + \
                            str(request_id.id) + \
                            "&&model=sh.gdpr.data.request&view_type=form"
                        ctx = {
                            "customer_url": url,
                        }
                        template_id = request.env['ir.model.data'].sudo().get_object(
                            'sh_website_gdpr', 'email_template_delete_responsible_person')
                        _ = request.env['mail.template'].sudo().browse(template_id.id).with_context(ctx).send_mail(
                            request_id.id, email_values=email_values, notif_layout='mail.mail_notification_light', force_send=True)
                    if request_id.website_id.is_enable_email and request_id.website_id.is_customer:
                        template_download_id = request.env['ir.model.data'].sudo().get_object(
                            'sh_website_gdpr', 'email_template_delete_customer')
                        url = ''
                        base_url = request.env['ir.config_parameter'].sudo(
                        ).get_param('web.base.url')
                        url = base_url + '/my/gdpr_request'
                        ctx = {
                            "customer_url": url,
                        }
                        _ = request.env['mail.template'].sudo().browse(template_download_id.id).with_context(
                            ctx).send_mail(request_id.id, notif_layout='mail.mail_notification_light', force_send=True)
                        return json.dumps(dic)
                else:
                    dic.update({
                        'msg': 'Are you sure !',
                        'hide_i_am_sure_btn': False,
                    })
                    return json.dumps(dic)
        return json.dumps(dic)
