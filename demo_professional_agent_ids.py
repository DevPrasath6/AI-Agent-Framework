#!/usr/bin/env python3
"""
Professional Agent ID System Demonstration

This script demonstrates the enhanced professional agent ID generation system with:
1. Unique, ordered, and readable agent IDs
2. Multiple ID generation strategies
3. Professional formatting with timestamps and sequences
4. Thread-safe generation
5. ID parsing and validation capabilities
"""

import asyncio
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from src.core.agent_base import SimpleAgent
from src.core.agent_id_generator import (
    AgentIDGenerator,
    SequentialAgentIDGenerator,
    HierarchicalAgentIDGenerator,
    generate_professional_agent_id,
    parse_agent_id,
    is_valid_agent_id
)
from src.core.execution_context import ExecutionContext


def demonstrate_id_generators():
    """Demonstrate different agent ID generation strategies."""
    print("=== Professional Agent ID Generation System ===\n")

    # 1. Professional ID Generator (Default)
    print("1. Professional Agent IDs (Default)")
    print("Format: AGENT-YYYYMMDD-HHMMSS-NNNN-XXXX")

    professional_ids = []
    for i in range(5):
        agent_id = generate_professional_agent_id(
            agent_name=f"test_agent_{i}",
            metadata={"type": "demo", "index": i}
        )
        professional_ids.append(agent_id)
        print(f"  {agent_id}")

        # Parse the ID
        parsed = parse_agent_id(agent_id)
        if parsed["is_valid"]:
            print(f"    → Created: {parsed['created_at']}, Sequence: {parsed['sequence']}")

        time.sleep(0.01)  # Small delay to ensure different timestamps

    print()

    # 2. Sequential ID Generator
    print("2. Sequential Agent IDs")
    print("Format: AGT_YYYYMMDD_NNNNNN")

    sequential_gen = SequentialAgentIDGenerator()
    for i in range(5):
        agent_id = sequential_gen.generate_id()
        print(f"  {agent_id}")

    print()

    # 3. Hierarchical ID Generator
    print("3. Hierarchical Agent IDs")
    print("Format: ORG-DEPT-TEAM-TYPE-NNNN")

    # Different organizational structures
    systems = [
        ("PROD", "AI", "WORKFLOW", "PROCESSOR"),
        ("PROD", "AI", "ANALYSIS", "CLASSIFIER"),
        ("DEV", "ML", "TRAINING", "OPTIMIZER"),
        ("TEST", "QA", "VALIDATION", "CHECKER"),
    ]

    for org, dept, team, agent_type in systems:
        hier_gen = HierarchicalAgentIDGenerator(org, dept, team)
        agent_id = hier_gen.generate_id(agent_type)
        print(f"  {agent_id}")

    print()
    return professional_ids


async def demonstrate_agent_creation():
    """Demonstrate professional agent creation with different ID types."""
    print("4. Agent Creation with Professional IDs")

    # Create agents with different ID generation strategies
    agents = []

    # Professional ID agent
    agent1 = SimpleAgent(
        name="professional_text_processor",
        description="Agent with professional ID format",
        id_generator_type="professional",
        processor_func=lambda inp, ctx: {
            "processed": f"PROFESSIONAL: {inp}",
            "agent_id": ctx.agent_id,
            "timestamp": datetime.now().isoformat()
        }
    )

    # Sequential ID agent
    agent2 = SimpleAgent(
        name="sequential_data_analyzer",
        description="Agent with sequential ID format",
        id_generator_type="sequential",
        processor_func=lambda inp, ctx: {
            "analyzed": f"SEQUENTIAL: {inp}",
            "agent_id": ctx.agent_id,
            "analysis_complete": True
        }
    )

    # Hierarchical ID agent
    agent3 = SimpleAgent(
        name="hierarchical_workflow_manager",
        description="Agent with hierarchical ID format",
        id_generator_type="hierarchical",
        processor_func=lambda inp, ctx: {
            "managed": f"HIERARCHICAL: {inp}",
            "agent_id": ctx.agent_id,
            "workflow_status": "active"
        }
    )

    agents = [agent1, agent2, agent3]

    # Display agent information
    for agent in agents:
        status = agent.get_status()
        print(f"\n--- {status['name']} ---")
        print(f"ID: {status['id']}")
        print(f"ID Valid: {is_valid_agent_id(status['id'])}")
        print(f"Description: {status['description']}")

        # Parse professional IDs
        if status['id'].startswith('AGENT-'):
            parsed = parse_agent_id(status['id'])
            if parsed['is_valid']:
                print(f"Created: {parsed['created_at']}")
                print(f"Sequence: {parsed['sequence']}")

    print()

    # Execute tasks to demonstrate ID tracking
    print("5. Task Execution with ID Tracking")

    tasks = [
        ("Process customer inquiry", agent1),
        ({"data": [1, 2, 3], "metrics": True}, agent2),
        ("Orchestrate multi-step workflow", agent3)
    ]

    for i, (task_input, agent) in enumerate(tasks, 1):
        print(f"\n--- Task {i}: {agent.name} ---")
        print(f"Agent ID: {agent.id}")

        # Execute the task
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run(task_input, context)

        print(f"Execution ID: {result['execution_id']}")
        print(f"Status: {result['status']}")
        print(f"Agent ID (result): {result['agent_id']}")
        print(f"Output: {result['output']}")

        # Verify ID consistency
        assert result['agent_id'] == agent.id, "Agent ID mismatch!"
        print("✅ Agent ID consistency verified")

    return agents


