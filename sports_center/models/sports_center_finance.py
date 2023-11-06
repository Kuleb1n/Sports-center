import datetime

from odoo import api, fields, models, _


class SportsCenterFinance(models.Model):
    _name = "sports.center.finance"
    _description = "Finance model"

    accrual_date = fields.Datetime(string="Accrual date",
                                   default=datetime.datetime.now(),
                                   readonly=True, )
    accrual_amount_profit = fields.Float(string="The amount of accrual of profit",
                                         readonly=True, )
    sports_center_card_id = fields.Many2one(comodel_name="sports.center.card",
                                            string="Sports center card",
                                            required=True, )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        record = self.env["sports.center.financial.report"].search(
            [("sports_center_card_id", "=", res.sports_center_card_id.id),
             ("current_year", "=", res.accrual_date.year)])
        dct_months = {1: "january", 2: "february", 3: "march", 4: "april",
                      5: "may", 6: "june", 7: "july", 8: "august",
                      9: "september", 10: "october", 11: "november", 12: "december", }
        current_month = dct_months.get(int(res.accrual_date.month))

        if record:
            record[str(current_month)] += res.accrual_amount_profit
            record.annual_profit += res.accrual_amount_profit
        else:
            self.env["sports.center.employee.salary"].create({
                "current_year": res.accrual_date.year,
                "sports_center_card_id": res.sports_center_card_id.id,
                str(current_month): res.accrual_amount_profit,
                "annual_salary": res.accrual_amount_profit,
            })
        return res


class SportsCenterFinancialReport(models.Model):
    _name = "sports.center.financial.report"
    _description = "Profit model by month"

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
    annual_profit = fields.Float(string="Annual profit",
                                 default=0,
                                 readonly=True, )
    sports_center_card_id = fields.Many2one(comodel_name="sports.center.card",
                                            string="Sports center card",
                                            readonly=True, )
