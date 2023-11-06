from odoo import api, fields, models, _


class SportsCenterCard(models.Model):
    _name = "sports.center"
    _description = "A model of a sports center"

    name = fields.Char(string="Name of the sports center",
                       required=True, )
    center_card_ids = fields.One2many(comodel_name="sports.center.card",
                                      inverse_name="sports_center_id",
                                      string="Sports center card", )
