from odoo import api, fields, models, _


class SportsCenterWorkout(models.Model):
    _name = "sports.center.workout"
    _description = "Training model"

    name = fields.Char(string="Type of training",
                       required=True, )
    sports_center_court_booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                                           inverse_name="type_training_id",
                                                           string="Booking time",
                                                           readonly=True, )
