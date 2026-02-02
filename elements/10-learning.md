## Element 10: LEARNING

> **Draft** — This outline is still being developed. Information may be incomplete; expect changes before finalization.

---

### Introduction

**What it is:** Feedback that persists beyond the current task to change future behavior. Learning is **externalized feedback in memory** — where Element 9 (Feedback) steers within a task, learning stores what was learned so it can steer future tasks.

**Why it's foundational:** The model's weights are frozen. Every API call hits the same parameters. Yet systems clearly improve over time — fewer mistakes, better handling of edge cases, adapted to user preferences. This improvement doesn't come from the model learning; it comes from changing what surrounds the model: prompts, examples, routing rules, knowledge, configuration. Learning is the mechanism that converts experience into these persistent changes.

**What it looks like:** Data flows from observation to storage to future behavior:
```
Feedback (current task)
    ↓
Collection (logs, outcomes, corrections)
    ↓
Extraction (data → parameter updates)
    ↓
Storage (prompts, examples, routing, config)
    ↓
Reconstruction (retrieved into future contexts)
    ↓
[Changed behavior on future tasks]
```

The model doesn't learn. The system learns by changing the learnable parameters that shape what the model sees.

---

### Demystification

#### Intelligent Behaviors → Code Patterns

| Behavior (looks like) | Implementation (actually is) |
|----------------------|------------------------------|
| "Gets better over time" | Prompts/examples updated based on logged outcomes |
| "Learns my preferences" | User feedback → preference store → injected into future prompts |
| "Remembers what works" | High-scoring outputs stored as few-shot examples |
| "Doesn't repeat mistakes" | Failure patterns extracted → added to system prompt as warnings |
| "Adapts to new domains" | Domain knowledge accumulated in retrieval store |
| "Improves at specific tasks" | Task-specific examples curated and retrieved |
| "Rewrites its own behavior" | Metaprogramming: system modifies its own prompts/routing/code |

#### The Core Mechanism

**The model is frozen; the wrapper learns.** The base model doesn't change between calls. All improvement comes from changing what surrounds it: the prompts it receives, the examples it sees, the routing that selects which prompt to use, the knowledge retrieved into context.

**Learning = feedback + persistence + reconstruction.** Feedback tells you what went right or wrong on a task. Learning stores that information and reconstructs it into future contexts so the system behaves differently next time.

**Learnable parameters are the configuration points.** Just like neural network weights are the learnable parameters of a model, agentic systems have their own learnable parameters:
- **Prompts:** System instructions that can be updated
- **Examples:** Few-shot demonstrations that can be added/removed
- **Routing rules:** Which agent/prompt handles which queries
- **Configuration:** Thresholds, parameters, limits
- **Knowledge:** Facts, procedures, documentation in retrieval stores
- **Code:** The system can modify its own logic (metaprogramming)

**Memory vs Learning:** Memory stores raw episodes. Learning extracts reusable patterns that change behavior. Storing "user asked X, system responded Y" is memory. Extracting "when users ask about billing, always confirm account ID first" is learning.

---

### Design Considerations

#### Key Questions

**1. Where are the learnable parameters?**

Identify what can change from experience — the configuration points that learning can update.

- **Prompts/instructions:** System prompts that define behavior. Can be edited based on observed failures or successes.
- **Examples:** Few-shot demonstrations retrieved into context. Can be added, removed, or reweighted.
- **Routing rules:** Which agent or prompt handles which query types. Can be updated based on success patterns.
- **Configuration:** Thresholds, limits, feature flags. Can be tuned based on observed performance.
- **Knowledge stores:** Facts, procedures, documentation. Can grow or be corrected.
- **Code itself:** The system can rewrite its own prompts, routing logic, or tool implementations (metaprogramming).

The more parameters are learnable, the more the system can adapt. But each learnable parameter is also a potential source of drift or degradation.

Look for: What can change in this system? What's hardcoded vs configurable? Where would you update if you wanted the system to behave differently on a class of inputs?

**2. How is data collected?**

Identify what observations feed the learning process.

