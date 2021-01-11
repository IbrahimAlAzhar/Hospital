from odoo import http
from odoo.http import request
#from odoo.addons.website_sale.controllers.main import WebsiteSale
'''
# inherit the existing 'shop' and override
class WebsiteSaleInherit(WebsiteSale):
    @http.route([

    ],type='http',auth="public",website=True)
    def shop(self,page=0,category=None,search='',ppg=False, **post):
        res = super(WebsiteSaleInherit,self).shop[page=0,category=None,search='',ppg=False,**post]
        print("Inherited Odoo Mates....",res)
        return res
'''


class AppointmentController(http.Controller):
    @http.route('/om_hospital/appointments',auth='user',type='json') # tree banner route in appointment.xml file is same as this http.route
    def appointment_banner(self):
        return {
            'html': """
                    <div>
                    <link>
                    <center><h1><font color="red">This is Hospital Management Systems.</font></h1></center> 
                    <center>
                    <p><fot color="blue"><a href="https://www.youtube.com">
                       Connected with us always.</a></p>
                       </font></div></center> """
        }


class Hospital(http.Controller):
    # sample controller created
    @http.route('/hospital/patient/', website=True,auth='public') # auth='public' means any user without logged in can access this page,auth='user' means only logged in user can access
    def hospital_patient(self,**kw):
        patients = request.env['hospital.patient'].sudo().search([]) # take all patients
        print("patients---", patients)
        return request.render("om_hospital.patients_page", {
            'patients': patients # return all patients to template.xml file
        }) # 'patients_page' is a template in template.xml file

    @http.route('/update_patient',type='json',auth='user')
    def update_patient(self, **rec):
        if request.jsonrequest:
            if rec['id']: # check whether 'id' is coming from the mobile app
                print("rec....",rec)
                patient = request.env['hospital.patient'].sudo().search([('id', '=', rec['id'])]) # take the current id,'id' is the model's attribute and rec['id'] is the frontend id
                if patient:
                    patient.sudo().write(rec) # update the fields
                args = {'success': True, 'message':'Success'}
        return args

    # how to create a data in odoo from mobile app
    @http.route('/create_patient',type='json',auth='user')
    def create_patient(self, **rec): # create a patient using postman(json file),using rec for set the data from mobile app
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                vals = {
                    'patient_name': rec['name'] # 'patient_name' is the field of model, and 'name' is the field of postman(front end mobile app)
                }
                new_patient = request.env['hospital.patient'].sudo().create(vals)
                print("new patient is: ", new_patient)
                args = {'success': True, 'message': 'Success', 'id': new_patient.id} # create 'id' from 'new_patient id'
            return args

    # how to fetch the data from odoo in mobilie app
    @http.route('/get_patients',type='json',auth='user')
    def get_patients(self): # get the patients from database and show it to postman (json file)
        print("Yes here entered")
        patients_rec = request.env['hospital.patient'].search([])
        patients = []
        for rec in patients_rec: # get the all 'patients_rec' and show it to postman(front end)
            vals = {
                'id': rec.id,
                'name': rec.patient_name,
            }
            patients.append(vals)
        print("Patient List-->",patients)
        data = {'status': 200, 'response': patients, 'message': 'Success'}
        return data

    @http.route('/patient_webform',type="http",auth="public",website=True) # take the url
    def patient_webform(self,**kw): # pass the all information by kw
        return http.request.render('om_hospital.create_patient', {}) # 'create_patient' is template id

    @http.route('/create/webpatient',type="http",auth="public",website=True)
    def create_webpatient(self,**kw):
        request.env['hospital.patient'].sudo().create(kw) # sudo means can create publicly
        return request.render("om_hospital.patient_thanks",{}) # 'patient_thanks' is record id in website_form.xml file

