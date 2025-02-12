from odoo import fields, models, api, exceptions

class AddEmployeeDocsInformation(models.Model):
    _inherit = "hr.employee"
    
    count_docs = fields.Integer(default=0, compute="count_docs_employee")
    
    def count_docs_employee(self):
        for rec in self:
            docs_ids = self.env['hr.employee.document'].search([('employee_id', '=', rec.id)])
            rec.count_docs = len(docs_ids)
    
    def view_employee_information(self):
        action = self.env.ref('docs_information.action_employee_document').read()[0]
        
        action['domain'] = [('employee_id', '=', self.id)]
        action['context'] = {'default_employee_id': self.id}
        
        return action
