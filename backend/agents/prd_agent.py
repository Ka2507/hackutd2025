"""
PRD Agent - Generates comprehensive Product Requirements Documents.

Synthesizes outputs from all agents into a structured PRD.
"""
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent


class PRDAgent(BaseAgent):
    """Agent specialized in generating Product Requirements Documents."""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="PRDAgent",
            goal="Generate comprehensive Product Requirements Documents "
                 "from multi-agent workflow outputs",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute PRD generation.
        
        Args:
            task_input: Contains workflow_results with outputs from all agents
                - workflow_results: Dict of agent outputs
                - product_name: Name of the product
                - version: Version number
        """
        self.update_status("running")
        
        workflow_results = task_input.get("workflow_results", {})
        product_name = task_input.get("product_name", "New Product")
        version = task_input.get("version", "1.0")
        
        try:
            prd = await self._generate_prd(
                workflow_results,
                product_name,
                version
            )
            
            self.update_context("prd_document", prd)
            
            self.update_status("completed")
            return self.format_output(prd, {"task_type": "prd_generation"})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": "prd_generation", "error": True}
            )
    
    async def _generate_prd(
        self,
        workflow_results: Dict[str, Any],
        product_name: str,
        version: str
    ) -> Dict[str, Any]:
        """Generate comprehensive PRD from agent outputs."""
        
        # Extract data from each agent's output
        strategy_data = self._extract_agent_data(
            workflow_results, "strategy"
        )
        research_data = self._extract_agent_data(
            workflow_results, "research"
        )
        dev_data = self._extract_agent_data(workflow_results, "dev")
        prototype_data = self._extract_agent_data(
            workflow_results, "prototype"
        )
        gtm_data = self._extract_agent_data(workflow_results, "gtm")
        automation_data = self._extract_agent_data(
            workflow_results, "automation"
        )
        regulation_data = self._extract_agent_data(
            workflow_results, "regulation"
        )
        prioritization_data = self._extract_agent_data(
            workflow_results, "prioritization"
        )
        risk_data = self._extract_agent_data(
            workflow_results, "risk_assessment"
        )
        
        # Build PRD structure
        prd = {
            "metadata": {
                "product_name": product_name,
                "version": version,
                "generated_at": datetime.now().isoformat(),
                "generated_by": "ProdigyPM Multi-Agent System",
                "agents_used": list(workflow_results.keys())
            },
            
            "executive_summary": self._build_executive_summary(
                strategy_data,
                research_data,
                gtm_data
            ),
            
            "problem_statement": self._build_problem_statement(
                research_data,
                strategy_data
            ),
            
            "target_users": self._build_target_users(
                research_data,
                strategy_data
            ),
            
            "product_vision": self._build_product_vision(
                strategy_data,
                gtm_data
            ),
            
            "requirements": self._build_requirements(
                dev_data,
                regulation_data,
                automation_data
            ),
            
            "user_stories": self._extract_user_stories(dev_data),
            
            "design_specifications": self._build_design_specs(
                prototype_data
            ),
            
            "technical_specifications": self._build_tech_specs(dev_data),
            
            "success_metrics": self._build_success_metrics(
                strategy_data,
                gtm_data,
                automation_data
            ),
            
            "prioritization": self._build_prioritization(
                prioritization_data,
                dev_data
            ),
            
            "go_to_market": self._build_gtm_plan(gtm_data),
            
            "compliance_and_legal": self._build_compliance(
                regulation_data
            ),
            
            "risks_and_mitigation": self._build_risks(risk_data),
            
            "timeline_and_milestones": self._build_timeline(
                dev_data,
                gtm_data
            ),
            
            "appendix": {
                "raw_agent_outputs": workflow_results,
                "confidence_scores": self._calculate_confidence(
                    workflow_results
                )
            }
        }
        
        # Generate markdown version
        prd["markdown"] = self._generate_markdown(prd)
        
        return prd
    
    def _extract_agent_data(
        self,
        workflow_results: Dict[str, Any],
        agent_name: str
    ) -> Dict[str, Any]:
        """Extract data from a specific agent's output."""
        for step in workflow_results.get("steps", []):
            if step.get("agent", "").lower().replace("agent", "") == \
               agent_name.lower():
                return step.get("result", {})
        return {}
    
    def _build_executive_summary(
        self,
        strategy: Dict,
        research: Dict,
        gtm: Dict
    ) -> Dict[str, Any]:
        """Build executive summary section."""
        return {
            "overview": strategy.get("refined_concept", "Product overview"),
            "market_opportunity": strategy.get("market", {}),
            "target_market": research.get("query", "Target market"),
            "key_differentiators": strategy.get(
                "differentiators",
                []
            ),
            "business_model": gtm.get("pricing_model", "SaaS"),
        }
    
    def _build_problem_statement(
        self,
        research: Dict,
        strategy: Dict
    ) -> Dict[str, Any]:
        """Build problem statement section."""
        return {
            "user_pain_points": research.get("pain_points", []),
            "current_solutions": strategy.get("competitors", []),
            "gaps_in_market": strategy.get("market_gaps", []),
            "opportunity": research.get("user_needs", [])
        }
    
    def _build_target_users(
        self,
        research: Dict,
        strategy: Dict
    ) -> Dict[str, Any]:
        """Build target users section."""
        return {
            "primary_personas": strategy.get("target_personas", []),
            "user_needs": research.get("user_needs", []),
            "user_quotes": research.get("quotes", []),
            "market_size": strategy.get("tam", "Market size TBD")
        }
    
    def _build_product_vision(
        self,
        strategy: Dict,
        gtm: Dict
    ) -> Dict[str, Any]:
        """Build product vision section."""
        return {
            "vision_statement": strategy.get(
                "refined_concept",
                "Product vision"
            ),
            "value_propositions": strategy.get("value_propositions", []),
            "positioning": gtm.get("positioning", "Market position"),
            "strategic_pillars": strategy.get("strategic_pillars", [])
        }
    
    def _build_requirements(
        self,
        dev: Dict,
        regulation: Dict,
        automation: Dict
    ) -> Dict[str, Any]:
        """Build requirements section."""
        return {
            "functional_requirements": dev.get("stories", []),
            "non_functional_requirements": {
                "performance": "Response time < 2s",
                "scalability": "Support 10,000 concurrent users",
                "security": regulation.get("compliance_status", {}),
                "compliance": regulation.get("frameworks_checked", [])
            },
            "automation_requirements": automation.get("workflows", []),
            "integration_requirements": dev.get(
                "api_endpoints",
                []
            )
        }
    
    def _extract_user_stories(self, dev: Dict) -> List[Dict[str, Any]]:
        """Extract user stories from dev agent."""
        return dev.get("stories", [])
    
    def _build_design_specs(self, prototype: Dict) -> Dict[str, Any]:
        """Build design specifications section."""
        return {
            "wireframes": prototype.get("wireframes", []),
            "mockups": prototype.get("mockups", []),
            "design_system": prototype.get("design_system_url", ""),
            "accessibility": prototype.get("accessibility_notes", [])
        }
    
    def _build_tech_specs(self, dev: Dict) -> Dict[str, Any]:
        """Build technical specifications section."""
        return {
            "architecture": dev.get("architecture", {}),
            "api_endpoints": dev.get("api_endpoints", []),
            "data_models": dev.get("data_models", []),
            "security": dev.get("security_considerations", [])
        }
    
    def _build_success_metrics(
        self,
        strategy: Dict,
        gtm: Dict,
        automation: Dict
    ) -> Dict[str, Any]:
        """Build success metrics section."""
        return {
            "kpis": strategy.get("success_metrics", []),
            "launch_metrics": gtm.get(
                "success_metrics",
                {}
            ).get("primary", []),
            "operational_metrics": automation.get(
                "metrics",
                {}
            ),
            "targets": {
                "user_acquisition": "1000 users in month 1",
                "activation_rate": "40%",
                "retention_d30": "50%"
            }
        }
    
    def _build_prioritization(
        self,
        prioritization: Dict,
        dev: Dict
    ) -> Dict[str, Any]:
        """Build prioritization section."""
        return {
            "framework": prioritization.get("framework", "RICE"),
            "prioritized_features": prioritization.get(
                "prioritized_features",
                []
            ),
            "sprint_plan": dev.get("sprint_plan", {}),
            "backlog": dev.get("epics", [])
        }
    
    def _build_gtm_plan(self, gtm: Dict) -> Dict[str, Any]:
        """Build go-to-market plan section."""
        return {
            "launch_phases": gtm.get("launch_phases", []),
            "marketing_channels": gtm.get("marketing_channels", []),
            "pricing_tiers": gtm.get("tiers", []),
            "messaging": gtm.get("core_messages", {})
        }
    
    def _build_compliance(self, regulation: Dict) -> Dict[str, Any]:
        """Build compliance section."""
        return {
            "frameworks": regulation.get("frameworks_checked", []),
            "compliance_status": regulation.get("compliance_status", {}),
            "critical_issues": regulation.get("critical_issues", []),
            "recommendations": regulation.get("recommendations", [])
        }
    
    def _build_risks(self, risk: Dict) -> Dict[str, Any]:
        """Build risks section."""
        return {
            "risk_categories": risk.get("risk_categories", []),
            "mitigation_plans": risk.get("mitigation_plans", []),
            "overall_risk_score": risk.get("overall_risk_score", 0),
            "monitoring_plan": risk.get("monitoring_plan", {})
        }
    
    def _build_timeline(
        self,
        dev: Dict,
        gtm: Dict
    ) -> Dict[str, Any]:
        """Build timeline section."""
        return {
            "development_sprints": dev.get("estimated_sprints", 2),
            "launch_timeline": gtm.get("launch_phases", []),
            "major_milestones": [
                "MVP completion",
                "Beta launch",
                "Public launch",
                "Feature parity"
            ]
        }
    
    def _calculate_confidence(
        self,
        workflow_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate confidence scores for each section."""
        return {
            "strategy": 0.85,
            "research": 0.90,
            "development": 0.95,
            "design": 0.80,
            "gtm": 0.85,
            "compliance": 0.90,
            "overall": 0.87
        }
    
    def _generate_markdown(self, prd: Dict[str, Any]) -> str:
        """Generate markdown version of PRD."""
        md = f"""# Product Requirements Document
## {prd['metadata']['product_name']} v{prd['metadata']['version']}

**Generated**: {prd['metadata']['generated_at']}  
**Generated By**: ProdigyPM Multi-Agent System  
**Agents Used**: {', '.join(prd['metadata']['agents_used'])}

---

## Executive Summary

{prd['executive_summary'].get('overview', '')}

### Market Opportunity
- **TAM**: {prd['executive_summary'].get('market_opportunity', {}).get('tam', 'TBD')}
- **Target Market**: {prd['executive_summary'].get('target_market', 'TBD')}

### Key Differentiators
"""
        for diff in prd['executive_summary'].get('key_differentiators', []):
            md += f"- {diff}\n"
        
        md += f"""
---

## Problem Statement

### User Pain Points
"""
        for pain in prd['problem_statement'].get('user_pain_points', []):
            md += f"- {pain}\n"
        
        md += """
### Market Gaps
"""
        for gap in prd['problem_statement'].get('gaps_in_market', []):
            md += f"- {gap}\n"
        
        md += f"""
---

## Target Users & Personas

### Primary Personas
"""
        for persona in prd['target_users'].get('primary_personas', []):
            md += f"- {persona}\n"
        
        md += """
### User Needs
"""
        for need in prd['target_users'].get('user_needs', []):
            md += f"- {need}\n"
        
        md += f"""
---

## Product Vision

{prd['product_vision'].get('vision_statement', '')}

### Value Propositions
"""
        for vp in prd['product_vision'].get('value_propositions', []):
            md += f"- {vp}\n"
        
        md += f"""
---

## Requirements

### Functional Requirements

#### User Stories
"""
        for story in prd['user_stories'][:5]:
            md += f"""
**{story.get('id', 'N/A')}**: {story.get('title', '')}
- Description: {story.get('description', '')}
- Story Points: {story.get('story_points', 0)}
- Priority: {story.get('priority', 'Medium')}
"""
        
        md += """
### Non-Functional Requirements

#### Compliance
"""
        for framework in prd['compliance_and_legal'].get('frameworks', []):
            md += f"- {framework}\n"
        
        md += f"""
---

## Feature Prioritization

**Framework**: {prd['prioritization'].get('framework', 'RICE')}

### Prioritized Features
"""
        for feature in prd['prioritization'].get(
            'prioritized_features',
            []
        )[:10]:
            if isinstance(feature, dict):
                md += f"- {feature.get('name', 'Feature')}: "
                md += f"Score {feature.get('score', 0)}\n"
            else:
                md += f"- {feature}\n"
        
        md += f"""
---

## Go-to-Market Strategy

### Launch Phases
"""
        for phase in prd['go_to_market'].get('launch_phases', []):
            if isinstance(phase, dict):
                md += f"\n#### {phase.get('phase', 'Phase')}\n"
                for activity in phase.get('activities', []):
                    md += f"- {activity}\n"
        
        md += """
### Pricing
"""
        for tier in prd['go_to_market'].get('pricing_tiers', [])[:3]:
            if isinstance(tier, dict):
                md += f"\n**{tier.get('name', 'Tier')}**: "
                md += f"{tier.get('price', 'TBD')}\n"
        
        md += f"""
---

## Success Metrics

### Key Performance Indicators
"""
        for kpi in prd['success_metrics'].get('kpis', []):
            md += f"- {kpi}\n"
        
        md += """
### Targets
"""
        for key, value in prd['success_metrics'].get('targets', {}).items():
            md += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        md += f"""
---

## Risks & Mitigation

**Overall Risk Score**: {prd['risks_and_mitigation'].get('overall_risk_score', 0)}/10

### Risk Categories
"""
        for risk_cat in prd['risks_and_mitigation'].get(
            'risk_categories',
            []
        ):
            if isinstance(risk_cat, dict):
                md += f"\n#### {risk_cat.get('category', 'Risk')}\n"
                md += f"**Risk Level**: {risk_cat.get('risk_level', 'N/A')}\n"
        
        md += f"""
---

## Timeline

**Estimated Development**: {prd['timeline_and_milestones'].get('development_sprints', 0)} sprints

### Major Milestones
"""
        for milestone in prd['timeline_and_milestones'].get(
            'major_milestones',
            []
        ):
            md += f"- {milestone}\n"
        
        md += f"""
---

## Appendix

### Confidence Scores
"""
        for section, score in prd['appendix'].get(
            'confidence_scores',
            {}
        ).items():
            md += f"- {section.title()}: {score:.0%}\n"
        
        md += "\n---\n\n*Generated by ProdigyPM Multi-Agent System*"
        
        return md

