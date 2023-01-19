from odoo import api, fields, models, _
import logging
import base64
from PyPDF2 import PdfFileMerger
from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    #Define how to send the email

    #Define how to get all manuals from invoice lines and append to docs, then send docs via email_func
    def emailManuals(self):
        def email_func(self,subject,message,id,dest,docs):
          template_obj = self.env['mail.mail']
          template_data = {
                          'subject': subject,
                          'body_html': message,
                          'email_from': "OdooBot@betterbee.odoo.com",
                          'email_to': dest,
                          'model':'account.move',
                          'res_id':id,
                          'attachment_ids':[(6,0,docs)]
                          }
          template_id = template_obj.create(template_data)
          template_id.send()
          return()
        for record in self:
            docs=[]
            for line in record['invoice_line_ids']:
              for product in line['product_id']:
                if product.product_tmpl_id.x_studio_product_manual:
                    #checking the attachment doesn't already exist to avoid storage size issue
                    doc = self.env['ir.attachment'].search([('name','=',str(product['name']+'_ User manual.pdf'))],limit=1)
                    _logger.warning(str(product.product_tmpl_id.x_studio_product_manual))
                    if len(doc)==0 or doc['datas']!= product.product_tmpl_id.x_studio_product_manual:
                          doc = self.env['ir.attachment'].create({
                              'name':product['name']+'_ User manual.pdf',
                              'store_fname':product['name']+'_ User manual.pdf',
                              'type':'binary',
                              'mimetype' : 'applications/pdf',
                              'datas':product.product_tmpl_id.x_studio_product_manual,
                          })

                    docs.append(doc.id)

            email_func(self,"You product manuals are here!","These are the product manual for your purchase. You'll find a lot of useful information in there. We hope you'll enjoy it !",record['id'],record['partner_id']['email'],docs)



    def printManuals(self):
        merger = PdfFileMerger()

        for record in self:
            docs=[]
            for line in record['invoice_line_ids']:
              for product in line['product_id']:
                if product.product_tmpl_id.x_studio_product_manual:
                    #checking the attachment doesn't already exist to avoid storage size issue
                    doc = self.env['ir.attachment'].search([('name','=',str(product['name']+'_ User manual.pdf'))],limit=1)

                    if len(doc)==0 or doc['datas']!= product.product_tmpl_id.x_studio_product_manual:
                          doc = self.env['ir.attachment'].create({
                              'name':product['name']+'_ User manual.pdf',
                              'store_fname':product['name']+'_ User manual.pdf',
                              'type':'binary',
                              'mimetype' : 'applications/pdf',
                              'datas':product.product_tmpl_id.x_studio_product_manual,
                          })

                    docs.append(doc)
                    #Concatenate PDFs and create 1 file to download
                    



        # "docs" is a list containing the PDF structures to merge
        # output = PdfFileWriter()
        # for doc in docs:
        #     _logger.warning(doc.datas)
        #     reader = PdfFileReader(StringIO(str(base64.b64decode(doc.datas))))
        #     for page in range(reader.getNumPages()):
        #         output.addPage(reader.getPage(page))
        #         _logger.warning(str(output))
        # s = StringIO()
        # output.write(s)
        # mega_doc = self.env['ir.attachment'].create({
        #     'name':'User manual concatenation.pdf',
        #     'store_fname':'User manual concatenation.pdf',
        #     'type':'binary',
        #     'mimetype' : 'applications/pdf',
        #     'datas':base64.b64encode(s.getvalue()),
        #     'res_id':record.id,
        #     'res_model':'account.move'
        #
        # })



        # for pdf in docs:
        #     _logger.warning(str(pdf.datas))
        #     merger.append(pdf)

        #merger.write("Manuals.pdf")
        #merger.close()
