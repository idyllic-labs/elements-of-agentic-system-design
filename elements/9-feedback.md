## Element 9: FEEDBACK

> **Draft** — This outline is still being developed. Information may be incomplete; expect changes before finalization.

---

### Introduction

**What it is:** The gradient signals that steer agent behavior toward better outcomes. Feedback is **evaluation applied inline** — not just measuring quality at the end, but injecting corrective information during execution to keep the model on track.

**Why it's foundational:** A single LLM call has no sense of whether it's succeeding. It generates tokens based on context, with no built-in correction mechanism. Feedback provides the "warmer/colder" signal that lets you build systems which search toward good outputs rather than hoping the first attempt works.

**What it looks like:** A control loop where signals flow back to influence the next step:
```
Generate → Evaluate → Feedback Signal → Adjust → Generate again
         ↑                                      |
         └──────────────────────────────────────┘
```

The feedback signal tells the system what's wrong and how to correct. Without it, evaluation just measures failure without enabling improvement.

---

### Demystification

#### Intelligent Behaviors → Code Patterns

| Behavior (looks like) | Implementation (actually is) |
|----------------------|------------------------------|
| "Improves with revision" | Generate → evaluate → inject issues → regenerate loop |
| "Responds to errors" | Tool output contains error message → model adjusts approach |
| "Stays on track" | System prompt reminder appended when drift detected |
| "Knows what to fix" | Specific error location + suggestion injected into context |
| "Gets better each attempt" | Previous output + feedback accumulated, informing next generation |
| "Searches for solutions" | Multiple candidates generated, best selected by evaluation |

#### The Core Mechanism

**Feedback is a gradient signal.** In optimization, a gradient tells you which direction improves the objective and by how much. In agentic systems, feedback plays the same role: it tells the model whether it's getting "warmer" (closer to the goal) or "colder" (drifting away), and ideally, what to change.

**The generate-evaluate loop is the basic structure.** You generate an output, evaluate it, and use the evaluation to produce feedback that influences the next generation. This is how single-shot generation becomes iterative search.

**Parallel generation explores different paths.** Instead of iterating on one output, you can generate multiple candidates simultaneously and select the best. This samples different regions of the output distribution — useful when you're unsure which approach will work and evaluation is cheap relative to generation.

**Agentic systems are search processes.** When you combine generation, evaluation, and feedback, you get something that looks like search: exploring a space of possible outputs, using gradient signals to move toward better regions. The useful behavior emerges from the control structure that coordinates repeated calls, not from any single generation.

#### What Makes Feedback Effective

**Verifiable signals steer reliably.** Code that fails tests, schemas that don't validate, API calls that return errors — these give unambiguous feedback. The model knows exactly what went wrong and can attempt a fix. Coding agents with test suites work well because the feedback loop has clear gradient signals.

**Vague signals steer poorly.** "This could be better" or "Score: 6/10" doesn't tell the model what to change. Without specific, located, actionable information, the model guesses — and often guesses wrong or changes nothing meaningful.

**Feedback only affects behavior when injected into context.** A quality score that's logged but not fed back into the next prompt changes nothing. The signal must appear where the model can act on it.

---

### Design Considerations

#### Key Questions

**1. What produces the feedback signal?**

Identify the sources that generate corrective information.

- **Tool outputs:** Error messages, test failures, linter warnings, API responses. These are often the most reliable because they're specific and verifiable.
- **Validators:** Schema checkers, constraint verifiers, rule-based systems. Binary pass/fail with clear failure reasons.
- **LLM critics:** A separate model call that evaluates and identifies issues. More flexible but less reliable than deterministic checks.
- **Human input:** Corrections, preferences, approvals. High quality but slow and expensive.

The reliability hierarchy: verifiable signals (tests, validators) > separate-call LLM critics > same-call self-evaluation. Same-call self-critique tends to rationalize rather than genuinely evaluate.

Look for: What sources exist? How verifiable are they? Is there a clear "right answer" the feedback can point to?

**2. What form does the feedback signal take?**

Identify how feedback is structured and how actionable it is.

- **Binary:** Pass/fail, valid/invalid. Clear but doesn't indicate how to fix.
- **Located errors:** "Line 23: undefined variable 'x'". Points to exactly what's wrong.
- **Suggested fixes:** "Replace X with Y". Directly actionable.
- **Comparative:** "Output A is better than B because...". Useful for selection, less for revision.
- **Vague assessment:** "Could be clearer". Hard to act on.

