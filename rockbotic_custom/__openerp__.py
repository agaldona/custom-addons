# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Rockbotic - Custom",
    "version": "8.0.1.2.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "product",
        "purchase",
        "crm",
        "mail",
        "marketing",
        "sale_order_create_event",
        "sale_order_line_performance",
        "sale_service_recurrence_configurator",
        "sale_crm_event_planned_by_sale_line",
        "sale_product_variants",
        "event_sale",
        "event_planned_by_sale_line",
        "event_registration_analytic",
        "website_event_track",
        "partner_group",
        "partner_contact_birthdate",
        "partner_student_course",
        "hr",
        "report_custom_filename",
        "l10n_es",
        "event_group_description",
        "account_payment_partner",
        "account_analytic_analysis_recurring_day",
        "website_quote",
        "event_registration_sepa",
        "event_track_info"
    ],
    "data": [
        "wizard/crm_make_sale_view.xml",
        "views/sale_order_view.xml",
        "views/crm_lead_view.xml",
        "views/res_partner_view.xml",
        "views/product_category_view.xml",
        "views/event_event_view.xml",
        "views/event_track_view.xml",
        "views/event_track_presence_view.xml",
        "views/hr_employee_view.xml",
        "views/account_invoice_view.xml",
        "views/res_company_view.xml",
        "views/account_view.xml",
        "views/event_registration_view.xml",
        "report/rockbotic_custom_view.xml",
        "report/rockbotic_layout_view.xml",
        "report/rockbotic_reports.xml",
        "report/rockbotic_presences_report.xml",
        "report/rockbotic_paperformat.xml",
        "views/access_rules.xml",
    ],
    "installable": True,
    "application": True,
}
