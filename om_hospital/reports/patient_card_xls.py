from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_xls' # use 'report_patient_xls' from report.xml file
    _inherit = 'report.report_xlsx.abstract' # inherit a module which is install from odoo apps store

    def generate_xlsx_report(self, workbook, data, lines):
        print("lines", lines, data)
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold':True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter',})
        sheet = workbook.add_worksheet('Patient Card')

        # sheet.right_to_left() # convert the excel sheet on right to left format
        sheet.set_column(3, 3, 50)  # we set the size(50) of 3rd row and 3rd column
        sheet.set_column(2, 2, 50)  # we set the size(50) of 2nd row and 2nd column
        sheet.write(2,2,'Name', format1)
        sheet.write(2,3, lines.patient_name,format2)
        sheet.write(3,2,'Age',format1)
        sheet.write(3,3,lines.patient_age,format1)


