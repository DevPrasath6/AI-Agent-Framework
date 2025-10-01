# Practical Guide: Import & Test AI Agent Framework with Real-Time Data

## 🎯 Step-by-Step Setup & Testing Guide

This guide shows you exactly how to import the framework and test it with real data sources.

## 📦 1. Framework Installation & Import

### Install Required Dependencies
```bash
# Navigate to your framework directory
cd f:\Intel\ai-agent-framework

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install additional packages for real-time data
pip install yfinance requests aiohttp pandas numpy
```

### Basic Framework Import
```python
# test_framework_import.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import core framework components
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext
from src.core.agent_id_generator import AgentIDGenerator

# Test basic agent creation
def test_basic_agent():
    agent = SimpleAgent(
        name="test_agent",
        description="Testing framework import"
    )
    print(f"✅ Agent created with ID: {agent.id}")
    return agent

if __name__ == "__main__":
    agent = test_basic_agent()
    print("🎉 Framework import successful!")
```

## 🌍 2. Real-Time Data Sources (Free & Easy to Use)

### A. Stock Market Data (Yahoo Finance - FREE)
```python
# stock_data_example.py
import yfinance as yf
import asyncio
from datetime import datetime

# Get real-time stock data
def get_stock_data(symbol="AAPL"):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    history = ticker.history(period="1d", interval="1m")

    if not history.empty:
        latest = history.iloc[-1]
        return {
            "symbol": symbol,
            "price": float(latest['Close']),
            "volume": int(latest['Volume']),
            "timestamp": datetime.now().isoformat(),
            "change": float(latest['Close'] - latest['Open']),
            "high": float(latest['High']),
            "low": float(latest['Low'])
        }
    return None

# Test it
if __name__ == "__main__":
    data = get_stock_data("AAPL")
    print("📈 Real-time stock data:", data)
```

### B. Cryptocurrency Data (CoinGecko - FREE)
```python
# crypto_data_example.py
import requests
import time

def get_crypto_data(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        coin_data = data[coin_id]
        return {
            "coin": coin_id,
            "price": coin_data["usd"],
            "change_24h": coin_data["usd_24h_change"],
            "last_updated": coin_data["last_updated_at"],
            "timestamp": time.time()
        }
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return None

# Test it
if __name__ == "__main__":
    data = get_crypto_data("bitcoin")
    print("₿ Real-time crypto data:", data)
```

### C. Weather Data (OpenWeatherMap - FREE)
```python
# weather_data_example.py
import requests

def get_weather_data(city="London", api_key="YOUR_API_KEY"):
    # Get free API key from: https://openweathermap.org/api
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "timestamp": data["dt"]
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Test it (replace with your API key)
if __name__ == "__main__":
    # Sign up at https://openweathermap.org/api for free API key
    # data = get_weather_data("London", "your_api_key_here")
    print("🌤️ Get your free API key from https://openweathermap.org/api")
```

### D. System Monitoring (No API needed - FREE)
```python
# system_monitoring_example.py
import psutil
import time
from datetime import datetime

def get_system_data():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_io": psutil.net_io_counters()._asdict(),
        "processes": len(psutil.pids()),
        "timestamp": datetime.now().isoformat()
    }

# Test it
if __name__ == "__main__":
    data = get_system_data()
    print("💻 Real-time system data:", data)
```

## 🧪 3. Complete Testing Examples

### Example 1: Stock Monitoring Agent
```python
# test_stock_agent.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import yfinance as yf
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class StockMonitorAgent(SimpleAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="stock_monitor",
            description="Monitor stock prices and detect significant changes",
            **kwargs
        )
        self.price_history = {}

    async def execute(self, input_data, context):
        symbol = input_data.get("symbol")
        current_price = input_data.get("price")

        # Store price history
        if symbol not in self.price_history:
            self.price_history[symbol] = []

        self.price_history[symbol].append(current_price)

        # Keep only last 10 prices
        if len(self.price_history[symbol]) > 10:
            self.price_history[symbol] = self.price_history[symbol][-10:]

        # Detect significant changes
        if len(self.price_history[symbol]) >= 2:
            prev_price = self.price_history[symbol][-2]
            change_percent = ((current_price - prev_price) / prev_price) * 100

            alert = None
            if abs(change_percent) > 1:  # 1% change threshold
                alert = f"📊 {symbol}: {change_percent:+.2f}% change detected!"

        return {
            "symbol": symbol,
            "current_price": current_price,
            "price_history": self.price_history[symbol],
            "alert": alert,
            "agent_id": self.id
        }

async def test_stock_agent():
    # Create agent
    agent = StockMonitorAgent()

    # Get real stock data
    ticker = yf.Ticker("AAPL")
    history = ticker.history(period="1d", interval="5m")

    print("🧪 Testing Stock Monitor Agent with real AAPL data...")

    # Process last 5 data points
    for i, (timestamp, row) in enumerate(history.tail(5).iterrows()):
        stock_data = {
            "symbol": "AAPL",
            "price": float(row['Close']),
            "timestamp": timestamp.isoformat()
        }

        # Run agent
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(stock_data, context)

        if result["status"] == "completed":
            output = result["output"]
            print(f"Step {i+1}: ${output['current_price']:.2f}")
            if output["alert"]:
                print(f"  {output['alert']}")

    print("✅ Stock agent test completed!")

if __name__ == "__main__":
    asyncio.run(test_stock_agent())
```

