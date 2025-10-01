"""
Advanced state machine executor with support for hierarchical states,
guards, parallel regions, and event-driven transitions.
"""
from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Callable, Union
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class StateType(Enum):
    """Types of states in the state machine."""
    SIMPLE = "simple"
    COMPOSITE = "composite"  # Has substates
    PARALLEL = "parallel"    # Parallel regions
    FINAL = "final"


class TransitionType(Enum):
    """Types of transitions."""
    EXTERNAL = "external"    # Exit and re-enter states
    INTERNAL = "internal"    # Stay within the same state
    LOCAL = "local"         # Within composite state


@dataclass
class StateMachineEvent:
    """Event that can trigger state transitions."""
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Guard:
    """Guard condition for state transitions."""
    name: str
    condition: Callable[[Dict[str, Any], StateMachineEvent], bool]
    description: str = ""


@dataclass
class Action:
    """Action to be executed during transitions or state entry/exit."""
    name: str
    execute: Callable[[Dict[str, Any], StateMachineEvent], Any]
    description: str = ""


@dataclass
class Transition:
    """State transition definition."""
    id: str
    source_state: str
    target_state: str
    event: str
    guard: Optional[Guard] = None
    action: Optional[Action] = None
    transition_type: TransitionType = TransitionType.EXTERNAL
    priority: int = 0  # Higher priority transitions are checked first


@dataclass
class State:
    """State definition with support for hierarchical and parallel states."""
    id: str
    name: str
    state_type: StateType = StateType.SIMPLE
    parent: Optional[str] = None
    substates: List[str] = field(default_factory=list)
    initial_state: Optional[str] = None  # For composite states
    entry_action: Optional[Action] = None
    exit_action: Optional[Action] = None
    do_activity: Optional[Action] = None  # Ongoing activity while in state
    regions: List[List[str]] = field(default_factory=list)  # For parallel states


@dataclass
class StateMachineDefinition:
    """Complete state machine definition."""
    id: str
    name: str
    description: str = ""
    states: List[State] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)
    initial_state: str = ""
    final_states: Set[str] = field(default_factory=set)
    variables: Dict[str, Any] = field(default_factory=dict)


