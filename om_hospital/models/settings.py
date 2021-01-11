from odoo import models, fields, api, _
from ast import literal_eval


class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    note = fields.Char(string='Default Note')
    module_crm = fields.Boolean(string='CRM') # using boolean field on settings for install a module(like CRM), use 'module_technical_name' then use boolean field for install/uninstall a module in settings
    product_ids = fields.Many2many('product.product',string='Medicines') # create many to many field where we select multiple products

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('om_hospital.note',self.note) # set the values on 'ir.config_parameter
        print("test",self.product_ids.ids)
        self.env['ir.config_parameter'].set_param('om_hospital.product_ids',self.product_ids.ids) # the 'ids' of 'prodcut_ids' set on the 'ir.config.parameter'
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo() # after set the value we get the value(print) from 'ir.config_parameter'
        notes = ICPSudo.get_param('om_hospital.note')
        product_ids = self.env['ir.config_parameter'].sudo().get_param('om_hospital.product_ids') # get the values from 'ir.config_parameter', the 'product_ids' is the field of front end and for we can take the value,use the value from 'ir.config.parameter'
        print("product_ids", product_ids)
        if product_ids:
            print("product_ids", type(literal_eval(product_ids)))
            res.update(
                note=notes,
                product_ids=[(6, 0, literal_eval(product_ids))], # literal_eval converts string to list
            )
        return res

