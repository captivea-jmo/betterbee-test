# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website Braintree Payment Acquirer",
  "summary"              :  """Integrate Braintree Payment with Odoo. With this module, your customers can pay for their online orders with Braintree payment gateway on Odoo website.""",
  "category"             :  "Website",
  "version"              :  "1.5.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Braintree-Payment-Acquirer.html",
  "description"          :  """Odoo Braintree Stripe Payment Acquirer
Odoo Braintree Payment Gateway
Payment Gateway
Braintree
Braintree
Braintree integration
Payment acquirer
Payment processing
Payment processor
Website payments
Sale orders payment
Customer payment
Integrate Braintree payment acquirer in Odoo
Integrate Braintree payment gateway in Odoo""",
  "live_test_url"        :  "https://webkul.com/blog/odoo-website-braintree-payment-acquirer/",
  "depends"              :  ['payment'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/payment_views.xml',
                             'views/payment_braintree_templates.xml',
                             'data/payment_acquirer_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  59,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
  "post_init_hook"       :  "create_missing_journal_for_acquirers",
  "external_dependencies":  {'python': ['braintree']},
}
