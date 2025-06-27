# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from collections import Counter, defaultdict
import json
from datetime import datetime

class SalesPortalDashboard(http.Controller):

    @http.route('/portal/sales-dashboard', type='http', auth='user', website=True)
    def sales_dashboard(self, **kwargs):
        domain = []

        # Filters
        selected_state = kwargs.get('state')
        selected_user = kwargs.get('user_id')
        selected_partner = kwargs.get('partner_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        if selected_state:
            domain.append(('state', '=', selected_state))
        if selected_user:
            domain.append(('user_id', '=', int(selected_user)))
        if selected_partner:
            domain.append(('partner_id', '=', int(selected_partner)))
        if start_date:
            domain.append(('create_date', '>=', start_date))
        if end_date:
            domain.append(('create_date', '<=', end_date + " 23:59:59"))

        orders = request.env['sale.order'].sudo().search(domain)

        # KPIs
        total_sales = sum(order.amount_total for order in orders)
        total_orders = len(orders)
        total_customers = len(set(order.partner_id.id for order in orders if order.partner_id))
        salesperson_totals = Counter(order.user_id.name for order in orders if order.user_id)
        top_salesperson = salesperson_totals.most_common(1)[0][0] if salesperson_totals else '-'

        # States chart
        state_counter = Counter(order.state for order in orders)

        # User sales chart
        user_sales = defaultdict(float)
        for order in orders:
            if order.user_id:
                user_sales[order.user_id.name] += order.amount_total

        # Monthly chart
        monthly_sales = defaultdict(float)
        for order in orders:
            if order.create_date:
                month_str = order.create_date.strftime('%b')  # e.g. Jan, Feb
                monthly_sales[month_str] += order.amount_total

        # Top 5 customers
        customer_sales = defaultdict(float)
        for order in orders:
            if order.partner_id:
                customer_sales[order.partner_id.name] += order.amount_total
        top_customers = dict(sorted(customer_sales.items(), key=lambda item: item[1], reverse=True)[:5])
        print(monthly_sales)

        # Top 20 products by quantity
        product_sales = defaultdict(lambda: {'qty': 0, 'amount': 0.0, 'image_url': ''})

        for order in orders:
            for line in order.order_line:
                product = line.product_id
                if product:
                    product_sales[product.id]['qty'] += line.product_uom_qty
                    product_sales[product.id]['amount'] += line.price_subtotal
                    product_sales[product.id]['image_url'] = f"/web/image/product.product/{product.id}/image_128"

        # Sort and take top 20
        top_products = sorted(product_sales.items(), key=lambda x: x[1]['qty'], reverse=True)[:20]

        # Convert to a list of dicts for easy template use
        top_products_list = []
        for product_id, data in top_products:
            product = request.env['product.product'].sudo().browse(product_id)
            top_products_list.append({
                'name': product.name,
                'qty': int(data['qty']),
                'amount': round(data['amount'], 2),
                'image': data['image_url'],
            })

        currency_symbol = request.env.company.currency_id.symbol

        return request.render('sales_dash.sales_portal_dashboard', {
            'orders': orders,
            'states': request.env['sale.order'].sudo().fields_get(allfields=['state'])['state']['selection'],
            'users': request.env['res.users'].sudo().search([]),
            'partners': request.env['res.partner'].sudo().search([]),
            'selected_state': selected_state,
            'selected_user': int(selected_user) if selected_user and selected_user.isdigit() else '',
            'selected_partner': int(selected_partner) if selected_partner and selected_partner.isdigit() else '',
            'start_date': start_date,
            'end_date': end_date,
            'json_state_data': json.dumps(dict(state_counter)),
            'json_user_sales': json.dumps(dict(user_sales)),
            'json_monthly_sales': json.dumps(dict(monthly_sales)),
            'json_top_customers': json.dumps(dict(top_customers)),
            'total_sales': round(total_sales, 2),
            'total_orders': total_orders,
            'total_customers': total_customers,
            'top_salesperson': top_salesperson,
            'user_name': request.env.user.name,
            'user_image': f"/web/image/res.users/{request.env.user.id}/image_128",
            'company_logo': f"/web/image/res.company/{request.env.company.id}/logo",
            'top_products': top_products_list,
            'currency_symbol': currency_symbol,
        })