The more specific and located the feedback, the more effectively it steers. Test failures are ideal: exact error, exact location, exact mismatch between expected and actual.

Look for: Does feedback point to specific locations? Does it suggest what to change? Can the model act on it directly, or must it guess?

**3. When and where is feedback injected?**

Identify where in the execution flow feedback appears and what it affects.

- **Tool results:** Errors returned from tool execution appear in context naturally. The model sees what went wrong immediately.
- **Appended context:** Issues from evaluation added to the next prompt. "Previous attempt had these problems: ..."
- **System prompt emphasis:** Reminders added when drift is detected. "Remember: you must X" reinforced at the end of system prompt.
- **Memory updates:** Patterns stored for retrieval in future similar situations.

Timing matters:
- **Inline (during execution):** Corrects before the task completes. Tool errors, validation failures.
- **Inter-attempt (between retries):** Informs the next full attempt. Evaluation results, critic feedback.
- **Cross-task (persistent):** Affects future tasks. Memory, prompt updates.

Look for: Where does feedback enter context? Is it immediate (tool results) or delayed (post-evaluation)? Does it persist beyond the current task?

**4. How is drift detected and corrected?**

Identify the control mechanisms that notice when the model is off track and steer it back.

Detection mechanisms:
- **Explicit checks:** Validation at key points. Did the output parse? Did tests pass?
- **Progress monitoring:** Is the model making progress toward the goal, or spinning?
- **Constraint violation:** Did the model attempt something forbidden or outside scope?

Correction mechanisms:
- **Retry with feedback:** Same task, but with error information added to context.
- **Constraint reinforcement:** Repeat key instructions when they're being ignored.
- **Strategy change:** If current approach isn't working, prompt for a different approach.
- **Escalation:** Flag for human review if automated correction isn't working.

Look for: What triggers a correction? How does the system distinguish "making progress" from "stuck"? What happens when the model repeatedly fails?

**5. What determines if feedback actually steers behavior?**

Identify whether the feedback loop is actually working — whether the model gets "warmer" over iterations.

Feedback works when:
- **Signals are verifiable:** Tests pass/fail, schemas validate, constraints are met. Clear right answer.
- **Errors are specific:** The model knows exactly what to fix, not just that something is wrong.
- **The model can act on it:** The fix is within the model's capability given the feedback.

Feedback fails when:
- **Signals are vague:** "Be more helpful" doesn't indicate what to change.
- **Evaluation is noisy:** Scores fluctuate without clear direction.
- **The task exceeds capability:** No amount of feedback helps if the model can't do the task.

Signs the loop is working: scores improve monotonically, errors decrease, outputs converge toward acceptance criteria.

Signs the loop is failing: scores oscillate, same errors recur, the model changes things randomly without improvement.

Look for: Do iterations actually improve quality? Is there convergence or oscillation? When feedback doesn't help, is it because the signal is weak or because the task is too hard?

#### Key Tradeoffs

| Tradeoff | Tension |
|----------|---------|
| Specific vs general feedback | Actionability vs coverage |
| Inline vs post-hoc | Immediate correction vs complete evaluation |
| Single iteration vs parallel candidates | Depth vs breadth of search |
| Automated vs human feedback | Speed/cost vs quality/reliability |

#### Patterns

- **Generate-evaluate-revise loop:** The basic iterative improvement structure
- **Best-of-N selection:** Generate multiple candidates, select best by evaluation
- **Tool error injection:** Let tool failures naturally provide feedback through their error messages
- **Progressive constraint tightening:** Start loose, add constraints as the model demonstrates capability
- **Drift detection with reminders:** Monitor for off-track behavior, reinject key instructions

---

### The Reframe

**Before:** "The model keeps making the same mistake."
**After:** "Feedback isn't being injected, or it's too vague to act on."

**Before:** "How do I make it improve over iterations?"
**After:** "What gradient signal tells it warmer vs colder, and where is that signal injected?"

**Before:** "Evaluation shows it's bad, but it doesn't get better."
**After:** "Evaluation measures; feedback steers. I need to convert the score into specific, located, actionable corrections."
