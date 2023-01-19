/* Copyright 2022 - Today TechKhedut.
 * Part of TechKhedut. See LICENSE file for full copyright and licensing details.
 */
odoo.define('gdpr_cookie_notice.cookie', function (require) {
    "use strict";
    const ajax = require('web.ajax');
    ajax.jsonRpc("/get-cookie-details", 'call').then(function (cookie) {
        if(cookie) {
            $('#wrapwrap').ultimateGDPR(cookie);
        }
    });
});