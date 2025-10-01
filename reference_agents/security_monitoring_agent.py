"""
Security Monitoring Agent - Advanced Reference Implementation

This agent demonstrates sophisticated security monitoring capabilities including:
- Real-time threat detection and analysis
- Security event correlation and alerting
- Compliance monitoring and reporting
- Vulnerability assessment and recommendations
- Incident response automation
"""

import asyncio
import json
import hashlib
import ipaddress
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging
import re

from src.core.agent_base import AgentBase, AgentCapability
from src.core.execution_context import ExecutionContext
from src.tools.llm_tools import get_llm_client

logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Security threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityEventType(Enum):
    """Types of security events."""
    AUTHENTICATION_FAILURE = "auth_failure"
    SUSPICIOUS_LOGIN = "suspicious_login"
    MALWARE_DETECTION = "malware_detection"
    NETWORK_INTRUSION = "network_intrusion"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    COMPLIANCE_VIOLATION = "compliance_violation"
    VULNERABILITY_DETECTED = "vulnerability_detected"
    ANOMALOUS_BEHAVIOR = "anomalous_behavior"

@dataclass
class SecurityEvent:
    """Security event data structure."""
    event_id: str
    event_type: SecurityEventType
    threat_level: ThreatLevel
    timestamp: datetime
    source_ip: str
    user_id: Optional[str]
    description: str
    details: Dict[str, Any]
    affected_systems: List[str]
    recommendations: List[str]

@dataclass
class SecurityAssessment:
    """Security assessment result."""
    overall_risk_score: float
    threat_summary: Dict[str, int]
    critical_issues: List[SecurityEvent]
    recommendations: List[str]
    compliance_status: Dict[str, bool]
    next_actions: List[str]

