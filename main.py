from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import yfinance as yf
import pandas as pd

app = FastAPI(title="Option Price Service")

class OptionRequest(BaseModel):
    ticker: str
    strike_price: float
    expiry_date: str
    target_date: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Option Price Service"}

@app.post("/get_option_price")
def get_option_price(request: OptionRequest):
    try:
        # Convert dates to datetime objects
        expiry_date = datetime.strptime(request.expiry_date, "%Y-%m-%d")
        target_date = datetime.strptime(request.target_date, "%Y-%m-%d")
        
        # Get the ticker data
        ticker = yf.Ticker(request.ticker)
        
        # Get options chain for the expiry date
        options = ticker.option_chain(request.expiry_date)
        
        # Find the option with matching strike price
        if request.strike_price in options.calls['strike'].values:
            option_data = options.calls[options.calls['strike'] == request.strike_price].iloc[0]
            option_type = 'call'
        elif request.strike_price in options.puts['strike'].values:
            option_data = options.puts[options.puts['strike'] == request.strike_price].iloc[0]
            option_type = 'put'
        else:
            raise HTTPException(status_code=404, detail="Option with specified strike price not found")
        
        return {
            "ticker": request.ticker,
            "strike_price": request.strike_price,
            "expiry_date": request.expiry_date,
            "target_date": request.target_date,
            "option_type": option_type,
            "last_price": float(option_data['lastPrice']),
            "bid": float(option_data['bid']),
            "ask": float(option_data['ask']),
            "volume": int(option_data['volume']) if not pd.isna(option_data['volume']) else 0,
            "implied_volatility": float(option_data['impliedVolatility'])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
