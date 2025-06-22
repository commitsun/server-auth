from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AuthJwtValidator(models.Model):
    _inherit = "auth.jwt.validator"

    user_id_strategy = fields.Selection(
        selection_add=[("login", "Login")],
        ondelete={"login": "cascade"},
    )

    def _get_uid(self, payload):
        if self.user_id_strategy == "login":
            if "username" in payload:
                user = self.env["res.users"].search(
                    [("login", "=", payload["username"])]
                )
                if not user:
                    raise ValidationError(_("Invalid credentials"))
                return user.id
            else:
                raise ValidationError(_("Username not found in token."))
        else:
            return super()._get_uid(payload)
