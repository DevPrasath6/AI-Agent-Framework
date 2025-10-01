#!/usr/bin/env python3
"""
Demonstration: Agent Creation with Agent IDs and Basic Task Execution

This script demonstrates:
1. Creating agents with automatic UUID generation for agent IDs
2. Executing basic tasks with proper agent identification
3. Tracking agent execution with persistent IDs
4. Showing agent status and metadata including IDs
"""

import asyncio
import uuid
from datetime import datetime

from src.core.agent_base import SimpleAgent, AgentCapability
from src.core.execution_context import ExecutionContext


async def demo_agent_creation_with_ids():
    """Demonstrate agent creation with IDs and basic task execution."""
    print("=== AI Agent Framework - Agent ID Demo ===\n")

    # 1. Create agents with automatic ID generation
    print("1. Creating agents with automatic UUID-based agent IDs...")

    # Agent 1: Text processor
    text_agent = SimpleAgent(
        name="text_processor_agent",
        description="Processes text inputs and returns formatted output",
        processor_func=lambda inp, ctx: {
            "processed_text": f"PROCESSED: {inp}",
            "word_count": len(str(inp).split()),
            "processed_at": datetime.now().isoformat(),
            "processed_by": ctx.agent_id
        }
    )

    # Agent 2: Data analyzer
    data_agent = SimpleAgent(
        name="data_analyzer_agent",
        description="Analyzes data and provides insights",
        processor_func=lambda inp, ctx: {
            "analysis": f"Data analysis of: {inp}",
            "insights": ["Pattern detected", "Quality: Good", "Confidence: 85%"],
            "analyzed_at": datetime.now().isoformat(),
            "analyzer_agent_id": ctx.agent_id
        }
    )

    # Agent 3: Custom agent with specific capabilities
    custom_agent = SimpleAgent(
        name="multi_capability_agent",
        description="Agent with multiple capabilities",
        processor_func=lambda inp, ctx: {
            "result": f"Multi-processed: {inp}",
            "capabilities_used": ["text_processing", "data_extraction"],
            "agent_metadata": {
                "id": ctx.agent_id,
                "execution_context": ctx.to_dict()
            }
        }
    )

    agents = [text_agent, data_agent, custom_agent]

    # Display agent information including IDs
    print("Created agents with their IDs:")
    for agent in agents:
        status = agent.get_status()
        print(f"  - Name: {status['name']}")
        print(f"    ID: {status['id']}")
        print(f"    Description: {status['description']}")
        print(f"    Capabilities: {status['capabilities']}")
        print(f"    Status: {status['status']}")
        print()

    # 2. Execute basic tasks with each agent
    print("2. Executing basic tasks with agent ID tracking...")

    tasks = [
        ("Hello World! This is a test message.", text_agent),
        ({"data": [1, 2, 3, 4, 5], "source": "demo"}, data_agent),
        ("Complex multi-step processing task", custom_agent)
    ]

    execution_results = []

    for i, (task_input, agent) in enumerate(tasks, 1):
        print(f"\n--- Task {i}: {agent.name} ---")
        print(f"Agent ID: {agent.id}")
        print(f"Input: {task_input}")

        # Create execution context with agent ID
        context = ExecutionContext(agent_id=agent.id)

        # Execute the task
        result = await agent.run(task_input, context)
        execution_results.append(result)

        print(f"Execution ID: {result['execution_id']}")
        print(f"Status: {result['status']}")
        print(f"Duration: {result['duration']:.3f}s")
        print(f"Agent ID (from result): {result['agent_id']}")
        print(f"Output: {result['output']}")

        # Verify agent ID consistency
        assert result['agent_id'] == agent.id, "Agent ID mismatch!"
        print("✅ Agent ID consistency verified")

    # 3. Demonstrate agent tracking and status
    print("\n3. Agent Status Summary with Execution Metrics...")

    for agent in agents:
        status = agent.get_status()
        print(f"\n--- {status['name']} ---")
        print(f"Agent ID: {status['id']}")
        print(f"Status: {status['status']}")
        print(f"Executions: {status['execution_count']}")
        print(f"Error Rate: {status['error_rate']:.1f}%")
        print(f"Last Executed: {status['last_executed']}")

    # 4. Demonstrate agent ID persistence across multiple executions
    print("\n4. Multiple executions with same agent ID...")

    # Execute multiple tasks with the same agent
    multi_execution_agent = text_agent
    original_agent_id = multi_execution_agent.id

    for i in range(3):
        result = await multi_execution_agent.run(f"Task {i+1} execution", ExecutionContext(agent_id=original_agent_id))
        print(f"Execution {i+1}: Agent ID = {result['agent_id']} (consistent: {result['agent_id'] == original_agent_id})")

        # Verify the agent ID remains the same
        assert result['agent_id'] == original_agent_id, f"Agent ID changed during execution {i+1}!"

    print("\n✅ All agent ID consistency checks passed!")

    # 5. Return summary
    summary = {
        "total_agents_created": len(agents),
        "total_executions": sum(agent.execution_count for agent in agents),
        "agent_ids": [agent.id for agent in agents],
        "execution_results": execution_results,
        "success_rate": "100%"
    }

    print(f"\n=== Demo Summary ===")
    print(f"Agents created: {summary['total_agents_created']}")
    print(f"Total executions: {summary['total_executions']}")
    print(f"Success rate: {summary['success_rate']}")
    print(f"All agent IDs: {summary['agent_ids']}")

    return summary


if __name__ == "__main__":
    # Run the demonstration
    summary = asyncio.run(demo_agent_creation_with_ids())
    print(f"\n🎉 Demo completed successfully! Framework can create agents with IDs and execute basic tasks.")
