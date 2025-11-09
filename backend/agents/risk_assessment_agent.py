"""
Risk Assessment Agent - Predicts bottlenecks and risks proactively
Uses pattern matching and Nemotron reasoning to identify potential issues
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .base_agent import BaseAgent
from orchestrator.memory_manager import memory_manager
from orchestrator.nemotron_bridge import nemotron_bridge
from utils.logger import logger


class RiskAssessmentAgent(BaseAgent):
    """Agent specialized in risk prediction and mitigation"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="RiskAssessmentAgent",
            goal="Predict and mitigate project risks proactively",
            context=context,
            agent_key="risk"
        )
        self.risk_patterns = self._load_risk_patterns()
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute risk assessment
        
        Args:
            task_input: Contains:
                - workflow_state: Current state of workflow
                - project_id: Project ID for historical analysis
                - risk_factors: Known risk factors (optional)
        """
        self.update_status("running")
        
        workflow_state = task_input.get("workflow_state", {})
        project_id = task_input.get("project_id")
        risk_factors = task_input.get("risk_factors", [])
        
        try:
            # Find similar past projects
            similar_projects = await self._find_similar_projects(workflow_state, project_id)
            
            # Analyze current state for risks
            current_risks = await self._analyze_current_risks(workflow_state, risk_factors)
            
            # Predict future bottlenecks
            predicted_bottlenecks = await self._predict_bottlenecks(
                workflow_state,
                similar_projects
            )
            
            # Generate mitigation strategies
            mitigations = await self._generate_mitigations(
                current_risks,
                predicted_bottlenecks,
                similar_projects
            )
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(current_risks, predicted_bottlenecks)
            
            result = {
                "risk_score": risk_score,
                "risk_level": self._get_risk_level(risk_score),
                "current_risks": current_risks,
                "predicted_bottlenecks": predicted_bottlenecks,
                "mitigations": mitigations,
                "similar_projects_analyzed": len(similar_projects),
                "confidence": self._calculate_confidence(similar_projects)
            }
            
            self.update_context("risk_assessment", result)
            self.update_status("completed")
            
            return self.format_output(result, {
                "task_type": "risk_assessment",
                "risk_score": risk_score
            })
            
        except Exception as e:
            self.update_status("failed")
            logger.error(f"Risk assessment failed: {e}")
            return self.format_output(
                {"error": str(e)},
                {"task_type": "risk_assessment", "error": True}
            )
    
    async def _find_similar_projects(
        self,
        workflow_state: Dict[str, Any],
        current_project_id: Optional[int]
    ) -> List[Dict[str, Any]]:
        """Find similar past projects using semantic search"""
        # Extract key characteristics from workflow state
        search_query = self._extract_search_query(workflow_state)
        
        # Search memory for similar projects
        similar = memory_manager.search(
            query=search_query,
            top_k=10,
            filter_metadata={"type": "project"}
        )
        
        # Filter out current project
        if current_project_id:
            similar = [s for s in similar if s["metadata"].get("project_id") != current_project_id]
        
        return [s["metadata"] for s in similar[:5]]
    
    def _extract_search_query(self, workflow_state: Dict[str, Any]) -> str:
        """Extract searchable query from workflow state"""
        parts = []
        
        if "feature" in workflow_state:
            parts.append(workflow_state["feature"])
        if "market" in workflow_state:
            parts.append(workflow_state["market"])
        if "workflow_type" in workflow_state:
            parts.append(workflow_state["workflow_type"])
        
        return " ".join(parts) if parts else "product management workflow"
    
    async def _analyze_current_risks(
        self,
        workflow_state: Dict[str, Any],
        known_risk_factors: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze current workflow state for immediate risks"""
        risks = []
        
        # Check for common risk patterns
        for pattern in self.risk_patterns:
            if pattern["detector"](workflow_state):
                risks.append({
                    "type": pattern["type"],
                    "severity": pattern["severity"],
                    "description": pattern["description"],
                    "detected_at": datetime.now().isoformat()
                })
        
        # Check known risk factors
        for factor in known_risk_factors:
            risks.append({
                "type": "known_risk",
                "severity": "medium",
                "description": factor,
                "detected_at": datetime.now().isoformat()
            })
        
        # Use Nemotron for deeper analysis
        if workflow_state:
            nemotron_analysis = await self._nemotron_risk_analysis(workflow_state)
            risks.extend(nemotron_analysis)
        
        return risks
    
    async def _nemotron_risk_analysis(
        self,
        workflow_state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Use Nemotron to identify subtle risks"""
        prompt = f"""
        Analyze this product management workflow state for potential risks:
        
        {workflow_state}
        
        Identify:
        1. Timeline risks (is the schedule realistic?)
        2. Resource risks (are there dependencies that could block progress?)
        3. Quality risks (are acceptance criteria clear enough?)
        4. Market risks (has the market changed since planning?)
        5. Technical risks (are there technical unknowns?)
        
        For each risk, provide:
        - Risk type
        - Severity (high/medium/low)
        - Description
        - Early warning signs
        
        Be specific and actionable.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="risk_analysis",
            priority="high",
            max_tokens=1000
        )
        
        # Parse Nemotron response into structured risks
        return self._parse_nemotron_risks(response["response"])
    
    def _parse_nemotron_risks(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse Nemotron response into structured risk objects"""
        risks = []
        lines = response_text.split("\n")
        
        current_risk = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for risk indicators
            if "risk" in line.lower() and ":" in line:
                if current_risk:
                    risks.append(current_risk)
                current_risk = {
                    "type": "nemotron_identified",
                    "severity": "medium",
                    "description": line,
                    "detected_at": datetime.now().isoformat()
                }
            elif current_risk and ("severity" in line.lower() or "high" in line.lower() or "medium" in line.lower() or "low" in line.lower()):
                if "high" in line.lower():
                    current_risk["severity"] = "high"
                elif "low" in line.lower():
                    current_risk["severity"] = "low"
        
        if current_risk:
            risks.append(current_risk)
        
        return risks if risks else [{
            "type": "general_risk",
            "severity": "medium",
            "description": "Workflow complexity may introduce unexpected challenges",
            "detected_at": datetime.now().isoformat()
        }]
    
    async def _predict_bottlenecks(
        self,
        workflow_state: Dict[str, Any],
        similar_projects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Predict future bottlenecks based on patterns"""
        bottlenecks = []
        
        # Analyze similar projects for common bottlenecks
        if similar_projects:
            common_bottlenecks = self._extract_common_bottlenecks(similar_projects)
            bottlenecks.extend(common_bottlenecks)
        
        # Use Nemotron to predict based on current state
        prediction = await self._nemotron_bottleneck_prediction(workflow_state, similar_projects)
        bottlenecks.extend(prediction)
        
        return bottlenecks
    
    def _extract_common_bottlenecks(
        self,
        similar_projects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract common bottlenecks from similar projects"""
        bottlenecks = []
        
        # Look for patterns in project metadata
        failed_steps = []
        for project in similar_projects:
            if "failed_steps" in project:
                failed_steps.extend(project["failed_steps"])
        
        # Count most common failures
        from collections import Counter
        common_failures = Counter(failed_steps).most_common(3)
        
        for failure, count in common_failures:
            bottlenecks.append({
                "type": "pattern_based_prediction",
                "agent": failure,
                "confidence": min(0.9, count / len(similar_projects)),
                "description": f"Based on {count} similar projects, {failure} step often encounters issues",
                "prevention": f"Add extra validation before {failure} step"
            })
        
        return bottlenecks
    
    async def _nemotron_bottleneck_prediction(
        self,
        workflow_state: Dict[str, Any],
        similar_projects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Use Nemotron to predict bottlenecks"""
        prompt = f"""
        Based on this workflow state and similar past projects, predict potential bottlenecks:
        
        Current Workflow: {workflow_state}
        Similar Projects: {len(similar_projects)} projects analyzed
        
        Predict:
        1. Which workflow steps are likely to take longer than expected?
        2. What dependencies could cause blocking?
        3. What resource constraints might appear?
        4. What quality issues might emerge?
        
        Provide specific, actionable predictions with confidence levels.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="risk_analysis",
            priority="medium",
            max_tokens=800
        )
        
        return self._parse_bottleneck_predictions(response["response"])
    
    def _parse_bottleneck_predictions(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse bottleneck predictions from Nemotron"""
        bottlenecks = []
        
        # Simple parsing - look for agent names and issues
        for agent_name in ["research", "strategy", "dev", "prototype", "gtm", "automation", "regulation"]:
            if agent_name in response_text.lower():
                bottlenecks.append({
                    "type": "nemotron_prediction",
                    "agent": agent_name,
                    "confidence": 0.7,
                    "description": f"Potential bottleneck identified in {agent_name} step",
                    "prevention": "Monitor this step closely and prepare alternatives"
                })
        
        return bottlenecks if bottlenecks else []
    
    async def _generate_mitigations(
        self,
        current_risks: List[Dict[str, Any]],
        predicted_bottlenecks: List[Dict[str, Any]],
        similar_projects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate mitigation strategies"""
        mitigations = []
        
        # Generate mitigations for high-severity risks
        high_risks = [r for r in current_risks if r.get("severity") == "high"]
        for risk in high_risks:
            mitigation = await self._generate_mitigation_for_risk(risk, similar_projects)
            mitigations.append(mitigation)
        
        # Generate mitigations for predicted bottlenecks
        for bottleneck in predicted_bottlenecks:
            if bottleneck.get("confidence", 0) > 0.7:
                mitigation = {
                    "for": bottleneck.get("agent"),
                    "strategy": bottleneck.get("prevention", "Monitor closely"),
                    "priority": "high" if bottleneck.get("confidence", 0) > 0.8 else "medium"
                }
                mitigations.append(mitigation)
        
        return mitigations
    
    async def _generate_mitigation_for_risk(
        self,
        risk: Dict[str, Any],
        similar_projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate specific mitigation for a risk"""
        prompt = f"""
        Risk identified: {risk.get('description')}
        Risk type: {risk.get('type')}
        Severity: {risk.get('severity')}
        
        Similar projects analyzed: {len(similar_projects)}
        
        Suggest a specific, actionable mitigation strategy. Include:
        1. Immediate actions to take
        2. Monitoring steps
        3. Contingency plan
        
        Be practical and specific.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="risk_analysis",
            priority="medium",
            max_tokens=500
        )
        
        return {
            "for_risk": risk.get("type"),
            "strategy": response["response"],
            "priority": "high" if risk.get("severity") == "high" else "medium"
        }
    
    def _calculate_risk_score(
        self,
        current_risks: List[Dict[str, Any]],
        predicted_bottlenecks: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall risk score (0-1, higher = more risky)"""
        score = 0.0
        
        # Weight current risks
        for risk in current_risks:
            severity_weight = {"high": 0.4, "medium": 0.2, "low": 0.1}.get(risk.get("severity", "medium"), 0.2)
            score += severity_weight
        
        # Weight predicted bottlenecks
        for bottleneck in predicted_bottlenecks:
            confidence = bottleneck.get("confidence", 0.5)
            score += confidence * 0.15
        
        # Normalize to 0-1
        return min(1.0, score)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level"""
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _calculate_confidence(self, similar_projects: List[Dict[str, Any]]) -> float:
        """Calculate confidence in risk assessment based on data quality"""
        if len(similar_projects) >= 5:
            return 0.9
        elif len(similar_projects) >= 3:
            return 0.7
        elif len(similar_projects) >= 1:
            return 0.5
        else:
            return 0.3
    
    def _load_risk_patterns(self) -> List[Dict[str, Any]]:
        """Load predefined risk detection patterns"""
        return [
            {
                "type": "missing_context",
                "severity": "high",
                "description": "Workflow lacks sufficient context for execution",
                "detector": lambda state: not state.get("feature") and not state.get("requirements")
            },
            {
                "type": "tight_timeline",
                "severity": "medium",
                "description": "Timeline appears aggressive for scope",
                "detector": lambda state: state.get("timeline_days", 999) < 14
            },
            {
                "type": "undefined_requirements",
                "severity": "high",
                "description": "Requirements are vague or undefined",
                "detector": lambda state: not state.get("requirements") or len(state.get("requirements", [])) == 0
            },
            {
                "type": "market_uncertainty",
                "severity": "medium",
                "description": "Market research incomplete or outdated",
                "detector": lambda state: not state.get("market_research_complete", False)
            }
        ]


