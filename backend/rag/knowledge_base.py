"""
Knowledge Base Seeding for Research Agent

Contains curated market trends, user insights, and PM best practices.
"""

# Market Research & Trends
MARKET_KNOWLEDGE = [
    {
        "id": "market_ai_pm_tools_2024",
        "text": """AI-Powered Product Management Tools Market Analysis 2024:
        
        Market Size: $400M-$500M globally, growing at 28% CAGR
        Key Players: Aha!, Productboard, Canny, Amplitude, Mixpanel
        Adoption Rate: 35% of B2B SaaS companies use AI-enhanced PM tools
        
        Top Trends:
        - Predictive analytics for roadmap planning
        - AI-driven user feedback categorization
        - Automated prioritization using RICE/ICE frameworks
        - Natural language PRD generation
        - Integration with design tools (Figma, Sketch)
        
        User Pain Points:
        - Manual data consolidation across tools
        - Difficulty quantifying feature impact
        - Time-consuming stakeholder alignment
        - Lack of real-time insights""",
        "metadata": {
            "category": "market_trends",
            "topic": "ai_tools",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "saas_user_research_2024",
        "text": """B2B SaaS User Research Insights 2024:
        
        Primary User Personas:
        1. Product Managers (50-500 employee companies)
           - Age: 28-42, Tech-savvy
           - Pain: Too much time in meetings, need data-driven decisions
           - Goal: Ship features faster with higher confidence
        
        2. Product Leaders/Directors
           - Age: 35-50, Strategic focus
           - Pain: Difficulty aligning teams on priorities
           - Goal: Demonstrate ROI, optimize team velocity
        
        3. Founders/Startup PMs
           - Age: 25-40, Wear multiple hats
           - Pain: Limited resources, need to validate quickly
           - Goal: Find product-market fit faster
        
        Common Workflows:
        - Weekly sprint planning (3-5 hours)
        - Quarterly roadmap reviews
        - User feedback triage (daily)
        - Stakeholder updates""",
        "metadata": {
            "category": "user_research",
            "topic": "personas",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "pm_prioritization_frameworks_2024",
        "text": """Product Prioritization Frameworks - Usage Analysis 2024:
        
        Most Popular Frameworks:
        1. RICE (Reach, Impact, Confidence, Effort) - 42% adoption
           - Best for: Data-driven teams with clear metrics
           - Pros: Quantitative, reduces bias
           - Cons: Requires good data, time-intensive
        
        2. Value vs Effort Matrix - 31% adoption
           - Best for: Quick decisions, startups
           - Pros: Simple, visual, fast
           - Cons: Subjective, lacks nuance
        
        3. Kano Model - 18% adoption
           - Best for: Understanding customer satisfaction
           - Pros: User-centric, reveals delighters
           - Cons: Complex surveys needed
        
        Emerging Trend: AI-assisted scoring
        - 23% of teams now use ML models to predict feature impact
        - Combines historical data with market signals""",
        "metadata": {
            "category": "best_practices",
            "topic": "prioritization",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "ai_adoption_barriers_2024",
        "text": """Barriers to AI Tool Adoption in Product Management 2024:
        
        Top Concerns:
        1. Data Privacy & Security (67%)
           - Especially for enterprise customers
           - GDPR, SOC2 compliance required
        
        2. Integration Complexity (54%)
           - Need to work with existing tools (Jira, Slack, Figma)
           - API limitations and data silos
        
        3. Learning Curve (48%)
           - Teams resist changing workflows
           - Need clear ROI demonstration
        
        4. Cost Justification (41%)
           - Budget constraints in current economy
           - Need to prove 3x+ productivity gain
        
        Success Factors:
        - Free trial with real data
        - Template library for quick starts
        - Strong Slack/Teams integration
        - Clear before/after metrics""",
        "metadata": {
            "category": "market_trends",
            "topic": "adoption_barriers",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "remote_pm_trends_2024",
        "text": """Remote Product Management Trends 2024:
        
        Key Statistics:
        - 73% of PM teams are hybrid/remote
        - Async collaboration tools usage up 156%
        - Average meetings reduced from 18 to 12 per week
        
        Tool Preferences:
        1. Communication: Slack (68%), Teams (24%)
        2. Documentation: Notion (42%), Confluence (31%)
        3. Design: Figma (81%), Miro (43%)
        4. Analytics: Amplitude (34%), Mixpanel (28%)
        
        Challenges:
        - Maintaining team alignment (62%)
        - Reduced serendipitous insights (54%)
        - Timezone coordination (47%)
        
        Solutions:
        - Async decision-making frameworks
        - Recorded video updates
        - Collaborative documentation
        - AI-powered meeting summaries""",
        "metadata": {
            "category": "trends",
            "topic": "remote_work",
            "date": "2024-11",
            "relevance": "medium"
        }
    },
    {
        "id": "prd_best_practices_2024",
        "text": """PRD (Product Requirements Document) Best Practices 2024:
        
        Modern PRD Structure:
        1. Executive Summary (1-2 paragraphs)
        2. Problem Statement (user pain points with data)
        3. Goals & Success Metrics (quantifiable OKRs)
        4. User Stories & Use Cases
        5. Requirements (functional & non-functional)
        6. Design Mockups/Wireframes
        7. Technical Considerations
        8. Launch Plan & Timeline
        9. Risks & Mitigation
        
        Trends:
        - 68% of teams use templates
        - Average PRD length: 8-12 pages
        - 54% include video walkthroughs
        - 41% use AI for first draft
        
        Common Mistakes:
        - Too much detail upfront (waterfall thinking)
        - No clear success metrics
        - Missing stakeholder sign-off
        - Outdated after first sprint""",
        "metadata": {
            "category": "best_practices",
            "topic": "documentation",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "feature_validation_methods_2024",
        "text": """Feature Validation Methods - Effectiveness Analysis 2024:
        
        Top Validation Techniques:
        
        1. User Interviews (87% usage)
           - Effectiveness: 8.2/10
           - Time: 2-4 weeks
           - Best for: Understanding deep needs
        
        2. A/B Testing (71% usage)
           - Effectiveness: 9.1/10
           - Time: 1-3 weeks
           - Best for: Optimizing existing features
        
        3. Prototype Testing (64% usage)
           - Effectiveness: 8.7/10
           - Time: 1-2 weeks
           - Best for: Early concept validation
        
        4. Analytics Analysis (91% usage)
           - Effectiveness: 7.8/10
           - Time: Ongoing
           - Best for: Identifying drop-off points
        
        5. Surveys (58% usage)
           - Effectiveness: 6.4/10
           - Time: 3-7 days
           - Best for: Quantifying sentiment
        
        ROI: Teams using 3+ validation methods launch 2.3x more successful features""",
        "metadata": {
            "category": "best_practices",
            "topic": "validation",
            "date": "2024-11",
            "relevance": "high"
        }
    },
    {
        "id": "competitive_intelligence_2024",
        "text": """Competitive Intelligence Tools & Techniques 2024:
        
        Popular Tools:
        1. Product Hunt - Track new launches
        2. SimilarWeb - Traffic analysis
        3. G2/Capterra - User reviews
        4. BuiltWith - Tech stack analysis
        5. Social listening - Twitter, Reddit, LinkedIn
        
        Key Metrics to Track:
        - Feature parity
        - Pricing strategy
        - User sentiment (NPS)
        - Market positioning
        - Growth trajectory
        
        Automation Trends:
        - 34% use AI for competitor monitoring
        - Automated alerts on competitor launches
        - Sentiment analysis on reviews
        
        Best Practices:
        - Weekly competitor scans
        - Quarterly deep-dive analysis
        - Focus on differentiation, not copying
        - Track 3-5 direct competitors max""",
        "metadata": {
            "category": "best_practices",
            "topic": "competitive_intelligence",
            "date": "2024-11",
            "relevance": "medium"
        }
    }
]


def get_all_knowledge():
    """Get all knowledge base documents."""
    return MARKET_KNOWLEDGE


def get_knowledge_by_category(category: str):
    """Get knowledge filtered by category."""
    return [doc for doc in MARKET_KNOWLEDGE if doc["metadata"]["category"] == category]

