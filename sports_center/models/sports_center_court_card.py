from odoo import api, fields, models, _


class SportsCenterCourtCard(models.Model):
    _name = "sports.center.court.card"
    _description = "The model of the sports card of the playgrounds"

    name = fields.Char(string="Name of the court card on the territory of the sports center",
                       required=True, )
    sports_center_card_id = fields.Many2one(comodel_name="sports.center.card",
                                            string="Center card",
                                            required=True,
                                            domain="[('court_card_ids', '=', False)]")

    court_ids = fields.One2many(comodel_name="sports.center.court",
                                inverse_name="sports_center_court_card_id",
                                string="Sports courts", )
    booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                       inverse_name="sports_center_court_card_id",
                                       string="Booking", )

    def action_create_tennis_court(self):
        """
        Creating a tennis court
        """
        self.ensure_one()
        return {
            "name": "Creating a tennis court",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": "sports.center.court",
            "target": "new",
            "context": {
                "sports_center_court_card_id": self.id,
            }

        }

    def action_go_tennis_court(self):
        """
        Viewing sports courts
        """

        self.ensure_one()
        return {
            "name": "Tennis courts",
            "type": "ir.actions.act_window",
            "view_type": "kanban",
            "view_mode": "kanban",
            "views": [(False, "kanban"), (False, "list")],
            "res_model": "sports.center.court",
            "target": "current",
            "domain": [("id", "in", self.court_ids.ids)],
        }

    def action_go_schedule(self):
        """
        Schedule of booked training sessions ( view - calendar)
        """

        self.ensure_one()
        return {
            "name": "Training schedule",
            "type": "ir.actions.act_window",
            "view_type": "calendar",
            "view_mode": "calendar",
            "views": [[False, "calendar"], [
                self.env.ref("sports_center.view_sports_center_court_booking_time_calendar_event_form").id, "form"]],
            "res_model": "sports.center.court.booking.time",
            "target": "current",
            "domain": [("sports_center_court_card_id", "=", self.id), ],
            "context": {
                "sports_center_court_card_id": self.id,
            }
        }

    def action_sign_up_training_session(self):
        """
        Booking of sports courts
        """
        self.ensure_one()

        return {
            "name": "Sign up for a training session",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": "sports.center.court.booking",
            "target": "new",
            "context": {
                "court_card_id": self.id,
                "tennis_court_id": self.sports_center_card_id.court_card_ids.court_ids.ids,
                "employee_id": self.sports_center_card_id.sports_center_employee_ids.ids,
            }
        }
