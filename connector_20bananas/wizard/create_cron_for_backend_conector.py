from odoo import api, fields, models


class CronBananasConector(models.TransientModel):
    _name = "wizard.cron.bananas.conector"
    _description = "Create the cron for the backend conector"

    name = fields.Char(string="Name")
    interval_num = fields.Integer(string="Repeat Every")
    interval_type = fields.Selection(
        [
            ("minutes", "Minutes"),
            ("hours", "Hours"),
            ("days", "Days"),
            ("weeks", "Weeks"),
            ("months", "Months"),
        ],
        string="Interval Unit",
        default="months",
    )
    numbercall = fields.Integer(
        string="Number of Calls",
        default=1,
        help="How many times the method is called,\na negative number indicates no limit.",
    )
    priority = fields.Integer(
        default=5,
        help="The priority of the job, as an integer: 0 means higher priority, 10 means lower priority.",
    )
    nextcall = fields.Datetime(
        string="Next Execution Date",
        required=True,
        default=fields.Datetime.now,
        help="Next planned execution date for this job.",
    )
    doall = fields.Boolean(
        string="Repeat Missed",
        help="Specify if missed occurrences should be executed when the server restarts.",
    )
    model_id = fields.Many2one(comodel_name="bananas.backend")

    type_import = fields.Char()

    def create_cron(self):
        code = "allrecord = env[model._name].search([])\nfor rec in allrecord:\n        rec.import_orders()"
        model = self.env["ir.model"].search([("model", "=", self.model_id._name)])
        cron = self.env["ir.cron"].create(
            {
                "name": self.name,
                "interval_number": self.interval_num,
                "interval_type": self.interval_type,
                "numbercall": self.numbercall,
                "priority": self.priority,
                "nextcall": self.nextcall,
                "doall": self.doall,
                "code": code,
                "model_id": model.id,
            }
        )
        # a lo mejor lo llevo a la pagina de listas de crones asociados con el modelo,
        # por ahora que se cierre
