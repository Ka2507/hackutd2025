"""
Prioritization Agent - Smart multi-factor prioritization with Nemotron reasoning
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .base_agent import BaseAgent
from orchestrator.nemotron_bridge import nemotron_bridge
from utils.logger import logger


class PrioritizationAgent(BaseAgent):
    """Agent specialized in intelligent feature prioritization"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="PrioritizationAgent",
            goal="Prioritize features using multi-factor analysis and data-driven scoring",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute prioritization task
        
        Args:
            task_input: Contains:
                - features: List of features to prioritize
                - context: Market data, user feedback, strategic goals
                - method: Prioritization method (RICE, Value/Effort, Custom)
        """
        self.update_status("running")
        
        features = task_input.get("features", [])
        context = task_input.get("context", {})
        method = task_input.get("method", "multi_factor")
        
        try:
            if method == "rice":
                result = await self._rice_prioritization(features, context)
            elif method == "value_effort":
                result = await self._value_effort_prioritization(features, context)
            else:
                result = await self._multi_factor_prioritization(features, context)
            
            self.update_context("prioritization", result)
            self.update_status("completed")
            
            return self.format_output(result, {
                "task_type": "prioritization",
                "method": method,
                "features_count": len(features)
            })
            
        except Exception as e:
            self.update_status("failed")
            logger.error(f"Prioritization failed: {e}")
            return self.format_output(
                {"error": str(e)},
                {"task_type": "prioritization", "error": True}
            )
    
    async def _multi_factor_prioritization(
        self,
        features: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Multi-factor prioritization with Nemotron reasoning"""
        scored_features = []
        
        for feature in features:
            # Calculate multiple factors
            market_impact = await self._assess_market_impact(feature, context)
            user_value = await self._assess_user_value(feature, context)
            effort = await self._estimate_effort(feature, context)
            risk = await self._assess_risk(feature, context)
            strategic_alignment = await self._check_strategic_alignment(feature, context)
            
            # Weighted score (higher is better)
            score = (
                market_impact * 0.3 +
                user_value * 0.3 +
                (1 - effort) * 0.2 +  # Lower effort = higher score
                (1 - risk) * 0.1 +
                strategic_alignment * 0.1
            )
            
            scored_features.append({
                "feature": feature,
                "score": round(score, 3),
                "factors": {
                    "market_impact": round(market_impact, 3),
                    "user_value": round(user_value, 3),
                    "effort": round(effort, 3),
                    "risk": round(risk, 3),
                    "strategic_alignment": round(strategic_alignment, 3)
                },
                "priority": self._score_to_priority(score)
            })
        
        # Sort by score
        scored_features.sort(key=lambda x: x["score"], reverse=True)
        
        # Use Nemotron to explain ranking
        explanation = await self._generate_explanation(scored_features, context)
        
        return {
            "prioritized_features": scored_features,
            "explanation": explanation,
            "method": "multi_factor",
            "total_features": len(features),
            "recommendations": self._generate_recommendations(scored_features)
        }
    
    async def _assess_market_impact(
        self,
        feature: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Assess market impact (0-1)"""
        # Use Nemotron for strategic assessment
        prompt = f"""
        Assess the market impact of this feature:
        {feature.get('name', feature.get('title', ''))}
        Description: {feature.get('description', '')}
        
        Market Context: {context.get('market_data', {})}
        
        Rate market impact from 0-1 considering:
        - Market size affected
        - Competitive advantage
        - Revenue potential
        - Market timing
        
        Provide a score and brief reasoning.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="prioritization",
            priority="medium",
            max_tokens=300
        )
        
        # Extract score from response (simplified)
        score = self._extract_score_from_response(response["response"])
        return min(1.0, max(0.0, score))
    
    async def _assess_user_value(
        self,
        feature: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Assess user value (0-1)"""
        # Check for user feedback in context
        user_feedback = context.get("user_feedback", [])
        
        # Simple heuristic - in production, use more sophisticated analysis
        if user_feedback:
            # Count mentions of feature-related keywords
            feature_name = feature.get("name", "").lower()
            mentions = sum(1 for feedback in user_feedback if feature_name in feedback.lower())
            score = min(1.0, mentions / 10.0)  # Normalize
        else:
            # Default based on feature type
            score = 0.6 if "core" in feature.get("name", "").lower() else 0.4
        
        return score
    
    async def _estimate_effort(
        self,
        feature: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Estimate effort (0-1, higher = more effort)"""
        # Use story points if available
        story_points = feature.get("story_points", 0)
        if story_points:
            # Normalize: 1-5 points = 0.2, 6-10 = 0.5, 11+ = 0.8
            if story_points <= 5:
                return 0.2
            elif story_points <= 10:
                return 0.5
            else:
                return 0.8
        
        # Estimate based on complexity
        complexity = feature.get("complexity", "medium")
        complexity_map = {"low": 0.3, "medium": 0.5, "high": 0.8}
        return complexity_map.get(complexity, 0.5)
    
    async def _assess_risk(
        self,
        feature: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Assess risk (0-1, higher = more risky)"""
        # Check for known risks
        risks = feature.get("risks", [])
        if risks:
            return min(1.0, len(risks) * 0.3)
        
        # Check dependencies
        dependencies = feature.get("dependencies", [])
        if len(dependencies) > 3:
            return 0.6  # High dependency risk
        
        return 0.3  # Default medium risk
    
    async def _check_strategic_alignment(
        self,
        feature: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Check strategic alignment (0-1)"""
        strategic_goals = context.get("strategic_goals", [])
        if not strategic_goals:
            return 0.5  # Neutral if no goals defined
        
        feature_name = feature.get("name", "").lower()
        alignment_score = 0.0
        
        for goal in strategic_goals:
            goal_lower = goal.lower()
            # Simple keyword matching
            if any(keyword in feature_name for keyword in goal_lower.split()):
                alignment_score += 0.3
        
        return min(1.0, alignment_score)
    
    def _extract_score_from_response(self, response_text: str) -> float:
        """Extract numeric score from Nemotron response"""
        import re
        # Look for numbers between 0 and 1
        matches = re.findall(r'0?\.\d+|0\.\d+|1\.0|1', response_text)
        if matches:
            try:
                return float(matches[0])
            except:
                pass
        
        # Look for percentage
        matches = re.findall(r'(\d+)%', response_text)
        if matches:
            return float(matches[0]) / 100.0
        
        # Default
        return 0.6
    
    async def _generate_explanation(
        self,
        scored_features: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> str:
        """Use Nemotron to explain prioritization"""
        top_features = scored_features[:5]
        
        prompt = f"""
        Explain why these features are prioritized in this order:
        
        {[{'name': f['feature'].get('name', ''), 'score': f['score'], 'factors': f['factors']} for f in top_features]}
        
        Context: {context}
        
        Provide a clear, concise explanation that a product manager can use to justify the prioritization to stakeholders.
        Focus on the key factors that drove the ranking.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="prioritization",
            priority="high",
            max_tokens=500
        )
        
        return response["response"]
    
    def _generate_recommendations(
        self,
        scored_features: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        high_priority = [f for f in scored_features if f["score"] >= 0.7]
        low_priority = [f for f in scored_features if f["score"] < 0.4]
        
        if high_priority:
            recommendations.append(
                f"Focus on {len(high_priority)} high-priority features first"
            )
        
        if low_priority:
            recommendations.append(
                f"Consider deprioritizing {len(low_priority)} low-scoring features"
            )
        
        # Check for high effort, low value
        bad_ratio = [
            f for f in scored_features
            if f["factors"]["effort"] > 0.7 and f["factors"]["user_value"] < 0.4
        ]
        if bad_ratio:
            recommendations.append(
                f"Review {len(bad_ratio)} features with high effort but low value - consider simplifying or deferring"
            )
        
        return recommendations
    
    def _score_to_priority(self, score: float) -> str:
        """Convert score to priority level"""
        if score >= 0.8:
            return "Critical"
        elif score >= 0.6:
            return "High"
        elif score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    async def _rice_prioritization(
        self,
        features: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """RICE framework prioritization"""
        # RICE = (Reach * Impact * Confidence) / Effort
        rice_scores = []
        
        for feature in features:
            reach = feature.get("reach", 1000)  # Users affected
            impact = feature.get("impact", 0.5)  # 0.25, 0.5, 1, 2, 3
            confidence = feature.get("confidence", 0.8)  # 0-1
            effort = feature.get("effort_days", 10)  # Person-days
            
            rice_score = (reach * impact * confidence) / effort if effort > 0 else 0
            
            rice_scores.append({
                "feature": feature,
                "rice_score": round(rice_score, 2),
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort
            })
        
        rice_scores.sort(key=lambda x: x["rice_score"], reverse=True)
        
        return {
            "prioritized_features": rice_scores,
            "method": "RICE",
            "explanation": "RICE prioritization: (Reach × Impact × Confidence) / Effort"
        }
    
    async def _value_effort_prioritization(
        self,
        features: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Value vs Effort matrix prioritization"""
        matrix_features = []
        
        for feature in features:
            value = await self._assess_user_value(feature, context)
            effort = await self._estimate_effort(feature, context)
            
            quadrant = self._get_quadrant(value, effort)
            
            matrix_features.append({
                "feature": feature,
                "value": round(value, 3),
                "effort": round(effort, 3),
                "quadrant": quadrant,
                "recommendation": self._get_quadrant_recommendation(quadrant)
            })
        
        # Sort: Quick wins first, then big bets, then fill-ins, avoid time sinks
        quadrant_order = {"quick_win": 1, "big_bet": 2, "fill_in": 3, "time_sink": 4}
        matrix_features.sort(key=lambda x: quadrant_order.get(x["quadrant"], 5))
        
        return {
            "prioritized_features": matrix_features,
            "method": "Value/Effort Matrix",
            "explanation": "Features plotted on value vs effort matrix"
        }
    
    def _get_quadrant(self, value: float, effort: float) -> str:
        """Determine quadrant in value/effort matrix"""
        if value >= 0.5 and effort < 0.5:
            return "quick_win"
        elif value >= 0.5 and effort >= 0.5:
            return "big_bet"
        elif value < 0.5 and effort < 0.5:
            return "fill_in"
        else:
            return "time_sink"
    
    def _get_quadrant_recommendation(self, quadrant: str) -> str:
        """Get recommendation for quadrant"""
        recommendations = {
            "quick_win": "Do first - high value, low effort",
            "big_bet": "Plan carefully - high value, high effort",
            "fill_in": "Consider if time permits - low value, low effort",
            "time_sink": "Avoid or simplify - low value, high effort"
        }
        return recommendations.get(quadrant, "Review")

