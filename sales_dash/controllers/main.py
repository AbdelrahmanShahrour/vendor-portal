# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from collections import Counter, defaultdict
import json

class SalesPortalDashboard(http.Controller):

    @http.route('/portal/sales-dashboard', type='http', auth='user', website=True)
    def sales_dashboard(self, **kwargs):
        SaleOrder = request.env['sale.order']
        Partner = request.env['res.partner']
        User = request.env['res.users']

        domain = []

        selected_state = kwargs.get('state')
        selected_user = kwargs.get('user_id')
        selected_partner = kwargs.get('partner_id')

        if selected_state:
            domain.append(('state', '=', selected_state))
        if selected_user and selected_user.isdigit():
            domain.append(('user_id', '=', int(selected_user)))
        if selected_partner and selected_partner.isdigit():
            domain.append(('partner_id', '=', int(selected_partner)))

        orders = SaleOrder.sudo().search(domain)

        # For filters
        states = list(SaleOrder._fields['state'].selection)
        users = User.sudo().search([])
        partners = Partner.sudo().search([])

        # Orders by State
        state_counter = Counter(order.state for order in orders)

        # Sales Total per User
        user_sales = defaultdict(float)
        for order in orders:
            user_name = order.user_id.name or 'Unknown'
            user_sales[user_name] += order.amount_total

        # Monthly Sales Trend
        monthly_sales = defaultdict(float)
        for order in orders:
            if order.date_order:
                month = order.date_order.strftime('%b')
                monthly_sales[month] += order.amount_total

        # Top Customers
        customer_sales = defaultdict(float)
        for order in orders:
            if order.partner_id:
                customer_sales[order.partner_id.name] += order.amount_total
        top_customers = dict(sorted(customer_sales.items(), key=lambda x: x[1], reverse=True)[:5])

        return request.render('sales_dash.sales_portal_dashboard', {
            'orders': orders,
            'states': states,
            'users': users,
            'partners': partners,
            'selected_state': selected_state,
            'selected_user': int(selected_user) if selected_user and selected_user.isdigit() else None,
            'selected_partner': int(selected_partner) if selected_partner and selected_partner.isdigit() else None,
            'json_state_data': json.dumps(state_counter),
            'json_user_sales': json.dumps(user_sales),
            'json_monthly_sales': json.dumps(monthly_sales),
            'json_top_customers': json.dumps(top_customers),
        })