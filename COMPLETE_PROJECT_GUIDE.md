# 🚀 AI Agent Framework - Complete Project Guide & Testing Manual

## 📋 **Table of Contents**
1. [Project Overview](#project-overview)
2. [Framework Architecture](#framework-architecture)
3. [Quick Setup & Installation](#quick-setup--installation)
4. [Testing Framework Components](#testing-framework-components)
5. [Agent Creation & Testing](#agent-creation--testing)
6. [Real-Time Data Integration](#real-time-data-integration)
7. [Mock Data Testing](#mock-data-testing)
8. [Advanced Workflows](#advanced-workflows)
9. [Performance & Benchmarking](#performance--benchmarking)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 **Project Overview**

### **What is this Framework?**
The AI Agent Framework is a **production-ready, enterprise-grade platform** for building and orchestrating intelligent agent workflows. Unlike existing solutions (crew.ai, AutoGen), this is built **from scratch** with proper enterprise architecture.

### **Key Capabilities**
- ✅ **DAG & State Machine Workflows** - Define complex task flows
- ✅ **Real-Time Data Processing** - Handle streaming data from any source
- ✅ **Professional Agent Management** - Unique IDs, execution tracking, audit trails
- ✅ **Intel OpenVINO Integration** - ML model optimization
- ✅ **Apache Kafka Messaging** - Enterprise messaging and orchestration
- ✅ **Django REST API** - Complete web interface
- ✅ **Vector Memory** - Persistent knowledge and conversation context
- ✅ **Guardrails & Policies** - Safety and compliance enforcement
- ✅ **Multi-Agent Orchestration** - Collaborative agent workflows

### **Built for Problem Statement Requirements**
- **Task Flows**: DAG or state machine execution ✅
- **Apache Integration**: Kafka, Airflow support ✅
- **Intel Tech**: OpenVINO optimization + DevCloud ready ✅
- **Framework SDK**: Complete APIs for flows, tools, policies ✅
- **Reference Agents**: Working customer support & document processing ✅
- **Performance**: Benchmarking with pre/post optimization ✅

---

## 🏗️ **Framework Architecture**

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │   Orchestrator  │    │     Agents      │
│   (Django)      │──▶ │   (Celery)      │──▶ │   (Executors)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kafka Queue   │    │   State/Memory  │    │   Guardrails    │
│   (Messaging)   │    │   (Vector DB)   │    │   (Policies)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Core Components**
1. **Agent Framework** (`src/core/`) - Base agent classes and execution context
2. **Orchestrator** (`src/orchestrator/`) - DAG/State machine workflow engines
3. **Messaging** (`src/messaging/`) - Kafka integration for event-driven architecture
4. **Tools** (`src/tools/`) - LLM, HTTP, database, and custom tool integrations
5. **Memory** (`src/state_memory/`) - Vector store and session management
6. **Guardrails** (`src/guardrails/`) - Policy enforcement and safety checks
7. **Observability** (`src/observability/`) - Logging, metrics, and audit trails

---

## ⚡ **Quick Setup & Installation**

### **Prerequisites**
- Python 3.10+
- Git
- Windows PowerShell (or Linux/Mac terminal)

### **Step 1: Clone and Setup**
```powershell
# Clone the repository
git clone https://github.com/DevPrasath6/AI-Agent-Framework.git
cd AI-Agent-Framework

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install yfinance psutil pandas numpy  # For real-time data
```

### **Step 2: Verify Installation**
```powershell
# Test framework import and basic functionality
python test_framework_import.py

# Expected output: "All tests passed! Framework is ready to use."
```

### **Step 3: Run Full Test Suite**
```powershell
# Run all framework tests
python -m pytest tests/ -v

# Expected: 15/15 tests passing
```

---

## 🧪 **Testing Framework Components**

### **1. Basic Framework Functionality**

#### **Test Agent Creation & Execution**
```powershell
# Test basic agent creation with professional IDs
python test_framework_import.py
```

**What this tests:**
- Agent creation with professional IDs (AGENT-YYYYMMDD-HHMMSS-NNNN-XXXX)
- Execution context management
- ID generation systems (timestamp, sequential, UUID, custom)

#### **Test Policy & Guardrails**
```powershell
# Test policy enforcement
python -c "
from src.guardrails.policy_checker import PolicyChecker
checker = PolicyChecker()
result = checker.check_input('Test input')
print('Guardrails working:', result.allowed)
"
```

### **2. Workflow Engine Testing**

#### **Test DAG Workflows**
```python
# Create file: test_dag_workflow.py
import asyncio
from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType, SimpleDAGWorkflow

async def test_dag():
    # Define workflow
    workflow_def = WorkflowDefinition(
        id="test_dag",
        name="Test DAG Workflow",
        steps=[
            WorkflowStep(id="step1", name="First Step", step_type=StepType.TOOL),
            WorkflowStep(id="step2", name="Second Step", step_type=StepType.TOOL, dependencies=["step1"])
        ]
    )

    # Create workflow instance
    workflow = SimpleDAGWorkflow(workflow_def)

    # Execute
    result = await workflow.execute({"test": "data"})
    print("DAG Result:", result)

asyncio.run(test_dag())
```

#### **Test State Machine Workflows**
```python
# Create file: test_state_machine.py
from src.orchestrator.state_machine import create_simple_workflow_state_machine, AdvancedStateMachine

# Create state machine
sm_def = create_simple_workflow_state_machine(
    "test_workflow",
    ["start", "processing", "complete"],
    [{"from": "start", "to": "processing"}, {"from": "processing", "to": "complete"}]
)

print("State Machine Created:", sm_def.id)
print("States:", [s.name for s in sm_def.states])
```

### **3. Messaging & Orchestration Testing**

#### **Test Kafka Integration**
```python
# Create file: test_kafka_messaging.py
import asyncio
from src.messaging.kafka_client import get_inmemory_broker

async def test_messaging():
    # Get in-memory broker for testing
    broker = get_inmemory_broker()

    # Test message sending
    await broker.produce("test-topic", {"message": "Hello Framework!"})
    print("✅ Message sent successfully")

    # Test message consumption
    consumer = broker.create_consumer("test-topic")
    async for message in consumer:
        print("✅ Message received:", message)
        break

asyncio.run(test_messaging())
```

---

## 🤖 **Agent Creation & Testing**

### **1. Create Your First Custom Agent**

```python
# Create file: my_custom_agent.py
import asyncio
from src.core.agent_base import AgentBase, AgentCapability
from src.core.execution_context import ExecutionContext

class MyCustomAgent(AgentBase):
    """Custom agent for demonstration."""

    def __init__(self, **kwargs):
        super().__init__(
            name="my_custom_agent",
            description="A custom agent for testing",
            capabilities=[AgentCapability.TEXT_PROCESSING],
            **kwargs
        )

    async def execute(self, input_data, context):
        """Custom processing logic."""
        message = input_data.get("message", "No message provided")

        # Your custom logic here
        processed_message = f"Processed: {message.upper()}"

        return {
            "original": message,
            "processed": processed_message,
            "agent_id": self.id,
            "timestamp": context.timestamp
        }

# Test the custom agent
async def test_custom_agent():
    agent = MyCustomAgent()
    context = ExecutionContext(agent_id=agent.id)

    result = await agent.run({"message": "hello world"}, context)
    print("Custom Agent Result:", result)

if __name__ == "__main__":
    asyncio.run(test_custom_agent())
```

### **2. Test Professional Agent ID Generation**

```python
# Create file: test_agent_ids.py
from src.core.agent_id_generator import AgentIDGenerator

def test_all_id_formats():
    generator = AgentIDGenerator()

    # Test different ID formats
    formats = ["timestamp", "sequential", "uuid", "custom"]

    for format_type in formats:
        agent_id = generator.generate_id(format_type)
        print(f"{format_type.upper()} ID: {agent_id}")

        # Validate format
        is_valid = generator.validate_id(agent_id)
        print(f"Valid: {is_valid}")

        # Parse ID components
        components = generator.parse_id(agent_id)
        print(f"Components: {components}")
        print("-" * 50)

if __name__ == "__main__":
    test_all_id_formats()
```

### **3. Test Agent Memory & Context**

```python
# Create file: test_agent_memory.py
import asyncio
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def test_agent_memory():
    # Create agent with memory enabled
    agent = SimpleAgent(
        name="memory_test_agent",
        description="Testing agent memory",
        memory_enabled=True
    )

    context = ExecutionContext(
        agent_id=agent.id,
        user_id="test_user",
        session_id="test_session"
    )

    # First interaction
    result1 = await agent.run({"message": "Remember: I like coffee"}, context)
    print("First interaction:", result1)

    # Second interaction
    result2 = await agent.run({"message": "What do I like?"}, context)
    print("Second interaction:", result2)

    # Check memory storage
    if agent.memory:
        interactions = await agent.memory.get_conversation_history(context.session_id)
        print(f"Stored interactions: {len(interactions)}")

if __name__ == "__main__":
    asyncio.run(test_agent_memory())
```

---

## 📡 **Real-Time Data Integration**

### **1. Stock Market Data (Yahoo Finance - FREE)**

```powershell
# Test real stock data
python stock_data_example.py

# Test stock monitoring agent
python test_stock_agent.py
```

**Features Demonstrated:**
- Real-time stock price monitoring
- Price change detection and alerts
- Moving average calculations
- Professional agent execution tracking

### **2. System Performance Monitoring**

```powershell
# Test system health monitoring
python test_system_agent.py
```

**Features Demonstrated:**
- Real-time CPU, memory, disk monitoring
- Performance trend analysis
- Automatic alerting on thresholds
- Health status assessment

### **3. Custom Real-Time Data Source**

```python
# Create file: test_custom_realtime.py
import asyncio
import json
import time
from datetime import datetime
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class CustomRealTimeAgent(SimpleAgent):
    """Agent for processing custom real-time data."""

    def __init__(self, **kwargs):
        super().__init__(
            name="custom_realtime_agent",
            description="Processes custom real-time data streams",
            **kwargs
        )
        self.data_buffer = []

    async def execute(self, input_data, context):
        """Process real-time data."""
        # Store in buffer
        self.data_buffer.append({
            "data": input_data,
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.id
        })

        # Keep only last 100 entries
        if len(self.data_buffer) > 100:
            self.data_buffer = self.data_buffer[-100:]

        # Analysis
        analysis = {
            "current_value": input_data.get("value", 0),
            "buffer_size": len(self.data_buffer),
            "processed_by": self.id
        }

        return analysis

async def simulate_realtime_data():
    """Simulate real-time data stream."""
    agent = CustomRealTimeAgent()

    print("🔄 Starting real-time data simulation...")

    for i in range(20):
        # Simulate sensor data
        sensor_data = {
            "sensor_id": f"SENSOR_{i % 3 + 1}",
            "value": 20 + (i * 2.5) + (i % 7),
            "location": {"lat": 37.7749, "lon": -122.4194}
        }

        # Process with agent
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(sensor_data, context)

        print(f"📊 Step {i+1}: Sensor {sensor_data['sensor_id']} = {sensor_data['value']:.1f}")
        print(f"   Agent: {result['output']['processed_by'][:8]}...")

        await asyncio.sleep(0.5)  # 500ms intervals

    print("✅ Real-time simulation completed!")

if __name__ == "__main__":
    asyncio.run(simulate_realtime_data())
```

### **4. IoT Sensor Data Simulation**

```python
# Create file: test_iot_sensors.py
import asyncio
import random
from datetime import datetime
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class IoTMonitoringAgent(SimpleAgent):
    """Agent for monitoring IoT sensor networks."""

    def __init__(self, **kwargs):
        super().__init__(
            name="iot_monitoring_agent",
            description="Monitors IoT sensor data for anomalies",
            **kwargs
        )
        self.sensor_history = {}
        self.alerts = []

    async def execute(self, input_data, context):
        """Monitor IoT sensor data."""
        sensor_id = input_data.get("sensor_id")
        value = input_data.get("value")
        sensor_type = input_data.get("type", "temperature")

        # Track history
        if sensor_id not in self.sensor_history:
            self.sensor_history[sensor_id] = []

        self.sensor_history[sensor_id].append(value)

        # Keep last 10 readings
        if len(self.sensor_history[sensor_id]) > 10:
            self.sensor_history[sensor_id] = self.sensor_history[sensor_id][-10:]

        # Check for anomalies
        alert = None
        if len(self.sensor_history[sensor_id]) >= 3:
            recent_values = self.sensor_history[sensor_id][-3:]
            avg = sum(recent_values) / len(recent_values)

            # Temperature thresholds
            if sensor_type == "temperature":
                if value > 35 or value < 10:
                    alert = f"🚨 Temperature alert: {value}°C on {sensor_id}"
                elif abs(value - avg) > 5:
                    alert = f"⚠️ Rapid temperature change: {value}°C on {sensor_id}"

        if alert:
            self.alerts.append(alert)

        return {
            "sensor_id": sensor_id,
            "value": value,
            "type": sensor_type,
            "alert": alert,
            "history_size": len(self.sensor_history[sensor_id]),
            "agent_id": self.id
        }

async def simulate_iot_network():
    """Simulate IoT sensor network."""
    agent = IoTMonitoringAgent()

    sensors = [
        {"id": "TEMP_001", "type": "temperature", "location": "Server Room"},
        {"id": "TEMP_002", "type": "temperature", "location": "Office Floor 1"},
        {"id": "HUMID_001", "type": "humidity", "location": "Warehouse"},
    ]

    print("🌐 IoT Network Monitoring Started...")

    for minute in range(15):  # 15 minutes simulation
        for sensor in sensors:
            # Generate realistic sensor data
            if sensor["type"] == "temperature":
                base_temp = 22 if "Office" in sensor["location"] else 18
                value = base_temp + random.uniform(-3, 8) + (minute * 0.1)
            else:  # humidity
                value = 45 + random.uniform(-10, 20)

            sensor_data = {
                "sensor_id": sensor["id"],
                "value": round(value, 1),
                "type": sensor["type"],
                "location": sensor["location"],
                "timestamp": datetime.now().isoformat()
            }

            # Process with agent
            context = ExecutionContext(agent_id=agent.id)
            result = await agent.run(sensor_data, context)

            if result["status"] == "completed":
                output = result["output"]
                status = "🔴" if output["alert"] else "🟢"
                print(f"{status} {output['sensor_id']}: {output['value']} | History: {output['history_size']}")

                if output["alert"]:
                    print(f"   {output['alert']}")

        await asyncio.sleep(1)  # 1 second per minute simulation

    print(f"\n📊 Monitoring Summary:")
    print(f"   Total alerts: {len(agent.alerts)}")
    print(f"   Sensors monitored: {len(agent.sensor_history)}")

if __name__ == "__main__":
    asyncio.run(simulate_iot_network())
```

---

## 🎭 **Mock Data Testing**

### **1. Mock Data Generators**

```python
# Create file: mock_data_generators.py
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class MockDataGenerator:
    """Generate mock data for testing agents."""

    @staticmethod
    def generate_financial_data(count: int = 10) -> List[Dict[str, Any]]:
        """Generate mock financial market data."""
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA"]
        data = []

        for i in range(count):
            symbol = random.choice(symbols)
            base_price = {"AAPL": 150, "GOOGL": 120, "MSFT": 300}.get(symbol, 100)

            data.append({
                "symbol": symbol,
                "price": round(base_price + random.uniform(-20, 20), 2),
                "volume": random.randint(1000000, 50000000),
                "change": round(random.uniform(-5, 5), 2),
                "timestamp": (datetime.now() - timedelta(minutes=i)).isoformat()
            })

        return data

    @staticmethod
    def generate_iot_data(count: int = 20) -> List[Dict[str, Any]]:
        """Generate mock IoT sensor data."""
        sensor_types = ["temperature", "humidity", "pressure", "motion"]
        locations = ["Building A", "Building B", "Warehouse", "Data Center"]
        data = []

        for i in range(count):
            sensor_type = random.choice(sensor_types)

            if sensor_type == "temperature":
                value = round(random.uniform(18, 35), 1)
                unit = "°C"
            elif sensor_type == "humidity":
                value = round(random.uniform(30, 80), 1)
                unit = "%"
            elif sensor_type == "pressure":
                value = round(random.uniform(990, 1020), 1)
                unit = "hPa"
            else:  # motion
                value = random.choice([0, 1])
                unit = "detected"

            data.append({
                "sensor_id": f"{sensor_type.upper()}_{random.randint(1, 10):03d}",
                "type": sensor_type,
                "value": value,
                "unit": unit,
                "location": random.choice(locations),
                "battery": random.randint(10, 100),
                "timestamp": (datetime.now() - timedelta(seconds=i*30)).isoformat()
            })

        return data

    @staticmethod
    def generate_customer_inquiries(count: int = 5) -> List[Dict[str, Any]]:
        """Generate mock customer support inquiries."""
        inquiries = [
            "My payment was declined, can you help?",
            "How do I reset my password?",
            "The app keeps crashing on my phone",
            "I want to cancel my subscription",
            "When will my order be delivered?",
            "I'm having trouble logging in",
            "Can I get a refund for my recent purchase?",
            "The website is loading very slowly",
            "I need help setting up my account",
            "Why was I charged twice?"
        ]

        categories = ["billing", "technical", "account", "shipping", "general"]
        priorities = ["low", "medium", "high"]

        data = []
        for i in range(count):
            data.append({
                "inquiry_id": f"INQ_{random.randint(10000, 99999)}",
                "customer_id": f"CUST_{random.randint(1000, 9999)}",
                "message": random.choice(inquiries),
                "category": random.choice(categories),
                "priority": random.choice(priorities),
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
            })

        return data

# Test mock data generation
if __name__ == "__main__":
    generator = MockDataGenerator()

    print("📈 Mock Financial Data:")
    financial_data = generator.generate_financial_data(3)
    for item in financial_data:
        print(f"  {item['symbol']}: ${item['price']} ({item['change']:+.2f})")

    print("\n🌡️ Mock IoT Data:")
    iot_data = generator.generate_iot_data(3)
    for item in iot_data:
        print(f"  {item['sensor_id']}: {item['value']} {item['unit']} at {item['location']}")

    print("\n💬 Mock Customer Inquiries:")
    inquiries = generator.generate_customer_inquiries(3)
    for item in inquiries:
        print(f"  {item['inquiry_id']}: {item['message'][:50]}...")
```

### **2. Mock Data Agent Testing**

```python
# Create file: test_mock_data_agents.py
import asyncio
from mock_data_generators import MockDataGenerator
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def test_agents_with_mock_data():
    """Test agents using mock data."""

    # Create test agent
    agent = SimpleAgent(
        name="mock_data_test_agent",
        description="Agent for testing with mock data"
    )

    generator = MockDataGenerator()

    print("🧪 Testing Agents with Mock Data\n")

    # Test 1: Financial Data
    print("1️⃣ Testing with Mock Financial Data:")
    financial_data = generator.generate_financial_data(3)

    for data in financial_data:
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(data, context)

        if result["status"] == "completed":
            print(f"  ✅ Processed {data['symbol']}: ${data['price']}")
        else:
            print(f"  ❌ Failed to process {data['symbol']}")

    # Test 2: IoT Data
    print("\n2️⃣ Testing with Mock IoT Data:")
    iot_data = generator.generate_iot_data(3)

    for data in iot_data:
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(data, context)

        if result["status"] == "completed":
            print(f"  ✅ Processed {data['sensor_id']}: {data['value']} {data['unit']}")
        else:
            print(f"  ❌ Failed to process {data['sensor_id']}")

    # Test 3: Customer Inquiries
    print("\n3️⃣ Testing with Mock Customer Inquiries:")
    inquiries = generator.generate_customer_inquiries(2)

    for inquiry in inquiries:
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(inquiry, context)

        if result["status"] == "completed":
            print(f"  ✅ Processed inquiry {inquiry['inquiry_id']}")
        else:
            print(f"  ❌ Failed to process inquiry {inquiry['inquiry_id']}")

    print(f"\n🎉 Mock data testing completed!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Total executions: {agent.execution_count}")

if __name__ == "__main__":
    asyncio.run(test_agents_with_mock_data())
```

### **3. Bulk Mock Data Testing**

```python
# Create file: test_bulk_mock_data.py
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from mock_data_generators import MockDataGenerator
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def bulk_test_agents():
    """Test agents with large volumes of mock data."""

    print("🚀 Bulk Mock Data Testing Started\n")

    # Create multiple agents
    agents = [
        SimpleAgent(name=f"bulk_test_agent_{i}", description=f"Bulk test agent {i}")
        for i in range(3)
    ]

    generator = MockDataGenerator()

    # Generate large datasets
    datasets = {
        "financial": generator.generate_financial_data(50),
        "iot": generator.generate_iot_data(100),
        "customer": generator.generate_customer_inquiries(25)
    }

    total_processed = 0
    start_time = time.time()

    for dataset_name, data in datasets.items():
        print(f"📊 Processing {dataset_name} dataset ({len(data)} items)...")

        # Process data with round-robin agent assignment
        for i, item in enumerate(data):
            agent = agents[i % len(agents)]
            context = ExecutionContext(agent_id=agent.id)

            result = await agent.run(item, context)
            if result["status"] == "completed":
                total_processed += 1

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"  ✅ Processed {i + 1}/{len(data)} items")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n📈 Bulk Testing Results:")
    print(f"   Total items processed: {total_processed}")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Processing rate: {total_processed/total_time:.2f} items/second")

    # Agent statistics
    print(f"\n🤖 Agent Statistics:")
    for agent in agents:
        print(f"   {agent.name}: {agent.execution_count} executions")

if __name__ == "__main__":
    asyncio.run(bulk_test_agents())
```

---

## 🔄 **Advanced Workflows**

### **1. Multi-Agent Collaboration**

```python
# Create file: test_multi_agent_workflow.py
import asyncio
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext
from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType, SimpleDAGWorkflow

class DataProcessorAgent(SimpleAgent):
    """Agent for initial data processing."""

    async def execute(self, input_data, context):
        data = input_data.get("raw_data", "")
        processed = data.upper() + " [PROCESSED]"
        return {"processed_data": processed, "processor_id": self.id}

class AnalyzerAgent(SimpleAgent):
    """Agent for data analysis."""

    async def execute(self, input_data, context):
        data = input_data.get("processed_data", "")
        analysis = f"Analysis: {len(data)} characters, contains PROCESSED tag"
        return {"analysis": analysis, "analyzer_id": self.id}

class ReporterAgent(SimpleAgent):
    """Agent for generating reports."""

    async def execute(self, input_data, context):
        analysis = input_data.get("analysis", "")
        report = f"REPORT: {analysis} [COMPLETED]"
        return {"final_report": report, "reporter_id": self.id}

async def test_multi_agent_workflow():
    """Test multi-agent collaboration workflow."""

    print("🤝 Multi-Agent Collaboration Test\n")

    # Create agents
    processor = DataProcessorAgent(name="data_processor")
    analyzer = AnalyzerAgent(name="data_analyzer")
    reporter = ReporterAgent(name="report_generator")

    # Create workflow definition
    workflow_def = WorkflowDefinition(
        id="multi_agent_workflow",
        name="Multi-Agent Processing Pipeline",
        steps=[
            WorkflowStep(
                id="process",
                name="Data Processing",
                step_type=StepType.AGENT,
                config={"agent_name": "data_processor"}
            ),
            WorkflowStep(
                id="analyze",
                name="Data Analysis",
                step_type=StepType.AGENT,
                config={"agent_name": "data_analyzer"},
                dependencies=["process"]
            ),
            WorkflowStep(
                id="report",
                name="Report Generation",
                step_type=StepType.AGENT,
                config={"agent_name": "report_generator"},
                dependencies=["analyze"]
            )
        ]
    )

    # Create agent registry
    agent_registry = {
        "data_processor": processor,
        "data_analyzer": analyzer,
        "report_generator": reporter
    }

    # Create and execute workflow
    workflow = SimpleDAGWorkflow(workflow_def, agent_registry=agent_registry)

    input_data = {"raw_data": "Hello World from Multi-Agent Framework"}
    result = await workflow.execute(input_data)

    print("🎯 Workflow Results:")
    print(f"   Status: {result.status}")
    print(f"   Steps completed: {len(result.step_results)}")
    print(f"   Final output: {result.output}")

    # Show individual agent contributions
    print(f"\n🤖 Agent Contributions:")
    for step_id, step_result in result.step_results.items():
        agent_id = step_result.get("processor_id") or step_result.get("analyzer_id") or step_result.get("reporter_id")
        if agent_id:
            print(f"   {step_id}: {agent_id[:12]}...")

if __name__ == "__main__":
    asyncio.run(test_multi_agent_workflow())
```

### **2. Human-in-the-Loop Workflow**

```python
# Create file: test_human_in_loop.py
import asyncio
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class ApprovalAgent(SimpleAgent):
    """Agent that requires human approval for certain actions."""

    def __init__(self, approval_threshold=0.8, **kwargs):
        super().__init__(
            name="approval_agent",
            description="Agent with human-in-the-loop approval",
            **kwargs
        )
        self.approval_threshold = approval_threshold
        self.pending_approvals = []

    async def execute(self, input_data, context):
        """Execute with approval logic."""
        action = input_data.get("action", "")
        confidence = input_data.get("confidence", 0.5)

        if confidence >= self.approval_threshold:
            # Auto-approve high confidence actions
            result = f"AUTO-APPROVED: {action}"
            status = "completed"
        else:
            # Require human approval
            approval_id = f"APPROVAL_{len(self.pending_approvals) + 1}"
            self.pending_approvals.append({
                "id": approval_id,
                "action": action,
                "confidence": confidence,
                "status": "pending"
            })

            result = f"PENDING APPROVAL: {action} (confidence: {confidence})"
            status = "pending_approval"

        return {
            "result": result,
            "status": status,
            "confidence": confidence,
            "requires_approval": confidence < self.approval_threshold,
            "agent_id": self.id
        }

    def approve_action(self, approval_id: str) -> bool:
        """Simulate human approval."""
        for approval in self.pending_approvals:
            if approval["id"] == approval_id:
                approval["status"] = "approved"
                return True
        return False

    def reject_action(self, approval_id: str) -> bool:
        """Simulate human rejection."""
        for approval in self.pending_approvals:
            if approval["id"] == approval_id:
                approval["status"] = "rejected"
                return True
        return False

async def test_human_in_loop():
    """Test human-in-the-loop workflow."""

    print("👤 Human-in-the-Loop Workflow Test\n")

    agent = ApprovalAgent(approval_threshold=0.7)

    # Test scenarios
    test_actions = [
        {"action": "Delete user account", "confidence": 0.9},  # Auto-approve
        {"action": "Send marketing email", "confidence": 0.6},  # Needs approval
        {"action": "Update user profile", "confidence": 0.8},  # Auto-approve
        {"action": "Refund payment", "confidence": 0.5},  # Needs approval
    ]

    print("🔄 Processing Actions:")
    for i, action_data in enumerate(test_actions, 1):
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(action_data, context)

        if result["status"] == "completed":
            output = result["output"]
            if output["requires_approval"]:
                print(f"{i}. ⏳ {output['result']}")
            else:
                print(f"{i}. ✅ {output['result']}")
        else:
            print(f"{i}. ❌ Failed to process action")

    # Show pending approvals
    print(f"\n📋 Pending Approvals ({len(agent.pending_approvals)}):")
    for approval in agent.pending_approvals:
        if approval["status"] == "pending":
            print(f"   {approval['id']}: {approval['action']} (confidence: {approval['confidence']})")

    # Simulate human decisions
    print(f"\n👤 Simulating Human Decisions:")
    if len(agent.pending_approvals) >= 2:
        # Approve first pending action
        first_pending = next(a for a in agent.pending_approvals if a["status"] == "pending")
        agent.approve_action(first_pending["id"])
        print(f"   ✅ Approved: {first_pending['action']}")

        # Reject second pending action if exists
        remaining_pending = [a for a in agent.pending_approvals if a["status"] == "pending"]
        if remaining_pending:
            agent.reject_action(remaining_pending[0]["id"])
            print(f"   ❌ Rejected: {remaining_pending[0]['action']}")

    # Final status
    print(f"\n📊 Final Status:")
    approved = sum(1 for a in agent.pending_approvals if a["status"] == "approved")
    rejected = sum(1 for a in agent.pending_approvals if a["status"] == "rejected")
    pending = sum(1 for a in agent.pending_approvals if a["status"] == "pending")

    print(f"   Approved: {approved}")
    print(f"   Rejected: {rejected}")
    print(f"   Still Pending: {pending}")

if __name__ == "__main__":
    asyncio.run(test_human_in_loop())
```

---

## 🚀 **Performance & Benchmarking**

### **1. Agent Performance Testing**

```python
# Create file: test_agent_performance.py
import asyncio
import time
from statistics import mean, median
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def performance_test_agents():
    """Test agent performance under load."""

    print("⚡ Agent Performance Testing\n")

    # Create test agent
    agent = SimpleAgent(
        name="performance_test_agent",
        description="Agent for performance testing"
    )

    # Test scenarios
    test_sizes = [10, 50, 100, 200]

    for size in test_sizes:
        print(f"🧪 Testing with {size} executions...")

        execution_times = []
        start_time = time.time()

        # Execute multiple times
        for i in range(size):
            context = ExecutionContext(agent_id=agent.id)
            exec_start = time.time()

            result = await agent.run({"test_data": f"item_{i}"}, context)

            exec_end = time.time()
            execution_times.append(exec_end - exec_start)

        total_time = time.time() - start_time

        # Calculate statistics
        avg_time = mean(execution_times)
        median_time = median(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        throughput = size / total_time

        print(f"   📊 Results:")
        print(f"      Total time: {total_time:.3f}s")
        print(f"      Average execution: {avg_time:.4f}s")
        print(f"      Median execution: {median_time:.4f}s")
        print(f"      Min execution: {min_time:.4f}s")
        print(f"      Max execution: {max_time:.4f}s")
        print(f"      Throughput: {throughput:.2f} executions/second")
        print()

    print(f"✅ Performance testing completed!")
    print(f"   Total executions: {agent.execution_count}")

if __name__ == "__main__":
    asyncio.run(performance_test_agents())
```

### **2. OpenVINO Benchmarking**

```powershell
# Test OpenVINO benchmarking system
python bench/openvino_bench.py --runs 50 --out bench_output/test_result.json --plot

# View results
python bench/aggregate_results.py --json bench_output/test_result.json --openvino false --model-path ""
```

### **3. Memory Usage Testing**

```python
# Create file: test_memory_usage.py
import asyncio
import psutil
import os
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def test_memory_usage():
    """Test agent memory usage patterns."""

    print("🧠 Memory Usage Testing\n")

    # Get initial memory usage
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    print(f"📊 Initial memory usage: {initial_memory:.2f} MB")

    # Create agents with memory enabled/disabled
    agent_with_memory = SimpleAgent(
        name="memory_enabled_agent",
        description="Agent with memory enabled",
        memory_enabled=True
    )

    agent_without_memory = SimpleAgent(
        name="memory_disabled_agent",
        description="Agent without memory",
        memory_enabled=False
    )

    # Test memory usage with different configurations
    agents = [
        ("With Memory", agent_with_memory),
        ("Without Memory", agent_without_memory)
    ]

    for agent_type, agent in agents:
        print(f"\n🧪 Testing {agent_type}:")

        # Execute multiple operations
        for i in range(100):
            context = ExecutionContext(
                agent_id=agent.id,
                session_id=f"session_{i % 10}"  # 10 different sessions
            )

            await agent.run({
                "message": f"Test message {i} with some content to process",
                "data": list(range(100))  # Some data to process
            }, context)

            # Check memory every 20 executions
            if (i + 1) % 20 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                print(f"   After {i+1} executions: {current_memory:.2f} MB (+{memory_increase:.2f} MB)")

    # Final memory check
    final_memory = process.memory_info().rss / 1024 / 1024
    total_increase = final_memory - initial_memory

    print(f"\n📈 Memory Usage Summary:")
    print(f"   Initial: {initial_memory:.2f} MB")
    print(f"   Final: {final_memory:.2f} MB")
    print(f"   Total increase: {total_increase:.2f} MB")
    print(f"   Agent with memory executions: {agent_with_memory.execution_count}")
    print(f"   Agent without memory executions: {agent_without_memory.execution_count}")

if __name__ == "__main__":
    asyncio.run(test_memory_usage())
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Import Errors**
```powershell
# Issue: "Module not found" errors
# Solution: Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Verify Python path
python -c "import sys; print(sys.path)"

# Install missing dependencies
pip install -r requirements.txt
```

#### **2. Agent Execution Failures**
```python
# Create file: debug_agent_execution.py
import asyncio
import logging
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def debug_agent():
    """Debug agent execution issues."""

    agent = SimpleAgent(name="debug_agent", description="Debug test")
    context = ExecutionContext(agent_id=agent.id)

    try:
        result = await agent.run({"test": "data"}, context)
        print("✅ Agent execution successful:", result)
    except Exception as e:
        print("❌ Agent execution failed:", str(e))

        # Check agent state
        print(f"   Agent status: {agent.status}")
        print(f"   Agent error count: {agent.error_count}")
        print(f"   Agent execution count: {agent.execution_count}")

if __name__ == "__main__":
    asyncio.run(debug_agent())
```

#### **3. Performance Issues**
```python
# Create file: debug_performance.py
import asyncio
import time
import cProfile
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def profile_agent_execution():
    """Profile agent execution for performance issues."""

    agent = SimpleAgent(name="profile_agent")
    context = ExecutionContext(agent_id=agent.id)

    # Profile agent execution
    pr = cProfile.Profile()
    pr.enable()

    # Execute agent multiple times
    for i in range(10):
        await agent.run({"data": f"test_{i}"}, context)

    pr.disable()
    pr.print_stats(sort='cumulative')

if __name__ == "__main__":
    asyncio.run(profile_agent_execution())
```

#### **4. Memory Leaks**
```python
# Create file: debug_memory_leaks.py
import asyncio
import gc
import psutil
import os
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def detect_memory_leaks():
    """Detect potential memory leaks in agent execution."""

    process = psutil.Process(os.getpid())

    for iteration in range(5):
        print(f"\n🔄 Iteration {iteration + 1}:")

        # Create agents
        agents = [SimpleAgent(name=f"agent_{i}") for i in range(10)]

        # Execute agents
        for agent in agents:
            context = ExecutionContext(agent_id=agent.id)
            await agent.run({"test": "data"}, context)

        # Check memory
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"   Memory usage: {memory_mb:.2f} MB")

        # Force garbage collection
        del agents
        gc.collect()

        # Check memory after cleanup
        memory_after_gc = process.memory_info().rss / 1024 / 1024
        print(f"   Memory after GC: {memory_after_gc:.2f} MB")

if __name__ == "__main__":
    asyncio.run(detect_memory_leaks())
```

### **Testing Checklist**

#### **✅ Framework Verification**
- [ ] `python test_framework_import.py` - Basic functionality
- [ ] `python -m pytest tests/ -v` - Full test suite (15/15 passing)
- [ ] `python stock_data_example.py` - Real data integration
- [ ] `python test_stock_agent.py` - Agent processing
- [ ] `python test_system_agent.py` - System monitoring

#### **✅ Custom Agent Testing**
- [ ] Create custom agent class
- [ ] Test agent execution with sample data
- [ ] Verify professional ID generation
- [ ] Test memory and context management
- [ ] Validate guardrails and policies

#### **✅ Real-Time Data Testing**
- [ ] Stock market data (Yahoo Finance)
- [ ] System performance monitoring
- [ ] Custom IoT sensor simulation
- [ ] Social media data (if API available)
- [ ] Custom real-time data sources

#### **✅ Mock Data Testing**
- [ ] Generate mock financial data
- [ ] Generate mock IoT sensor data
- [ ] Generate mock customer inquiries
- [ ] Test agents with large datasets
- [ ] Validate bulk processing performance

#### **✅ Advanced Features**
- [ ] Multi-agent workflows
- [ ] Human-in-the-loop processes
- [ ] State machine workflows
- [ ] DAG workflow execution
- [ ] Kafka messaging integration

#### **✅ Performance & Benchmarking**
- [ ] Agent execution performance
- [ ] Memory usage patterns
- [ ] OpenVINO benchmarking
- [ ] Throughput testing
- [ ] Resource utilization

---

## 🎉 **Success Criteria**

### **Framework is Working Correctly When:**

1. **✅ All Tests Pass**: 15/15 tests in test suite
2. **✅ Agents Execute Successfully**: Professional IDs generated, execution tracked
3. **✅ Real-Time Data Processing**: Stock/system data processed without errors
4. **✅ Mock Data Integration**: Bulk processing completes successfully
5. **✅ Workflows Function**: DAG and state machine execution works
6. **✅ Performance Acceptable**: >10 executions/second for simple agents
7. **✅ Memory Stable**: No significant memory leaks detected
8. **✅ OpenVINO Integration**: Benchmarking system runs successfully

### **Ready for Production When:**

- All success criteria met ✅
- Custom agents created and tested ✅
- Real-time data sources integrated ✅
- Performance benchmarks established ✅
- Documentation complete ✅
- Deployment strategy defined ✅

---

**🚀 This framework is ready to handle real-world, production-scale AI agent workflows with enterprise-grade reliability and performance!**

---

### **Quick Reference Commands:**

```powershell
# Setup
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt yfinance psutil pandas numpy

# Basic Testing
python test_framework_import.py
python -m pytest tests/ -v

# Real-Time Data
python stock_data_example.py
python test_stock_agent.py
python test_system_agent.py

# Custom Testing
python my_custom_agent.py
python test_mock_data_agents.py
python test_multi_agent_workflow.py

# Performance
python test_agent_performance.py
python bench/openvino_bench.py --runs 50
```
