
from stripe import StripeClient
from decouple import config

from . import date_utils 

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY", default="", cast=str)
STRIPE_TEST_OVERRIDE = config("STRIPE_TEST_OVERRIDE", default=False, cast=bool)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG and not STRIPE_TEST_OVERRIDE:
    raise ValueError("Invalid stripe key for prod")

client = StripeClient(STRIPE_SECRET_KEY)

def serialize_subscription_data(subscription_response):
    status = subscription_response.status
    sub_item = subscription_response["items"]["data"][0]
    current_period_start = date_utils.timestamp_as_datetime(sub_item["current_period_start"])
    current_period_end = date_utils.timestamp_as_datetime(sub_item["current_period_end"])
    cancel_at_period_end = subscription_response.cancel_at_period_end
    return {
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "status": status,
        "cancel_at_period_end": cancel_at_period_end,
    }

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

def start_checkout_session(customer_id, 
                           success_url="", 
                           cancel_url="", 
                           price_stripe_id="", 
                           raw=True):
    if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
        success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"
    response= client.v1.checkout.sessions.create({
        "customer": customer_id,
        "success_url": success_url,
        "cancel_url": cancel_url,
        "line_items": [{"price": price_stripe_id, "quantity": 1}],
        "mode": "subscription",
        })
    if raw:
        return response
    return response.url

def get_checkout_session(stripe_id, raw=True):
    response = session = client.v1.checkout.sessions.retrieve(
            stripe_id,
        )
    if raw:
        return response
    return response.url

def get_subscription(stripe_id, raw=True):
    response = session = client.v1.subscriptions.retrieve(
            stripe_id,
        )
    if raw:
        return response
    return serialize_subscription_data(response)

def get_customer_active_subscriptions(customer_stripe_id):
    response = session = client.v1.subscriptions.list(
            params={
                "customer": customer_stripe_id,
                "status": "active",
            }
        )
    return response


def cancel_subscription(stripe_id, reason="", feedback="other", cancel_at_period_end=False, raw=True):
    if cancel_at_period_end:
        response = client.v1.subscriptions.update(
            stripe_id,
            params={
                "cancel_at_period_end": cancel_at_period_end,
                "cancellation_details": {
                    "comment": reason,
                    "feedback": feedback,
                }
            }
        )
    else:
        response = client.v1.subscriptions.cancel(
            stripe_id,
            params={
                "cancellation_details": {
                    "comment": reason,
                    "feedback": feedback,
                }
            }
        )

    if raw:
        return response
    return serialize_subscription_data(response)




def get_checkout_customer_plan(session_id):
    checkout_r = get_checkout_session(session_id, raw=True)
    customer_id = checkout_r.customer
    sub_stripe_id = checkout_r.subscription
    sub_r = get_subscription(sub_stripe_id, raw=True)

    sub_plan = sub_r.plan
    subscription_data = serialize_subscription_data(sub_r)

    data = {
        "customer_id": customer_id,
        "plan_id": sub_plan.id,
        "sub_stripe_id": sub_stripe_id,
        **subscription_data,
    }
    return data