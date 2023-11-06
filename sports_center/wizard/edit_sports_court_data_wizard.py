from odoo import fields, models


class EditSportCourtData(models.TransientModel):
    _name = "edit.sports.court.data"
    _description = "Editing sports ground data"

    name = fields.Char(string="New name of the sports ground",
                       required=True)
    standard_rental_price = fields.Float(string="Standard rental price per hour",
                                         required=True, )
    rental_price = fields.Float(string="Seasonal rental",
                                required=True, )

    def update_sports_court(self):
        """
        Updating sports court data
        """

        sports_court_id = self.env.context.get("sports_court_id")
        sports_court = self.env["sports.center.court"].browse(sports_court_id)
        sports_court.name = self.name
        sports_court.standard_rental_price = self.standard_rental_price
        sports_court.rental_price = self.rental_price

        return sports_court
