from odoo import api, fields, models


class SportsCenterBookingTimeStart(models.Model):
    _name = "sports.center.court.booking.time.start"
    _description = "Training start intervals"

    name = fields.Char(string="Time")
    sports_center_court_booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                                           inverse_name="training_start_time_id",
                                                           string="Booking time", )

    def name_get(self):
        res = []
        for record in self:
            name = str(record.name) + "" + ":00"
            res.append((record.id, name))
        return res


class SportsCenterBookingTimeEnd(models.Model):
    _name = "sports.center.court.booking.time.end"
    _description = "Training end intervals"

    name = fields.Char(string="Hour")
    sports_center_court_booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                                           inverse_name="training_end_time_id",
                                                           string="Booking time", )

    def name_get(self):
        res = []
        for record in self:
            name = str(record.name) + "" + ":00"
            res.append((record.id, name))
        return res