class SecurityMonitoringAgent(AgentBase):
    """
    Professional security monitoring agent for comprehensive threat detection.

    Capabilities:
    - Real-time security event analysis
    - Threat intelligence correlation
    - Compliance monitoring (SOC2, GDPR, HIPAA)
    - Incident response automation
    - Vulnerability assessment
    - Security metrics and reporting
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="security_monitoring_agent",
            description="Advanced security monitoring and threat detection agent",
            capabilities=[
                AgentCapability.SECURITY_MONITORING,
                AgentCapability.DATA_ANALYSIS,
                AgentCapability.TEXT_PROCESSING,
                AgentCapability.API_INTEGRATION
            ],
            **kwargs
        )
        self.llm_client = get_llm_client()
        self.security_events = []
        self.threat_intelligence = self._initialize_threat_intelligence()
        self.compliance_rules = self._initialize_compliance_rules()
        self.known_threats = set()

    async def execute(self, input_data: Dict[str, Any], context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute security monitoring and analysis.

        Args:
            input_data: Dictionary containing:
                - event_data: Security events or logs to analyze
                - analysis_type: Type of security analysis to perform
                - config: Analysis configuration options
            context: Execution context

        Returns:
            Security analysis results and recommendations
        """
        try:
            # Extract input parameters
            event_data = input_data.get("event_data", [])
            analysis_type = input_data.get("analysis_type", "threat_detection")
            config = input_data.get("config", {})

            # Perform analysis based on type
            if analysis_type == "threat_detection":
                result = await self._threat_detection_analysis(event_data, config, context)
            elif analysis_type == "compliance_check":
                result = await self._compliance_monitoring(event_data, config, context)
            elif analysis_type == "vulnerability_assessment":
                result = await self._vulnerability_assessment(event_data, config, context)
            elif analysis_type == "incident_response":
                result = await self._incident_response(event_data, config, context)
            elif analysis_type == "security_audit":
                result = await self._security_audit(event_data, config, context)
            else:
                result = await self._comprehensive_security_analysis(event_data, config, context)

            return {
                "security_assessment": result.__dict__ if hasattr(result, '__dict__') else result,
                "metadata": {
                    "analysis_type": analysis_type,
                    "events_processed": len(event_data) if isinstance(event_data, list) else 1,
                    "processing_time": context.elapsed_time,
                    "agent_id": self.id,
                    "timestamp": datetime.now().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Security analysis failed: {str(e)}")
            return {
                "error": f"Security analysis failed: {str(e)}",
                "security_assessment": None,
                "metadata": {"error_type": type(e).__name__}
            }

    def _initialize_threat_intelligence(self) -> Dict[str, Any]:
        """Initialize threat intelligence database."""
        return {
            "malicious_ips": {
                "192.168.1.100",  # Example suspicious IPs
                "10.0.0.50",
                "172.16.0.25"
            },
            "suspicious_user_agents": {
                "sqlmap",
                "nikto",
                "nessus",
                "openvas",
                "burp"
            },
            "malware_signatures": {
                "EICAR-STANDARD-ANTIVIRUS-TEST-FILE",
                "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR",
                "suspicious_powershell_base64"
            },
            "attack_patterns": {
                "sql_injection": [r"union\s+select", r"or\s+1\s*=\s*1", r"drop\s+table"],
                "xss": [r"<script", r"javascript:", r"onerror\s*="],
                "directory_traversal": [r"\.\.\/", r"\.\.\\", r"%2e%2e%2f"],
                "command_injection": [r";\s*ls", r";\s*cat", r"&&\s*whoami"]
            }
        }

    def _initialize_compliance_rules(self) -> Dict[str, Any]:
        """Initialize compliance monitoring rules."""
        return {
            "SOC2": {
                "access_logging": "All system access must be logged",
                "encryption_at_rest": "Sensitive data must be encrypted at rest",
                "encryption_in_transit": "Data transmission must be encrypted",
                "access_controls": "Role-based access controls must be enforced",
                "incident_response": "Security incidents must be documented"
            },
            "GDPR": {
                "data_minimization": "Collect only necessary personal data",
                "right_to_deletion": "Support data deletion requests",
                "breach_notification": "Report breaches within 72 hours",
                "consent_management": "Obtain explicit consent for data processing",
                "data_protection_officer": "Designate data protection officer"
            },
            "HIPAA": {
                "phi_encryption": "Protected health information must be encrypted",
                "access_audit": "All PHI access must be audited",
                "minimum_necessary": "Access only minimum necessary PHI",
                "workforce_training": "Regular security awareness training required",
                "business_associate_agreements": "BAAs required for third parties"
            }
        }

    async def _threat_detection_analysis(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> SecurityAssessment:
        """Analyze events for security threats."""

        security_events = []
        threat_counts = {level.value: 0 for level in ThreatLevel}

        for event in event_data:
            analyzed_event = await self._analyze_security_event(event)
            if analyzed_event:
                security_events.append(analyzed_event)
                threat_counts[analyzed_event.threat_level.value] += 1

        # Calculate overall risk score
        risk_score = self._calculate_risk_score(security_events)

        # Identify critical issues
        critical_issues = [event for event in security_events if event.threat_level == ThreatLevel.CRITICAL]

        # Generate recommendations
        recommendations = await self._generate_security_recommendations(security_events)

        # Check compliance status
        compliance_status = self._check_compliance_status(security_events)

        # Determine next actions
        next_actions = self._determine_next_actions(security_events, critical_issues)

        return SecurityAssessment(
            overall_risk_score=risk_score,
            threat_summary=threat_counts,
            critical_issues=critical_issues,
            recommendations=recommendations,
            compliance_status=compliance_status,
            next_actions=next_actions
        )

    async def _analyze_security_event(self, event: Dict[str, Any]) -> Optional[SecurityEvent]:
        """Analyze individual security event."""
        try:
            # Extract event details
            event_id = event.get("id", f"event_{len(self.security_events) + 1}")
            timestamp = datetime.fromisoformat(event.get("timestamp", datetime.now().isoformat()))
            source_ip = event.get("source_ip", "unknown")
            user_id = event.get("user_id")
            message = event.get("message", "")
            details = event.get("details", {})

            # Detect event type and threat level
            event_type, threat_level = self._classify_security_event(event, message)

            # Generate description and recommendations
            description = await self._generate_event_description(event, event_type)
            recommendations = self._generate_event_recommendations(event_type, threat_level, details)

            # Identify affected systems
            affected_systems = self._identify_affected_systems(event, details)

            security_event = SecurityEvent(
                event_id=event_id,
                event_type=event_type,
                threat_level=threat_level,
                timestamp=timestamp,
                source_ip=source_ip,
                user_id=user_id,
                description=description,
                details=details,
                affected_systems=affected_systems,
                recommendations=recommendations
            )

            # Store for correlation
            self.security_events.append(security_event)

            return security_event

        except Exception as e:
            logger.error(f"Event analysis failed: {str(e)}")
            return None

    def _classify_security_event(self, event: Dict, message: str) -> tuple[SecurityEventType, ThreatLevel]:
        """Classify security event type and threat level."""

        message_lower = message.lower()
        source_ip = event.get("source_ip", "")

        # Check for known malicious IPs
        if source_ip in self.threat_intelligence["malicious_ips"]:
            return SecurityEventType.NETWORK_INTRUSION, ThreatLevel.HIGH

        # Authentication failures
        if any(keyword in message_lower for keyword in ["failed login", "authentication failed", "invalid credentials"]):
            # Multiple failures indicate brute force
            if event.get("details", {}).get("attempt_count", 1) > 5:
                return SecurityEventType.AUTHENTICATION_FAILURE, ThreatLevel.HIGH
            else:
                return SecurityEventType.AUTHENTICATION_FAILURE, ThreatLevel.MEDIUM

        # Suspicious login patterns
        if any(keyword in message_lower for keyword in ["unusual location", "new device", "suspicious login"]):
            return SecurityEventType.SUSPICIOUS_LOGIN, ThreatLevel.MEDIUM

        # Malware detection
        if any(keyword in message_lower for keyword in ["malware", "virus", "trojan", "ransomware"]):
            return SecurityEventType.MALWARE_DETECTION, ThreatLevel.CRITICAL

        # Attack pattern detection
        for attack_type, patterns in self.threat_intelligence["attack_patterns"].items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                if attack_type == "sql_injection":
                    return SecurityEventType.NETWORK_INTRUSION, ThreatLevel.HIGH
                elif attack_type == "xss":
                    return SecurityEventType.NETWORK_INTRUSION, ThreatLevel.MEDIUM
                else:
                    return SecurityEventType.NETWORK_INTRUSION, ThreatLevel.HIGH

        # Data access anomalies
        if any(keyword in message_lower for keyword in ["large data download", "unusual data access", "bulk export"]):
            return SecurityEventType.DATA_EXFILTRATION, ThreatLevel.HIGH

        # Privilege escalation
        if any(keyword in message_lower for keyword in ["privilege escalation", "sudo", "administrator access"]):
            return SecurityEventType.PRIVILEGE_ESCALATION, ThreatLevel.HIGH

        # Default classification
        return SecurityEventType.ANOMALOUS_BEHAVIOR, ThreatLevel.LOW

    async def _generate_event_description(self, event: Dict, event_type: SecurityEventType) -> str:
        """Generate human-readable event description."""
        try:
            context = f"""
            Security Event Analysis:
            Type: {event_type.value}
            Source IP: {event.get('source_ip', 'unknown')}
            User: {event.get('user_id', 'unknown')}
            Message: {event.get('message', '')[:200]}

            Generate a clear, professional description of this security event.
            """

            response = await self.llm_client.chat_completion(
                messages=[{"role": "user", "content": context}],
                max_tokens=150
            )

            return response.get("content", f"Security event of type {event_type.value} detected")

        except Exception as e:
            logger.warning(f"Description generation failed: {str(e)}")
            return f"Security event: {event_type.value} from {event.get('source_ip', 'unknown')}"

    def _generate_event_recommendations(self, event_type: SecurityEventType, threat_level: ThreatLevel, details: Dict) -> List[str]:
        """Generate specific recommendations for the event."""
        recommendations = []

        if event_type == SecurityEventType.AUTHENTICATION_FAILURE:
            recommendations.extend([
                "Monitor for brute force attack patterns",
                "Consider implementing account lockout policies",
                "Review and strengthen password requirements"
            ])

        elif event_type == SecurityEventType.MALWARE_DETECTION:
            recommendations.extend([
                "Immediately isolate affected systems",
                "Run comprehensive malware scan",
                "Update antivirus signatures",
                "Review recent file downloads and email attachments"
            ])

        elif event_type == SecurityEventType.NETWORK_INTRUSION:
            recommendations.extend([
                "Block suspicious IP addresses",
                "Review firewall and IDS rules",
                "Conduct network traffic analysis",
                "Verify system integrity"
            ])

        elif event_type == SecurityEventType.DATA_EXFILTRATION:
            recommendations.extend([
                "Immediately review data access logs",
                "Verify data encryption status",
                "Contact data protection officer",
                "Consider breach notification requirements"
            ])

        elif event_type == SecurityEventType.PRIVILEGE_ESCALATION:
            recommendations.extend([
                "Review user permissions and roles",
                "Audit system administrator accounts",
                "Check for unauthorized privilege changes",
                "Implement principle of least privilege"
            ])

        # Add threat level specific recommendations
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.insert(0, "IMMEDIATE ACTION REQUIRED")
            recommendations.append("Activate incident response procedures")
        elif threat_level == ThreatLevel.HIGH:
            recommendations.append("Escalate to security team")

        return recommendations[:5]  # Limit to 5 recommendations

    def _identify_affected_systems(self, event: Dict, details: Dict) -> List[str]:
        """Identify systems affected by the security event."""
        affected_systems = []

        # Add source system
        if "hostname" in details:
            affected_systems.append(details["hostname"])

        # Add target systems from event details
        if "target_system" in details:
            affected_systems.append(details["target_system"])

        # Extract from message
        message = event.get("message", "")
        # Simple regex to find system names
        system_matches = re.findall(r'\b[a-zA-Z0-9-]+\.(local|com|org|net)\b', message)
        affected_systems.extend(system_matches)

        return list(set(affected_systems))  # Remove duplicates

    def _calculate_risk_score(self, events: List[SecurityEvent]) -> float:
        """Calculate overall security risk score (0-100)."""
        if not events:
            return 0.0

        # Weight by threat level
        weights = {
            ThreatLevel.LOW: 1,
            ThreatLevel.MEDIUM: 3,
            ThreatLevel.HIGH: 7,
            ThreatLevel.CRITICAL: 15
        }

        total_score = sum(weights[event.threat_level] for event in events)

        # Normalize to 0-100 scale
        max_possible_score = len(events) * weights[ThreatLevel.CRITICAL]
        normalized_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0

        return min(normalized_score, 100.0)

    async def _generate_security_recommendations(self, events: List[SecurityEvent]) -> List[str]:
        """Generate overall security recommendations."""
        recommendations = set()

        # Collect all event recommendations
        for event in events:
            recommendations.update(event.recommendations)

        # Add general recommendations based on event patterns
        event_types = [event.event_type for event in events]

        if SecurityEventType.AUTHENTICATION_FAILURE in event_types:
            recommendations.add("Implement multi-factor authentication")

        if SecurityEventType.MALWARE_DETECTION in event_types:
            recommendations.add("Conduct comprehensive security audit")

        if any(level == ThreatLevel.CRITICAL for event in events for level in [event.threat_level]):
            recommendations.add("Activate incident response team")

        # Generate strategic recommendations using LLM
        try:
            context = f"""
            Security Analysis Summary:
            - Total events: {len(events)}
            - Critical events: {sum(1 for e in events if e.threat_level == ThreatLevel.CRITICAL)}
            - Event types: {list(set(e.event_type.value for e in events))}

            Provide 3-5 strategic security recommendations.
            """

            response = await self.llm_client.chat_completion(
                messages=[{"role": "user", "content": context}],
                max_tokens=200
            )

            llm_recommendations = [line.strip("- ").strip() for line in response.get("content", "").split("\n") if line.strip()]
            recommendations.update(llm_recommendations[:3])

        except Exception as e:
            logger.warning(f"LLM recommendation generation failed: {str(e)}")

        return list(recommendations)[:8]  # Limit to 8 recommendations

    def _check_compliance_status(self, events: List[SecurityEvent]) -> Dict[str, bool]:
        """Check compliance status based on security events."""
        compliance_status = {}

        # SOC2 compliance checks
        has_logging = any("access" in event.description.lower() for event in events)
        no_critical_breaches = not any(event.threat_level == ThreatLevel.CRITICAL for event in events)

        compliance_status["SOC2_access_logging"] = has_logging
        compliance_status["SOC2_security_controls"] = no_critical_breaches

        # GDPR compliance checks
        no_data_breaches = not any(event.event_type == SecurityEventType.DATA_EXFILTRATION for event in events)
        compliance_status["GDPR_data_protection"] = no_data_breaches

        # HIPAA compliance checks (if applicable)
        no_phi_breaches = not any("phi" in event.description.lower() or "health" in event.description.lower() for event in events)
        compliance_status["HIPAA_phi_protection"] = no_phi_breaches

        return compliance_status

    def _determine_next_actions(self, events: List[SecurityEvent], critical_issues: List[SecurityEvent]) -> List[str]:
        """Determine immediate next actions."""
        actions = []

        if critical_issues:
            actions.append("IMMEDIATE: Address critical security events")
            actions.append("Notify security incident response team")
            actions.append("Document all critical findings")

        if len(events) > 10:
            actions.append("Conduct comprehensive security review")

        # Check for patterns requiring specific actions
        auth_failures = [e for e in events if e.event_type == SecurityEventType.AUTHENTICATION_FAILURE]
        if len(auth_failures) > 5:
            actions.append("Investigate potential brute force attacks")

        malware_events = [e for e in events if e.event_type == SecurityEventType.MALWARE_DETECTION]
        if malware_events:
            actions.append("Initiate malware containment procedures")

        if not actions:
            actions.append("Continue monitoring and maintain security posture")

        return actions[:5]  # Limit to 5 actions

    async def _compliance_monitoring(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> Dict[str, Any]:
        """Monitor compliance with security standards."""

        compliance_results = {}

        for standard, rules in self.compliance_rules.items():
            compliance_results[standard] = {
                "status": "compliant",
                "issues": [],
                "recommendations": []
            }

            # Check each rule
            for rule_name, rule_description in rules.items():
                is_compliant = await self._check_compliance_rule(event_data, standard, rule_name)

                if not is_compliant:
                    compliance_results[standard]["status"] = "non_compliant"
                    compliance_results[standard]["issues"].append(f"{rule_name}: {rule_description}")
                    compliance_results[standard]["recommendations"].append(f"Address {rule_name} compliance gap")

        return {
            "compliance_summary": compliance_results,
            "overall_compliance": all(result["status"] == "compliant" for result in compliance_results.values()),
            "total_issues": sum(len(result["issues"]) for result in compliance_results.values())
        }

    async def _check_compliance_rule(self, events: List[Dict], standard: str, rule: str) -> bool:
        """Check if a specific compliance rule is met."""
        # Simplified compliance checking - in practice, this would be much more sophisticated

        if standard == "SOC2":
            if rule == "access_logging":
                return any("login" in event.get("message", "").lower() for event in events)
            elif rule == "encryption_at_rest":
                return True  # Would check actual encryption status

        elif standard == "GDPR":
            if rule == "breach_notification":
                # Check if any data breaches were reported within 72 hours
                return True  # Would check actual breach reporting

        elif standard == "HIPAA":
            if rule == "phi_encryption":
                return True  # Would check PHI encryption status

        return True  # Default to compliant

    async def _vulnerability_assessment(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> Dict[str, Any]:
        """Assess system vulnerabilities."""

        vulnerabilities = []

        # Analyze events for vulnerability indicators
        for event in event_data:
            vulns = self._identify_vulnerabilities_from_event(event)
            vulnerabilities.extend(vulns)

        # Categorize vulnerabilities
        vuln_categories = {
            "network": [v for v in vulnerabilities if v.get("category") == "network"],
            "application": [v for v in vulnerabilities if v.get("category") == "application"],
            "system": [v for v in vulnerabilities if v.get("category") == "system"],
            "configuration": [v for v in vulnerabilities if v.get("category") == "configuration"]
        }

        # Calculate severity distribution
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for vuln in vulnerabilities:
            severity_counts[vuln.get("severity", "low")] += 1

        return {
            "vulnerability_summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "by_category": {cat: len(vulns) for cat, vulns in vuln_categories.items()},
                "by_severity": severity_counts
            },
            "top_vulnerabilities": vulnerabilities[:10],  # Top 10 by severity
            "remediation_priority": self._prioritize_vulnerabilities(vulnerabilities)
        }

    def _identify_vulnerabilities_from_event(self, event: Dict) -> List[Dict[str, Any]]:
        """Identify potential vulnerabilities from security events."""
        vulnerabilities = []
        message = event.get("message", "").lower()

        # Check for common vulnerability indicators
        if "unpatched" in message or "outdated" in message:
            vulnerabilities.append({
                "type": "outdated_software",
                "severity": "high",
                "category": "system",
                "description": "Outdated software detected",
                "recommendation": "Update software to latest version"
            })

        if "weak password" in message or "default credentials" in message:
            vulnerabilities.append({
                "type": "weak_authentication",
                "severity": "medium",
                "category": "configuration",
                "description": "Weak authentication mechanisms",
                "recommendation": "Enforce strong password policies"
            })

        if "open port" in message or "exposed service" in message:
            vulnerabilities.append({
                "type": "network_exposure",
                "severity": "medium",
                "category": "network",
                "description": "Unnecessary network exposure",
                "recommendation": "Close unused ports and services"
            })

        return vulnerabilities

    def _prioritize_vulnerabilities(self, vulnerabilities: List[Dict]) -> List[str]:
        """Prioritize vulnerability remediation."""
        priority_order = []

        # Critical vulnerabilities first
        critical = [v for v in vulnerabilities if v.get("severity") == "critical"]
        if critical:
            priority_order.append("Address critical vulnerabilities immediately")

        # High severity vulnerabilities
        high = [v for v in vulnerabilities if v.get("severity") == "high"]
        if high:
            priority_order.append(f"Remediate {len(high)} high-severity vulnerabilities")

        # Medium and low severity
        medium = [v for v in vulnerabilities if v.get("severity") == "medium"]
        low = [v for v in vulnerabilities if v.get("severity") == "low"]

        if medium:
            priority_order.append(f"Plan remediation for {len(medium)} medium-severity issues")
        if low:
            priority_order.append(f"Schedule {len(low)} low-severity vulnerability fixes")

        return priority_order

    async def _incident_response(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> Dict[str, Any]:
        """Coordinate incident response activities."""

        # Classify incident severity
        incident_severity = self._classify_incident_severity(event_data)

        # Generate incident response plan
        response_plan = self._generate_incident_response_plan(incident_severity, event_data)

        # Create incident timeline
        timeline = self._create_incident_timeline(event_data)

        return {
            "incident_classification": incident_severity,
            "response_plan": response_plan,
            "timeline": timeline,
            "containment_actions": self._get_containment_actions(incident_severity),
            "recovery_steps": self._get_recovery_steps(incident_severity),
            "lessons_learned": ["Document incident details", "Review response effectiveness", "Update procedures"]
        }

    def _classify_incident_severity(self, events: List[Dict]) -> str:
        """Classify overall incident severity."""
        if any("critical" in event.get("message", "").lower() for event in events):
            return "critical"
        elif any("high" in event.get("message", "").lower() for event in events):
            return "high"
        elif len(events) > 10:
            return "medium"
        else:
            return "low"

    def _generate_incident_response_plan(self, severity: str, events: List[Dict]) -> List[str]:
        """Generate incident response plan based on severity."""
        plan = []

        if severity == "critical":
            plan.extend([
                "Immediately notify CISO and executive team",
                "Activate emergency response procedures",
                "Isolate affected systems",
                "Preserve evidence for forensic analysis",
                "Prepare external communications"
            ])
        elif severity == "high":
            plan.extend([
                "Notify security team lead",
                "Begin containment procedures",
                "Assess impact scope",
                "Document all actions taken"
            ])
        else:
            plan.extend([
                "Monitor situation closely",
                "Apply standard remediation procedures",
                "Update security monitoring rules"
            ])

        return plan

    def _create_incident_timeline(self, events: List[Dict]) -> List[Dict[str, Any]]:
        """Create chronological timeline of incident events."""
        timeline = []

        for event in sorted(events, key=lambda x: x.get("timestamp", "")):
            timeline.append({
                "timestamp": event.get("timestamp"),
                "event": event.get("message", "Unknown event"),
                "source": event.get("source_ip", "Unknown"),
                "severity": "high" if "critical" in event.get("message", "").lower() else "medium"
            })

        return timeline[:20]  # Limit to 20 events

    def _get_containment_actions(self, severity: str) -> List[str]:
        """Get containment actions based on incident severity."""
        actions = []

        if severity in ["critical", "high"]:
            actions.extend([
                "Isolate affected network segments",
                "Disable compromised user accounts",
                "Block malicious IP addresses",
                "Shut down non-essential services"
            ])
        else:
            actions.extend([
                "Monitor affected systems",
                "Apply security patches",
                "Review access logs"
            ])

        return actions

    def _get_recovery_steps(self, severity: str) -> List[str]:
        """Get recovery steps based on incident severity."""
        steps = []

        if severity == "critical":
            steps.extend([
                "Restore systems from clean backups",
                "Rebuild compromised infrastructure",
                "Implement additional security controls",
                "Conduct thorough security testing"
            ])
        else:
            steps.extend([
                "Apply security updates",
                "Reset affected credentials",
                "Enhance monitoring coverage"
            ])

        return steps

    async def _security_audit(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> Dict[str, Any]:
        """Perform comprehensive security audit."""

        audit_results = {
            "authentication_security": self._audit_authentication(event_data),
            "network_security": self._audit_network_security(event_data),
            "data_protection": self._audit_data_protection(event_data),
            "access_controls": self._audit_access_controls(event_data),
            "monitoring_effectiveness": self._audit_monitoring(event_data)
        }

        # Calculate overall security score
        scores = [result.get("score", 0) for result in audit_results.values()]
        overall_score = sum(scores) / len(scores) if scores else 0

        return {
            "audit_results": audit_results,
            "overall_security_score": overall_score,
            "recommendations": self._generate_audit_recommendations(audit_results),
            "compliance_gaps": self._identify_compliance_gaps(audit_results)
        }

    def _audit_authentication(self, events: List[Dict]) -> Dict[str, Any]:
        """Audit authentication security."""
        auth_events = [e for e in events if "auth" in e.get("message", "").lower()]

        failed_attempts = len([e for e in auth_events if "failed" in e.get("message", "").lower()])
        total_attempts = len(auth_events)

        failure_rate = failed_attempts / total_attempts if total_attempts > 0 else 0

        return {
            "score": max(0, 100 - (failure_rate * 100)),
            "failed_attempts": failed_attempts,
            "total_attempts": total_attempts,
            "failure_rate": failure_rate,
            "recommendations": ["Implement MFA", "Enforce strong passwords"] if failure_rate > 0.1 else []
        }

    def _audit_network_security(self, events: List[Dict]) -> Dict[str, Any]:
        """Audit network security."""
        network_events = [e for e in events if "network" in e.get("message", "").lower()]
        intrusion_attempts = len([e for e in network_events if "intrusion" in e.get("message", "").lower()])

        return {
            "score": max(0, 100 - (intrusion_attempts * 10)),
            "intrusion_attempts": intrusion_attempts,
            "recommendations": ["Review firewall rules", "Update IDS signatures"] if intrusion_attempts > 0 else []
        }

    def _audit_data_protection(self, events: List[Dict]) -> Dict[str, Any]:
        """Audit data protection measures."""
        data_events = [e for e in events if "data" in e.get("message", "").lower()]
        breaches = len([e for e in data_events if "breach" in e.get("message", "").lower()])

        return {
            "score": 100 if breaches == 0 else max(0, 100 - (breaches * 50)),
            "data_breaches": breaches,
            "recommendations": ["Implement DLP", "Encrypt sensitive data"] if breaches > 0 else []
        }

    def _audit_access_controls(self, events: List[Dict]) -> Dict[str, Any]:
        """Audit access control effectiveness."""
        access_events = [e for e in events if "access" in e.get("message", "").lower()]
        unauthorized_access = len([e for e in access_events if "unauthorized" in e.get("message", "").lower()])

        return {
            "score": max(0, 100 - (unauthorized_access * 20)),
            "unauthorized_attempts": unauthorized_access,
            "recommendations": ["Review user permissions", "Implement RBAC"] if unauthorized_access > 0 else []
        }

    def _audit_monitoring(self, events: List[Dict]) -> Dict[str, Any]:
        """Audit monitoring system effectiveness."""
        # Simple heuristic: more diverse events indicate better monitoring
        unique_event_types = len(set(e.get("message", "")[:20] for e in events))

        return {
            "score": min(100, unique_event_types * 10),
            "event_diversity": unique_event_types,
            "recommendations": ["Enhance logging coverage", "Improve alert rules"] if unique_event_types < 5 else []
        }

    def _generate_audit_recommendations(self, audit_results: Dict) -> List[str]:
        """Generate overall audit recommendations."""
        recommendations = set()

        for category, results in audit_results.items():
            if results.get("score", 100) < 80:
                recommendations.update(results.get("recommendations", []))

        # Add general recommendations
        recommendations.add("Regular security awareness training")
        recommendations.add("Periodic penetration testing")
        recommendations.add("Update incident response procedures")

        return list(recommendations)[:10]

    def _identify_compliance_gaps(self, audit_results: Dict) -> List[str]:
        """Identify compliance gaps from audit results."""
        gaps = []

        for category, results in audit_results.items():
            if results.get("score", 100) < 70:
                gaps.append(f"{category.replace('_', ' ').title()} requires attention")

        return gaps

    async def _comprehensive_security_analysis(self, event_data: List[Dict], config: Dict, context: ExecutionContext) -> SecurityAssessment:
        """Perform comprehensive security analysis combining all methods."""

        # Run threat detection
        threat_assessment = await self._threat_detection_analysis(event_data, config, context)

        # Add compliance and vulnerability information
        compliance_results = await self._compliance_monitoring(event_data, config, context)
        vuln_results = await self._vulnerability_assessment(event_data, config, context)

        # Combine results
        threat_assessment.compliance_status.update(compliance_results.get("compliance_summary", {}))

        # Add vulnerability recommendations
        vuln_recommendations = vuln_results.get("remediation_priority", [])
        threat_assessment.recommendations.extend(vuln_recommendations[:3])

        return threat_assessment

    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics and statistics."""
        total_events = len(self.security_events)

        if total_events == 0:
            return {"message": "No security events processed yet"}

        # Calculate metrics
        threat_distribution = {}
        for level in ThreatLevel:
            threat_distribution[level.value] = len([e for e in self.security_events if e.threat_level == level])

        event_type_distribution = {}
        for event_type in SecurityEventType:
            event_type_distribution[event_type.value] = len([e for e in self.security_events if e.event_type == event_type])

        return {
            "total_events_processed": total_events,
            "threat_level_distribution": threat_distribution,
            "event_type_distribution": event_type_distribution,
            "average_risk_score": self._calculate_risk_score(self.security_events),
            "agent_id": self.id,
            "last_analysis": self.security_events[-1].timestamp.isoformat() if self.security_events else None
        }

# Example usage and testing
async def demo_security_monitoring_agent():
    """Demonstrate the security monitoring agent capabilities."""

    print("🔒 Security Monitoring Agent Demo\n")

    # Create agent
    agent = SecurityMonitoringAgent()

    # Create sample security events
    sample_events = [
        {
            "id": "event_001",
            "timestamp": datetime.now().isoformat(),
            "source_ip": "192.168.1.100",
            "user_id": "user123",
            "message": "Failed login attempt from unusual location",
            "details": {"attempt_count": 3, "location": "Unknown"}
        },
        {
            "id": "event_002",
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "source_ip": "10.0.0.50",
            "user_id": "admin",
            "message": "Malware detected in file download",
            "details": {"file_name": "suspicious.exe", "virus_name": "Trojan.Generic"}
        },
        {
            "id": "event_003",
            "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "source_ip": "172.16.0.25",
            "user_id": "service_account",
            "message": "SQL injection attempt detected: union select * from users",
            "details": {"target_url": "/api/login", "payload": "' union select * from users--"}
        },
        {
            "id": "event_004",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "source_ip": "192.168.1.200",
            "user_id": "user456",
            "message": "Large data download detected - 500MB in 5 minutes",
            "details": {"data_size": "500MB", "duration": "5 minutes"}
        }
    ]

    print("🚨 Sample security events created:")
    for event in sample_events:
        print(f"   {event['id']}: {event['message'][:50]}...")
    print()

    # Test different analysis types
    analysis_types = [
        ("threat_detection", "Threat Detection Analysis"),
        ("compliance_check", "Compliance Monitoring"),
        ("vulnerability_assessment", "Vulnerability Assessment"),
        ("incident_response", "Incident Response"),
        ("security_audit", "Security Audit")
    ]

    for analysis_type, description in analysis_types:
        print(f"🔍 {description}:")

        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run({
            "event_data": sample_events,
            "analysis_type": analysis_type,
            "config": {}
        }, context)

        if result["status"] == "completed":
            output = result["output"]
            assessment = output["security_assessment"]

            print(f"   ✅ Analysis completed")

            if "overall_risk_score" in assessment:
                print(f"   🎯 Risk Score: {assessment['overall_risk_score']:.1f}/100")

            if "critical_issues" in assessment:
                print(f"   🚨 Critical Issues: {len(assessment['critical_issues'])}")

            if "recommendations" in assessment:
                print(f"   💡 Recommendations: {len(assessment['recommendations'])}")
                if assessment['recommendations']:
                    print(f"      - {assessment['recommendations'][0]}")

            if "compliance_summary" in assessment:
                compliant_count = sum(1 for v in assessment['compliance_summary'].values()
                                    if isinstance(v, dict) and v.get('status') == 'compliant')
                total_count = len(assessment['compliance_summary'])
                print(f"   📋 Compliance: {compliant_count}/{total_count} standards")

        else:
            print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")

        print()

    # Show security metrics
    print("📊 Security Metrics:")
    metrics = agent.get_security_metrics()
    if "total_events_processed" in metrics:
        print(f"   Total events processed: {metrics['total_events_processed']}")
        print(f"   Average risk score: {metrics['average_risk_score']:.1f}")

        # Show threat distribution
        threat_dist = metrics['threat_level_distribution']
        print(f"   Threat distribution:")
        for level, count in threat_dist.items():
            if count > 0:
                print(f"      {level}: {count}")

    print("\n✅ Security Monitoring Agent demo completed!")

if __name__ == "__main__":
    asyncio.run(demo_security_monitoring_agent())
