"""
Policy checking and guardrails for agent execution.
"""

import re
import logging
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class PolicyType(Enum):
    """Types of policies that can be enforced."""

    CONTENT_FILTER = "content_filter"
    DATA_PRIVACY = "data_privacy"
    RATE_LIMIT = "rate_limit"
    RESOURCE_LIMIT = "resource_limit"
    SECURITY = "security"
    CUSTOM = "custom"


@dataclass
class PolicyResult:
    """Result of a policy check."""

    allowed: bool
    policy_type: PolicyType
    reason: str
    details: Optional[Dict[str, Any]] = None


class PolicyRule:
    """Base class for policy rules."""

    def __init__(self, name: str, policy_type: PolicyType, enabled: bool = True):
        self.name = name
        self.policy_type = policy_type
        self.enabled = enabled

    def check(self, data: Any, context: Dict[str, Any] = None) -> PolicyResult:
        """Check if data passes this policy rule."""
        if not self.enabled:
            return PolicyResult(True, self.policy_type, "Policy disabled")

        return self._evaluate(data, context or {})

    def _evaluate(self, data: Any, context: Dict[str, Any]) -> PolicyResult:
        """Override this method to implement policy logic."""
        return PolicyResult(True, self.policy_type, "No evaluation implemented")


class ContentFilterRule(PolicyRule):
    """Content filtering policy rule."""

    def __init__(
        self,
        name: str = "content_filter",
        blocked_patterns: List[str] = None,
        blocked_words: List[str] = None,
        max_length: Optional[int] = None,
    ):
        super().__init__(name, PolicyType.CONTENT_FILTER)
        self.blocked_patterns = blocked_patterns or []
        self.blocked_words = blocked_words or []
        self.max_length = max_length

    def _evaluate(self, data: Any, context: Dict[str, Any]) -> PolicyResult:
        """Evaluate content filtering rules."""
        text_data = str(data).lower()

        # Check length limits
        if self.max_length and len(text_data) > self.max_length:
            return PolicyResult(
                False,
                PolicyType.CONTENT_FILTER,
                f"Content exceeds maximum length of {self.max_length} characters",
                {"length": len(text_data), "max_length": self.max_length},
            )

        # Check blocked words
        for word in self.blocked_words:
            if word.lower() in text_data:
                return PolicyResult(
                    False,
                    PolicyType.CONTENT_FILTER,
                    f"Content contains blocked word: {word}",
                    {"blocked_word": word},
                )

        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text_data, re.IGNORECASE):
                return PolicyResult(
                    False,
                    PolicyType.CONTENT_FILTER,
                    f"Content matches blocked pattern: {pattern}",
                    {"blocked_pattern": pattern},
                )

        return PolicyResult(True, PolicyType.CONTENT_FILTER, "Content passed filtering")


class DataPrivacyRule(PolicyRule):
    """Data privacy policy rule."""

    def __init__(
        self,
        name: str = "data_privacy",
        pii_patterns: List[str] = None,
        sensitive_fields: List[str] = None,
    ):
        super().__init__(name, PolicyType.DATA_PRIVACY)
        self.pii_patterns = pii_patterns or [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card pattern
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email pattern
        ]
        self.sensitive_fields = sensitive_fields or ["password", "ssn", "credit_card"]

    def _evaluate(self, data: Any, context: Dict[str, Any]) -> PolicyResult:
        """Evaluate data privacy rules."""
        text_data = str(data)

        # Check for PII patterns
        for pattern in self.pii_patterns:
            if re.search(pattern, text_data):
                return PolicyResult(
                    False,
                    PolicyType.DATA_PRIVACY,
                    f"Data contains potential PII matching pattern: {pattern}",
                    {"detected_pattern": pattern},
                )

        # Check for sensitive fields if data is a dict
        if isinstance(data, dict):
            for field in self.sensitive_fields:
                if any(field.lower() in key.lower() for key in data.keys()):
                    return PolicyResult(
                        False,
                        PolicyType.DATA_PRIVACY,
                        f"Data contains sensitive field: {field}",
                        {"sensitive_field": field},
                    )

        return PolicyResult(
            True, PolicyType.DATA_PRIVACY, "No privacy violations detected"
        )


