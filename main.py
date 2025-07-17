from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.stats import norm
import yfinance as yf

app = Flask(__name__)

class blackScholes:
    def __init__(self, volatility: float, price: float, strike: float, time_To_Expire: float, interest_Rate: float) -> None:
        self.sigma = volatility
        self.S = price
        self.K = strike
        self.T = time_To_Expire
        self.r = interest_Rate

    def get_d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def get_d2(self):
        return self.get_d1() - self.sigma * np.sqrt(self.T)

    def get_call(self):
        d1 = self.get_d1()
        d2 = self.get_d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def get_put(self):
        d1 = self.get_d1()
        d2 = self.get_d2()
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

    def get_all_greeks(self):
        d1 = self.get_d1()
        d2 = self.get_d2()
        delta_call = norm.cdf(d1)
        delta_put = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))
        vega = self.S * norm.pdf(d1) * np.sqrt(self.T)
        theta_call = (
            -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
            - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        )
        theta_put = (
            -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
            + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        )
        rho_call = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2)
        rho_put = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2)
        return {
            "delta_call": round(delta_call, 4),
            "delta_put": round(delta_put, 4),
            "gamma": round(gamma, 6),
            "vega": round(vega, 4),
            "theta_call": round(theta_call, 2),
            "theta_put": round(theta_put, 2),
            "rho_call": round(rho_call, 4),
            "rho_put": round(rho_put, 4),
        }

@app.route("/fetch_stock/<ticker>")
def fetch_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"ticker": ticker, "price": round(price, 2)})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data for {ticker}: {str(e)}"})

@app.route("/", methods=["GET", "POST"])
def index():
    call = None
    put = None
    error = None
    ticker = None
    stock_data = {}
    greeks = {}

    if request.method == "POST":
        try:
            ticker = request.form.get("ticker")
            volatility = float(request.form.get("volatility", 0))
            strike = float(request.form.get("strike", 0))
            time_To_Expire = float(request.form.get("time_To_Expire", 0))
            interest_Rate = float(request.form.get("interest_Rate", 0))

            # Fetch price from yfinance
            if not ticker:
                error = "Please enter a ticker."
            else:
                stock = yf.Ticker(ticker)
                price = stock.history(period="1d")["Close"].iloc[-1]
                if volatility <= 0 or price <= 0 or strike <= 0 or time_To_Expire <= 0:
                    error = "Inputs must be positive."
                else:
                    bs = blackScholes(volatility, price, strike, time_To_Expire, interest_Rate)
                    call = round(bs.get_call(), 2)
                    put = round(bs.get_put(), 2)
                    greeks = bs.get_all_greeks()
                    stock_data = {"ticker": ticker, "price": round(price, 2)}
        except ValueError:
            error = "Invalid input. Please enter numeric values."
        except Exception as e:
            error = f"Failed to fetch price for {ticker}: {str(e)}"

    return render_template("index.html", error=error, call=call, put=put, ticker=ticker, stock_data=stock_data, **greeks)

if __name__ == "__main__":
    app.run(debug=True)