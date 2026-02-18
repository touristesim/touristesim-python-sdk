# Tourist eSIM Python SDK

Official Python SDK for Tourist eSIM Partner API. Enable easy integration for resellers and affiliates to manage eSIM plans, orders, and customer data.

## Features

- 🔐 **OAuth 2.0 Authentication** - Secure Client Credentials flow with automatic token refresh
- 🚀 **Auto-Retry Logic** - Exponential backoff with 3 retry attempts on connection failures
- 📦 **Type-Supported** - Full type hints throughout the SDK
- 💾 **Token Caching** - In-memory token cache to reduce OAuth requests
- ⚡ **Pythonic API** - Clean, intuitive API design following Python conventions
- 🔄 **Pagination Support** - Built-in pagination for catalog queries
- 🎯 **Exception Hierarchy** - Specific exceptions for different error scenarios

## Requirements

- Python 3.8+
- requests >= 2.28.0

## Testing

Run the included test script to verify SDK functionality:

```bash
python3 test_sdk.py
```

This runs basic tests for SDK import, instantiation, structure, and resource modules without making actual API calls.

## Installation

```bash
pip install touristesim-python-sdk
```

## Quick Start

```python
from touristesim import TouristEsim

sdk = TouristEsim('your-client-id', 'your-client-secret')

# Fetch all plans
plans = sdk.plans().get()
for plan in plans:
    print(f"{plan.get('name')} - {plan.get('price')} {plan.get('currency')}")
```

## API Usage

### Plans

```python
# Get all plans with filters
plans = sdk.plans().get({
    'country': 'US',
    'type': 'global',
    'per_page': 50,
    'sort_by': 'price'
})

# Get single plan
plan = sdk.plans().find(123)

# Get plans by country
us_plans = sdk.plans().by_country('US')

# Get global plans
global_plans = sdk.plans().global_plans()

# Validate plan
validation = sdk.plans().validate(123, 5)
```

### Countries

```python
# Get all countries
countries = sdk.countries().all()

# Find by code
usa = sdk.countries().find('US')

# Search countries
asian = sdk.countries().search('china')

# Featured countries
featured = sdk.countries().featured()
```

### Orders

```python
# Create order
order = sdk.orders().create({
    'plan_id': 123,
    'quantity': 2,
    'customer_email': 'customer@example.com'
})

# Get orders
orders = sdk.orders().all()

# Get single order
order = sdk.orders().find(456)

# Cancel order
sdk.orders().cancel(456)
```

### eSIMs

```python
# Get eSIMs
esims = sdk.esims().all()

# Find eSIM
esim = sdk.esims().find('8955001000000000000')

# Check usage
usage = sdk.esims().usage('8955001000000000000')

# Get topup packages
packages = sdk.esims().topup_packages('8955001000000000000')

# Purchase topup
sdk.esims().topup('8955001000000000000', 789)

# Send setup email
sdk.esims().send_email('8955001000000000000', 'user@example.com')
```

## Error Handling

```python
from touristesim.exceptions import (
    AuthenticationException,
    ValidationException,
    RateLimitException,
    ResourceNotFoundException
)

try:
    plan = sdk.plans().find(999)
except AuthenticationException as e:
    print('Auth failed:', e)
except ValidationException as e:
    print('Validation errors:', e.get_errors())
except RateLimitException as e:
    print('Rate limited. Retry after:', e.get_retry_after(), 'seconds')
except ResourceNotFoundException as e:
    print('Not found:', e)
```

## API Documentation

For complete API documentation, visit:
- **API Docs**: https://docs.touristesim.net/
- **SDK Guides**: https://docs.touristesim.net/sdks/guides
- **Partner Dashboard**: https://partners.touristesim.net

## Support

For issues or questions:
- **Technical Support**: tech@touristesim.net
- **GitHub Issues**: https://github.com/touristesim/touristesim-python-sdk/issues
- **Dashboard**: https://partners.touristesim.net

## License

MIT - see LICENSE file
