from odoo import api, models


class PatientCardReport(models.AbstractModel):
    _name = 'report.om_hospital.report_patient' #'report_patient' is a template of 'patient_card.xml' file
    _description = 'Patient card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("yes entered here in the function")
        print("docids",docids)
        docs = self.env['hospital.patient'].browse(docids[0])
        print("docs is ",docs)
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])]) # print all appointments of this current patient
        appointment_list = []
        for app in appointments: # take all appointments of current patient
            vals = {
                'name': app.name,
                'notes': app.notes,
                'appointment_date': app.appointment_date
            }
            appointment_list.append(vals)
        print("appointments",appointments)
        print("appointment_list",appointment_list)

        return {
            'doc_model': 'hospital.patient',
            'data': data,
            'docs': docs,  # 'doc' is call to 'patient_card.xml' file
            'appointment_list': appointment_list,
        }


