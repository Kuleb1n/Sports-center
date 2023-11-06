from odoo import api, fields, models, _


class SportsCenterCard(models.Model):
    _name = "sports.center.card"
    _description = """Sports center card. From the card, you can view information about 
                        the working staff, staff earnings, financial statements of income"""

    name = fields.Char(string="Name of the sports center card",
                       required=True, )

    sports_center_employee_ids = fields.One2many(comodel_name="sports.center.employee",
                                                 inverse_name="card_id",
                                                 string="Working staff", )

    court_card_ids = fields.One2many(comodel_name="sports.center.court.card",
                                     inverse_name="sports_center_card_id",
                                     string="Sports court card", )

    sports_center_id = fields.Many2one(comodel_name="sports.center",
                                       string="Sports Center",
                                       required=True,
                                       domain='[("center_card_ids", "=", False)]')
    finance_ids = fields.One2many(comodel_name="sports.center.finance",
                                  inverse_name="sports_center_card_id",
                                  string="Finance", )
    financial_report_ids = fields.One2many(comodel_name="sports.center.financial.report",
                                           inverse_name="sports_center_card_id",
                                           string="Financial report", )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self.env["sports.center.financial.report"].create({
            "current_year": res.write_date.year,
            "sports_center_card_id": res.id,
        })
        return res

    def action_staff(self):
        """
        Method of displaying information about working personnel
        """
        self.ensure_one()
        return {
            "name": _("Earnings of employees"),
            "type": "ir.actions.act_window",
            "view_type": "list",
            "view_mode": "list",
            "views": [(False, "list")],
            "res_model": "sports.center.employee",
            "target": "new",
            "domain": [("card_id", "=", self.id)],
        }

    def action_earnings_employee(self):
        """
        Displaying information about the earnings of the staff
        """
        self.ensure_one()
        return {
            "name": _("Earnings of employees"),
            "type": "ir.actions.act_window",
            "view_type": "list",
            "view_mode": "list",
            "views": [(False, "list")],
            "res_model": "sports.center.employee.salary",
            "target": "current",
            "domain": [("employee_id", "in", self.sports_center_employee_ids.ids)],
        }

    def action_tennis_court_card(self):
        """
        Opening the sports card of the center in the current window
        """
        self.ensure_one()
        return {
            "name": _("Sports center court card"),
            "type": "ir.actions.act_window",
            "view_type": "kanban",
            "view_mode": "kanban",
            "views": [(False, "kanban")],
            "res_model": "sports.center.court.card",
            "target": "current",
            "domain": [("id", "=", self.court_card_ids.ids)],
        }

    def action_financial_statements(self):
        """
        Displaying the financial statements of the sports center
        """
        self.ensure_one()
        return {
            "name": _("Financial statements"),
            "type": "ir.actions.act_window",
            "view_type": "list",
            "view_mode": "list",
            "views": [(False, "list")],
            "res_model": "sports.center.financial.report",
            "target": "current",
            "domain": [("sports_center_card_id", "=", self.id)],
        }

    def action_edit_center_card(self):
        """
        Changing the name of the sports center card
        """
        self.ensure_one()
        return {
            "name": _("Edit the center card"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "edit.center.card",
            "view": [(False, "form")],
            "target": "new",
            "context": {
                "card_id": self.id,
                "default_new_name": self.name,
            }
        }
