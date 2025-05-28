from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class Property(models.Model):
    _name="property"
    _description = "Property"
    _inherit=["mail.thread", "mail.activity.mixin"]
    name = fields.Text(size=4)
    description = fields.Text(tracking=1, default="New Description")
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float(required=1)
    diff = fields.Float(compute='_compute_diff')
    selling_price = fields.Float(required=1)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    postcode = fields.Char()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related="owner_id.address", readonly=0)
    owner_phone = fields.Char(related="owner_id.phone", readonly=0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default="draft")
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'this name already exist')
    ]
    line_ids = fields.One2many("property.line", "property_id")
    # لازم نستعملها فى الكمبيوتد علطول ودى بتبقى علائقيه يعنى ممكن تربط كذا فورم فيو مع بعض
    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            print("inside computed diff")
            rec.diff = rec.expected_price - rec.selling_price
    # دى بنستعمها فى الفورم نفسها ملهاش علاقه بأى فورم تانيه
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print("inside onchange diff")
            return {
                'warning' : {'title': "warning", "message": "negative number", 'type': 'notification' }
            }



    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("please add valid number")
    def action_draft(self):
        for rec in self:
            print("inside draft action")
            rec.state = 'draft'
            # rec.write({'state': 'draft'})

    def action_pending(self):
        for rec in self:
            print("inside pending action")
            rec.state = 'pending'
            # rec.write({'state': 'draft'})

    def action_sold(self):
        for rec in self:
            print("inside sold action")
            rec.state = 'sold'
            # rec.write({'state': 'draft'})

    def action_closed(self):
        for rec in self:
            print("inside sold action")
            rec.state = 'closed'
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("inside create")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("inside search")
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property,self).write(vals)
    #     print("inside write")
    #     return res
    #
    #
    # def unlink(self, vals):
    #     res = super(Property,self).unlink()
    #     print("inside unlink")
    #     return res

class PropertyLine(models.Model):
    _name="property.line"
    property_id = fields.Many2one("property")
    area = fields.Float()
    description = fields.Char()