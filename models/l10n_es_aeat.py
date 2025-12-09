# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


# --------------------------------------------------------------------------------------------------------------
class MotsoftL10nEsAeatMod111Report(models.Model):
    _inherit = "l10n.es.aeat.mod111.report"

    partners_info_8_9 = fields.One2many(comodel_name='aeat.perceptor', compute="compute_partners_info_8_9", store=False)

    def compute_partners_info_8_9(self):
        # Buscar algún tipo de abstracción y reuso con las funciones de desglose del Mod-115

        myrecords_base = []
        myrecords_tax = []

        for line in self.tax_line_ids.filtered(lambda l: l.field_number == 8 or l.field_number == 9):
            grouped_lines = line.move_line_ids.read_group(domain=[('id', 'in', line.move_line_ids.ids)],
                                                          fields=['partner_id', 'debit', 'credit'],
                                                          groupby=['partner_id'],
                                                          lazy=False)

            for move_line in grouped_lines:
                partner_id = self.env['res.partner'].browse(move_line['partner_id'][0])
                amount = move_line['debit'] - move_line['credit']
                if line.field_number == 8:
                    myrecords_base.append({"name": partner_id.name, "vat": partner_id.vat, "base_amount": amount})
                if line.field_number == 9:
                    myrecords_tax.append({"name": partner_id.name, "vat": partner_id.vat, "tax_amount": amount})

        myrecords = []
        for i in range(0, len(myrecords_base)):
            myrecords.append({"name": myrecords_base[i]["name"],
                              "vat": myrecords_base[i]["vat"],
                              "base_amount": myrecords_base[i]["base_amount"],
                              "tax_amount": abs(myrecords_tax[i]["tax_amount"]),
                              })

        if len(myrecords) == 0:
            raise ValidationError("No hay registros con saldo distinto a 0.")

        self.partners_info_8_9 = myrecords

    def show_tax_lines(self):
        self.ensure_one()
        action = self.env.ref('motsoft_aeat.aeat_report_action').read()[0]
        action['domain'] = [('model', '=', 'l10n.es.aeat.mod111.report'),('res_id', '=', self.id)]
        return action
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
class MotsoftAeatPerceptor(models.Model):
    _name = "aeat.perceptor"

    name = fields.Char(store=False)
    vat = fields.Char(store=False)
    base_amount = fields.Float(store=False)
    tax_amount = fields.Float(store=False)
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
class MotsoftL10nEsAeatMod115Report(models.Model):
    _inherit = "l10n.es.aeat.mod115.report"

    partners_info_2_3 = fields.One2many(comodel_name='aeat.perceptor', compute="compute_partners_info_2_3", store=False)

    def compute_partners_info_2_3(self):
        # Buscar algún tipo de abstracción y reuso con las funciones de desglose del Mod-111

        myrecords_base = []
        myrecords_tax = []
        for line in self.tax_line_ids:
            grouped_lines = line.move_line_ids.read_group(domain=[('id', 'in', line.move_line_ids.ids)],
                                                          fields=['partner_id', 'debit', 'credit'],
                                                          groupby=['partner_id'],
                                                          lazy=False)

            for move_line in grouped_lines:
                partner_id = self.env['res.partner'].browse(move_line['partner_id'][0])
                amount = move_line['debit'] - move_line['credit']
                if line.field_number == 2:
                    myrecords_base.append({"name": partner_id.name, "vat": partner_id.vat, "base_amount": amount})
                if line.field_number == 3:
                    myrecords_tax.append({"name": partner_id.name, "vat": partner_id.vat, "tax_amount": amount})

        myrecords = []
        for i in range(0, len(myrecords_base)):
            myrecords.append({"name": myrecords_base[i]["name"],
                              "vat": myrecords_base[i]["vat"],
                              "base_amount": myrecords_base[i]["base_amount"],
                              "tax_amount": abs(myrecords_tax[i]["tax_amount"]),
                              })

        if len(myrecords) == 0:
            raise ValidationError("No hay registros con saldo distinto a 0.")

        self.partners_info_2_3 = myrecords

    def show_tax_lines(self):
        self.ensure_one()
        action = self.env.ref('motsoft_aeat.aeat_report_action').read()[0]
        action['domain'] = [('model', '=', 'l10n.es.aeat.mod115.report'),('res_id', '=', self.id)]
        return action
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
class MotsoftL10nEsAeatMod303Report(models.Model):
    _inherit = "l10n.es.aeat.mod303.report"

    def show_tax_lines(self):
        self.ensure_one()
        action = self.env.ref('motsoft_aeat.aeat_report_action').read()[0]
        action['domain'] = [('model', '=', 'l10n.es.aeat.mod303.report'), ('res_id', '=', self.id)]
        #action['domain'] = literal_eval(action['domain'])
        #action['domain'].append(('res_id', '=', self.id))
        #action['domain'].append(('model', '=', 'l10n.es.aeat.mod303.report'))

        return action
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
class MotsoftL10nEsAeatMod347Report(models.Model):
    _inherit = "l10n.es.aeat.mod347.partner_record"

    amount_matches = fields.Boolean(compute="compute_amount_matches", store=False, default=False)

    @api.depends('amount', 'first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter')
    def compute_amount_matches(self):
        amount_from_quarters = self.first_quarter + self.second_quarter + self.third_quarter + self.fourth_quarter

        self.amount_matches = float_compare(amount_from_quarters, self.amount, precision_digits=2) == 0
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
class MotsoftL10nEsAeatTaxLine(models.Model):
    _inherit = "l10n.es.aeat.tax.line"

    def get_calculated_move_lines(self):
        res = super(MotsoftL10nEsAeatTaxLine, self).get_calculated_move_lines()

        view_form = self.env.ref('account.view_move_line_form')
        res['views'].append((view_form.id, 'form'))

        return res
# --------------------------------------------------------------------------------------------------------------
