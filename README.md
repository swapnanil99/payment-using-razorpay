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



## URLs

- `/` - store home
- `/checkout/<id>/` - checkout
- `/payment/success/` - success page
- `/payment/failed/` - failed page

