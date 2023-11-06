from odoo import api, fields, models, _


class SportsCenterPost(models.Model):
    _name = "sports.center.post"
    _description = "Employee position model"

    name = fields.Char(string="Name of the position held",
                       required=True)
    salary_per_hour = fields.Float(string="Payment per hour of work",
                                   default=7.50,
                                   required=True)
    name_post_id = fields.Many2one(comodel_name="sports.center.employee",
                                   string="Name of the tennis sports center card",
                                   readonly=True)
