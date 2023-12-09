from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    purchase_order = fields.Many2many('purchase.order', string='Purchase Orders')

    vehicle_count = fields.Integer(compute='compute_count')

    def compute_count(self):
        for record in self:
            record.vehicle_count = self.env['purchase.order'].search_count(
                [('origin', '=', self.name)])

# smartbutton for click time the added record only see

    def smart_button(self):
        purchase_order_obj = self.env['purchase.order']

        origin = self.name

        purchase_orders = purchase_order_obj.search([('origin', '=', origin)])

        return {
            'name': _('RFQ '),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('id', 'in', purchase_orders.ids)],
            'target': 'current',
        }

    def open_purchase_order_lines(self):
        return {
            'name': _('RFQ Wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.wizards',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_test_test_ids': [(0, 0, {
                    'product_i': line.product_id.id,
                    'description': line.name,
                    'quantity': line.product_uom_qty,
                    'unit_price': line.price_unit,
                    'subtotal': line.price_subtotal,
                }) for line in self.order_line],
                'origin': self.name,  # Set the origin context with the sale order's name
            }
        }



class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.wizards'

    vendorss = fields.Many2one('res.partner', string='Vendor')
    test_test_ids = fields.One2many('test.test', 'linked_ids', string='Test')

# orderplace button click time order added in to purchasemodule and add in to the sourse doccument

    def to_order(self):
        purchase_order_obj = self.env['purchase.order']

        purchase_order = purchase_order_obj.create({
            'partner_id': self.vendorss.id,
            'origin': self._context.get('origin')
        })

        purchase_order_lines = []
        for test in self.test_test_ids:
            purchase_order_line_vals = {
                'product_id': test.product_i.id,
                'name': test.description,
                'product_qty': test.quantity,
                'price_unit': test.unit_price,
                # Add other required fields here
            }

            # Validate mandatory fields before creating the line
            if not all(purchase_order_line_vals.values()):
                raise UserError('Missing required fields in purchase order line!')

            purchase_order_lines.append((0, 0, purchase_order_line_vals))

        purchase_order.write({'order_line': purchase_order_lines})

        return {'type': 'ir.actions.act_window_close'}





class demo(models.TransientModel):
    _name = 'test.test'

    linked_ids = fields.Many2one('purchase.order', string='Linked ID')
    product_i = fields.Many2one('product.product', string='Product')

    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')
    delivered = fields.Float(string='Delivered')
    invoiced = fields.Float(string='Invoiced')
    unit_price = fields.Float(string='Unit Price')
    taxes = fields.Float(string='Taxes')
    subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id')

    currency_id = fields.Many2one('res.currency', string='Currency')
