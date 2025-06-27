# vendor-portal

# 💼 Odoo Sales Portal Dashboard

A custom Odoo 18.0 module that provides a **visual and interactive sales dashboard** for portal users.

---

## 🚀 Features

- 📊 **Sales Dashboard Page** for portal users (accessible at `/portal/sales-dashboard`)
- 🎯 Filters:
  - Sales Status (`state`)
  - Salesperson (`user_id`)
  - Customer (`partner_id`)
- 📈 **Interactive Charts** powered by Chart.js:
  - Orders by State (Pie Chart)
  - Sales Total per Salesperson (Bar Chart)
  - Monthly Sales Trend (Line Chart)
  - Top 5 Customers (Doughnut Chart)
- 🔎 **Searchable and Sortable Table**
  - Real-time search with [List.js](https://listjs.com/)
  - Column sorting with [Tablesort](https://github.com/tristen/tablesort)
- 🎨 UI styled with [Tailwind CSS](https://tailwindcss.com/)
- 🔽 Filter dropdowns with [Choices.js](https://github.com/Choices-js/Choices)

---

---

## 📷 Screenshots

>  ![image](https://github.com/AbdelrahmanShahrour/vendor-portal/blob/18.0/screencapture-localhost-8069-portal-sales-dashboard-2025-06-27-23_14_12.png)
- The dashboard with filters and charts
- The searchable table

---

## ⚙️ Installation

1. Copy `sales_dash` folder to your Odoo `addons/` directory.
2. Activate developer mode in Odoo.
3. Go to **Apps → Update Apps List**
4. Search for **Sales Portal Dashboard** and install the module.

---

## 🧠 Notes

- You must have sales orders and users for charts to render meaningfully.
- Portal users need `read` access to `sale.order`, `res.partner`, and `res.users`.

---

## 👨‍💻 Author

**Abdalrahman Shahrour**

---

## 📝 License

This module is distributed under the **Odoo Community License (LGPL-3)**.
