# Black-Scholes Option Pricing Web Application

## Overview
This is a Flask-based web application that calculates option prices and Greeks using the Black-Scholes model. Users can input a stock ticker, strike price, time to expiration, volatility, and interest rate to compute call and put option prices, along with key option Greeks (Delta, Gamma, Vega, Theta, and Rho). The application fetches real-time stock prices using the `yfinance` library.

This was mainly to deepen my understanding on flask, the black scholes model, using the yfinance api and launching web applications in general

## Features
- **Real-Time Stock Price Fetching**: Retrieves current stock prices for a given ticker using Yahoo Finance (`yfinance`).
- **Black-Scholes Calculations**: Computes call and put option prices based on user inputs.
- **Option Greeks**: Calculates Delta, Gamma, Vega, Theta, and Rho for both call and put options.
- **User-Friendly Interface**: A simple HTML form for inputting parameters and displaying results.
- **Debounced Stock Price Updates**: Fetches stock prices with a debounce mechanism to prevent excessive API calls.
- **Error Handling**: Provides clear error messages for invalid inputs or failed API requests.

## Prerequisites
- Python 3.6+
- Flask
- NumPy
- SciPy
- yfinance

## Installation
1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/black-scholes-pricing.git
cd black-scholes-pricing
```
2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3.**Install dependencies**:
```bash
pip install flask numpy scipy yfinance
```
4.**Run**:
```bash
python main.py
```


