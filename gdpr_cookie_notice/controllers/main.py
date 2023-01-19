# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request



class WebsiteCookies(http.Controller):

    @http.route(['/get-cookie-details'], type='json', auth="public")
    def get_cookie_details(self, **kw):
        """ Method return cookie details"""
        ck = request.env.ref('gdpr_cookie_notice.cookie_settings').sudo()
        content_before_slider = '<h2>' + ck.setting_popup_title + '</h2>'
        content_before_slider += '<div class="ct-ultimate-gdpr-cookie-modal-desc">' + str(ck.setting_popup_description) + '</div>'
        content_before_slider += '<h3>' + ck.group_slider_title + '</h3>'

        cookies_group = {}
        for rec in ck.cookie_group_ids:
            cookies_group[rec.code] = {
                'name': rec.name,
                'enable': True,
                'icon': 'fas ' + rec.fa_icon,
                'list': rec.cookie_popup_group_info_ids.mapped('name'),
                'blocked_url': [],
                'local_cookies_name': [],
            }
        cookie = {
            'popup_style': {
                'position': ck.popup_position,
                'distance': str(ck.distance) + 'px',
                'box_style': ck.box_style,
                'box_shape': ck.box_shape,
                'background_color': ck.background_color,
                'text_color': ck.text_color,
                'button_shape': ck.button_shape,
                'button_color': ck.button_color,
                'button_size': ck.button_size,
                'box_skin': ck.box_skin,
                'gear_icon_position': ck.gear_icon_position,
                'gear_icon_color': ck.gear_icon_color,
            },
            'popup_options': {
                'parent_container': 'body',
                'always_show': False,
                'gear_display': ck.gear_display,
                'popup_title': ck.popup_title,
                'popup_text': ck.popup_text,
                'accept_button_text': ck.accept_button_text,
                'reject_button_text': ck.reject_button_text,
                'read_button_text': ck.read_button_text,
                'read_more_link': ck.read_more_link,
                'advenced_button_text': ck.advenced_button_text,
                'grouped_popup': True,
                'default_group': ck.default_group_id.code,
                'content_before_slider': content_before_slider,
                'accepted_text': ck.accepted_text,
                'declined_text': ck.declined_text,
                'save_btn': ck.save_btn,
                'prevent_cookies_on_document_write': False,
                'check_country': False,
                'countries_prefixes': ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
                                       'IE',
                                       'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE',
                                       'GB'],
                'cookies_expire_time': ck.cookies_expire_time,
                'cookies_path': ck.cookies_path,
                'reset_link_selector': '.ct-uGdpr-reset',
                'first_party_cookies_whitelist': [],
                'third_party_cookies_whitelist': [],
                'cookies_groups_design': ck.cookies_groups_design,
                'assets_path': '',
                'video_blocked': '',
                'iframe_blocked': False,
                'cookie_popup_close_color': ck.cookie_popup_close_color,
                'close_popup_text': ck.close_popup_text,
                'cookies_groups': cookies_group
            },
            'forms': {
                'prevent_forms_send': False,
                'prevent_forms_text': '',
                'prevent_forms_exclude': [],
            },
            'configure_mode': {
                'on': False,
                'parametr': '',
                'dependencies': ['/gdpr_cookie_notice/static/src/css/ct-ultimate-gdpr.min.css',
                                 'https://use.fontawesome.com/releases/v5.0.13/css/all.css'],
                'debug': False,
            }
        }
        return cookie
