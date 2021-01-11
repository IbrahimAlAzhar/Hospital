from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    # _inherit = {'hospital.patient': 'related_patient_id'}
    _description = "Doctor Record"

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female')
    ], default='male', string='Gender')
    user_id = fields.Many2one('res.users', string='Related_fields')
    appointment_ids = fields.Many2many('hospital.appointment','hospital_patient_rel','doctor_id','appointment_id',string='Appointments') # for many2many field it create a table automatically,we set the table name is 'hospital_patient_rel',and 1st column is 'doctor_id'(current db field),and 2nd column is 'appointment_id'(build in)




