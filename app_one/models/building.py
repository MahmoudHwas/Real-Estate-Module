from email.policy import default

from odoo import models, fields


class Building(models.Model):
    _name = "building"
    _description = "Building Record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_names = 'code'

    name = fields.Char()
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)