def demonstrate_thread_safety():
    """Demonstrate thread-safe agent ID generation."""
    print("\n6. Thread-Safe ID Generation")
    print("Creating 20 agents concurrently across 4 threads...")

    def create_agent_batch(batch_id):
        """Create a batch of agents in a thread."""
        agents = []
        for i in range(5):
            agent = SimpleAgent(
                name=f"thread_{batch_id}_agent_{i}",
                description=f"Agent {i} from thread batch {batch_id}",
                id_generator_type="professional"
            )
            agents.append(agent)
        return agents

    # Create agents concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(create_agent_batch, i) for i in range(4)]
        all_agents = []
        for future in futures:
            batch_agents = future.result()
            all_agents.extend(batch_agents)

    # Verify all IDs are unique
    agent_ids = [agent.id for agent in all_agents]
    unique_ids = set(agent_ids)

    print(f"Created agents: {len(all_agents)}")
    print(f"Unique IDs: {len(unique_ids)}")
    print(f"ID uniqueness: {len(unique_ids) == len(all_agents)}")

    # Show first few IDs to demonstrate ordering
    print("\nFirst 10 agent IDs (showing ordering):")
    for i, agent_id in enumerate(sorted(agent_ids)[:10]):
        print(f"  {i+1:2d}. {agent_id}")

    assert len(unique_ids) == len(all_agents), "Duplicate agent IDs detected!"
    print("✅ All agent IDs are unique")

    return all_agents


def demonstrate_id_validation():
    """Demonstrate agent ID validation and parsing."""
    print("\n7. Agent ID Validation and Parsing")

    # Test various ID formats
    test_ids = [
        "AGENT-20251001-143052-0001-A7B3",  # Valid professional
        "AGT_20251001_000042",               # Valid sequential
        "PROD-AI-WORKFLOW-PROCESSOR-0001",  # Valid hierarchical
        "invalid-id-format",                # Invalid
        "AGENT-20251001-143052-0001",       # Incomplete professional
        "",                                 # Empty
        "AGENT-20251001-143052-0001-A7B3-EXTRA"  # Too many parts
    ]

    print("Validating different ID formats:")
    for test_id in test_ids:
        is_valid = is_valid_agent_id(test_id)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"  {test_id:<35} → {status}")

        if is_valid:
            parsed = parse_agent_id(test_id)
            if parsed.get('created_at'):
                print(f"    Created: {parsed['created_at']}")


async def main():
    """Run the complete professional agent ID demonstration."""
    print("🚀 Starting Professional Agent ID System Demonstration\n")

    # Run all demonstrations
    professional_ids = demonstrate_id_generators()
    agents = await demonstrate_agent_creation()
    concurrent_agents = demonstrate_thread_safety()
    demonstrate_id_validation()

    # Final summary
    total_agents = len(agents) + len(concurrent_agents)
    all_ids = [agent.id for agent in agents + concurrent_agents] + professional_ids

    print(f"\n=== Demonstration Summary ===")
    print(f"Total agents created: {total_agents}")
    print(f"Total IDs generated: {len(all_ids)}")
    print(f"All IDs unique: {len(set(all_ids)) == len(all_ids)}")
    print(f"ID formats demonstrated: Professional, Sequential, Hierarchical")
    print(f"Thread safety: ✅ Verified")
    print(f"ID validation: ✅ Implemented")
    print(f"ID parsing: ✅ Available")

    print(f"\n🎉 Professional Agent ID System demonstration completed successfully!")
    print(f"The framework now supports professional, unique, and ordered agent IDs!")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
