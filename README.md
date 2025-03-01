# Option Price Service

A FastAPI-based web service that fetches option prices for a given ticker, strike price, and expiry date.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```

The service will start on http://localhost:8000

## API Endpoints

### GET /
Welcome message endpoint

### POST /get_option_price
Fetches option price data for the specified parameters.

Request body:
```json
{
    "ticker": "AAPL",
    "strike_price": 180.0,
    "expiry_date": "2024-03-15",
    "target_date": "2024-02-27"
}
```

## Example Usage
```bash
curl -X POST "http://localhost:8000/get_option_price" \
     -H "Content-Type: application/json" \
     -d '{"ticker": "AAPL", "strike_price": 180.0, "expiry_date": "2024-03-15", "target_date": "2024-02-27"}'
```
