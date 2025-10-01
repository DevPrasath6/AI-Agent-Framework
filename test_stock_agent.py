"""
Stock Monitoring Agent Test - Combine real stock data with AI agents
This shows how to create an agent that processes real-time stock market data.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import yfinance as yf
import time
from datetime import datetime
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class StockMonitorAgent(SimpleAgent):
    """Agent that monitors stock prices and detects significant changes."""

    def __init__(self, change_threshold=2.0, **kwargs):
        super().__init__(
            name="stock_monitor",
            description="Monitor stock prices and detect significant changes",
            **kwargs
        )
        self.price_history = {}
        self.change_threshold = change_threshold
        self.alerts_generated = []

    async def execute(self, input_data, context):
        """Process stock data and detect significant changes."""
        symbol = input_data.get("symbol")
        current_price = input_data.get("price")
        timestamp = input_data.get("timestamp")

        if not symbol or current_price is None:
            return {"error": "Invalid stock data format"}

        # Initialize price history for this symbol
        if symbol not in self.price_history:
            self.price_history[symbol] = []

        # Store current price
        self.price_history[symbol].append({
            "price": current_price,
            "timestamp": timestamp
        })

        # Keep only last 20 prices to manage memory
        if len(self.price_history[symbol]) > 20:
            self.price_history[symbol] = self.price_history[symbol][-20:]

        # Analyze price movement
        analysis = self._analyze_price_movement(symbol, current_price)

        return {
            "symbol": symbol,
            "current_price": current_price,
            "timestamp": timestamp,
            "analysis": analysis,
            "agent_id": self.id
        }

    def _analyze_price_movement(self, symbol, current_price):
        """Analyze price movement and generate alerts."""
        history = self.price_history[symbol]

        if len(history) < 2:
            return {
                "trend": "insufficient_data",
                "change_percent": 0,
                "alert": None,
                    "confidence": 0,
                    "moving_average": None,
            }

        # Calculate percentage change from previous price
        prev_price = history[-2]["price"]
        change_percent = ((current_price - prev_price) / prev_price) * 100

        # Calculate moving average if we have enough data
        moving_avg = None
        if len(history) >= 5:
            prices = [h["price"] for h in history[-5:]]
            moving_avg = sum(prices) / len(prices)
            trend = "bullish" if current_price > moving_avg else "bearish"
        else:
            trend = "neutral"

        # Generate alert if significant change
        alert = None
        if abs(change_percent) >= self.change_threshold:
            direction = "📈 SURGE" if change_percent > 0 else "📉 DROP"
            alert = f"{direction}: {symbol} moved {change_percent:+.2f}%"

            # Store alert
            alert_data = {
                "symbol": symbol,
                "change_percent": change_percent,
                "timestamp": datetime.now().isoformat(),
                "type": "significant_movement"
            }
            self.alerts_generated.append(alert_data)

        # Final analysis output
        return {
            "trend": trend,
            "change_percent": round(change_percent, 2),
            "alert": alert,
            "confidence": min(len(history) / 10, 1.0),
            "moving_average": round(moving_avg, 2) if moving_avg is not None else None,
        }

async def test_with_real_stock_data():
    """Test the stock monitoring agent with real Yahoo Finance data."""
    print("🧪 Testing Stock Monitor Agent with Real Data")
    print("=" * 50)

    # Create the agent
    agent = StockMonitorAgent(change_threshold=1.0)  # 1% threshold for demo

    # Get real stock data for testing
    symbol = "AAPL"
    print(f"📈 Fetching recent data for {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        # Get last 10 data points from today
        history = ticker.history(period="1d", interval="5m")

        if history.empty:
            print(f"❌ No data available for {symbol}")
            return

        print(f"✅ Got {len(history)} data points")
        print(f"\nProcessing data through agent...")

        # Process each data point through the agent
        for i, (timestamp, row) in enumerate(history.tail(10).iterrows()):
            stock_data = {
                "symbol": symbol,
                "price": float(row['Close']),
                "volume": int(row['Volume']),
                "timestamp": timestamp.isoformat()
            }

            # Create execution context
            context = ExecutionContext(agent_id=agent.id)

            # Run the agent
            result = await agent.run(stock_data, context)

            if result["status"] == "completed":
                output = result["output"]
                analysis = output["analysis"]

                # Display results
                print(f"\n🔍 Analysis #{i+1}:")
                print(f"   💰 Price: ${output['current_price']:.2f}")
                print(f"   📊 Change: {analysis['change_percent']:+.2f}%")
                print(f"   📈 Trend: {analysis['trend']}")
                print(f"   🎯 Confidence: {analysis['confidence']:.2f}")

                if analysis["alert"]:
                    print(f"   🚨 {analysis['alert']}")

                if analysis["moving_average"]:
                    print(f"   📊 MA(5): ${analysis['moving_average']:.2f}")

            else:
                print(f"❌ Agent execution failed: {result.get('error', 'Unknown error')}")

            # Small delay for readability
            await asyncio.sleep(0.5)

        # Show summary
        print(f"\n📊 Summary:")
        print(f"   🔍 Total analyses: {len(agent.price_history.get(symbol, []))}")
        print(f"   🚨 Alerts generated: {len(agent.alerts_generated)}")

        if agent.alerts_generated:
            print(f"\n🚨 All Alerts:")
            for alert in agent.alerts_generated:
                print(f"   • {alert['symbol']}: {alert['change_percent']:+.2f}% at {alert['timestamp'][:19]}")

    except Exception as e:
        print(f"❌ Error during test: {e}")

async def test_multi_stock_monitoring():
    """Test monitoring multiple stocks simultaneously."""
    print(f"\n🧪 Testing Multi-Stock Monitoring")
    print("=" * 50)

    symbols = ["AAPL", "GOOGL", "MSFT"]
    agents = {}

    # Create an agent for each stock
    for symbol in symbols:
        agents[symbol] = StockMonitorAgent(change_threshold=1.5)

    print(f"📊 Monitoring {len(symbols)} stocks...")

    # Get current data for all stocks
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="1d", interval="1h")

            if not history.empty:
                latest = history.iloc[-1]
                stock_data = {
                    "symbol": symbol,
                    "price": float(latest['Close']),
                    "timestamp": datetime.now().isoformat()
                }

                # Process with the respective agent
                context = ExecutionContext(agent_id=agents[symbol].id)
                result = await agents[symbol].run(stock_data, context)

                if result["status"] == "completed":
                    output = result["output"]
                    print(f"✅ {symbol}: ${output['current_price']:.2f} | Agent: {output['agent_id'][:8]}...")

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")

        await asyncio.sleep(0.5)

def main():
    """Run all stock agent tests."""
    print("📈 Stock Monitoring Agent Test Suite\n")

    async def run_all_tests():
        await test_with_real_stock_data()
        await test_multi_stock_monitoring()

        print(f"\n🎉 All stock agent tests completed!")
        print(f"\nNext steps:")
        print(f"1. Try modifying the change_threshold parameter")
        print(f"2. Add more sophisticated analysis logic")
        print(f"3. Run the system monitoring test: python test_system_agent.py")

    # Run the tests
    asyncio.run(run_all_tests())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test stopped by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Make sure yfinance is installed: pip install yfinance")
        print(f"2. Check internet connection")
        print(f"3. Run test_framework_import.py first to verify setup")
