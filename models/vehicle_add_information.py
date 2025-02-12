from odoo import models, fields, api, exceptions

class AddVehicleDocsInformation(models.Model):
    _inherit = 'fleet.vehicle'
    
    count_docs = fields.Integer(default=0, compute="count_docs_employee")
    
    def count_docs_employee(self):
        for rec in self:
            docs_ids = self.env['fleet.vehicle.document'].search([('vehicle_id', '=', rec.id)])
            rec.count_docs = len(docs_ids)
    
    def view_vehicle_information(self):
        action = self.env.ref('docs_information.action_vehicle_document').read()[0]
        
        action['domain'] = [('vehicle_id', '=', self.id)]
        action['context'] = {'default_vehicle_id': self.id}
        
        return action