- **Outcomes:** Success/failure signals, scores, test results
- **Feedback:** User corrections, ratings, explicit preferences
- **Traces:** Full execution logs, tool calls, intermediate states
- **Corrections:** Human-provided fixes to system outputs

Collection can be passive (log everything) or selective (only log interesting cases). The quality of learning depends on the quality of data — garbage in, garbage out.

Look for: What gets logged? What feedback channels exist? Is there human-in-the-loop correction? How much signal vs noise is in the collected data?

**3. How does data become parameter updates?**

Identify the extraction pipeline — how raw observations turn into changes to learnable parameters.

- **Direct storage:** High-scoring outputs become examples directly
- **Pattern extraction:** LLM analyzes failures and proposes prompt changes
- **Aggregation:** Many observations combined before making updates (avoid overreacting to single cases)
- **Human curation:** People review proposed changes before they're applied

The extraction mechanism determines what the system actually learns. Poor extraction means the system stores noise or learns wrong lessons.

Look for: What transforms raw data into parameter updates? Is there aggregation or smoothing? Who or what decides what gets learned?

**4. How are updates reconstructed into behavior?**

Identify how stored learning affects future tasks — the path from storage to context.

- **Retrieval:** Relevant examples/knowledge fetched based on current query
- **Injection:** Retrieved content added to prompt before model call
- **Routing:** Query classified and sent to appropriate (learned) handler
- **Configuration:** Parameters read at runtime to control behavior

Learning only affects behavior if it's reconstructed into context. Stored patterns that never get retrieved are inert.

Look for: How do stored updates get into the prompt? What retrieval mechanism selects relevant learned content? Is there a gap between what's stored and what's used?

**5. How is learning validated?**

Identify how the system ensures updates improve rather than degrade performance.

- **Holdout evaluation:** Test changes against held-out examples before deploying
- **A/B testing:** Run old and new configurations in parallel, compare metrics
- **Rollback capability:** Ability to revert if changes cause problems
- **Regression monitoring:** Track whether old capabilities still work after updates

Without validation, learning can drift toward worse behavior — overfitting to recent cases, accumulating contradictory rules, or degrading on edge cases.

Look for: How do you know if a learned update actually helps? Can changes be reverted? Is there monitoring for regression?

**6. How is accumulation managed?**

Identify how the system handles growth over time — selection, staleness, and forgetting.

- **Selection:** Store many candidates, retrieve few (learning is a retrieval problem)
- **Staleness:** Old patterns may no longer apply; need age penalties or expiration
- **Forgetting:** Actively remove outdated or superseded content
- **Compression:** Many examples condensed into canonical archetypes

Without management, learned content accumulates and conflicts: old patterns can contradict new ones, and the context window becomes cluttered with outdated information.

Look for: Does learned content have expiration? How is relevance scored for retrieval? Is there periodic cleanup or compression? What prevents unbounded growth?

#### Key Tradeoffs

| Tradeoff | Tension |
|----------|---------|
| More learnable parameters vs stability | Adaptability vs predictability |
| Aggressive vs conservative updates | Fast learning vs avoiding bad lessons |
| Store everything vs curate tightly | Coverage vs noise |
| Real-time vs periodic updates | Responsiveness vs stability |

#### Patterns

- **Example managers:** Store many, retrieve few based on similarity/recency/quality
- **Lesson extraction:** LLM analyzes outcomes and proposes reusable rules
- **Nightly reflection:** Scheduled job analyzes recent performance and updates prompts
- **Human-in-the-loop curation:** People review before learned content goes live
- **A/B testing for updates:** Validate changes improve metrics before full rollout

---

### The Reframe

**Before:** "Why doesn't it learn from its mistakes?"
**After:** "Where are the learnable parameters, and how does feedback flow into them?"

**Before:** "The system should get smarter over time."
**After:** "What data is collected, how is it extracted into updates, and how are updates validated?"

**Before:** "It keeps making the same errors."
**After:** "Either the error pattern isn't being captured, or captured patterns aren't being reconstructed into future contexts."
