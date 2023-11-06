import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SportsCenterEmployee(models.Model):
    _name = "sports.center.employee"
    _description = "Model of a sports center employee"

    name = fields.Char(string="Name",
                       required=True, )
    surname = fields.Char(string="Surname",
                          required=True, )
    patronymic = fields.Char(string="Patronymic",
                             required=True, )
    birth_date = fields.Date(string="Date of birth",
                             required=True, )
    email = fields.Char(string='Email',
                        required=True)
    card_id = fields.Many2one(comodel_name="sports.center.card",
                              string="Name of the sports center card",
                              required=True, )
    sports_center_post_ids = fields.One2many(comodel_name="sports.center.post",
                                             inverse_name="name_post_id",
                                             string="Employee's position", )
    user_id = fields.Many2one(comodel_name="res.users",
                              string="User",
                              default=lambda self: self.env.user,
                              required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.company,
                                 index=True,
                                 required=True, )
    sports_center_court_booking_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                                      inverse_name="employee_id",
                                                      string="Booking time",
                                                      readonly=True)

    sports_center_accrual_employee_ids = fields.One2many(comodel_name="sports.center.accrual.employee",
                                                         inverse_name="employee_id",
                                                         string="Accrual", )

    sports_center_employee_salary_ids = fields.One2many(comodel_name="sports.center.employee.salary",
                                                        inverse_name="employee_id",
                                                        string="Employee's salary", )

    _sql_constraints = [
        ("email", "unique (email)",
         "An employee with such an email address already exists!"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self.env["sports.center.employee.salary"].create({
            "current_year": res.write_date.year,
            "employee_id": res.id,
        })
        return res

    @api.depends('name')
    def name_get(self):
        res = []
        for record in self:
            name = f"{record.email} | {record.name}"
            res.append((record.id, name))
        return res

    @api.constrains("sports_center_post_ids")
    def _check_sports_center_post(self):

        if len(self.mapped("sports_center_post_ids")) != 1:
            raise UserError(_("One employee - one position!"))

    def action_view_earnings(self):
        """
        Viewing earnings
        """
        self.ensure_one()
        return {
            "name": "Income",
            "type": "ir.actions.act_window",
            "view_type": "list",
            "view_mode": "list",
            "views": [(False, "list")],
            "res_model": "sports.center.employee.salary",
            "target": "current",
            "domain": [("employee_id", "=", self.id)],
        }


class SportsCenterAccrualEmployee(models.Model):
    _name = "sports.center.accrual.employee"
    _description = "All charges for bookings"

    accrual_date = fields.Datetime(string="Accrual date",
                                   default=datetime.datetime.now(),
                                   readonly=True, )
    accrual_amount = fields.Float(string="Accrual amount",
                                  readonly=True, )
    employee_id = fields.Many2one(comodel_name="sports.center.employee",
                                  string="Employee",
                                  readonly=True, )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        record = self.env["sports.center.employee.salary"].search([("employee_id", "=", res.employee_id.id),
                                                                   ("current_year", "=", res.accrual_date.year)])
        dct_months = {1: "january", 2: "february", 3: "march", 4: "april",
                      5: "may", 6: "june", 7: "july", 8: "august",
                      9: "september", 10: "october", 11: "november", 12: "december", }
        current_month = dct_months.get(int(res.accrual_date.month))

        if record:
            record[str(current_month)] += res.accrual_amount
            record.annual_salary += res.accrual_amount
        else:
            self.env["sports.center.employee.salary"].create({
                "current_year": res.accrual_date.year,
                "employee_id": res.employee_id.id,
                str(current_month): res.accrual_amount,
                "annual_salary": res.accrual_amount,
            })

        return res


class SportsCenterEmployeeSalary(models.Model):
    _name = "sports.center.employee.salary"
    _description = "Employee's salary model"

    current_year = fields.Char(string="Year",
                               readonly=True, )
    january = fields.Float(string="January",
                           default=0,
                           readonly=True, )
    february = fields.Float(string="February",
                            default=0,
                            readonly=True, )
    march = fields.Float(string="March",
                         default=0,
                         readonly=True, )
    april = fields.Float(string="April",
                         default=0,
                         readonly=True, )
    may = fields.Float(string="May",
                       default=0,
                       readonly=True, )
    june = fields.Float(string="June",
                        default=0,
                        readonly=True, )
    july = fields.Float(string="July",
                        default=0,
                        readonly=True, )
    august = fields.Float(string="August",
                          default=0,
                          readonly=True, )
    september = fields.Float(string="September",
                             default=0,
                             readonly=True, )
    october = fields.Float(string="October",
                           default=0,
                           readonly=True, )
    november = fields.Float(string="November",
                            default=0,
                            readonly=True, )
    december = fields.Float(string="December",
                            default=0,
                            readonly=True, )
    annual_salary = fields.Float(string="Annual salary",
                                 default=0,
                                 readonly=True, )
    employee_id = fields.Many2one(comodel_name="sports.center.employee",
                                  string="Employee",
                                  store=True,
                                  readonly=True, )
