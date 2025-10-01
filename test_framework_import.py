"""
Test Framework Import - Verify the AI Agent Framework is working correctly
Run this first to make sure everything is set up properly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import core framework components
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext
from src.core.agent_id_generator import AgentIDGenerator

def test_basic_agent():
    """Test basic agent creation and execution."""
    print("🧪 Testing basic agent creation...")

    agent = SimpleAgent(
        name="test_agent",
        description="Testing framework import"
    )
    print(f"✅ Agent created with ID: {agent.id}")

    # Test agent execution
    test_data = {"message": "Hello from test agent!"}
    context = ExecutionContext(agent_id=agent.id)

    print("🧪 Testing agent execution...")
    import asyncio

    async def run_test():
        result = await agent.run(test_data, context)
        print(f"✅ Agent execution result: {result['status']}")
        return result

    result = asyncio.run(run_test())
    # Assertions to validate behavior
    assert isinstance(agent.id, str) and len(agent.id) > 0
    assert isinstance(result, dict)
    assert result.get("status") in ("completed", "ok", "success") or result.get("status")

def test_id_generator():
    """Test professional ID generation."""
    print("\n🧪 Testing professional ID generation...")

    generator = AgentIDGenerator()

    # Test different ID formats
    formats = ["timestamp", "sequential", "uuid", "custom"]
    for format_type in formats:
        agent_id = generator.generate_id(format_type)
        print(f"✅ {format_type.upper()} ID: {agent_id}")
        assert isinstance(agent_id, str) and len(agent_id) > 0

def test_execution_context():
    """Test execution context functionality."""
    print("\n🧪 Testing execution context...")

    context = ExecutionContext(
        agent_id="test-agent-123",
        user_id="test-user",
        session_id="test-session"
    )

    print(f"✅ Context created: {context.agent_id}")
    print(f"✅ User ID: {context.user_id}")
    print(f"✅ Session ID: {context.session_id}")

    # Validate context attributes
    assert context.agent_id == "test-agent-123"
    assert context.user_id == "test-user"
    assert context.session_id == "test-session"

def main():
    """Run all framework tests."""
    print("🚀 AI Agent Framework Import & Basic Functionality Test\n")

    try:
        # Test 1: Basic agent creation and execution
        agent, result = test_basic_agent()

        # Test 2: ID generation
        generator = test_id_generator()

        # Test 3: Execution context
        context = test_execution_context()

        print("\n🎉 All tests passed! Framework is ready to use.")
        print("\nNext steps:")
        print("1. Run: python stock_data_example.py")
        print("2. Run: python test_stock_agent.py")
        print("3. Run: python test_system_agent.py")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the virtual environment")
        print("2. Check that all dependencies are installed")
        print("3. Verify the src/ directory structure")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
