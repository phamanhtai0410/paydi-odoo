from odoo import fields, models, api


class FileData(models.Model):
    _name = 'file.data'
    _description = 'Description'
   

    STT = fields.Char()
    MID = fields.Char()
    name = fields.Char()
    product_name = fields.Char()
    bank_value = fields.Char()
    agency = fields.Char()
    bank_number = fields.Char()
    citab_code = fields.Char()
    bin_code = fields.Char()
    beneficiary = fields.Char()
    totol_amount = fields.Char()
    file_name_id = fields.Many2one(comodel_name="for.control", string="file name id")
