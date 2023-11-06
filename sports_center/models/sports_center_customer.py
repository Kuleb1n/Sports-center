from odoo import api, fields, models, _


class SportsCenterCustomer(models.Model):
    _name = "sports.center.customer"
    _description = "User Model"

    name = fields.Char(string="Username",
                       required=True)
    email = fields.Char(string="Email",
                        required=True)
    phone_number = fields.Char(string="Phone number",
                               required=True)

    booking_time_ids = fields.Many2many(string="Booking(s)",
                                        comodel_name="sports.center.court.booking.time",
                                        relation="user_booking_time_rel",
                                        column1="booking_time_id",
                                        column2="user_id", )

    _sql_constraints = [
        ("email", "unique (email)",
         "A user with this email address already exists!"),
    ]

    @api.depends("name")
    def name_get(self):
        res = []
        for record in self:
            name = f"{record.email} | {record.name}"
            res.append((record.id, name))
        return res
