# Payment Using Razorpay (Django)

Demo Django project integrating **Razorpay Checkout (test mode)**.

## Features

- Product listing (plant store UI)
- Checkout page with Razorpay popup
- Server-side Razorpay **Order** creation
- Payment verification (signature) and redirect to success/failed pages

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (do **not** commit it):

```env
DJANGO_SECRET_KEY=django-insecure-change-me-in-development
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
```

Run migrations and start the server:

```bash
python3 manage.py migrate
python3 manage.py runserver
```

Optional: seed demo products:

```bash
python3 manage.py seed_products --count 24
```

## URLs

- `/` - store home
- `/checkout/<id>/` - checkout
- `/payment/success/` - success page
- `/payment/failed/` - failed page

