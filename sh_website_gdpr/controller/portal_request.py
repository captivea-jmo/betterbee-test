# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RequestPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(RequestPortal, self)._prepare_portal_layout_values()
        request_obj = request.env['sh.gdpr.data.request']
        request_domain = [('partner_id', '=', request.env.user.partner_id.id)
                          ] + request.website.website_domain()
        gdpr_requests = request_obj.sudo().search(request_domain)
        gdpr_request_count = request_obj.sudo().search_count(request_domain)
        values['gdpr_request_count'] = gdpr_request_count
        values['gdpr_requests'] = gdpr_requests
        return values

    @http.route(['/my/gdpr_request', '/my/gdpr_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gdpr_requests(self, page=1, **kw):
        Request_sudo = request.env['sh.gdpr.data.request'].sudo()
        values = self._prepare_portal_layout_values()
        domain = [('partner_id', '=', request.env.user.partner_id.id)]
        gdpr_request_count = Request_sudo.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/gdpr_request",
            total=gdpr_request_count,
            page=page,
            step=self._items_per_page,
        )

        requests = Request_sudo.search(
            domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'requests': requests,
            'page_name': 'gdpr_request',
            'default_url': '/my/gdpr_request',
            'gdpr_request_count': gdpr_request_count,
            'pager': pager,
        })
        return request.render("sh_website_gdpr.request_my_gdpr_request", values)
