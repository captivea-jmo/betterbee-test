# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Website GDPR",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "14.0.1",
    "category": "Website",
    "summary": """
Manage GDPR App,
Website GDPR Module,
General Data Protection Regulation At Web,
EU GDPR Management, European Countries GDPR,
EU Website GDPR, Privacy GDPR, GDPR Cookies Odoo
""",
    "description": """
General Data Protection Regulation (GDPR) is the law that sets the guidelines
for the collection of personal information of
individuals within the European Countries.
The European Union Parliament passed GDPR on the 14th of April 2016.
Soon GDPR will get into effect by 25th May 2018.
The EU"s says GDPR was designed to "harmonise" data privacy laws
across all of its member countries as well as providing greater protection
and rights to individuals.
About Module: Clients can request to access their data stored in the database.
They can send a request to download their data.
They can request to delete their data from the website.
If a client request to download/delete data then they
get mail for that and the responsible person also gets mail about that request.
The responsible person can easily handle all GDPR requests with the categories.
We provide the GDPR notice feature on the website.
""",
    "depends": [
        "website_sale",
        "sh_cookie_notice",
    ],
    "data": [
        "security/sh_website_gdpr_security.xml",
        "security/ir.model.access.csv",
        "wizard/cancel_reason_wizard_view.xml",
        "views/gdpr_category_view.xml",
        "views/gdpr_request_view.xml",
        "views/res_config_settings.xml",
        "views/portal_category_template_view.xml",
        "views/portal_request_template_view.xml",
        "reports/generate_request_date.xml",
        "data/mail_template.xml",
    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "50",
    "currency": "EUR"
}
