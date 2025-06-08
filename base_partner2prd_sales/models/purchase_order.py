from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            products = order.order_line.mapped('product_id')
            if order.partner_id:
                order.partner_id.product_ids = [(4, p.id) for p in products if p.id not in order.partner_id.product_ids.ids]
        return res