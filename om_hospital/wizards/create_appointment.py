from odoo import models, fields, api


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string='Appointment Date')

    def print_report(self):
        print("kkkk----->",self.read()[0])
        data = {
            'model': 'create_appointment', # not necessary to use 'model' here
            'form': self.read()[0]
        }

        print("Data", data)
        d_id = self.read()[0]['patient_id'][0] # take the 'patient_id' which is one to many field of patient and appointment
        print('did',d_id)
        return self.env.ref('om_hospital.record_id').report_action(d_id) # 'record_id' is the action of 'reports/appointment.xml' file
    '''
    # for landscape mode of pdf
        return self.env.ref('om_hospital.record_id').with_context(landscape=True).report_action(d_id) # 'record_id' is the action of 'reports/appointment.xml' file
    '''

    def delete_patient(self):  # delete the 'patient_id' (patient) from 'create_appointment' wizard
        for rec in self:
            rec.patient_id.unlink()

    def create_appointment(self): # for creating an appointment from wizard
        vals = {
            'patient_id': self.patient_id.id, # 'patient_id' is attribute of 'hospital.appointment' model,,'id' is build in attribute
            'appointment_date': self.appointment_date,
            'notes': 'Create From the Wizard/code'
        }
        self.patient_id.message_post(body="Appointment Created Successfully",subject="Appointment") # when you create a appointment from wizard then a message is create on the chatter
        # create appointments from code
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'  # after create appointment then the form view is open in edit mode
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': new_appointment.id,  # take the id of appointment
            'context': context
        }
    def get_data(self):
        print("Get Data Function")
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', 3)]) # take all the appointments where patient_id(field of appointment model) is 3
        print("appointments", appointments)
        for rec in appointments:
            print("Appointment Name", rec.name) # name is the field of 'hospital.appointment' model (print all appointments of this patient)

        return {
            "type": "ir.actions.do_nothing" # this return means if you click 'get_data' in wizard then the wizard is not closed,you can use any words in place of 'don_nothing'
        }


