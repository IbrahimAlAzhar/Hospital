from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


# class ResPartners(models.Model):  # override 'contacts' model(model name is 'res.partner') and if we create something the message prints 'yes_working'
#     _inherit = 'res.partner'
#
#     @api.model
#     def create(self, vals_list):
#         res = super(ResPartners, self).create(vals_list)
#         print("yes working")
#         return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'  # inherit this model (model name is 'sale.order')

    def action_confirm(self):  # override the 'action_confirm' function from 'sale.order' model in sale.py file
        print("odoo mates")
        res = super(SaleOrderInherit, self).action_confirm() # using super class for inheriting purpose,so we can access all of items in super class
        return res

    patient_name = fields.Char(string='Patient Name') # add a field of 'sale.order' model by inheriting


class ResPartner(models.Model): # inherit 'contacts' module and add some field
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('om','Odoo Mates'),('odoodev', 'Odoo Dev')]) # 'Odoo Mates' and 'Odoo Dev' show in front end,and back end coding we use 'om' and 'odoodev'


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit these things for chatter purpose(footer)
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    def action_patients(self): # for server action purpose,in 'server_action.xml' file
        print("server action works")
        return {
            'name': _('Patients Server Action'),
            'domain': [], # there are no domain means condition so all items will be show
            'view_type': 'form',
            'res_model': 'hospital.patient', # using this model for server action
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)

    def print_report_excel(self):  # this method name is using in button name in 'patient.xml' file
        return self.env.ref("om_hospital.report_patient_card_xlx").report_action(self) # call the 'report_patient_card_xlx' which is 'id' name of report.xml file

    @api.model
    def test_cron_job(self):
        for rec in self:
            print("Abcd", rec)

    def name_get(self): # show patient name with patient id in dropdown bar when creating an appointment form
        res = []
        for rec in self:
            res.append([rec.id, '%s %s' % (rec.name_seq, rec.patient_name)])
        return res

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValueError(_('The Age Must be Greater than 5')) # the underscore in font of message means the message can translate we if we change the language

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self: # in form view handles just one age group,but in tree view it handles multiple age group for that reason we have to use a loop for multiple values
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    # for smart button purpose(appointments button in patients page)
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],  # take all appointments(patient id) of a patient
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)]) # take all appointments of a patient and count it
        self.appointment_count = count

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id: # if there are a doctor_id in patient patient create file then the doctor gender selects automatically
                rec.doctor_gender = rec.doctor_id.gender

    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id # using 'mail_template.xml' id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    patient_name = fields.Char(string='Name',track_visibility='always')
    patient_age = fields.Integer('Age',track_visibility='always',group_operator=False) # track visibility is using for when a user change age then it shows in chatter box,'group_operator=False' means in tree view the age are not sum up by group
    patient_age2 = fields.Float(string="Age2")
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image")
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New')) # when you create item it preserves the order
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male',string="Gender")

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor','Minor'),
    ], string="Age Group", compute='set_age_group', store=True)  # call 'set_age_group' function,if you use 'store=True' then you have to declare api depends on 'set_age_group' function(if age below 18 age group shows minor etc),if you don't use 'store' then you don't to use api on function
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count') # using 'get_appointment_count' method
    active = fields.Boolean("Active",default=True)
    doctor_id = fields.Many2one('hospital.doctor',string='Doctor')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female')
    ],string='Doctor Gender')
    email_id = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', string='PRO')
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name') # 'compute' field is using for to convert the upper name,and 'inverse' field is using for to make editable of 'upper_name_field'


    @api.depends('patient_name')
    def _compute_upper_name(self): # this method is using for converting the upper field
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def _inverse_upper_name(self): # this method is using for editable the upper name field
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    # when we create an item it maintains a sequence order
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result





