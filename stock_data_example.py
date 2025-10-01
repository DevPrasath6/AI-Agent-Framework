"""
Stock Data Example - Get real-time stock data using Yahoo Finance (FREE)
No API key required! This example shows how to fetch real stock market data.
"""

import yfinance as yf
import time
from datetime import datetime, timedelta

def get_stock_data(symbol="AAPL"):
    """Fetch real-time stock data for a given symbol."""
    print(f"📈 Fetching data for {symbol}...")

    try:
        ticker = yf.Ticker(symbol)

        # Get recent data (last few hours)
        history = ticker.history(period="1d", interval="5m")

        if not history.empty:
            latest = history.iloc[-1]
            previous = history.iloc[-2] if len(history) > 1 else latest

            return {
                "symbol": symbol,
                "price": round(float(latest['Close']), 2),
                "volume": int(latest['Volume']),
                "timestamp": datetime.now().isoformat(),
                "change": round(float(latest['Close'] - previous['Close']), 2),
                "change_percent": round(((latest['Close'] - previous['Close']) / previous['Close']) * 100, 2),
                "high": round(float(latest['High']), 2),
                "low": round(float(latest['Low']), 2),
                "open": round(float(latest['Open']), 2)
            }
        else:
            print(f"❌ No data available for {symbol}")
            return None

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None

def get_multiple_stocks(symbols=None):
    """Get data for multiple stock symbols."""
    if symbols is None:
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

    print(f"📊 Fetching data for {len(symbols)} stocks...")

    stock_data = {}
    for symbol in symbols:
        data = get_stock_data(symbol)
        if data:
            stock_data[symbol] = data
        time.sleep(0.5)  # Be nice to the API

    return stock_data

def display_stock_data(data):
    """Display stock data in a nice format."""
    if not data:
        print("No data to display")
        return

    print(f"\n📈 {data['symbol']} Stock Data:")
    print(f"💰 Price: ${data['price']}")
    print(f"📊 Change: ${data['change']} ({data['change_percent']:+.2f}%)")
    print(f"📈 High: ${data['high']}")
    print(f"📉 Low: ${data['low']}")
    print(f"🔄 Volume: {data['volume']:,}")
    print(f"⏰ Updated: {data['timestamp']}")

def simulate_real_time_stream(symbol="AAPL", duration=30):
    """Simulate a real-time data stream by fetching data repeatedly."""
    print(f"\n🔄 Starting real-time simulation for {symbol} ({duration} seconds)")
    print("=" * 50)

    start_time = time.time()
    iteration = 1

    while time.time() - start_time < duration:
        print(f"\n🔄 Update #{iteration}")
        data = get_stock_data(symbol)

        if data:
            print(f"📈 {data['symbol']}: ${data['price']} ({data['change_percent']:+.2f}%)")

        iteration += 1
        time.sleep(5)  # Update every 5 seconds

    print(f"\n✅ Real-time simulation completed for {symbol}")

def main():
    """Run stock data examples."""
    print("📈 Yahoo Finance Stock Data Example\n")

    # Example 1: Single stock
    print("1️⃣ Getting single stock data...")
    apple_data = get_stock_data("AAPL")
    if apple_data:
        display_stock_data(apple_data)

    # Example 2: Multiple stocks
    print("\n2️⃣ Getting multiple stock data...")
    stocks = get_multiple_stocks(["AAPL", "GOOGL", "MSFT"])

    for symbol, data in stocks.items():
        print(f"\n📊 {symbol}: ${data['price']} ({data['change_percent']:+.2f}%)")

    # Example 3: Popular cryptocurrencies (if available)
    print("\n3️⃣ Getting crypto data...")
    crypto_symbols = ["BTC-USD", "ETH-USD"]
    crypto_data = get_multiple_stocks(crypto_symbols)

    for symbol, data in crypto_data.items():
        crypto_name = symbol.replace("-USD", "")
        print(f"₿ {crypto_name}: ${data['price']} ({data['change_percent']:+.2f}%)")

    # Example 4: Ask user if they want real-time simulation
    print(f"\n4️⃣ Real-time simulation available")
    print("This will fetch live data every 5 seconds for 30 seconds.")

    user_input = input("Run real-time simulation? (y/n): ").lower().strip()
    if user_input in ['y', 'yes']:
        simulate_real_time_stream("AAPL", 30)
    else:
        print("Skipping real-time simulation.")

    print("\n🎉 Stock data example completed!")
    print("\nNext step: Run 'python test_stock_agent.py' to see how agents process this data")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Install yfinance: pip install yfinance")
        print("2. Check internet connection")
        print("3. Try a different stock symbol")
