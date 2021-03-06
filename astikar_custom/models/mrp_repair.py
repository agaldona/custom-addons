# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    def _defaul_quotation_notes(self):
        return self.env.user.company_id.sale_note

    @api.depends('partner_id', 'operations', 'fees_lines', 'operations.tax_id',
                 'operations.to_invoice', 'operations.price_unit',
                 'operations.expected_qty', 'operations.product_uom_qty',
                 'operations.product_id', 'operations.discount',
                 'operations.discount2', 'operations.discount3',
                 'operations.price_subtotal', 'fees_lines.to_invoice',
                 'fees_lines.tax_id', 'fees_lines.price_unit',
                 'fees_lines.product_uom_qty', 'fees_lines.product_id',
                 'fees_lines.discount', 'fees_lines.discount2',
                 'fees_lines.discount3', 'fees_lines.price_subtotal')
    @api.multi
    def _compute_repair_amount(self):
        for repair in self:
            untaxed = 0.0
            taxed = 0.0
            for line in repair.operations.filtered(lambda x: x.to_invoice):
                untaxed += line.price_subtotal
                qty = line.expected_qty or line.product_uom_qty
                price = (line.price_unit *
                         (1 - (line.discount or 0.0) / 100) *
                         (1 - (line.discount2 or 0.0) / 100) *
                         (1 - (line.discount3 or 0.0) / 100))
                tax_calculate = line.tax_id.compute_all(
                    price, qty, line.product_id, repair.partner_id)
                taxed += sum(x['amount'] for x in tax_calculate['taxes'])
            for line in repair.fees_lines.filtered(lambda x: x.to_invoice):
                untaxed += line.price_subtotal
                price = (line.price_unit *
                         (1 - (line.discount or 0.0) / 100) *
                         (1 - (line.discount2 or 0.0) / 100) *
                         (1 - (line.discount3 or 0.0) / 100))
                tax_calculate = line.tax_id.compute_all(
                    price, line.product_uom_qty, line.product_id,
                    repair.partner_id)
                taxed += sum(x['amount'] for x in tax_calculate['taxes'])
            repair.amnt_untaxed = untaxed
            repair.amnt_tax = taxed
            repair.amnt_total = untaxed + taxed

    @api.multi
    @api.depends('partner_id', 'partner_id.property_payment_term')
    def _compute_date_due(self):
        for repair in self:
            if repair.partner_id and repair.partner_id.property_payment_term:
                pterm_list = repair.partner_id.property_payment_term.compute(
                    value=1, date_ref=False)[0]
                if pterm_list:
                    repair.date_due = max(line[0] for line in pterm_list)
            else:
                repair.date_due = fields.Date.from_string(fields.Date.today())

    name = fields.Char(default='/')
    quotation_notes = fields.Text(default=_defaul_quotation_notes)
    amnt_untaxed = fields.Float(string='Untaxed Amount',
                                compute='_compute_repair_amount', store=True)
    amnt_tax = fields.Float(string='Taxes', compute='_compute_repair_amount',
                            store=True)
    amnt_total = fields.Float(string='Total', compute='_compute_repair_amount',
                              store=True)
    date_due = fields.Date(compute='_compute_date_due')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).copy(default)

    @api.multi
    def action_show_purchase_order(self):
        self.ensure_one()
        self = self.with_context(
            default_repair_analytic_id=self.analytic_account.id)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,graph,calendar',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'purchase.view_purchase_order_filter').id,
            'domain': "[('repair_analytic_id', '=', " +
            str(self.analytic_account.id) + ")]",
            'context': self.env.context
            }

    @api.multi
    def action_show_account_invoice(self):
        self.ensure_one()
        self = self.with_context(
            default_repair_analytic_id=self.analytic_account.id,
            default_type='in_invoice', type='in_invoice',
            journal_type='purchase')
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,calendar,graph',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'account.view_account_invoice_filter').id,
            'domain': "[('repair_analytic_id', '=', " +
            str(self.analytic_account.id) + "), ('type','=','in_invoice')]",
            'context': self.env.context
            }

    @api.multi
    def action_show_purchase_order_lines(self):
        self.ensure_one()
        self = self.with_context(
            default_account_analytic_id=self.analytic_account.id)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order.line',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'purchase.view_purchase_order_filter').id,
            'domain': "[('account_analytic_id', '=', " +
            str(self.analytic_account.id) + ")]",
            'context': self.env.context
            }

    @api.multi
    def action_show_account_invoice_lines(self):
        self.ensure_one()
        self = self.with_context(
            default_account_analytic_id=self.analytic_account.id)
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,calendar,graph',
            'res_model': 'account.invoice.line',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'account.view_account_invoice_filter').id,
            'domain': "[('account_analytic_id', '=', " +
            str(self.analytic_account.id) + "),"
            "('invoice_id.type', '=', 'in_invoice')]",
            'context': self.env.context
            }


class MrpRepairLine(models.Model):

    _inherit = 'mrp.repair.line'

    @api.multi
    def write(self, vals):
        if 'product_uom_qty'in vals:
            vals['load_cost'] = bool(vals.get('product_uom_qty', 0.0))
        return super(MrpRepairLine, self).write(vals)

    @api.model
    def create(self, vals):
        vals['load_cost'] = bool(vals.get('product_uom_qty', 0.0))
        return super(MrpRepairLine, self).create(vals)


class MrpRepairFee(models.Model):

    _inherit = 'mrp.repair.fee'

    is_from_menu = fields.Boolean(string='Created from menu', default=False)

    @api.model
    def create(self, vals):
        vals['load_cost'] = not vals.get('to_invoice', False)
        return super(MrpRepairFee, self).create(vals)
