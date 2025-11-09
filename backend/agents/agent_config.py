"""
Agent Configuration - Defines Product Management Lifecycle Order and Model Assignments

This module defines:
1. The order of agents in the Product Management Lifecycle
2. The optimal Nemotron model for each agent based on their purpose
"""

from typing import Dict, List
from enum import IntEnum


class AgentLifecycleStage(IntEnum):
    """
    Product Management Lifecycle Stages - Ordered by typical workflow
    """
    STRATEGY = 1  # Ideation, market sizing, strategic planning
    RESEARCH = 2  # User research, competitor analysis, validation
    PRIORITIZATION = 3  # Feature prioritization, roadmap planning
    RISK_ASSESSMENT = 4  # Risk identification and mitigation (runs in parallel with prioritization)
    REGULATION = 5  # Compliance checks, regulatory requirements (ongoing but early)
    DEVELOPMENT = 6  # User stories, backlog, technical specs
    PROTOTYPE = 7  # Design, wireframes, mockups
    GTM = 8  # Go-to-market strategy, launch planning
    AUTOMATION = 9  # Ongoing automation and monitoring


# Agent to Lifecycle Stage Mapping
AGENT_LIFECYCLE_ORDER = {
    "strategy": AgentLifecycleStage.STRATEGY,
    "research": AgentLifecycleStage.RESEARCH,
    "prioritization": AgentLifecycleStage.PRIORITIZATION,
    "risk": AgentLifecycleStage.RISK_ASSESSMENT,
    "regulation": AgentLifecycleStage.REGULATION,
    "dev": AgentLifecycleStage.DEVELOPMENT,
    "prototype": AgentLifecycleStage.PROTOTYPE,
    "gtm": AgentLifecycleStage.GTM,
    "automation": AgentLifecycleStage.AUTOMATION,
}

# Nemotron Model Assignments based on Agent Purpose
# Models available in Nemotron family:
# - nemotron-4-340b-instruct: Large model for complex reasoning, strategic planning
# - nemotron-4-70b-instruct: Faster model for code generation, data analysis
# - nemotron-steerlm: For controlled generation and steering
# - nemotron-rewards: For reward modeling (typically not used for agents)

AGENT_NEMOTRON_MODELS = {
    "strategy": "nvidia/llama-3.1-nemotron-ultra-253b-v1",  # Complex strategic reasoning, market analysis
    "research": "meta/llama-3.1-70b-instruct",  # Fast data synthesis, research analysis
    "prioritization": "nvidia/llama-3.1-nemotron-ultra-253b-v1",  # Complex multi-factor decision making
    "risk": "nvidia/llama-3.1-nemotron-ultra-253b-v1",  # Complex pattern recognition, risk analysis
    "regulation": "nvidia/llama-3.1-nemotron-ultra-253b-v1",  # Compliance reasoning, regulatory analysis
    "dev": "meta/llama-3.1-70b-instruct",  # Code generation, technical specs (faster for dev tasks)
    "prototype": "meta/llama-3.1-70b-instruct",  # Design understanding, UI/UX (faster for design tasks)
    "gtm": "nvidia/llama-3.1-nemotron-ultra-253b-v1",  # Strategic planning, market strategy
    "automation": "meta/llama-3.1-70b-instruct",  # Simple automation, reporting (faster for routine tasks)
}

