from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    builder_visible = fields.Boolean("Builder Visible")


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    display_type = fields.Selection(selection_add=[
        ('upload_image', "Image")
    ], ondelete={'upload_image': 'cascade'})


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    upload_image_value = fields.Binary(string="Upload Image")


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    upload_image_value = fields.Binary(
        related="product_attribute_value_id.upload_image_value")
