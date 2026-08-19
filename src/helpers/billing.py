
from stripe import StripeClient
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")

client = StripeClient(STRIPE_SECRET_KEY)

def create_customer(
        name="", 
        email="",
        metadata={},
        raw=False):
    response = client.v1.customers.create({
        "name": name,
        "email": email,
        "metadata": metadata,
    })
    if raw:
        return response
    stripe_id = response.id
    return stripe_id

def create_product(
        name="", 
        metadata={},
        raw=False):
    response = client.v1.products.create({
        "name": name,
        "metadata": metadata,
    })
    if raw:
        return response
    stripe_id = response.id
    return stripe_id

def create_price(currency="usd",
                unit_amount="99999",
                interval = "month",
                product=None,
                metadata={}, 
        raw=False):
    if product is None:
        return None 
    response = price = client.v1.prices.create({
                    "currency": currency,
                    "unit_amount": unit_amount,
                    "recurring": {"interval": interval},
                    "product": product,
                    "metadata": metadata, 
                })
    if raw:
        return response
    stripe_id = response.id
    return stripe_id