import logging
import time
import tempfile
import binascii
import zipfile
import io
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _
from io import BytesIO, StringIO
from PIL import Image
import os
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')


class gen_sale(models.TransientModel):
	_name = "gen.sale"

	file = fields.Binary('Zip File')
	img_for = fields.Selection([('product', 'Product')],
			 string='Images For', default='product')
	product_by = fields.Selection([('name', 'Name'), 
								('internal ref', 'Internal Reference')],
								string='Product By', default='name')
	product_model = fields.Selection([('product template',
									'Product Template'),
									('product variants', 'Product Variants')], string='Product Model', default='product template')
	def import_img(self):
		try:
			book = BytesIO()
			book.write(base64.decodestring(self.file))
			book.seek(0)    
			zf = zipfile.ZipFile(book, 'r')
		except Exception:
			raise UserError("Please select an Zip file or You have selected invalid file")

		count = 0
		list_file = []
		list_record = []
		for img in zf.namelist()[1:]:
			outpath = "~/"
			p = zf.extract(img, outpath)
			filename = os.path.basename(img) 
			(file, ext) = os.path.splitext(filename)

			if self.img_for == 'product':
				if self.product_model == 'product template':
					model = self.env['product.template']
				elif self.product_model == 'product variants':
					model = self.env['product.product']
				if self.product_by == 'name':
					record = model.search([('name', '=', file)])
				if self.product_by == 'internal ref':
					record = model.search([('default_code', '=', file)])
				try:
					with open(p, "rb") as image_file:
						f = base64.b64encode(image_file.read())                        
				except:
					f = False
				record.write({'image_1920':f})

			if record:
				list_file.append(file)
			else:
				list_record.append(file)
		if list_record:
			Note = 'Note:' + '\n' + '\n'.join(['Image Name "%s" : Record Not Found For This Image.' % (i) for i in list_record])
		else:
			Note = ''
		context = {'default_name':"%s Images Successfully Imported." % (len(list_file)) + '\n' + Note
					} 
		return {
			'name': 'Success',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'custom.pop.message',
			'target':'new',
			'context':context,
			'tag':'reload'
			}


class CustomPopMessage(models.TransientModel):
	_name = "custom.pop.message"

	name = fields.Text('Message')
