from odoo import models, fields, api, _
import pytz


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit these things for chatter purpose(footer)
    #_order = "id desc"  # take the order where latest id shows on top
    _order = "appointment_date desc"

    '''
    def delete_lines(self): # check using local timezone
        for rec in self:
            print("Time in UTC", rec.appointment_date)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            print("user_tz",user_tz)
            date_today = pytz.utc.localize(rec.appointment_date).astimezone(user_tz)
            print("Time in Local Timezone.",date_today)
            rec.appointment_lines = [(5, 0, 0)] 
    '''
    def test_recordset(self):
        for rec in self:
            print("Odoo ORM: Record Set Operations")
            partners = self.env['res.partner'].search([]) # take all partners id from res.partner(contacts)
            print("partners name....",partners.mapped('name')) # take the 'name' attribute of res.partner model(contact model) using mapped
            print("partners email...",partners.mapped('email')) # 'email' is the field of res.partner model(contact model)
            # print("partners...",partners.sorted(lambda o: o.create_date)) # sorting based on the create_date (build in)
            # print("partners...",partners.sorted(lambda o: o.write_date)) # sorting based on the write_date ascending order (build in)
            print("partners...",partners.sorted(lambda o: o.write_date,reverse=True)) # sorting based on the create_date descending order (build in)
            # print("Filtered partners...", partners.filtered(lambda o: o.customer)) # print the customer,though customer field is not in 'contcts'(res.partner)

    def action_notify(self):
        for rec in self:
            rec.env.user.notify_danger("An Appointment Receive") # doctor_id is the field of appointment model,and user_id is field of doctor model

    def delete_lines(self):  # for deleting the lines purpose
        for rec in self:
            print("rec",rec)
            rec.appointment_lines = [(5, 0, 0)]  # for delete the lines we have to use this line

    def action_confirm(self): # a button name in xml file file which name is 'action_confirm'
        for rec in self:  # once the button is clicked then the state is change into 'confirm'
            rec.state = 'confirm'
            # when the appointment is confirmed then welcome with rainbow effect
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed.Thank You',
                    'type': 'rainbow_man',
                }
            }


    def action_done(self): # for 'done' button purpose and state is change onto 'done' stage
        for rec in self:
            rec.state = 'done'  # state tuple is defined below the code

    # when we create an item it maintains a sequence order
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New') # using sequence for creating a seq order
        result = super(HospitalAppointment, self).create(vals)
        return result
    
    # override the appointment model,if you override(edit) then you see the print
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self): # see the order of current user when you select a user(partner id)
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}} # partner_id is equal to the selected id(id is build in)

    # this function is using for default value of appointment lines when you create a appointment it takes all product automatically in appointment lines
    @api.model
    def default_get(self, fields): # when you create appointment,these default values are given (you don't need to declare on xml file)
        res = super(HospitalAppointment, self).default_get(fields)
        appointment_lines = []
        product_rec = self.env['product.product'].search([]) # take the all 'product' field in 'product' model(this is build in model in odoo)
        for pro in product_rec:
            line = (0,0, { # this is a tuple consisting some value
                'product_id': pro.id, # 'product_id,'product_qty' is the field of 'appointment_lines' class
                'product_qty': 1,
            })
            appointment_lines.append(line) # append the tuple's value in a list
        print(appointment_lines)
        res.update({ # take the all products in appointment_lines by default
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'This is odoo mates'
        })
        return res

    #def get_default_note(self):
        #return "Subscribe Our Youtube channel"

    def get_default_note(self):
        return 1

    name = fields.Char(string='Appointment_ID',require=True,copy=False,readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient',string='Patient',required=True,default=get_default_note)
    patient_age = fields.Integer('Age',related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note") # using default note
    appointment_date = fields.Date(string='Date')
    appointment_date_end = fields.Date(string='End Date')
    doctor_note = fields.Text(string="Note")
    appointment_lines = fields.One2many('hospital.appointment.lines','appointment_id', string='Appointment Lines') # using model 'hospital.appointment' and field 'appointment_id',call the 'hospital.appointment.lines' class
    pharmacy_note = fields.Text(string="Note")
    partner_id = fields.Many2one('res.partner',string="Customer")  # 'res.partner' is build in for all users (odoo sales module)
    order_id = fields.Many2one('sale.order',string="Sale Order")  # 'sale.order' is build in for all sale of users(odoo sales module)
    amount = fields.Float(string='Amount')
    doctor_id = fields.Many2one('hospital.doctor',string='Doctor')
    doctor_ids = fields.Many2many('hospital.doctor','hospital_patient_rel','appointment_id','doctor_id',string='Doctors') # for many2many field it create a table automatically,we set the table name is 'hospital_patient_rel',and 1st column is 'appointment_id'(build in),and 2nd column is 'doctor_id'

    state = fields.Selection(selection=[  # declare the the state in status bar
        ('draft', 'Draft'),  # first item is using for database and 2nd item is using for frontend(odoo)
        ('confirm', 'Confirm'),
        ('done', 'Done')
    ], string='Status', readonly=True, default='draft')
    product_id = fields.Many2one('product.template',string="Product Template") # using 'product.template' model(build in

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            print("self.product_id",self.product_id.product_variant_ids) # product id is the attribute,and 'product_variant_ids' is the field of product.template
            lines = [(5,0,0)] # it means if we select a product id then it deletes all prev product in appointment line
            # lines = []  # if we declare a empty dictionary then it preserves all product on appointment lines
            for line in self.product_id.product_variant_ids: # 'product_id.product_variant_ids' take all variants of product
                val = {
                    'product_id': line.id,
                    'product_qty': 15
                } # 'product_id','product_qty' is the field of appointment model
                lines.append((0, 0, val))  # append the tuple in 'lines' list,
            print("lines",lines)
            rec.appointment_lines = lines # 'appointment_lines' is the attribute of appointment model,take the 'lines' list value on this attribute,so if we change a product id then it save onto appointment lines


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='product')  # model is product.product
    product_qty = fields.Integer(string='Quantity')
    sequence = fields.Integer(string="Sequence") # this field is using for drag in product in appointments
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment ID') # using foreign key








