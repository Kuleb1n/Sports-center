import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SportsCenterCourtBooking(models.Model):
    _name = "sports.center.court.booking"
    _description = "Booking and calculation of the cost of training"

    sports_center_court_booking_time_ids = fields.One2many(comodel_name="sports.center.court.booking.time",
                                                           inverse_name="court_booking_id",
                                                           string="Booking time", )

    total_hours = fields.Integer(string="Total number of training hours",
                                 default=0,
                                 compute="_compute_total_hours")
    cost_training = fields.Float(string="The cost of training",
                                 default=0,
                                 compute="_compute_cost_training", )
    is_discount = fields.Boolean(string="Discount",
                                 compute="_compute_is_discount",
                                 help="If the training time is more than forty hours, a discount of "
                                      "fifteen percent of the cost of renting a court is provided.",
                                 )
    dimension_discount = fields.Float(string="The dimension of the discount",
                                      default=15,
                                      readonly=True, )
    discount_equal = fields.Float(string="The discount is equal to",
                                  default=0,
                                  compute="_compute_discount_equal", )

    final_price = fields.Float(string="Final price",
                               default=0,
                               compute="_compute_final_price", )

    @api.depends("sports_center_court_booking_time_ids")
    def _compute_total_hours(self):
        if self.sports_center_court_booking_time_ids:
            self.total_hours = sum(self.sports_center_court_booking_time_ids.mapped(lambda x: x.duration))
        else:
            self.total_hours = 0

    @api.depends("sports_center_court_booking_time_ids")
    def _compute_cost_training(self):
        if self.sports_center_court_booking_time_ids:
            self.cost_training = sum(
                self.sports_center_court_booking_time_ids.mapped(lambda x: x.cost_training))
        else:
            self.cost_training = 0

    @api.depends("total_hours")
    def _compute_is_discount(self):
        for record in self:
            if record.total_hours >= 40:
                record.is_discount = True
            else:
                record.is_discount = False

    @api.depends("is_discount")
    def _compute_discount_equal(self):
        if self.is_discount:
            self.discount_equal = sum(self.sports_center_court_booking_time_ids.tennis_court_id.mapped(
                lambda x: x.total_price * self.dimension_discount * 0.01)) * self.total_hours
        else:
            self.discount_equal = 0

    @api.depends("cost_training")
    def _compute_final_price(self):
        if self.is_discount:
            self.final_price = round(self.cost_training - self.discount_equal + 0.5)
        else:
            self.final_price = self.cost_training

    @api.onchange("sports_center_court_booking_time_ids")
    def _onchange_booking_time(self):
        cort_ids = list(set(self.sports_center_court_booking_time_ids.mapped(lambda x: x.tennis_court_id.id)))

        for cort_id in cort_ids:
            lst_start_training = sorted(self.sports_center_court_booking_time_ids.filtered(
                lambda x: x.tennis_court_id.id == cort_id).mapped("start_training"))
            lst_end_training = sorted(self.sports_center_court_booking_time_ids.filtered(
                lambda x: x.tennis_court_id.id == cort_id).mapped("end_training"))

            booking_list = list(zip(lst_start_training, lst_end_training))
            count = 0
            for i in booking_list[1:]:
                first_booking = booking_list[0 + count]
                if first_booking[0].date() == i[0].date():
                    if (first_booking[0].time() <= i[0].time() < first_booking[1].time() or
                            first_booking[0].time() < i[1].time() <= first_booking[1].time()):
                        raise UserError(
                            _(f"This time is already booked: {first_booking[0]} - {first_booking[1]}! "
                              f"Add to Time GMT +3"))
                count += 1


