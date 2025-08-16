# Fruitkha 🍎 - E-Commerce Platform

A comprehensive e-commerce platform built with Python Django, designed to provide a seamless shopping experience for users and powerful management tools for administrators.

## 🌟 Features

### User-Side Features
- **Authentication System**: User registration, login, and profile management
- **Cart & Wishlist**: Add, manage, and organize products for purchase or future reference
- **Digital Wallet**: Integrated wallet system for storing funds and making purchases
- **Address Management**: Save and manage multiple shipping addresses
- **User Profile**: Complete profile management with editable user information
- **Secure Payments**: Multiple payment gateway integration (Razorpay)
- **Order Management**: Track orders, view order history, and request cancellations
- **Invoice Generation**: Automatic invoice generation and printing functionality
- **SMS Notifications**: Order updates and notifications via Twilio integration

### Admin-Side Features
- **Comprehensive Dashboard**: Interactive sales analytics with graphical representations
- **Sales Reporting**: Generate detailed sales reports with Excel export functionality
- **Category Management**: Create, edit, and organize product categories
- **Product Management**: Complete product CRUD operations with inventory tracking
- **Order Management**: Process orders, handle cancellation requests
- **Coupon System**: Create and manage discount coupons and promotional codes
- **Product Offers**: Set up special offers and discounts on specific products
- **User Management**: Monitor and manage user accounts and activities

## 🛠 Technology Stack

- **Backend**: Python 3.x, Django 5.0.1
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Payment Gateway**: Razorpay
- **SMS Service**: Twilio
- **Environment Management**: python-decouple
- **Static Files**: Django static files handling

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- PostgreSQL
- Git
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fruitkha-ecommerce.git
cd fruitkha-ecommerce
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root directory:

```env
# Database Configuration
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Payment Gateway (Razorpay)
RAZOR_KEY_ID=your_razorpay_key_id
RAZOR_KEY_SECRET=your_razorpay_key_secret

# SMS Service (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token

# Security
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 5. Database Setup
```bash
# Create and configure PostgreSQL database
createdb your_database_name

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
fruitkha-ecommerce/
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── home/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── cart/
├── orders/
├── wishlist/
├── templates/
├── static/
├── media/
├── requirements.txt
├── manage.py
└── .env
```

## 🔧 Configuration

### Database Configuration
The project uses PostgreSQL as the primary database. Update your `.env` file with your database credentials.

### Payment Gateway Setup
1. Create a Razorpay account
2. Obtain your Key ID and Secret
3. Add them to your `.env` file

### SMS Configuration
1. Set up a Twilio account
2. Get your Account SID and Auth Token
3. Configure them in the `.env` file

## 📱 API Endpoints

### User Endpoints
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /profile/` - User profile
- `POST /cart/add/` - Add to cart
- `GET /orders/` - Order history

### Admin Endpoints
- `GET /admin/dashboard/` - Admin dashboard
- `GET /admin/products/` - Product management
- `GET /admin/orders/` - Order management
- `GET /admin/reports/` - Sales reports

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in your environment
2. Configure `ALLOWED_HOSTS` properly
3. Set up a production-ready database
4. Configure static file serving
5. Set up SSL certificates

### Deployment Options

#### Option 1: Heroku Deployment
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn project.wsgi" > Procfile

# Create requirements.txt with production dependencies
pip freeze > requirements.txt

# Deploy to Heroku
heroku create your-app-name
heroku config:set DJANGO_SETTINGS_MODULE=project.settings
git push heroku main
heroku run python manage.py migrate
```

#### Option 2: Digital Ocean/AWS
1. Set up a Ubuntu server
2. Install Python, PostgreSQL, and Nginx
3. Clone your repository
4. Set up virtual environment and dependencies
5. Configure Gunicorn and Nginx
6. Set up SSL with Let's Encrypt

#### Option 3: Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📈 Performance Optimization

- **Database**: Use database indexing and query optimization
- **Caching**: Implement Redis caching for frequently accessed data
- **Static Files**: Use CDN for static file delivery
- **Images**: Implement image compression and lazy loading

## 🔒 Security Features

- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure password validation
- Environment-based configuration
- Secure payment processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Django community for the amazing framework
- Razorpay for payment gateway integration
- Twilio for SMS services
- Bootstrap for responsive UI components

## 📞 Support

For support, email affilpm2004@gmail.com or create an issue in the GitHub repository.

---

**Built with ❤️ by [AFFIL P M]**
