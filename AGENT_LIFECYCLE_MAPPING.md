# Agent Lifecycle Order and Nemotron Model Mapping

## Product Management Lifecycle Order

Agents are ordered according to the Product Management Lifecycle, ensuring a logical flow from ideation to launch and ongoing operations.

### Lifecycle Stages

1. **Strategy Agent** - Ideation & Strategy
   - Market sizing, idea generation, competitive analysis
   - **Nemotron Model**: `nvidia/nemotron-4-340b-instruct`
   - **Reasoning**: Complex strategic reasoning and market analysis requires the large 340B model

2. **Research Agent** - Research & Validation
   - User research, competitor analysis, trend analysis, data synthesis
   - **Nemotron Model**: `nvidia/nemotron-4-70b-instruct`
   - **Reasoning**: Fast data analysis and research synthesis benefits from the faster 70B model

3. **Prioritization Agent** - Feature Prioritization
   - Multi-factor prioritization, roadmap planning, value/effort analysis
   - **Nemotron Model**: `nvidia/nemotron-4-340b-instruct`
   - **Reasoning**: Complex decision-making with multiple factors requires the large model

4. **Risk Assessment Agent** - Risk Assessment
   - Risk identification, mitigation planning, pattern recognition
   - **Nemotron Model**: `nvidia/nemotron-4-340b-instruct`
   - **Reasoning**: Complex risk pattern recognition and analysis requires advanced reasoning

5. **Regulation Agent** - Compliance & Regulation
   - Compliance checks, regulatory requirements, audit reports
   - **Nemotron Model**: `nvidia/nemotron-4-340b-instruct`
   - **Reasoning**: Complex compliance reasoning and regulatory analysis requires deep understanding

6. **Development Agent** - Development Planning
   - User stories, backlog generation, technical specifications, sprint planning
   - **Nemotron Model**: `nvidia/nemotron-4-70b-instruct`
   - **Reasoning**: Faster code generation and technical documentation benefits from the 70B model

7. **Prototype Agent** - Design & Prototyping
   - Wireframes, mockups, design systems, Figma integration
   - **Nemotron Model**: `nvidia/nemotron-4-70b-instruct`
   - **Reasoning**: Design understanding and UI/UX tasks benefit from faster processing

8. **GTM Agent** - Go-to-Market
   - Launch planning, marketing strategy, pricing, messaging
   - **Nemotron Model**: `nvidia/nemotron-4-340b-instruct`
   - **Reasoning**: Complex strategic planning and market strategy requires the large model

9. **Automation Agent** - Automation & Monitoring
   - Sprint summaries, standup reports, workflow automation, metrics
   - **Nemotron Model**: `nvidia/nemotron-4-70b-instruct`
   - **Reasoning**: Routine task automation and reporting benefits from faster processing

## Model Selection Strategy

### Nemotron-4-340B-Instruct (Large Model)
**Used for**: Strategy, Prioritization, Risk Assessment, Regulation, GTM

**Characteristics**:
- Complex reasoning capabilities
- Strategic planning and analysis
- Multi-factor decision making
- Pattern recognition
- Regulatory and compliance analysis

### Nemotron-4-70B-Instruct (Faster Model)
**Used for**: Research, Development, Prototype, Automation

**Characteristics**:
- Faster response times
- Code generation
- Data analysis and synthesis
- Design understanding
- Routine task automation

## Implementation Details

### Agent Configuration
- Each agent is assigned a `lifecycle_stage` number (1-9)
- Each agent has an assigned `nemotron_model` based on its purpose
- Agents can override the default model if needed

### Task Graph Ordering
- Agents are automatically ordered by lifecycle stage in `TaskGraph`
- Workflows respect the lifecycle order
- Parallel execution is possible for independent stages

### Model Usage
- Agents use their assigned model when calling Nemotron
- Model selection is automatic based on agent type
- Fallback to local LLM if Nemotron is unavailable
- Budget-aware model selection (cost orchestrator)

## Benefits

1. **Logical Flow**: Agents execute in the natural order of product management
2. **Optimal Performance**: Each agent uses the most suitable model for its tasks
3. **Cost Efficiency**: Faster models used for routine tasks, large models for complex reasoning
4. **Flexibility**: Model assignments can be easily adjusted per agent
5. **Scalability**: System supports adding new agents with appropriate model assignments

## Usage

```python
from agents.agent_config import get_agents_in_lifecycle_order, get_agent_model

# Get agents in lifecycle order
agents = get_agents_in_lifecycle_order()
# Returns: ['strategy', 'research', 'prioritization', 'risk', 'regulation', 'dev', 'prototype', 'gtm', 'automation']

# Get model for specific agent
model = get_agent_model('strategy')
# Returns: 'nvidia/nemotron-4-340b-instruct'
```

## Future Enhancements

- Support for additional Nemotron models as they become available
- Dynamic model selection based on task complexity
- Model performance metrics and optimization
- Agent-specific temperature and token limits
- Cost tracking per agent and model type