class SportsCenterCourtBookingTime(models.Model):
    _name = "sports.center.court.booking.time"
    _description = """Booking model with a choice of training date, time, 
                    coach, type of training, as well as training participants
                    """

    def _domain_tennis_court_id(self):
        if self.env.context.get("tennis_court_id"):
            return [("id", "in", self.env.context.get("tennis_court_id"))]
        else:

            return []

    sports_center_court_card_id = fields.Many2one(comodel_name="sports.center.court.card",
                                                  string="Center court card",
                                                  readonly=True)
    court_booking_id = fields.Many2one(comodel_name="sports.center.court.booking",
                                       string="Court booking",
                                       readonly=True)

    user_ids = fields.Many2many(string="User(s)",
                                comodel_name="sports.center.customer",
                                relation="user_booking_time_rel",
                                column1="user_id",
                                column2="booking_time_id",
                                required=True, )

    tennis_court_id = fields.Many2one(comodel_name="sports.center.court",
                                      string="Tennis court",
                                      domain=_domain_tennis_court_id,
                                      required=True)

    type_training_id = fields.Many2one(comodel_name="sports.center.workout",
                                       string="Type of training",
                                       required=True, )

    employee_id = fields.Many2one(comodel_name="sports.center.employee",
                                  string="Employee",
                                  required=True, )

    date_registration_training = fields.Date(string="Date of registration for training",
                                             default=fields.Date.context_today,
                                             required=True)

    booking_status = fields.Selection([("draft", "Draft"), ("active", "Active"),
                                       ("inactive", "Inactive"), ],
                                      string="Booking status",
                                      default="draft", )

    training_start_time_id = fields.Many2one(comodel_name="sports.center.court.booking.time.start",
                                             string="Time from",
                                             required=True, )

    training_end_time_id = fields.Many2one(comodel_name="sports.center.court.booking.time.end",
                                           string="Time until",
                                           required=True, )

    start_training = fields.Datetime(string="Start of training in",
                                     default=lambda self: datetime.datetime.now().replace(minute=0, second=0,
                                                                                          microsecond=0),
                                     compute="_compute_start_training",
                                     store=True, )

    end_training = fields.Datetime(string="End of training in",
                                   default=lambda self: datetime.datetime.now().replace(minute=0, second=0,
                                                                                        microsecond=0),
                                   compute="_compute_end_training",
                                   store=True,
                                   readonly=True)

    cost_training = fields.Float(string="The cost of training",
                                 default=0,
                                 compute="_compute_cost_training",
                                 readonly=True)

    duration = fields.Integer(string="Duration",
                              default=0,
                              compute="_compute_duration",
                              readonly=True)

    @api.model_create_multi
    def create(self, values_list):
        res = super().create(values_list)
        for record in res:
            accrual_amount = record.duration * record.employee_id.sports_center_post_ids.salary_per_hour * 0.8
            self.env["sports.center.accrual.employee"].create({
                "accrual_amount": accrual_amount,
                "employee_id": record.employee_id.id,
            })
            accrual_amount_profit = record.cost_training - accrual_amount
            self.env["sports.center.finance"].create({
                "accrual_amount_profit": accrual_amount_profit,
                "sports_center_card_id": record.tennis_court_id.sports_center_court_card_id.sports_center_card_id.id,
            })
        res.sports_center_court_card_id = self.env.context.get("court_card_id")
        return res

    def write(self, vals):
        res = super().write(vals)

        return res

    def name_get(self):
        res = []
        for record in self:
            name = "Booking № " + str(record.id)
            res.append((record.id, name))
        return res

    @api.depends("date_registration_training", "training_start_time_id")
    def _compute_start_training(self):
        for record in self:
            if record.date_registration_training and record.training_start_time_id:
                record.start_training = datetime.datetime(year=record.date_registration_training.year,
                                                          month=record.date_registration_training.month,
                                                          day=record.date_registration_training.day,
                                                          hour=int(record.training_start_time_id.name) - 3,
                                                          minute=0, )

    @api.depends("date_registration_training", "training_end_time_id")
    def _compute_end_training(self):
        for record in self:
            if record.date_registration_training and record.training_end_time_id:
                record.end_training = datetime.datetime(year=record.date_registration_training.year,
                                                        month=record.date_registration_training.month,
                                                        day=record.date_registration_training.day,
                                                        hour=int(record.training_end_time_id.name) - 3,
                                                        minute=0, )

    @api.depends("training_start_time_id", "training_end_time_id")
    def _compute_duration(self):
        for record in self:
            if record.training_start_time_id and record.training_end_time_id:
                record.duration = int(record.training_end_time_id.name) - int(record.training_start_time_id.name)
            else:
                record.duration = 0

    @api.depends("tennis_court_id", "employee_id", "duration")
    def _compute_cost_training(self):
        for record in self:
            if not record.tennis_court_id and not record.employee_id and not record.duration:
                record.cost_training = 0
            elif record.tennis_court_id and not record.employee_id and not record.duration:
                record.cost_training = record.tennis_court_id.total_price

            elif record.tennis_court_id and record.employee_id and not record.duration:
                record.cost_training = (record.tennis_court_id.total_price +
                                        record.employee_id.sports_center_post_ids.salary_per_hour)

            elif record.tennis_court_id and not record.employee_id and record.duration:
                record.cost_training = record.tennis_court_id.total_price * record.duration

            elif record.tennis_court_id and record.employee_id and record.duration:
                record.cost_training = (record.tennis_court_id.total_price +
                                        record.employee_id.sports_center_post_ids.salary_per_hour) * record.duration

    @api.constrains("date_registration_training")
    def _check_date_registration_training(self):
        for record in self:
            if record.date_registration_training < datetime.date.today():
                raise UserError("The date of registration for training cannot be set as past")

    @api.onchange("date_registration_training", "tennis_court_id", "training_start_time_id", "training_end_time_id")
    def _onchange_training_time(self):
        """
        The domain with unoccupied intervals (id) of the beginning and end of training is returned
        """

        if self.date_registration_training and self.tennis_court_id:

            lst_start_time_ids = self.env["sports.center.court.booking.time"].search(
                [("date_registration_training", "=", self.date_registration_training),
                 ("tennis_court_id", "=", self.tennis_court_id.id)]).mapped(lambda x: x.training_start_time_id.id)

            lst_end_time_ids = self.env["sports.center.court.booking.time"].search(
                [("date_registration_training", "=", self.date_registration_training),
                 ("tennis_court_id", "=", self.tennis_court_id.id)]).mapped(lambda x: x.training_end_time_id.id)

            list_booked_training_start_intervals = []
            list_booked_training_end_intervals = []

            for i in list(zip(lst_start_time_ids, lst_end_time_ids)):
                for j in range(i[0], i[1] + 1):
                    list_booked_training_start_intervals.append(j)

            if self.date_registration_training == datetime.date.today():
                hour = datetime.datetime.now().hour
                if hour >= 4:
                    for i in range(1, hour - 2):
                        list_booked_training_start_intervals.append(i)
                        list_booked_training_end_intervals.append(i)

            if self.training_start_time_id:
                for i in range(1, self.training_start_time_id.id):
                    list_booked_training_end_intervals.append(i)
                if list_booked_training_end_intervals:
                    for num in sorted(lst_start_time_ids):
                        if num >= list_booked_training_end_intervals[-1] + 1:
                            for j in range(num, 16):
                                list_booked_training_end_intervals.append(j)
                            break
                else:
                    if lst_start_time_ids:
                        first_occurrence = sorted(lst_start_time_ids)[0]
                        for j in range(first_occurrence, 16):
                            list_booked_training_end_intervals.append(j)

            return {
                "domain": {
                    "training_start_time_id": [("id", "not in", list_booked_training_start_intervals)],
                    "training_end_time_id": [("id", "not in", list_booked_training_end_intervals)]
                }
            }

    @api.onchange("date_registration_training", "training_start_time_id", "training_end_time_id", "employee_id")
    def _onchange_employee_id(self):
        """
        Based on the data received, when registering for training,
        the domain with trainers who are not working at this time is returned
        """

        if self.date_registration_training and self.training_start_time_id and self.training_end_time_id:
            coach_ids = self.env["sports.center.court.booking.time"].search([
                ("date_registration_training", "=", self.date_registration_training),
                ("training_start_time_id", ">=", self.training_start_time_id.id),
                ("training_end_time_id", "<=", self.training_end_time_id.id),
            ]).mapped(lambda x: x.employee_id.id)
            if self.env.context.get("employee_id"):
                return {
                    "domain": {
                        "employee_id": [("id", "not in", coach_ids),
                                        ("id", "in", self.env.context.get("employee_id"))
                                        ]
                    }}

            return {
                "domain": {
                    "employee_id": [("id", "not in", coach_ids),
                                    ],
                }
            }

    def action_cancel_booking(self):
        """
        Deleting a booked workout
        """

        self.ensure_one()
        booking_time_id = self.env["sports.center.court.booking.time"]
        booking_time_id.search([("id", "=", self.id)]).unlink()

        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "/web"
        }
