{
    "name": "Connector 20 Bananas",
    "version": "15.0.1.0.1",
    "author": "Guadaltech Soluciones Tecnológicas, Juan Carlos Jaén Iglesias",
    "website": "https://github.com/OCA/queue",
    "license": "AGPL-3",
    "category": "Generic Modules",
    "depends": [
        "connector",
        "sale",
        "sale_management",
        "product",
        "contacts",
        "l10n_es",
    ],
    "data": [
        "data/cast_days_data.xml",
        "data/sequences.xml",
        "data/crons.xml",
        "security/ir.model.access.csv",
        "views/bananas_connector_menus.xml",
        "views/bananas_backend_views.xml",
        "views/res_partner_views.xml",
        "views/delivery_days_views.xml",
        "views/sale_order_views.xml",
        "views/connections_bananas_cron_views.xml",
        "views/product_views.xml",
        "views/bananas_binding_res_partner_views.xml",
        "views/bananas_binding_product_template_views.xml",
        "views/bananas_binding_product_pricelist_views.xml",
        "wizard/create_cron_for_backend_conector_views.xml",
    ],
    "application": True,
}