class RateLimitRule(PolicyRule):
    """Rate limiting policy rule."""

    def __init__(
        self,
        name: str = "rate_limit",
        max_requests_per_minute: int = 60,
        max_requests_per_hour: int = 1000,
    ):
        super().__init__(name, PolicyType.RATE_LIMIT)
        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_hour = max_requests_per_hour
        # In a real implementation, this would track actual request counts
        # For now, we'll just allow all requests

    def _evaluate(self, data: Any, context: Dict[str, Any]) -> PolicyResult:
        """Evaluate rate limiting rules."""
        # This is a simplified implementation
        # In practice, you'd track actual request counts with Redis or similar
        agent_id = context.get("agent_id", "unknown")

        # For demonstration, we'll always allow requests
        # Real implementation would check actual rate limits
        return PolicyResult(True, PolicyType.RATE_LIMIT, "Rate limit check passed")


class PolicyChecker:
    """
    Main policy checker that enforces rules and guardrails.
    """

    def __init__(self, rules: List[PolicyRule] = None):
        """
        Initialize policy checker.

        Args:
            rules: List of policy rules to enforce
        """
        self.rules = rules or self._get_default_rules()
        self.logger = logging.getLogger("policy_checker")

    def _get_default_rules(self) -> List[PolicyRule]:
        """Get default policy rules."""
        return [
            ContentFilterRule(
                blocked_words=["hack", "exploit", "malware"], max_length=10000
            ),
            DataPrivacyRule(),
            RateLimitRule(),
        ]

    async def check_input(
        self, data: Any, context: Dict[str, Any] = None
    ) -> PolicyResult:
        """Check input data against all policies."""
        return await self._check_policies(data, context or {}, "input")

    async def check_output(
        self, data: Any, context: Dict[str, Any] = None
    ) -> PolicyResult:
        """Check output data against all policies."""
        return await self._check_policies(data, context or {}, "output")

    async def _check_policies(
        self, data: Any, context: Dict[str, Any], check_type: str
    ) -> PolicyResult:
        """Check data against all enabled policy rules."""
        context = {**context, "check_type": check_type}

        for rule in self.rules:
            if not rule.enabled:
                continue

            try:
                result = rule.check(data, context)
                if not result.allowed:
                    self.logger.warning(
                        f"Policy violation in {check_type}: {result.reason}",
                        extra={
                            "rule_name": rule.name,
                            "policy_type": result.policy_type.value,
                            "check_type": check_type,
                            "details": result.details,
                        },
                    )
                    return result
            except Exception as e:
                self.logger.error(f"Error checking policy rule {rule.name}: {e}")
                # Continue checking other rules even if one fails

        return PolicyResult(
            True, PolicyType.CUSTOM, f"All {check_type} policies passed"
        )

    def add_rule(self, rule: PolicyRule) -> None:
        """Add a new policy rule."""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove a policy rule by name."""
        original_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        return len(self.rules) < original_count

    def enable_rule(self, rule_name: str) -> bool:
        """Enable a policy rule by name."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = True
                return True
        return False

    def disable_rule(self, rule_name: str) -> bool:
        """Disable a policy rule by name."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = False
                return True
        return False

    def get_rules(self) -> List[Dict[str, Any]]:
        """Get information about all policy rules."""
        return [
            {"name": rule.name, "type": rule.policy_type.value, "enabled": rule.enabled}
            for rule in self.rules
        ]


# Legacy function for compatibility
def check_policy(action: str, ctx: Dict[str, Any]) -> bool:
    """Legacy policy check function for backward compatibility."""
    logger = logging.getLogger("policy.legacy")
    logger.info(f"Legacy policy check - Action: {action}, Context: {ctx}")
    return True
