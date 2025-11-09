"""
Demo Scenarios - Pre-configured workflows for impressive demos
"""
from typing import Dict, Any

DEMO_SCENARIOS = {
    "pnc_mobile_feature": {
        "name": "Launch PNC Mobile Banking Feature",
        "description": "AI-powered expense categorization for mobile banking",
        "workflow_type": "full_feature_planning",
        "input_data": {
            "feature": "AI-Powered Expense Categorization",
            "market": "Mobile Banking - Financial Services",
            "target_users": "PNC Bank customers using mobile banking app",
            "business_goals": [
                "Increase user engagement with mobile app",
                "Provide personalized financial insights",
                "Improve customer retention",
                "Differentiate from competitors"
            ],
            "constraints": [
                "Must comply with financial regulations (GLBA, PCI-DSS)",
                "Must protect customer privacy",
                "Must integrate with existing PNC systems",
                "Must be accessible (WCAG 2.1 AA)"
            ]
        },
        "expected_outputs": {
            "strategy": "Market analysis showing 40% of mobile banking users want expense categorization",
            "research": "Competitive analysis of Chase, Bank of America, and Capital One features",
            "dev": "23 user stories with acceptance criteria",
            "prototype": "Wireframes showing expense categorization UI",
            "gtm": "Launch plan with phased rollout strategy",
            "regulation": "Compliance checklist for financial data handling",
            "risk": "Identified 3 potential risks with mitigation strategies",
            "prioritization": "Ranked 12 features by ROI and user value"
        }
    },
    "competitive_response": {
        "name": "Competitive Response Strategy",
        "description": "Respond to competitor's new feature launch",
        "workflow_type": "research_and_strategy",
        "input_data": {
            "competitor": "Chase Bank",
            "feature": "Real-time fraud alerts via push notifications",
            "market": "Banking - Security Features",
            "urgency": "high"
        }
    },
    "compliance_audit": {
        "name": "Compliance Audit for New Feature",
        "description": "Full compliance review for financial data feature",
        "workflow_type": "compliance_check",
        "input_data": {
            "feature": "Open Banking API Integration",
            "regulations": ["GLBA", "PCI-DSS", "SOC 2", "GDPR"],
            "data_types": ["Customer financial data", "Transaction history", "Account information"]
        }
    }
}

def get_demo_scenario(scenario_key: str) -> Dict[str, Any]:
    """Get a demo scenario by key"""
    return DEMO_SCENARIOS.get(scenario_key, {})

def list_demo_scenarios() -> Dict[str, Dict[str, str]]:
    """List all available demo scenarios"""
    return {
        key: {
            "name": value["name"],
            "description": value["description"]
        }
        for key, value in DEMO_SCENARIOS.items()
    }

