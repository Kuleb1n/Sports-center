import datetime

from odoo import api, fields, models, _


class SportsCenterCourt(models.Model):
    _name = "sports.center.court"
    _description = "Sports court model"

    def _default_season(self):
        return self.current_season()

    name = fields.Char(string="Name of the sports court",
                       required=True, )
    season = fields.Selection(selection=[("winter", "Winter"),
                                         ("spring", "Spring"),
                                         ("summer", "Summer"),
                                         ("autumn", "Autumn")],
                              string="Annual season",
                              default=_default_season,
                              compute="_compute_season",
                              readonly=True, )
    standard_rental_price = fields.Float(string="Standard rental price per hour",
                                         default=15,
                                         required=True, )
    rental_price = fields.Float(string="Seasonal rental",
                                default=5,
                                required=True, )
    total_price = fields.Float(string="The final rental price per hour",
                               readonly=True,
                               compute="_compute_total_price", )

    sports_center_court_card_id = fields.Many2one(comodel_name="sports.center.court.card",
                                                  string="Sports center court card", )

    court_booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                             inverse_name="tennis_court_id",
                                             string="Court booking time", )

    _sql_constraints = [
        ("name", "unique (name)",
         "Such a name of the sports ground already exists!"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.sports_center_court_card_id = self.env["sports.center.court.card"].browse(
            self.env.context["sports_center_court_card_id"])

        return res

    @api.depends()
    def _compute_season(self):
        for record in self:
            record.season = self.current_season()

    @api.depends("standard_rental_price", "rental_price")
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.standard_rental_price + record.rental_price

    @staticmethod
    def current_season():
        """
        The method returns the current season of the year
        """

        current_month = datetime.date.today().month
        dict_seasons = {
            "winter": [12, 1, 2],
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11],
        }
        for season, months in dict_seasons.items():
            if current_month in months:
                return season

    def update_tennis_court(self):
        """
        Sports court renovation(name, rental value, seasonal rental)
        """

        self.ensure_one()
        return {
            "name": _("Updating sports court data"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": "edit.sports.court.data",
            "target": "new",
            "context": {
                "sports_court_id": self.id,
                "default_name": self.name,
                "default_standard_rental_price": self.standard_rental_price,
                "default_rental_price": self.rental_price,
            }

        }
