from odoo import models, api, fields, exceptions

doc_types_list = [
    ('registration', 'Registro del vehículo'),
    ('title', 'Título de propiedad'),
    ('insurance', 'Seguro del vehículo'),
    ('inspection', 'Certificado de inspección'),
    ('license_plate', 'Placa del vehículo'),
    ('emissions', 'Certificado de emisiones'),
    ('warranty', 'Garantía'),
    ('leasing_contract', 'Contrato de arrendamiento'),
    ('purchase_invoice', 'Factura de compra'),
    ('driver_license', 'Licencia de conducir'),
    ('road_tax', 'Impuesto de circulación'),
    ('accident_report', 'Informe de accidente'),
    ('service_history', 'Historial de mantenimiento'),
    ('authorization', 'Autorización para conducir'),
    ('import_certificate', 'Certificado de importación'),
    ('others', 'Otros'),
]

class EmployeeDoument(models.Model):
    _name = "fleet.vehicle.document"
    
    name = fields.Char(string="Nombre del docuimento", required=True)
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehiculo", required=True, ondelete="cascade")
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