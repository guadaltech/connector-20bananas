{
    "name": "Connector 20 Bananas",
    "version": "13.0.1.0.0",
    "author": "Guadaltech Soluciones Tecnológicas",
    "category": "Generic Modules",
    "depends": ["connector", "sale", "product", "contacts", "l10n_es"],
    "data": [
        "data/cast_days_data.xml",
        "security/ir.model.access.csv",
        "views/bananas_connector_menus.xml",
        "views/bananas_backend_views.xml",
        "views/res_partner_views.xml",
        "views/delivery_days_views.xml",
        "views/sale_order_views.xml",
        "wizard/create_cron_for_backend_conector_views.xml",
    ],
    "application": True,
}
