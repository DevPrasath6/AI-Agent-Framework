"""
System Health Monitoring Agent Test - Monitor real system performance
This shows how to create an agent that monitors actual system resources.
No external APIs needed - uses built-in system data!
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import psutil
import time
from datetime import datetime
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

class SystemHealthAgent(SimpleAgent):
    """Agent that monitors system health and detects performance issues."""

    def __init__(self, cpu_threshold=75, memory_threshold=80, **kwargs):
        super().__init__(
            name="system_health_monitor",
            description="Monitor system performance and detect issues",
            **kwargs
        )
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.performance_history = []
        self.alerts_generated = []

    async def execute(self, input_data, context):
        """Analyze system performance data."""
        cpu_percent = input_data.get("cpu_percent", 0)
        memory_percent = input_data.get("memory_percent", 0)
        disk_usage = input_data.get("disk_usage", 0)
        timestamp = input_data.get("timestamp")

        # Store performance data
        perf_data = {
            "cpu": cpu_percent,
            "memory": memory_percent,
            "disk": disk_usage,
            "timestamp": timestamp
        }
        self.performance_history.append(perf_data)

        # Keep only last 50 readings
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]

        # Analyze performance and generate alerts
        analysis = self._analyze_system_performance(cpu_percent, memory_percent, disk_usage)

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "disk_usage": disk_usage,
            "timestamp": timestamp,
            "analysis": analysis,
            "agent_id": self.id
        }

    def _analyze_system_performance(self, cpu, memory, disk):
        """Analyze system performance and generate alerts."""
        alerts = []
        health_status = "healthy"
        recommendations = []

        # CPU analysis
        if cpu > self.cpu_threshold:
            severity = "critical" if cpu > 90 else "warning"
            alerts.append({
                "type": "high_cpu",
                "severity": severity,
                "message": f"High CPU usage: {cpu:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
            health_status = severity
            recommendations.append("Consider closing unnecessary applications")

        # Memory analysis
        if memory > self.memory_threshold:
            severity = "critical" if memory > 95 else "warning"
            alerts.append({
                "type": "high_memory",
                "severity": severity,
                "message": f"High memory usage: {memory:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
            if health_status != "critical":
                health_status = severity
            recommendations.append("Free up memory by closing applications")

        # Disk analysis
        if disk > 85:
            severity = "critical" if disk > 95 else "warning"
            alerts.append({
                "type": "high_disk",
                "severity": severity,
                "message": f"High disk usage: {disk:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
            if health_status != "critical":
                health_status = severity
            recommendations.append("Clean up disk space")

        # Calculate performance trend
        trend = self._calculate_performance_trend()

        # Store alerts
        self.alerts_generated.extend(alerts)

        return {
            "health_status": health_status,
            "alerts": alerts,
            "recommendations": recommendations,
            "performance_trend": trend,
            "data_points": len(self.performance_history)
        }

    def _calculate_performance_trend(self):
        """Calculate performance trend over time."""
        if len(self.performance_history) < 5:
            return "insufficient_data"

        # Get recent CPU values
        recent_cpu = [p["cpu"] for p in self.performance_history[-5:]]
        cpu_trend = "increasing" if recent_cpu[-1] > recent_cpu[0] else "decreasing"

        # Get recent memory values
        recent_memory = [p["memory"] for p in self.performance_history[-5:]]
        memory_trend = "increasing" if recent_memory[-1] > recent_memory[0] else "decreasing"

        return {
            "cpu": cpu_trend,
            "memory": memory_trend,
            "overall": "degrading" if cpu_trend == "increasing" and memory_trend == "increasing" else "stable"
        }

def get_system_performance():
    """Get current system performance metrics."""
    try:
        # CPU percentage (1 second interval for accuracy)
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory information
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk information
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100

        # Additional system info
        boot_time = psutil.boot_time()
        processes = len(psutil.pids())

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "disk_usage": disk_percent,
            "total_memory_gb": round(memory.total / (1024**3), 2),
            "available_memory_gb": round(memory.available / (1024**3), 2),
            "total_disk_gb": round(disk.total / (1024**3), 2),
            "free_disk_gb": round(disk.free / (1024**3), 2),
            "process_count": processes,
            "uptime_hours": round((time.time() - boot_time) / 3600, 1),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting system performance: {e}")
        return None

async def test_system_health_agent():
    """Test the system health agent with real system data."""
    print("🧪 Testing System Health Agent with Real Data")
    print("=" * 50)

    # Create the agent
    agent = SystemHealthAgent(cpu_threshold=60, memory_threshold=70)  # Lower thresholds for demo

    print("💻 Starting system monitoring...")
    print("   (Monitoring for 30 seconds with 3-second intervals)")

    start_time = time.time()
    iteration = 1

    while time.time() - start_time < 30:  # Monitor for 30 seconds
        print(f"\n🔍 Health Check #{iteration}")

        # Get real system data
        system_data = get_system_performance()

        if system_data:
            # Create execution context
            context = ExecutionContext(agent_id=agent.id)

            # Run the agent
            result = await agent.run(system_data, context)

            if result["status"] == "completed":
                output = result["output"]
                analysis = output["analysis"]

                # Display current metrics
                print(f"   💾 CPU: {output['cpu_percent']:.1f}%")
                print(f"   🧠 Memory: {output['memory_percent']:.1f}%")
                print(f"   💿 Disk: {output['disk_usage']:.1f}%")

                # Show health status
                status_emoji = {
                    "healthy": "✅",
                    "warning": "⚠️",
                    "critical": "🔴"
                }
                emoji = status_emoji.get(analysis["health_status"], "❓")
                print(f"   {emoji} Status: {analysis['health_status'].upper()}")

                # Show alerts
                if analysis["alerts"]:
                    for alert in analysis["alerts"]:
                        severity_emoji = "🔴" if alert["severity"] == "critical" else "⚠️"
                        print(f"   {severity_emoji} {alert['message']}")

                # Show recommendations
                if analysis["recommendations"]:
                    print(f"   💡 Recommendations:")
                    for rec in analysis["recommendations"]:
                        print(f"      • {rec}")

                # Show trend if available
                if analysis["performance_trend"] != "insufficient_data":
                    trend = analysis["performance_trend"]
                    print(f"   📊 Trend: {trend['overall']}")

            else:
                print(f"   ❌ Agent execution failed: {result.get('error', 'Unknown error')}")

        else:
            print("   ❌ Failed to get system data")

        iteration += 1
        await asyncio.sleep(3)  # Wait 3 seconds between checks

    # Show summary
    print(f"\n📊 Monitoring Summary:")
    print(f"   🔍 Total checks: {len(agent.performance_history)}")
    print(f"   🚨 Total alerts: {len(agent.alerts_generated)}")

    if agent.alerts_generated:
        print(f"\n🚨 Alert Summary:")
        alert_types = {}
        for alert in agent.alerts_generated:
            alert_type = alert["type"]
            if alert_type not in alert_types:
                alert_types[alert_type] = 0
            alert_types[alert_type] += 1

        for alert_type, count in alert_types.items():
            print(f"   • {alert_type}: {count} alerts")

async def test_system_stress_simulation():
    """Simulate system stress to trigger alerts."""
    print(f"\n🧪 System Stress Test")
    print("=" * 50)

    agent = SystemHealthAgent(cpu_threshold=50, memory_threshold=60)

    print("⚠️ Simulating high system load...")
    print("   (This will create artificial high CPU/memory usage)")

    # Create some CPU load
    import threading
    import time

    def cpu_stress():
        """Function to create CPU load."""
        end_time = time.time() + 10  # Run for 10 seconds
        while time.time() < end_time:
            # Busy wait to consume CPU
            for _ in range(1000000):
                pass

    # Start CPU stress in background
    stress_thread = threading.Thread(target=cpu_stress)
    stress_thread.daemon = True
    stress_thread.start()

    # Monitor during stress test
    for i in range(5):
        system_data = get_system_performance()

        if system_data:
            context = ExecutionContext(agent_id=agent.id)
            result = await agent.run(system_data, context)

            if result["status"] == "completed":
                output = result["output"]
                analysis = output["analysis"]

                print(f"\n📊 Stress Test Check #{i+1}:")
                print(f"   💾 CPU: {output['cpu_percent']:.1f}%")
                print(f"   🧠 Memory: {output['memory_percent']:.1f}%")

                if analysis["alerts"]:
                    for alert in analysis["alerts"]:
                        print(f"   🚨 {alert['message']}")

        await asyncio.sleep(2)

    print(f"\n✅ Stress test completed")

async def test_system_info_display():
    """Display detailed system information."""
    print(f"\n🧪 System Information Display")
    print("=" * 50)

    system_data = get_system_performance()

    if system_data:
        print(f"💻 System Overview:")
        print(f"   🧠 Total Memory: {system_data['total_memory_gb']} GB")
        print(f"   🧠 Available Memory: {system_data['available_memory_gb']} GB")
        print(f"   💿 Total Disk: {system_data['total_disk_gb']} GB")
        print(f"   💿 Free Disk: {system_data['free_disk_gb']} GB")
        print(f"   🔄 Running Processes: {system_data['process_count']}")
        print(f"   ⏰ System Uptime: {system_data['uptime_hours']} hours")

def main():
    """Run all system monitoring tests."""
    print("💻 System Health Monitoring Agent Test Suite\n")

    async def run_all_tests():
        # Display system info first
        await test_system_info_display()

        # Main monitoring test
        await test_system_health_agent()

        # Optional stress test
        print(f"\n❓ Would you like to run a stress test?")
        print("   This will temporarily increase CPU usage to trigger alerts.")

        # For automation, skip user input in demo
        run_stress = False  # Set to True to enable stress test

        if run_stress:
            await test_system_stress_simulation()
        else:
            print("   Skipping stress test (set run_stress=True to enable)")

        print(f"\n🎉 All system monitoring tests completed!")
        print(f"\nNext steps:")
        print(f"1. Adjust CPU/memory thresholds in the agent")
        print(f"2. Add more sophisticated analysis algorithms")
        print(f"3. Integrate with external monitoring systems")
        print(f"4. Set up alerting via email/Slack/etc.")

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
        print(f"1. Make sure psutil is installed: pip install psutil")
        print(f"2. Run test_framework_import.py first to verify setup")
        print(f"3. Check system permissions for monitoring")
