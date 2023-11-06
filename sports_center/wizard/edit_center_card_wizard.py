from odoo import fields, models


class EditCenterCard(models.TransientModel):
    _name = "edit.center.card"
    _description = "Edit the center card"

    new_name = fields.Char(string="New name of the center card")

    def update_name_center_card(self):
        """
        Updating the name of the center card
        """

        card_id = self.env.context.get("card_id")
        card = self.env["sports.center.card"].browse(card_id)
        card.name = self.new_name
        return card
