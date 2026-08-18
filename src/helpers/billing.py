
from stripe import StripeClient
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")

client = StripeClient(STRIPE_SECRET_KEY)

def create_customer():
    customer = client.v1.customers.create({
    "name": "Jenny Rosen",
    "email": "jennyrosen@example.com",
    })