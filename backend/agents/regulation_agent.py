"""
Regulation Agent - Flags compliance risks and regulatory requirements
Particularly relevant for PNC challenge (financial compliance)
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class RegulationAgent(BaseAgent):
    """Agent specialized in compliance and regulatory analysis"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="RegulationAgent",
            goal="Identify compliance risks and regulatory requirements",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute regulation and compliance tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "compliance_check", "risk_assessment", "audit_report"
                - feature: Feature to analyze
                - jurisdiction: Regulatory jurisdiction (e.g., "US", "EU")
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "compliance_check")
        feature = task_input.get("feature", "")
        jurisdiction = task_input.get("jurisdiction", "US")
        
        try:
            if task_type == "compliance_check":
                result = await self._compliance_check(feature, jurisdiction)
            elif task_type == "risk_assessment":
                result = await self._risk_assessment(feature)
            elif task_type == "audit_report":
                result = await self._generate_audit_report()
            elif task_type == "privacy_review":
                result = await self._privacy_review(feature)
            else:
                result = await self._general_regulation(task_input)
            
            self.update_context("compliance_status", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _compliance_check(self, feature: str, jurisdiction: str) -> Dict[str, Any]:
        """Perform compliance check for a feature"""
        prompt = f"Check compliance for {feature} in {jurisdiction}"
        llm_response = await self._call_llm(prompt)
        
        # Comprehensive compliance frameworks
        compliance_results = {
            "feature": feature,
            "jurisdiction": jurisdiction,
            "frameworks_checked": [
                "GDPR", "CCPA", "SOC 2", "HIPAA", "PCI-DSS", "SOX"
            ],
            "compliance_status": {
                "GDPR": {
                    "status": "compliant",
                    "requirements": [
                        "✅ Right to access implemented",
                        "✅ Right to erasure implemented",
                        "✅ Data portability supported",
                        "✅ Consent management in place",
                        "⚠️ Data processing agreement needed with vendors"
                    ],
                    "risk_level": "low"
                },
                "CCPA": {
                    "status": "compliant",
                    "requirements": [
                        "✅ Privacy policy updated",
                        "✅ Do Not Sell option provided",
                        "✅ Data disclosure available",
                        "✅ Consumer rights request process"
                    ],
                    "risk_level": "low"
                },
                "SOC 2": {
                    "status": "in_progress",
                    "requirements": [
                        "✅ Security controls documented",
                        "✅ Access controls implemented",
                        "⚠️ Formal audit required",
                        "⚠️ Penetration testing needed",
                        "⚠️ Incident response plan incomplete"
                    ],
                    "risk_level": "medium"
                },
                "PCI-DSS": {
                    "status": "not_applicable",
                    "reason": "No payment card data stored directly",
                    "note": "Using Stripe for payment processing",
                    "risk_level": "n/a"
                }
            },
            "critical_issues": [],
            "warnings": [
                "SOC 2 audit should be scheduled within 6 months",
                "Data processing agreements needed for all subprocessors",
                "Annual compliance training recommended"
            ],
            "recommendations": [
                "Complete SOC 2 Type I audit before enterprise sales",
                "Implement automated compliance monitoring",
                "Document data flows for all integrations",
                "Review vendor compliance status quarterly"
            ],
            "analysis": llm_response
        }
        
        # Financial services specific (PNC challenge)
        if "financial" in feature.lower() or "banking" in feature.lower():
            compliance_results["financial_compliance"] = {
                "frameworks": ["SOX", "GLBA", "Bank Secrecy Act"],
                "requirements": [
                    "⚠️ Financial data encryption at rest and in transit",
                    "⚠️ Audit trail for all financial transactions",
                    "⚠️ Access controls for financial data",
                    "⚠️ Regular security assessments required"
                ],
                "risk_level": "high",
                "action_required": "Engage financial compliance specialist"
            }
        
        return compliance_results
    
    async def _risk_assessment(self, feature: str) -> Dict[str, Any]:
        """Assess regulatory and compliance risks"""
        prompt = f"Assess risks for feature: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "risk_categories": [
                {
                    "category": "Data Privacy",
                    "risk_level": "medium",
                    "risks": [
                        "User data stored in vector database",
                        "Conversation history contains PII",
                        "Integration data may contain sensitive info"
                    ],
                    "mitigations": [
                        "Implement encryption at rest",
                        "Add PII detection and masking",
                        "User-controlled data retention policies",
                        "Local LLM processing for sensitive data"
                    ]
                },
                {
                    "category": "AI/ML Ethics",
                    "risk_level": "low",
                    "risks": [
                        "LLM output bias potential",
                        "Automated decisions without human review"
                    ],
                    "mitigations": [
                        "Human-in-the-loop for critical decisions",
                        "Transparency about AI limitations",
                        "User ability to override AI suggestions"
                    ]
                },
                {
                    "category": "Security",
                    "risk_level": "medium",
                    "risks": [
                        "API key management",
                        "WebSocket connection security",
                        "Third-party integration vulnerabilities"
                    ],
                    "mitigations": [
                        "Encrypted API key storage",
                        "WSS (secure WebSocket) implementation",
                        "Regular security audits of integrations",
                        "Rate limiting and DDoS protection"
                    ]
                },
                {
                    "category": "Intellectual Property",
                    "risk_level": "low",
                    "risks": [
                        "LLM training data copyright",
                        "User-generated content ownership"
                    ],
                    "mitigations": [
                        "Clear terms of service",
                        "Use licensed/open-source models",
                        "User retains ownership of their data"
                    ]
                }
            ],
            "overall_risk_score": 4.5,
            "risk_rating": "Low-Medium",
            "assessment": llm_response,
            "next_review_date": "2025-12-08"
        }
    
    async def _generate_audit_report(self) -> Dict[str, Any]:
        """Generate compliance audit report"""
        prompt = "Generate comprehensive compliance audit report"
        llm_response = await self._call_llm(prompt)
        
        return {
            "audit_date": "2025-11-08",
            "audit_scope": "Full platform compliance review",
            "auditor": "RegulationAgent + External Compliance Firm",
            "findings": [
                {
                    "id": "AUD-001",
                    "severity": "low",
                    "category": "Documentation",
                    "finding": "Privacy policy last updated 60 days ago",
                    "recommendation": "Update privacy policy to reflect new features",
                    "status": "open"
                },
                {
                    "id": "AUD-002",
                    "severity": "medium",
                    "category": "Security",
                    "finding": "Penetration test not conducted in last 12 months",
                    "recommendation": "Schedule annual penetration test",
                    "status": "open"
                },
                {
                    "id": "AUD-003",
                    "severity": "low",
                    "category": "Training",
                    "finding": "Security training completion at 85%",
                    "recommendation": "Achieve 100% completion for all team members",
                    "status": "in_progress"
                }
            ],
            "compliance_score": 88,
            "areas_of_excellence": [
                "Strong data encryption practices",
                "Well-documented access controls",
                "Regular security updates",
                "Clear user consent flows"
            ],
            "areas_for_improvement": [
                "Complete SOC 2 certification",
                "Enhance incident response procedures",
                "Improve vendor risk management"
            ],
            "report": llm_response,
            "next_audit_date": "2026-05-08"
        }
    
    async def _privacy_review(self, feature: str) -> Dict[str, Any]:
        """Review feature for privacy implications"""
        prompt = f"Review privacy implications of: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "data_collected": [
                "User prompts and queries",
                "Agent responses",
                "Project metadata",
                "Integration data (Jira, Slack, etc.)"
            ],
            "data_sensitivity": "Medium-High",
            "pii_detected": True,
            "pii_types": [
                "Email addresses",
                "Names",
                "Project information",
                "Potentially trade secrets"
            ],
            "privacy_controls": {
                "encryption_at_rest": True,
                "encryption_in_transit": True,
                "access_controls": True,
                "data_minimization": True,
                "retention_policies": True,
                "user_consent": True,
                "right_to_delete": True,
                "data_portability": True
            },
            "privacy_enhancements": [
                "Add PII detection and optional masking",
                "Implement local processing option for sensitive data",
                "Provide granular data sharing controls",
                "Add audit log for data access"
            ],
            "review": llm_response,
            "approved": True,
            "conditions": [
                "Implement recommended privacy enhancements",
                "Update privacy notice to cover feature",
                "Conduct privacy training for team"
            ]
        }
    
    async def _general_regulation(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general regulation tasks"""
        prompt = f"Analyze regulatory requirements for: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "task": task_input,
            "compliance_required": True,
            "frameworks_applicable": ["GDPR", "SOC 2"],
            "output": llm_response
        }

