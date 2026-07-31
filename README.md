# 🍎 Fruitkha - Modern Django E-Commerce Platform

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0.1-092E20.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791.svg?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=docker&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020.svg?style=flat&logo=cloudflare&logoColor=white)

**Fruitkha** is a comprehensive, production-ready e-commerce platform built with Django. It provides a seamless shopping experience for customers and a powerful, data-rich management dashboard for store administrators. The project is fully containerized with Docker, uses Cloudflare Tunnels for secure and straightforward internet access, and leverages Cloudflare R2 for scalable media storage.

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Environment Variables](#-environment-variables)
- [Installation & Setup](#-installation--setup)
- [Usage & Access](#-usage--access)
- [Project Structure](#-project-structure)
- [Security & Best Practices](#-security--best-practices)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 About the Project

Fruitkha is designed to be a complete end-to-end e-commerce solution. Unlike basic shopping carts, it includes advanced features such as an integrated digital wallet, comprehensive sales reporting, coupon management, and robust email OTP-based authentication. 

It is built with modern deployment in mind, utilizing **Docker Compose** to orchestrate the PostgreSQL database, Django backend application, Nginx web server, and a Cloudflare Tunnel for secure remote access without exposing local network ports.

---

## 🌟 Key Features

### 🛒 For Customers
- **Passwordless Authentication**: Secure login and registration using **Email OTP** instead of passwords.
- **Shopping Cart & Wishlist**: Intuitive product discovery, cart management, and saving items for later.
- **Digital Wallet System**: A built-in wallet allowing users to store funds, receive refunds, and pay for orders seamlessly.
- **Address Management**: Users can save and manage multiple shipping addresses (Home, Work, etc.).
- **Order Tracking**: Detailed order history, invoice downloads, and the ability to request cancellations.
- **Secure Checkout**: Integrated with **Razorpay** for safe, encrypted payment processing.

### 📊 For Administrators
- **Custom Analytics Dashboard**: Interactive sales analytics with graphical charts and key performance indicators.
- **Advanced Sales Reporting**: Filter and generate detailed sales reports with Excel export functionality.
- **Inventory & Product Management**: Full CRUD operations for products, categories, and stock tracking.
- **Order Fulfillment**: Process incoming orders, manage statuses, and handle user cancellation requests.
- **Marketing Tools**: Create and manage discount coupons and promotional product offers.

---

## 🏗 System Architecture

The application is distributed across several Docker containers:
1. **Web (Django App)**: The core Python application serving business logic and rendering HTML templates.
2. **Database (PostgreSQL)**: The relational database storing all persistent data (users, products, orders).
3. **Nginx**: Acts as a reverse proxy, routing traffic to the Django app and serving static/media files efficiently.
4. **Cloudflared (Tunnel)**: Connects the Nginx container directly to Cloudflare's edge network, exposing the app to the internet securely on your custom domain.
5. **Cloudflare R2**: External object storage for user-uploaded media and product images.

---

## 🛠 Technology Stack

- **Backend Framework**: Python 3, Django 5
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap
- **Payment Gateway**: Razorpay
- **Email Delivery**: SMTP (for OTPs and transactional emails)
- **Object Storage**: Cloudflare R2
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **Networking**: Cloudflare Zero Trust Tunnels

---

## 📋 Prerequisites

Before setting up the project, ensure you have the following ready:
- **Docker** and **Docker Compose** installed on your machine or server.
- A **Cloudflare Account** with:
  - A Zero Trust Tunnel created (you'll need the Tunnel Token).
  - An R2 Bucket created (you'll need the Access Keys and Endpoint URL).
- A **Razorpay Account** (for live/test API keys).
- An **SMTP Email Account** (e.g., Gmail with an App Password).

---

## ⚙️ Environment Variables

Create a `.env` file inside the `project/` directory. Here is what each variable does:

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_DB` | Name of the PostgreSQL database | `ecom` |
| `POSTGRES_USER` | Database username | `postgres` |
| `POSTGRES_PASSWORD`| Database password | `1234` |
| `POSTGRES_HOST` | Database host (Docker service name) | `db` |
| `POSTGRES_PORT` | Database port | `5432` |
| `RAZOR_KEY_ID` | Razorpay public key | `rzp_test_...` |
| `RAZOR_KEY_SECRET` | Razorpay secret key | `...` |
| `EMAIL_HOST` | SMTP server address | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Enable TLS encryption | `True` |
| `EMAIL_HOST_USER` | Your sending email address | `admin@example.com` |
| `EMAIL_HOST_PASSWORD`| Your email app password | `xxxx xxxx xxxx xxxx` |
| `TUNNEL_TOKEN` | Cloudflare Tunnel authentication token | `eyJhIjoi...` |
| `R2_ACCESS_KEY_ID` | Cloudflare R2 Access Key | `9c144...` |
| `R2_SECRET_ACCESS_KEY`| Cloudflare R2 Secret Key | `b7b4d...` |
| `R2_BUCKET_NAME` | Name of your R2 bucket | `fruitkha-media` |
| `R2_ENDPOINT_URL` | Cloudflare R2 endpoint | `https://<account-id>.r2.cloudflarestorage.com` |
| `R2_CUSTOM_DOMAIN` | Custom public domain for R2 assets | `https://media.yourdomain.com` |

---

## 💻 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fruitkha-ecommerce.git
cd fruitkha-ecommerce/project
```

### 2. Configure Environment
Create the `.env` file as described in the Environment Variables section above.

### 3. Build and Start the Containers
Run the following command to download the images, build the Django app, and start all services in the background:
```bash
docker-compose up -d --build
```
*Note: The `entrypoint.sh` script will automatically handle database migrations and static file collection when the `web` container starts.*

### 4. Create an Admin Superuser
To access the admin dashboard, you need a superuser account. Run this command inside the running web container:
```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the interactive prompts to set your admin email and details.

---

## 🌐 Usage & Access

Because this project uses **Cloudflare Tunnels**, you do not need to open ports on your router or configure complicated firewall rules.

1. Ensure your Cloudflare Tunnel is running and properly routed to the `nginx:80` service in your Cloudflare Zero Trust dashboard.
2. Visit the public hostname you assigned to the tunnel (e.g., `https://shop.yourdomain.com`).
3. **Customer Access**: Browse the store, add items to the cart, and login using your Email to receive an OTP.
4. **Admin Access**: Navigate to `/admin/` (or your custom admin URL) and log in using the superuser credentials created in step 4.

---

## 📁 Project Structure

```text
fruitkha-ecommerce/
├── README.md                 # Project documentation
└── project/
    ├── docker-compose.yml    # Docker orchestration configuration
    ├── Dockerfile            # Python/Django image build instructions
    ├── entrypoint.sh         # Startup script for database migrations & static collection
    ├── .env                  # Environment variables (Ignored by Git)
    ├── nginx/                # Nginx web server configurations
    ├── project/              # Core Django settings (settings.py, urls.py)
    ├── home/                 # Django App: Frontend views, user profiles, authentication
    ├── cart/                 # Django App: Shopping cart logic
    ├── orders/               # Django App: Order processing and payment integration
    ├── wishlist/             # Django App: User wishlist management
    ├── static/               # CSS, JS, and Images for the frontend UI
    └── templates/            # HTML templates rendered by Django
```

---

## 🔒 Security & Best Practices

- **Zero-Trust Network**: By using Cloudflare Tunnels, the server is completely isolated from the public internet. Only traffic routed through Cloudflare reaches the application.
- **Secure Media Storage**: User uploads and product images are stored securely on Cloudflare R2, offloading bandwidth from the main application server.
- **Passwordless Auth**: Reduces the risk of password credential stuffing or brute-force attacks by relying on dynamic Email OTPs.
- **Django Security**: Leverages Django's built-in protections against SQL Injection, Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF).

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>Built with ❤️ by AFFIL P M</strong>
  <br>
  <a href="mailto:affilpm2004@gmail.com">Contact Support</a>
</div>
