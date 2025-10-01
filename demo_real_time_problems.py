"""
Real-Time Problem Solving with AI Agent Framework

This module demonstrates the framework's capabilities for handling real-time problems
including streaming data, live APIs, real-time analytics, and event-driven workflows.
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import aiohttp
import requests
from dataclasses import dataclass

from src.core.agent_base import SimpleAgent, AgentCapability
from src.core.execution_context import ExecutionContext
from src.messaging.kafka_client import get_inmemory_broker


@dataclass
class RealTimeProblem:
    """Definition of a real-time problem scenario."""
    name: str
    description: str
    data_source: str
    update_frequency: str
    complexity: str
    example_data: Dict[str, Any]


class RealTimeDataSimulator:
    """Simulates real-time data streams for testing."""

    def __init__(self):
        self.is_running = False
        self.data_streams = {}

    async def start_stock_stream(self, symbols: List[str] = None):
        """Simulate real-time stock price updates."""
        symbols = symbols or ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

        async def generate_stock_data():
            while self.is_running:
                for symbol in symbols:
                    price = random.uniform(100, 500)
                    change = random.uniform(-5, 5)
                    yield {
                        "symbol": symbol,
                        "price": round(price, 2),
                        "change": round(change, 2),
                        "change_percent": round((change/price)*100, 2),
                        "timestamp": datetime.now().isoformat(),
                        "volume": random.randint(1000, 100000)
                    }
                await asyncio.sleep(1)  # Update every second

        return generate_stock_data()

    async def start_iot_sensor_stream(self):
        """Simulate IoT sensor data."""
        async def generate_sensor_data():
            while self.is_running:
                yield {
                    "sensor_id": f"SENSOR_{random.randint(1, 10)}",
                    "temperature": round(random.uniform(18, 35), 1),
                    "humidity": round(random.uniform(30, 80), 1),
                    "pressure": round(random.uniform(990, 1020), 1),
                    "location": {"lat": random.uniform(-90, 90), "lon": random.uniform(-180, 180)},
                    "timestamp": datetime.now().isoformat(),
                    "battery_level": random.randint(10, 100)
                }
                await asyncio.sleep(0.5)  # Update every 500ms

        return generate_sensor_data()

    async def start_log_stream(self):
        """Simulate application log stream."""
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        services = ["api-gateway", "user-service", "payment-service", "notification-service"]

        async def generate_log_data():
            while self.is_running:
                yield {
                    "timestamp": datetime.now().isoformat(),
                    "level": random.choice(log_levels),
                    "service": random.choice(services),
                    "message": f"Sample log message {random.randint(1000, 9999)}",
                    "user_id": f"user_{random.randint(1, 1000)}",
                    "request_id": f"req_{random.randint(10000, 99999)}",
                    "response_time": random.randint(10, 2000)
                }
                await asyncio.sleep(0.1)  # High frequency logs

        return generate_log_data()


class RealTimeMarketAnalysisAgent(SimpleAgent):
    """Agent for real-time market data analysis."""

    def __init__(self, **kwargs):
        super().__init__(
            name="market_analysis_agent",
            description="Real-time market data analysis and alerts",
            **kwargs
        )
        self.price_history = {}
        self.alerts = []

    async def execute(self, input_data: Any, context: ExecutionContext) -> Dict[str, Any]:
        """Analyze real-time market data."""
        if not isinstance(input_data, dict) or "symbol" not in input_data:
            return {"error": "Invalid market data format"}

        symbol = input_data["symbol"]
        current_price = input_data["price"]
        timestamp = input_data["timestamp"]

        # Track price history
        if symbol not in self.price_history:
            self.price_history[symbol] = []

        self.price_history[symbol].append({
            "price": current_price,
            "timestamp": timestamp
        })

        # Keep only last 100 data points
        if len(self.price_history[symbol]) > 100:
            self.price_history[symbol] = self.price_history[symbol][-100:]

        # Generate analysis
        analysis = self._analyze_price_trend(symbol, current_price)

        return {
            "symbol": symbol,
            "current_price": current_price,
            "analysis": analysis,
            "timestamp": timestamp,
            "agent_id": self.id
        }

    def _analyze_price_trend(self, symbol: str, current_price: float) -> Dict[str, Any]:
        """Analyze price trend and generate alerts."""
        history = self.price_history[symbol]

        if len(history) < 5:
            return {"trend": "insufficient_data", "confidence": 0}

        # Calculate moving averages
        prices = [h["price"] for h in history[-10:]]
        short_ma = sum(prices[-5:]) / 5 if len(prices) >= 5 else current_price
        long_ma = sum(prices) / len(prices)

        # Determine trend
        if short_ma > long_ma * 1.02:
            trend = "bullish"
        elif short_ma < long_ma * 0.98:
            trend = "bearish"
        else:
            trend = "sideways"

        # Check for significant price movements
        if len(history) >= 2:
            prev_price = history[-2]["price"]
            price_change = (current_price - prev_price) / prev_price * 100

            if abs(price_change) > 5:  # 5% movement
                alert = {
                    "type": "significant_movement",
                    "symbol": symbol,
                    "change_percent": round(price_change, 2),
                    "timestamp": datetime.now().isoformat()
                }
                self.alerts.append(alert)

        return {
            "trend": trend,
            "short_ma": round(short_ma, 2),
            "long_ma": round(long_ma, 2),
            "confidence": min(len(history) / 20, 1.0),
            "alerts": self.alerts[-5:]  # Last 5 alerts
        }


class RealTimeAnomalyDetectionAgent(SimpleAgent):
    """Agent for detecting anomalies in real-time data streams."""

    def __init__(self, threshold: float = 2.5, **kwargs):
        super().__init__(
            name="anomaly_detection_agent",
            description="Real-time anomaly detection using statistical methods",
            **kwargs
        )
        self.threshold = threshold
        self.data_windows = {}
        self.anomalies = []

    async def execute(self, input_data: Any, context: ExecutionContext) -> Dict[str, Any]:
        """Detect anomalies in real-time sensor data."""
        sensor_id = input_data.get("sensor_id", "unknown")
        temperature = input_data.get("temperature")
        timestamp = input_data.get("timestamp")

        if temperature is None:
            return {"error": "No temperature data provided"}

        # Maintain sliding window for each sensor
        if sensor_id not in self.data_windows:
            self.data_windows[sensor_id] = []

        self.data_windows[sensor_id].append(temperature)

        # Keep only last 50 readings
        if len(self.data_windows[sensor_id]) > 50:
            self.data_windows[sensor_id] = self.data_windows[sensor_id][-50:]

        # Detect anomaly using Z-score
        window = self.data_windows[sensor_id]
        is_anomaly, z_score = self._detect_anomaly(temperature, window)

        result = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 3) if z_score else None,
            "timestamp": timestamp,
            "window_size": len(window),
            "agent_id": self.id
        }

        if is_anomaly:
            anomaly = {
                "sensor_id": sensor_id,
                "value": temperature,
                "z_score": z_score,
                "timestamp": timestamp
            }
            self.anomalies.append(anomaly)
            result["recent_anomalies"] = self.anomalies[-10:]

        return result

    def _detect_anomaly(self, value: float, window: List[float]) -> tuple[bool, Optional[float]]:
        """Detect anomaly using Z-score method."""
        if len(window) < 10:  # Need sufficient data
            return False, None

        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std_dev = variance ** 0.5

        if std_dev == 0:
            return False, 0

        z_score = abs(value - mean) / std_dev
        is_anomaly = z_score > self.threshold

        return is_anomaly, z_score


class RealTimeLogAnalysisAgent(SimpleAgent):
    """Agent for real-time log analysis and monitoring."""

    def __init__(self, **kwargs):
        super().__init__(
            name="log_analysis_agent",
            description="Real-time log analysis and alert generation",
            **kwargs
        )
        self.error_counts = {}
        self.response_times = {}
        self.alerts = []

    async def execute(self, input_data: Any, context: ExecutionContext) -> Dict[str, Any]:
        """Analyze real-time log data."""
        log_level = input_data.get("level")
        service = input_data.get("service")
        response_time = input_data.get("response_time")
        timestamp = input_data.get("timestamp")

        # Track error rates
        if service not in self.error_counts:
            self.error_counts[service] = {"total": 0, "errors": 0}

        self.error_counts[service]["total"] += 1
        if log_level in ["ERROR", "WARNING"]:
            self.error_counts[service]["errors"] += 1

        # Track response times
        if service not in self.response_times:
            self.response_times[service] = []

        if response_time:
            self.response_times[service].append(response_time)
            # Keep only last 100 response times
            if len(self.response_times[service]) > 100:
                self.response_times[service] = self.response_times[service][-100:]

        # Generate analysis
        analysis = self._analyze_service_health(service)

        return {
            "service": service,
            "log_level": log_level,
            "analysis": analysis,
            "timestamp": timestamp,
            "agent_id": self.id
        }

    def _analyze_service_health(self, service: str) -> Dict[str, Any]:
        """Analyze service health metrics."""
        error_data = self.error_counts.get(service, {"total": 0, "errors": 0})
        response_data = self.response_times.get(service, [])

        # Calculate error rate
        error_rate = (error_data["errors"] / error_data["total"]) * 100 if error_data["total"] > 0 else 0

        # Calculate average response time
        avg_response_time = sum(response_data) / len(response_data) if response_data else 0

        # Generate alerts
        alerts = []
        if error_rate > 10:  # More than 10% error rate
            alerts.append({
                "type": "high_error_rate",
                "service": service,
                "error_rate": round(error_rate, 2),
                "timestamp": datetime.now().isoformat()
            })

        if avg_response_time > 1000:  # Response time > 1 second
            alerts.append({
                "type": "slow_response",
                "service": service,
                "avg_response_time": round(avg_response_time, 2),
                "timestamp": datetime.now().isoformat()
            })

        return {
            "error_rate": round(error_rate, 2),
            "avg_response_time": round(avg_response_time, 2),
            "total_requests": error_data["total"],
            "health_status": "unhealthy" if alerts else "healthy",
            "alerts": alerts
        }


async def demo_real_time_market_analysis():
    """Demonstrate real-time market data analysis."""
    print("=== Real-Time Market Analysis Demo ===")

    # Create market analysis agent
    market_agent = RealTimeMarketAnalysisAgent()

    # Create data simulator
    simulator = RealTimeDataSimulator()
    simulator.is_running = True

    # Start stock data stream
    stock_stream = await simulator.start_stock_stream(["AAPL", "GOOGL"])

    print("Starting real-time market analysis (10 seconds)...")
    start_time = time.time()

    # Process stream for 10 seconds
    async for stock_data in stock_stream:
        if time.time() - start_time > 10:
            break

        # Analyze the data
        context = ExecutionContext(agent_id=market_agent.id)
        result = await market_agent.run(stock_data, context)

        # Display results
        if result["status"] == "completed":
            output = result["output"]
            print(f"📈 {output['symbol']}: ${output['current_price']} | "
                  f"Trend: {output['analysis']['trend']} | "
                  f"Confidence: {output['analysis']['confidence']:.2f}")

            # Show alerts
            alerts = output['analysis'].get('alerts', [])
            for alert in alerts[-1:]:  # Show latest alert only
                print(f"🚨 ALERT: {alert['type']} for {alert['symbol']} "
                      f"({alert['change_percent']:+.2f}%)")

    simulator.is_running = False
    print("Market analysis demo completed.\n")


async def demo_real_time_anomaly_detection():
    """Demonstrate real-time anomaly detection."""
    print("=== Real-Time Anomaly Detection Demo ===")

    # Create anomaly detection agent
    anomaly_agent = RealTimeAnomalyDetectionAgent(threshold=2.0)

    # Create data simulator
    simulator = RealTimeDataSimulator()
    simulator.is_running = True

    # Start IoT sensor stream
    sensor_stream = await simulator.start_iot_sensor_stream()

    print("Starting real-time anomaly detection (8 seconds)...")
    start_time = time.time()

    # Process stream for 8 seconds
    async for sensor_data in sensor_stream:
        if time.time() - start_time > 8:
            break

        # Detect anomalies
        context = ExecutionContext(agent_id=anomaly_agent.id)
        result = await anomaly_agent.run(sensor_data, context)

        # Display results
        if result["status"] == "completed":
            output = result["output"]
            status = "🔴 ANOMALY" if output["is_anomaly"] else "🟢 NORMAL"
            print(f"{status} {output['sensor_id']}: {output['temperature']}°C "
                  f"(Z-score: {output['z_score']})")

    simulator.is_running = False
    print(f"Anomaly detection completed. Found {len(anomaly_agent.anomalies)} anomalies.\n")


async def demo_real_time_log_analysis():
    """Demonstrate real-time log analysis."""
    print("=== Real-Time Log Analysis Demo ===")

    # Create log analysis agent
    log_agent = RealTimeLogAnalysisAgent()

    # Create data simulator
    simulator = RealTimeDataSimulator()
    simulator.is_running = True

    # Start log stream
    log_stream = await simulator.start_log_stream()

    print("Starting real-time log analysis (5 seconds)...")
    start_time = time.time()

    # Process stream for 5 seconds
    processed_logs = 0
    async for log_data in log_stream:
        if time.time() - start_time > 5:
            break

        # Analyze logs
        context = ExecutionContext(agent_id=log_agent.id)
        result = await log_agent.run(log_data, context)

        processed_logs += 1

        # Display results every 20 logs
        if processed_logs % 20 == 0:
            if result["status"] == "completed":
                output = result["output"]
                analysis = output["analysis"]
                status = "🔴" if analysis["health_status"] == "unhealthy" else "🟢"
                print(f"{status} {output['service']}: "
                      f"Error Rate: {analysis['error_rate']}% | "
                      f"Avg Response: {analysis['avg_response_time']}ms")

    simulator.is_running = False
    print(f"Log analysis completed. Processed {processed_logs} logs.\n")


def get_real_world_problem_sources():
    """Provide information about real-world problem sources."""

    problems = [
        RealTimeProblem(
            name="Financial Market Data",
            description="Real-time stock prices, crypto currencies, forex rates",
            data_source="Alpha Vantage API, Yahoo Finance, Binance API, IEX Cloud",
            update_frequency="Every second to minute",
            complexity="Medium",
            example_data={
                "symbol": "AAPL",
                "price": 178.25,
                "change": 2.15,
                "volume": 52389000
            }
        ),
        RealTimeProblem(
            name="IoT Sensor Networks",
            description="Temperature, humidity, air quality, motion sensors",
            data_source="AWS IoT, Azure IoT Hub, ThingSpeak, Arduino Cloud",
            update_frequency="Every few seconds",
            complexity="High",
            example_data={
                "sensor_id": "TEMP_001",
                "temperature": 23.5,
                "humidity": 65.2,
                "location": {"lat": 37.7749, "lon": -122.4194}
            }
        ),
        RealTimeProblem(
            name="Social Media Streams",
            description="Twitter feeds, Reddit posts, news articles",
            data_source="Twitter API, Reddit API, NewsAPI, RSS feeds",
            update_frequency="Continuous",
            complexity="High",
            example_data={
                "text": "Breaking news about technology...",
                "sentiment": "neutral",
                "hashtags": ["#tech", "#ai"],
                "timestamp": "2025-10-01T17:30:00Z"
            }
        ),
        RealTimeProblem(
            name="Web Traffic Analytics",
            description="Website visits, user behavior, performance metrics",
            data_source="Google Analytics API, custom tracking, CDN logs",
            update_frequency="Every minute",
            complexity="Medium",
            example_data={
                "page": "/homepage",
                "visitors": 245,
                "bounce_rate": 0.32,
                "load_time": 1.2
            }
        ),
        RealTimeProblem(
            name="System Monitoring",
            description="Server metrics, application logs, error tracking",
            data_source="Prometheus, Grafana, ELK Stack, custom APIs",
            update_frequency="Every few seconds",
            complexity="High",
            example_data={
                "cpu_usage": 78.5,
                "memory_usage": 85.2,
                "disk_io": 150.3,
                "error_count": 12
            }
        ),
        RealTimeProblem(
            name="E-commerce Events",
            description="Product views, purchases, cart abandonment",
            data_source="Shopify API, WooCommerce, custom e-commerce APIs",
            update_frequency="Real-time",
            complexity="Medium",
            example_data={
                "event": "purchase",
                "product_id": "PROD_123",
                "price": 29.99,
                "user_id": "USER_456"
            }
        )
    ]

    return problems


async def main():
    """Run all real-time problem demonstrations."""
    print("🚀 AI Agent Framework - Real-Time Problem Solving Demonstration\n")

    # Run real-time demos
    await demo_real_time_market_analysis()
    await demo_real_time_anomaly_detection()
    await demo_real_time_log_analysis()

    # Show real-world problem sources
    print("=== Real-World Problem Sources ===")
    problems = get_real_world_problem_sources()

    for i, problem in enumerate(problems, 1):
        print(f"\n{i}. {problem.name}")
        print(f"   Description: {problem.description}")
        print(f"   Data Sources: {problem.data_source}")
        print(f"   Update Frequency: {problem.update_frequency}")
        print(f"   Complexity: {problem.complexity}")
        print(f"   Example Data: {problem.example_data}")

    print(f"\n=== Framework Real-Time Capabilities ===")
    print("✅ Streaming data processing with async agents")
    print("✅ Real-time analytics and pattern detection")
    print("✅ Event-driven workflow orchestration")
    print("✅ Kafka integration for high-throughput messaging")
    print("✅ Professional agent ID tracking for all operations")
    print("✅ Memory and state management for continuous learning")
    print("✅ Anomaly detection and alerting systems")
    print("✅ Multi-agent collaboration for complex problems")

    print(f"\n🎉 Real-time problem solving demonstration completed!")
    print("The framework is ready to handle real-world, real-time problems!")


if __name__ == "__main__":
    asyncio.run(main())