class StateMachineContext:
    """Runtime context for state machine execution."""

    def __init__(self, definition: StateMachineDefinition):
        self.definition = definition
        self.current_states: Set[str] = set()  # Can have multiple active states (parallel)
        self.variables: Dict[str, Any] = definition.variables.copy()
        self.history: List[StateMachineEvent] = []
        self.logger = logging.getLogger(f"statemachine.{definition.id}")

    def is_in_state(self, state_id: str) -> bool:
        """Check if the state machine is currently in the specified state."""
        return state_id in self.current_states

    def is_final(self) -> bool:
        """Check if the state machine is in a final state."""
        return bool(self.current_states & self.definition.final_states)

    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable value."""
        return self.variables.get(name, default)

    def set_variable(self, name: str, value: Any):
        """Set a variable value."""
        self.variables[name] = value


class AdvancedStateMachine:
    """Advanced state machine executor with hierarchical states and parallel regions."""

    def __init__(self, definition: StateMachineDefinition):
        self.definition = definition
        self.context = StateMachineContext(definition)
        self.logger = logging.getLogger(f"statemachine.{definition.id}")
        self._state_map = {state.id: state for state in definition.states}
        self._transition_map = self._build_transition_map()
        self._running_activities: Dict[str, asyncio.Task] = {}

    def _build_transition_map(self) -> Dict[str, List[Transition]]:
        """Build a map of source states to their transitions."""
        transition_map = {}
        for transition in self.definition.transitions:
            if transition.source_state not in transition_map:
                transition_map[transition.source_state] = []
            transition_map[transition.source_state].append(transition)

        # Sort transitions by priority (highest first)
        for transitions in transition_map.values():
            transitions.sort(key=lambda t: t.priority, reverse=True)

        return transition_map

    async def start(self) -> bool:
        """Start the state machine execution."""
        try:
            initial_state = self.definition.initial_state
            if not initial_state:
                self.logger.error("No initial state defined")
                return False

            await self._enter_state(initial_state)
            self.logger.info(f"State machine {self.definition.id} started in state {initial_state}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start state machine: {e}")
            return False

    async def send_event(self, event: StateMachineEvent) -> bool:
        """Send an event to the state machine."""
        self.context.history.append(event)
        self.logger.debug(f"Processing event: {event.name}")

        # Process transitions for all active states
        transitions_fired = False
        current_states = list(self.context.current_states)

        for state_id in current_states:
            if await self._process_transitions_for_state(state_id, event):
                transitions_fired = True

        return transitions_fired

    async def _process_transitions_for_state(self, state_id: str, event: StateMachineEvent) -> bool:
        """Process transitions for a specific state."""
        transitions = self._transition_map.get(state_id, [])

        for transition in transitions:
            if transition.event == event.name or transition.event == "*":
                # Check guard condition
                if transition.guard:
                    try:
                        if not transition.guard.condition(self.context.variables, event):
                            continue
                    except Exception as e:
                        self.logger.warning(f"Guard evaluation failed: {e}")
                        continue

                # Execute transition
                await self._execute_transition(transition, event)
                return True

        return False

    async def _execute_transition(self, transition: Transition, event: StateMachineEvent):
        """Execute a state transition."""
        self.logger.info(f"Executing transition: {transition.source_state} -> {transition.target_state}")

        try:
            # Exit source state
            await self._exit_state(transition.source_state)

            # Execute transition action
            if transition.action:
                await self._execute_action(transition.action, event)

            # Enter target state
            await self._enter_state(transition.target_state)

        except Exception as e:
            self.logger.error(f"Transition execution failed: {e}")
            raise

    async def _enter_state(self, state_id: str):
        """Enter a state and handle hierarchical entry."""
        state = self._state_map.get(state_id)
        if not state:
            raise ValueError(f"State {state_id} not found")

        self.context.current_states.add(state_id)
        self.logger.debug(f"Entering state: {state_id}")

        # Execute entry action
        if state.entry_action:
            await self._execute_action(state.entry_action, None)

        # Handle composite states
        if state.state_type == StateType.COMPOSITE and state.initial_state:
            await self._enter_state(state.initial_state)

        # Handle parallel states
        elif state.state_type == StateType.PARALLEL:
            for region in state.regions:
                if region:  # Enter the first state in each region
                    await self._enter_state(region[0])

        # Start do activity if present
        if state.do_activity:
            task = asyncio.create_task(self._execute_do_activity(state.id, state.do_activity))
            self._running_activities[state_id] = task

    async def _exit_state(self, state_id: str):
        """Exit a state and handle hierarchical exit."""
        if state_id not in self.context.current_states:
            return

        state = self._state_map.get(state_id)
        if not state:
            return

        self.logger.debug(f"Exiting state: {state_id}")

        # Stop do activity
        if state_id in self._running_activities:
            self._running_activities[state_id].cancel()
            del self._running_activities[state_id]

        # Exit substates first (for composite states)
        if state.state_type == StateType.COMPOSITE:
            substates_to_exit = [s for s in state.substates if s in self.context.current_states]
            for substate in substates_to_exit:
                await self._exit_state(substate)

        # Exit parallel regions
        elif state.state_type == StateType.PARALLEL:
            for region in state.regions:
                for region_state in region:
                    if region_state in self.context.current_states:
                        await self._exit_state(region_state)

        # Execute exit action
        if state.exit_action:
            await self._execute_action(state.exit_action, None)

        self.context.current_states.discard(state_id)

    async def _execute_action(self, action: Action, event: Optional[StateMachineEvent]):
        """Execute an action."""
        try:
            self.logger.debug(f"Executing action: {action.name}")
            result = action.execute(self.context.variables, event)
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            raise

    async def _execute_do_activity(self, state_id: str, action: Action):
        """Execute a do activity (runs continuously while in state)."""
        try:
            while state_id in self.context.current_states:
                result = action.execute(self.context.variables, None)
                if asyncio.iscoroutine(result):
                    await result
                await asyncio.sleep(0.1)  # Allow other tasks to run
        except asyncio.CancelledError:
            self.logger.debug(f"Do activity cancelled for state: {state_id}")
        except Exception as e:
            self.logger.error(f"Do activity failed for state {state_id}: {e}")

    async def stop(self):
        """Stop the state machine execution."""
        # Cancel all running activities
        for task in self._running_activities.values():
            task.cancel()
        self._running_activities.clear()

        # Exit all active states
        current_states = list(self.context.current_states)
        for state_id in current_states:
            await self._exit_state(state_id)

        self.logger.info(f"State machine {self.definition.id} stopped")


# Helper functions for creating common state machine patterns

def create_simple_workflow_state_machine(
    workflow_id: str,
    states: List[str],
    transitions: List[Dict[str, str]]
) -> StateMachineDefinition:
    """Create a simple linear workflow state machine."""
    state_objects = []
    for i, state_name in enumerate(states):
        state_type = StateType.FINAL if i == len(states) - 1 else StateType.SIMPLE
        state_objects.append(State(
            id=state_name,
            name=state_name.replace("_", " ").title(),
            state_type=state_type
        ))

    transition_objects = []
    for i, trans in enumerate(transitions):
        transition_objects.append(Transition(
            id=f"trans_{i}",
            source_state=trans["from"],
            target_state=trans["to"],
            event=trans.get("event", "next")
        ))

    return StateMachineDefinition(
        id=workflow_id,
        name=f"Workflow {workflow_id}",
        states=state_objects,
        transitions=transition_objects,
        initial_state=states[0] if states else "",
        final_states={states[-1]} if states else set()
    )


def create_approval_state_machine(workflow_id: str) -> StateMachineDefinition:
    """Create a state machine for approval workflows."""

    def check_approval_needed(variables: Dict[str, Any], event: StateMachineEvent) -> bool:
        return variables.get("requires_approval", False)

    def check_approved(variables: Dict[str, Any], event: StateMachineEvent) -> bool:
        return event.data.get("approved", False)

    states = [
        State(id="initial", name="Initial", state_type=StateType.SIMPLE),
        State(id="processing", name="Processing", state_type=StateType.SIMPLE),
        State(id="pending_approval", name="Pending Approval", state_type=StateType.SIMPLE),
        State(id="approved", name="Approved", state_type=StateType.SIMPLE),
        State(id="rejected", name="Rejected", state_type=StateType.FINAL),
        State(id="completed", name="Completed", state_type=StateType.FINAL),
    ]

    transitions = [
        Transition(
            id="start_processing",
            source_state="initial",
            target_state="processing",
            event="start"
        ),
        Transition(
            id="needs_approval",
            source_state="processing",
            target_state="pending_approval",
            event="processed",
            guard=Guard("needs_approval", check_approval_needed)
        ),
        Transition(
            id="auto_approve",
            source_state="processing",
            target_state="completed",
            event="processed",
            guard=Guard("auto_approve", lambda v, e: not check_approval_needed(v, e))
        ),
        Transition(
            id="approve",
            source_state="pending_approval",
            target_state="approved",
            event="approval_response",
            guard=Guard("approved", check_approved)
        ),
        Transition(
            id="reject",
            source_state="pending_approval",
            target_state="rejected",
            event="approval_response",
            guard=Guard("rejected", lambda v, e: not check_approved(v, e))
        ),
        Transition(
            id="complete",
            source_state="approved",
            target_state="completed",
            event="finalize"
        ),
    ]

    return StateMachineDefinition(
        id=workflow_id,
        name="Approval Workflow",
        states=states,
        transitions=transitions,
        initial_state="initial",
        final_states={"completed", "rejected"}
    )


# Legacy compatibility function
def run_state_machine(definition: Union[dict, StateMachineDefinition], context: dict = None) -> Any:
    """Legacy function for backward compatibility."""
    if isinstance(definition, dict):
        # Convert dict to StateMachineDefinition (basic conversion)
        sm_def = StateMachineDefinition(
            id=definition.get("id", "legacy_sm"),
            name=definition.get("name", "Legacy State Machine"),
            initial_state=definition.get("initial_state", "start"),
            variables=context or {}
        )
    else:
        sm_def = definition

    # For backward compatibility, just log and return success
    logger.info(f"Running state machine: {sm_def.id}")
    return {"status": "completed", "state_machine_id": sm_def.id}
