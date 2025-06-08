from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.Many2many(
        'product.product', string='Purchased Products', readonly=True
    )