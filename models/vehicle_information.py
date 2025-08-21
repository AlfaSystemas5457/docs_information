from odoo import models, api, fields, exceptions


class VehicleDocumentType(models.Model):
    _name = "fleet.vehicle.document.type"
    _description = "Tipos de documentos de los vehiculos"
    _rec_name = 'display_name'

    name = fields.Char(string="Nombre del tipo de documento", required=True)
    code = fields.Char(string="Código del tipo de documento", required=True)
    display_name = fields.Char(
        string="Nombre para mostrar", compute="_compute_display_name")

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.code} - {record.name}" if record.code else record.name


class VehicleDoument(models.Model):
    _name = "fleet.vehicle.document"
    _description = "Administración de documentos de los vehiculos"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nombre del docuimento",
                       required=True, tracking=True)
    vehicle_id = fields.Many2one(
        "fleet.vehicle", string="Vehiculo", required=True, ondelete="cascade", tracking=True)

    document_type = fields.Many2one(
        'fleet.vehicle.document.type', string="Tipo de documento", required=True, tracking=True)
    file = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_vehicle_attachment_relation",
                            column1="m2m_id", column2="attachment_id", string="Adjuntar archivos", tracking=True)

    issue_date = fields.Date("Fecha de emision", tracking=True)
    expiration_date = fields.Date("Fecha de expiración", tracking=True)
    notes = fields.Text("Notas", tracking=True)

    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = f"{self.name} (Copia)"
        return super(VehicleDoument, self).copy(default)
