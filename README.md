# 🕴️ L I O R A — Formalwear E-Commerce Platform

Liora is a **full-stack e-commerce platform** built with **Django**, **JavaScript**, and **PostgreSQL**, designed for selling elegant **formal wear** like blazers, shirts, and trousers.  
It offers a seamless shopping experience with cart, wishlist, coupon, and secure payment features — along with a powerful admin dashboard for store management.

🌐 **Live Demo:** [https://liora.duckdns.org/](https://liora.duckdns.org/)  
💻 **Tech Stack:** HTML, CSS, JavaScript, Bootstrap, Django, ORM, PostgreSQL, AWS, Git

---

## 🚀 Features

### 🛍️ User Side
- Browse and purchase formal wear products (blazers, shirts, trousers, etc.)
- Add items to **Cart** and **Wishlist**
- View **Product Variations** (color and size)
- Apply **Coupon Codes** and view **Offers**
- Secure online payment integration with **Razorpay**
- Receive **Email Confirmation** upon successful order
- **Forgot Password** option for account recovery
- Fully **Responsive Design** across devices

### ⚙️ Admin Side
- Dedicated **Admin Dashboard** for managing:
  - Products
  - Categories
  - Inventory
  - Banners
  - Offers
  - Coupons
- Generate and download **Sales Reports (PDF)**
- Manage dynamic **Homepage Banners**
- Control order status and delivery updates
- Role-based access (admin-only controls)

---

## 🧱 Tech Stack

| Layer | Technologies Used |
|-------|-------------------|
| **Frontend** | HTML, CSS, JavaScript, Bootstrap |
| **Backend** | Django, Django ORM |
| **Database** | PostgreSQL |
| **Payment Gateway** | Razorpay |
| **Deployment** | AWS EC2, Gunicorn, Nginx |
| **Version Control** | Git & GitHub |

---

## 🧩 Project Structure
iora/
├── accounts/ # User authentication, registration, profile
├── liora/ # Project folder
├── orders/ # Checkout, payments, cart
├── products/ # Categories, products
├── adminpanel/ # Admin dashboard and sales reports
├── templates/ # HTML templates
├── static/ # CSS, JS, images
├── media/ # Uploaded product images
└── manage.py


---

## ⚡ Installation & Setup

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Swetha-ep/liora-ecommerce
cd Liora

# 2️⃣ Create a virtual environment and activate it
python -m venv venv
venv\Scripts\activate   # for Windows
# source venv/bin/activate  # for Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5️⃣ Create a superuser
python manage.py createsuperuser

# 6️⃣ Run the server
python manage.py runserver

Admin Demo:
Credentials available upon request.