# Agent descriptions for documentation
AGENT_DESCRIPTIONS = {
    "strategy": {
        "name": "Strategy Agent",
        "stage": "Ideation & Strategy",
        "purpose": "Market sizing, idea generation, competitive analysis, strategic planning",
        "model_reasoning": "Uses 340B model for complex strategic reasoning and market analysis"
    },
    "research": {
        "name": "Research Agent",
        "stage": "Research & Validation",
        "purpose": "User research, competitor analysis, trend analysis, data synthesis",
        "model_reasoning": "Uses 70B model for fast data analysis and research synthesis"
    },
    "prioritization": {
        "name": "Prioritization Agent",
        "stage": "Feature Prioritization",
        "purpose": "Multi-factor prioritization, roadmap planning, value/effort analysis",
        "model_reasoning": "Uses 340B model for complex decision-making with multiple factors"
    },
    "risk": {
        "name": "Risk Assessment Agent",
        "stage": "Risk Assessment",
        "purpose": "Risk identification, mitigation planning, pattern recognition",
        "model_reasoning": "Uses 340B model for complex risk pattern recognition and analysis"
    },
    "regulation": {
        "name": "Regulation Agent",
        "stage": "Compliance & Regulation",
        "purpose": "Compliance checks, regulatory requirements, audit reports",
        "model_reasoning": "Uses 340B model for complex compliance reasoning and regulatory analysis"
    },
    "dev": {
        "name": "Development Agent",
        "stage": "Development Planning",
        "purpose": "User stories, backlog generation, technical specifications, sprint planning",
        "model_reasoning": "Uses 70B model for faster code generation and technical documentation"
    },
    "prototype": {
        "name": "Prototype Agent",
        "stage": "Design & Prototyping",
        "purpose": "Wireframes, mockups, design systems, Figma integration",
        "model_reasoning": "Uses 70B model for faster design understanding and UI/UX tasks"
    },
    "gtm": {
        "name": "GTM Agent",
        "stage": "Go-to-Market",
        "purpose": "Launch planning, marketing strategy, pricing, messaging",
        "model_reasoning": "Uses 340B model for complex strategic planning and market strategy"
    },
    "automation": {
        "name": "Automation Agent",
        "stage": "Automation & Monitoring",
        "purpose": "Sprint summaries, standup reports, workflow automation, metrics",
        "model_reasoning": "Uses 70B model for faster routine task automation and reporting"
    },
}


def get_agents_in_lifecycle_order() -> List[str]:
    """
    Get list of agent keys ordered by Product Management Lifecycle
    
    Returns:
        List of agent keys in lifecycle order
    """
    return sorted(
        AGENT_LIFECYCLE_ORDER.keys(),
        key=lambda x: AGENT_LIFECYCLE_ORDER[x]
    )


def get_agent_model(agent_key: str) -> str:
    """
    Get the assigned Nemotron model for an agent
    
    Args:
        agent_key: Agent identifier (e.g., "strategy", "research")
        
    Returns:
        Nemotron model identifier
    """
    return AGENT_NEMOTRON_MODELS.get(agent_key, "nvidia/llama-3.1-nemotron-ultra-253b-v1")


def get_agent_stage(agent_key: str) -> int:
    """
    Get the lifecycle stage number for an agent
    
    Args:
        agent_key: Agent identifier
        
    Returns:
        Lifecycle stage number
    """
    return int(AGENT_LIFECYCLE_ORDER.get(agent_key, AgentLifecycleStage.AUTOMATION))


def get_stage_name(stage: AgentLifecycleStage) -> str:
    """
    Get human-readable stage name
    
    Args:
        stage: Lifecycle stage enum
        
    Returns:
        Stage name
    """
    stage_names = {
        AgentLifecycleStage.STRATEGY: "Ideation & Strategy",
        AgentLifecycleStage.RESEARCH: "Research & Validation",
        AgentLifecycleStage.PRIORITIZATION: "Feature Prioritization",
        AgentLifecycleStage.RISK_ASSESSMENT: "Risk Assessment",
        AgentLifecycleStage.REGULATION: "Compliance & Regulation",
        AgentLifecycleStage.DEVELOPMENT: "Development Planning",
        AgentLifecycleStage.PROTOTYPE: "Design & Prototyping",
        AgentLifecycleStage.GTM: "Go-to-Market",
        AgentLifecycleStage.AUTOMATION: "Automation & Monitoring",
    }
    return stage_names.get(stage, "Unknown Stage")

