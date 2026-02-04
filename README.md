# Elements of Agentic System Design

*A Conceptual Framework for the Design of Intelligent Systems from First Principles*

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**[Read the complete framework](complete-elements.md)** | **[Raw text (LLM-friendly)](https://raw.githubusercontent.com/idyllic-labs/elements-of-agentic-system-design/main/complete-elements.md)**

**Who this is for:** This is a design space map for people building agent frameworks, languages, SDKs, and platforms. It shows what users expect from agents, the code patterns that implement those expectations, and where agentic system designs vary.

Also useful for practitioners building agents on these systems, and for readers who want to understand how agentic systems map to concrete software components. Some familiarity with LLMs and software systems is assumed.

This repository contains the outline for **a forthcoming book**. **Interested in co-authoring?** Reach out to **william@idylliclabs.com**.

![The Three Layers](assets/three-layers-overview.png)

## Contents

- [The 10 Elements](#the-10-elements)
- [What This Framework Provides](#what-this-framework-provides)
- [Motivation](#motivation)
- [Key Relationships](#key-relationships)
- [Quick Reference: Behavior → Implementation](#quick-reference-behavior--implementation)
- [Claude Code Skill](#claude-code-skill)
- [Related Work & Influences](#related-work--influences)
- [Contributing](#contributing)
- [License](#license)

## The 10 Elements

| # | Element | What it is | Where capability lives |
|---|---------|------------|------------------------|
| 1 | [**Context**](elements/1-context.md) | Information available to the model for a single call | Token budget + context construction |
| 2 | [**Memory**](elements/2-memory.md) | External storage for selective retrieval into context | Storage structures + retrieval mechanisms |
| 3 | [**Agency**](elements/3-agency.md) | Translation layer from text to effects | Execution boundary + policy enforcement |
| 4 | [**Reasoning**](elements/4-reasoning.md) | Grammar of call composition (chaining, looping, branching) | Call structure + interstitial computation |
| 5 | [**Coordination**](elements/5-coordination.md) | Communication and sequencing between reasoning structures | Execution flow + data flow |
| 6 | [**Artifacts**](elements/6-artifacts.md) | Shared persistent state for coordination | Typed objects + operations + lifecycle |
| 7 | [**Autonomy**](elements/7-autonomy.md) | What triggers execution, who owns the main loop | Trigger infrastructure + context reconstruction |
| 8 | [**Evaluation**](elements/8-evaluation.md) | Determining whether the system succeeded | Quality signals + measurement functions |
| 9 | [**Feedback**](elements/9-feedback.md) | Gradient signals that steer behavior | Signal sources + injection points |
| 10 | [**Learning**](elements/10-learning.md) | Feedback that persists to change future behavior | Learnable parameters + extraction pipeline |


## What This Framework Provides

The 10 elements are indexed on **intuitive notions of intelligence**, not implementation categories. Each element is named for the behavior its code patterns produce.

### A Conceptual Map
Defined terms for each element (context, memory, agency, etc.) and the mechanisms that implement them.

### An Analysis Tool
A way to **take apart any agentic system**. Given an agent, you can break it down into these 10 elements and understand how it works mechanistically.

### A Debugging Framework
When something isn't working, the elements help you **isolate the problem**:
- Agent forgetting things? → Context or Memory problem
- Agent not doing what you want? → Agency or Reasoning problem
- Agents stepping on each other? → Coordination or Artifacts problem
- Agent not improving? → Evaluation, Feedback, or Learning problem

### Behavior-to-Code Mapping
For each observed behavior, the framework names the corresponding code pattern.

## Motivation

This framework came from building agent frameworks and platforms, and from the frustration of working in a space that moves fast but lacks conceptual grounding. The excitement around the technology leads people to conflate model capability with system intelligence. As models improve, the bottleneck shifts to system design, but there's no shared vocabulary for where things should go.

When you want to implement something smart in an agentic system, you need to know where it belongs: is it a context problem, a memory problem, a coordination problem? Without a clean conceptual framework, every design decision feels ad hoc. You end up reinventing patterns or mislocating functionality because there's no map of the design space.

This framework provides that map. The model is a stateless text-to-text function. Everything else (memory, agency, reasoning, coordination, learning) is architecture you build around it. Every intelligent-seeming behavior traces to concrete code: loops, database queries, schedulers, policy checks. Once you see this, agentic systems become software you design, inspect, and debug like any other program.

![The Basic Agent Loop](diagrams/agent-loop.svg)

## Key Relationships

![The Externalization Pattern](assets/externalization-pattern.png)

A recurring **externalization pattern** appears throughout the framework:
- **Memory** = externalized context (storage for a single agent)
- **Artifacts** = externalized coordination (shared state for multiple agents)
- **Learning** = externalized feedback (patterns stored for future behavior)

**The improvement stack:**
- **Evaluation** measures quality
- **Feedback** steers the current task
- **Learning** persists feedback to steer future tasks

## Quick Reference: Behavior → Implementation

Each behavior in the left column corresponds to a concrete implementation pattern in the right column.

| "It seems to..." | Actually is... |
|------------------|----------------|
| Remember what I said | Conversation history array in prompt |
| Have long-term memory | Database + retrieval into context |
| Do things in the world | Structured output → parser → function dispatch |
| Think step by step | Multiple calls with state passed between |
| Plan before acting | `plan = llm(task)` → `for step in plan: execute(step)` |
| Check its own work | Generate → separate verify call → conditional retry |
| Have multiple experts | Different system prompts routed by classifier |
| Work while I sleep | Cron job triggers agent |
| Learn from experience | Outcomes → extraction → stored → retrieved into future contexts |

## Claude Code Skill

This repository includes a [Claude Code](https://claude.ai/claude-code) skill that lets you analyze and design agentic systems using this framework.

### Installation

**Personal (all your projects):**
```bash
mkdir -p ~/.claude/skills/intelligence-designer
curl -o ~/.claude/skills/intelligence-designer/SKILL.md \
  https://raw.githubusercontent.com/idyllic-labs/elements-of-agentic-system-design/main/SKILL.md
```

**Project-specific:**
```bash
mkdir -p .claude/skills/intelligence-designer
curl -o .claude/skills/intelligence-designer/SKILL.md \
  https://raw.githubusercontent.com/idyllic-labs/elements-of-agentic-system-design/main/SKILL.md
```

### Usage

Once installed, use the skill in Claude Code:

```
/intelligence-designer Analyze how Claude Code handles context management

/intelligence-designer How does a typical RAG chatbot work?

/intelligence-designer Design an agent that monitors GitHub issues and auto-triages them
```

The skill injects the full framework into context and guides Claude to think mechanistically about agentic systems, tracing behaviors to code patterns, identifying elements, and spotting tradeoffs.

## Related Work & Influences

This framework builds on and is influenced by the following resources:

### Foundational Reading

- **[Intelligence Design](https://www.wcdc.io/writing/intelligence-design)** — Argues that intelligent behavior in AI systems is designed, not emergent. Understanding agentic systems means understanding the architecture that produces intelligent-seeming behavior.

### Analyses

- **[OpenClaw vs Claude Code](https://www.wcdc.io/writing/openclaw-vs-cc)** — An analysis of two agentic coding systems using this framework.

### Prior Art

- **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic, 2024) — Anthropic's guide to building agents with simple, composable patterns. Emphasizes starting simple and only adding complexity when needed. Introduces workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.

- **[12-Factor Agents](https://github.com/humanlayer/12-factor-agents)** (HumanLayer) — Principles for building production-ready LLM applications, inspired by Heroku's 12-Factor App methodology. Key insights: own your prompts, manage context windows explicitly, own your control flow, small focused agents beat monoliths.

- **[Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)** (Andrew Ng, 2024) — Four key patterns: Reflection, Tool Use, Planning, and Multi-Agent Collaboration. Helped popularize the term "agentic" in the AI community.

- **[Agentic Design Patterns: A System-Theoretic Framework](https://arxiv.org/abs/2601.19752)** (arXiv, 2025) — Academic framework decomposing agentic systems into five functional subsystems: Reasoning & World Model, Perception & Grounding, Action Execution, Learning & Adaptation, and Inter-Agent Communication.

### How This Framework Differs

The above resources focus on **how to build** agents (patterns, best practices, implementation). This framework focuses on **analyzing** agents: decomposing their behavior into elements and mapping each to specific code patterns.

## Contributing

Contributions are welcome! This is an open project and we appreciate help from the community.

### Ways to Contribute

- **Report issues** — Found an error or unclear explanation? Open an issue.
- **Suggest improvements** — Have ideas for better examples or clearer framing? Let us know.
- **Add examples** — Real-world case studies that illustrate the elements are valuable.
- **Translate** — Help make this framework accessible in other languages.

### Co-Authorship

This outline will be expanded into a book. If you're interested in co-authoring or making substantial contributions, please contact **william@idylliclabs.com** with:
- Your background and expertise
- Which elements you're interested in contributing to
- Any relevant writing samples or prior work

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, including commercially

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

## Attribution

**Elements of Agentic System Design**

A project by [Idyllic Labs](https://idyllic.so).

Created by [William Chen](https://twitter.com/stablechen), based on over two years of experience building agentic systems.

AI tools assisted in the editing and structuring of this work, primarily Claude Opus 4.5 (Anthropic) and GPT-5.2 (OpenAI).

## Contact

- **Email**: william@idylliclabs.com
- **Twitter**: [@stablechen](https://twitter.com/stablechen)
