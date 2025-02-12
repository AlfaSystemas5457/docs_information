from odoo import models, api, fields, exceptions

doc_types_list = [
    ('id', 'Identificación'),
    ('contract', 'Contrato'),
    ('certificate', 'Certificado'),
    ('passport', 'Pasaporte'),
    ('payroll', 'Nómina'),
    ('qualification', 'Certificación'),
    ('medical', 'Certidicado médico'),
    ('resume', 'Currículum Vitae'),
    ('insurange', 'Seguro'),
    ('work_permit', 'Permiso de trabajo'),
    ('training', 'Formación'),
    ('others', 'Otros'),
]

class EmployeeDoument(models.Model):
    _name = "hr.employee.document"
    
    name = fields.Char(string="Nombre del docuimento", required=True)
    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, ondelete="cascade")
    document_type = fields.Selection(doc_types_list, string="Tipo de documento", required=True)
    file = fields.Binary("Archivo (PDF)", attachment=True)
    file_name = fields.Char("Nombre del archivo")
    issue_date = fields.Date("Fecha de emision")
    expiration_date = fields.Date("Fecha de expiración")
    notes = fields.Text("Notas")
    
    @api.constrains('file', 'file_name')
    @api.onchange('file', 'file_name')
    def _check_pdf_extension(self):
        for record in self:
            if record.file_name:
                extension = record.file_name.split('.')[-1].lower()
                
                if extension != 'pdf':
                    raise exceptions.UserError('Solo se permiten archivos PDF')