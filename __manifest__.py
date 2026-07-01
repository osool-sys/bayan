# -*- coding: utf-8 -*-
{
    'name': 'Bayan',
    'version': '17.0.1.0.0',
    'summary': 'Mobile HR & attendance backend — secure REST API for the Bayan app',
    'description': """
Bayan
=====

Bayan is the Odoo backend that powers the Bayan mobile application. It exposes a
secure, token-authenticated REST API that lets employees manage their attendance
and profile from their phone, and lets each company brand and configure the app
from Odoo.

Key features
------------
* **Token-based authentication** — public login/register/refresh endpoints issue
  API tokens; every protected endpoint is guarded by per-request token validation
  (independent of Odoo web sessions).
* **Attendance from mobile** — check-in / check-out, current status, and history,
  acting on the employee linked to the authenticated user.
* **Automatic check-out** — a scheduled job force-closes any attendance left open
  longer than the allowed window, keeping records clean.
* **User profile & account** — user info endpoint and soft account deletion
  (archiving) with safe re-registration handling.
* **Per-company app configuration** — theme colors, geofence center coordinates,
  and signup requirements are configured on the Company form and served to the
  app, so branding and location rules are managed entirely from Odoo.
* **Localized responses** — datetimes are converted to the company timezone and
  worked hours are formatted for display.

Bayan depends on the standard **HR** and **Attendance** modules and adds no new
models — it extends existing ones and layers the mobile API on top.
    """,
    'category': 'Human Resources',
    'author': 'Osool Systems',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