### Example 2: System Health Agent
```python
# test_system_agent.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import psutil
import time
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class SystemHealthAgent(SimpleAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="system_health",
            description="Monitor system health and detect issues",
            **kwargs
        )
        self.cpu_threshold = 80
        self.memory_threshold = 85

    async def execute(self, input_data, context):
        cpu_percent = input_data.get("cpu_percent", 0)
        memory_percent = input_data.get("memory_percent", 0)

        alerts = []
        health_status = "healthy"

        if cpu_percent > self.cpu_threshold:
            alerts.append(f"🔴 High CPU usage: {cpu_percent:.1f}%")
            health_status = "warning"

        if memory_percent > self.memory_threshold:
            alerts.append(f"🔴 High memory usage: {memory_percent:.1f}%")
            health_status = "critical"

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "health_status": health_status,
            "alerts": alerts,
            "timestamp": input_data.get("timestamp"),
            "agent_id": self.id
        }

async def test_system_agent():
    agent = SystemHealthAgent()

    print("🧪 Testing System Health Agent with real system data...")

    # Monitor system for 10 seconds
    for i in range(5):
        # Get real system data
        system_data = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }

        # Run agent
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(system_data, context)

        if result["status"] == "completed":
            output = result["output"]
            print(f"Check {i+1}: CPU {output['cpu_percent']:.1f}% | "
                  f"Memory {output['memory_percent']:.1f}% | "
                  f"Status: {output['health_status']}")

            for alert in output["alerts"]:
                print(f"  {alert}")

        time.sleep(2)

    print("✅ System health agent test completed!")

if __name__ == "__main__":
    asyncio.run(test_system_agent())
```

## 🚀 4. Running the Tests

### Step 1: Install Dependencies
```bash
# In PowerShell (framework directory)
.\.venv\Scripts\Activate.ps1
pip install yfinance psutil requests pandas numpy
```

### Step 2: Test Basic Import
```bash
python test_framework_import.py
```

### Step 3: Test Real Data Sources
```bash
# Test stock data
python stock_data_example.py

# Test crypto data
python crypto_data_example.py

# Test system monitoring
python system_monitoring_example.py
```

### Step 4: Test Complete Agents
```bash
# Test stock monitoring agent
python test_stock_agent.py

# Test system health agent
python test_system_agent.py
```

## 📊 5. Where to Get More Real-Time Problems

### Free APIs (No Credit Card Required)
1. **JSONPlaceholder** - Fake REST API for testing
   - URL: `https://jsonplaceholder.typicode.com/`
   - Use: Mock social media posts, user data

2. **Random User Generator** - Fake user data
   - URL: `https://randomuser.me/api/`
   - Use: User behavior simulation

3. **GitHub API** - Repository events
   - URL: `https://api.github.com/`
   - Use: Code commit monitoring, issue tracking

4. **RSS Feeds** - News and updates
   - Sources: BBC, CNN, Reddit, HackerNews
   - Use: News sentiment analysis

### Free with Registration
1. **Alpha Vantage** - Stock market data
   - Free: 5 calls/minute, 500 calls/day
   - Sign up: `https://www.alphavantage.co/`

2. **OpenWeatherMap** - Weather data
   - Free: 1000 calls/day
   - Sign up: `https://openweathermap.org/api`

3. **CoinGecko** - Cryptocurrency data
   - Free tier available
   - URL: `https://www.coingecko.com/en/api`

## 🎯 6. Next Steps

1. **Choose your data source** from the examples above
2. **Copy and modify** one of the test scripts
3. **Run the tests** to see real data flowing through agents
4. **Expand gradually** by adding more complex logic
5. **Deploy** using the Django API for web access

## 🆘 Troubleshooting

### Common Issues
```
Error: "Module not found"
→ Make sure you're in the virtual environment and src/ is in Python path

Error: "API key required"
→ Sign up for free API keys where indicated

Error: "Rate limit exceeded"
→ Add delays between API calls or use different endpoints

Error: "Agent execution failed"
→ Check agent input data format matches expected structure
```

### Getting Help
- Check the logs in `django_app/` for detailed error messages
- Run tests individually to isolate issues
- Use the existing demo: `python demo_real_time_problems.py`

---

**You now have everything needed to import the framework and test it with real-time data! Start with the stock or system monitoring examples - they require no API keys and work immediately.** 🚀
