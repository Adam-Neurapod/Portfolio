# Cybersecurity Model Merging — Gen 1 & Gen 2

**Method:** Evolutionary Model Merging (mergekit) — inspired by Sakana AI

---

## TL;DR — what this project actually shows

I built a cybersecurity-focused LLM by merging two existing models (Mistral-7B + Lily-Cybersecurity-7B) with no training involved, using three merge strategies (flat SLERP, gradient SLERP, DARE-TIES). I then built a 25-question benchmark with objective scoring and honestly compared all three generations.

**Key finding:** after a fair manual review, all three strategies performed **identically (13/22)**. Merging between these two models didn't change factual or reasoning capability — both seed models already had that knowledge, and merging just blends it. **CVSS scoring was a wall for every variant** (0–2 out of 7), because it's not knowledge stored in the weights — it's a computation. That result defines the direction for Gen 3: not another merge, but fine-tuning on CVSS data or a tool-use approach.

The value of this project isn't "I produced a winning model" — it's the ability to **build a benchmark, test hypotheses, and let the data prove the limits of a method.**

---

## 1. Theoretical background

### Model merging vs. classic fine-tuning

| | Fine-tuning | Model merging |
|---|---|---|
| Needs training data | yes | no |
| Needs GPU time | hours–days | minutes |
| Cost | high | near zero |
| How the new model is created | learning from data | arithmetic over weights |

### Why merging works — task vectors

Every LLM is a vector of billions of weights. If two models share the same base (here, Mistral-7B), their weights live in a similar geometric structure. Fine-tuning (Lily) isn't random — it's a **systematic shift** away from the base model toward a domain. This shift is called a *task vector*:

```
τ_cyber = Lily_weights − Mistral_weights
Lily = Mistral + τ_cyber
Merge = Mistral + t · τ_cyber
```

Merging adds a fraction of this meaningful shift back onto the base model. This is also why models with different architectures can't be merged — they don't share a coordinate system.

### SLERP (Spherical Linear Interpolation)

Interpolates between two vectors along a spherical arc, not a straight line:

```
SLERP(v1, v2, t) = sin((1−t)·θ)/sin(θ) · v1 + sin(t·θ)/sin(θ) · v2
```

Linear interpolation in high-dimensional space shrinks the resulting vector's magnitude and passes through "empty space" with no meaningful models. SLERP stays on the sphere, where every point is a valid model.

### Where knowledge lives in the layers (motivation for the gradient merge)

An empirical pattern in transformer layers:
- **Early layers (0–8):** syntax, tokens, surface structure
- **Middle layers (9–20):** factual knowledge, entities, security facts (CVEs, ATT&CK)
- **Late layers (21–32):** reasoning, abstraction, response planning

This motivated the Gen 2 hypothesis: push more Lily into the middle layers (facts) and more Mistral into the late layers (reasoning).

---

## 2. Seed models

| Role | Model | Note |
|---|---|---|
| Base / reasoning | `mistralai/Mistral-7B-Instruct-v0.2` | strong reasoning, merge backbone |
| Security | `segolilylabs/Lily-Cybersecurity-7B-v0.2` | Mistral fine-tune on ~22k security scenarios |

Both share the identical Mistral-7B architecture (32 layers), which is what makes merging possible.

---

## 3. Environment & reproducibility

```
Python 3.10.11
torch 2.12.1+cu128   (CUDA build — not CPU!)
mergekit 0.1.4
pydantic 2.9.2       (2.10+ breaks mergekit — critical)
transformers 5.12.1
bitsandbytes         (4-bit quantization for inference)
```

### Problems solved during setup
1. **torch installed as CPU-only** → reinstalled via `torch --index-url .../cu128`
2. **mergekit CLI doesn't resolve on Windows** → use `python -m mergekit.scripts.run_yaml`
3. **pydantic 2.10 bug** (`ConfiguredModuleArchitecture is not fully defined`) → downgrade to 2.9.2
4. **SLERP requires `slices:` + `t:` syntax**, not `models:` + `weight:`

---

## 4. Three merge strategies

### Gen 1 — Flat SLERP
A single interpolation factor for the whole model.
```yaml
merge_method: slerp
base_model: mistralai/Mistral-7B-Instruct-v0.2
parameters:
  t: 0.6      # 60% Lily, 40% Mistral, uniform across all layers
```

### Gen 2a — Gradient SLERP
Per-layer `t` — a gradient across layers, set separately for attention and MLP.
```yaml
parameters:
  t:
    - filter: self_attn
      value: [0.5, 0.5, 0.75, 0.75, 0.6, 0.4]
    - filter: mlp
      value: [0.5, 0.7, 0.8, 0.8, 0.6, 0.4]
    - value: 0.5
```
Hypothesis: more Lily in middle layers (facts), more Mistral in late layers (reasoning).

### Gen 2b — DARE-TIES
A task-vector method: pruning (density) + sign-conflict resolution.
```yaml
merge_method: dare_ties
models:
  - model: mistralai/Mistral-7B-Instruct-v0.2
  - model: segolilylabs/Lily-Cybersecurity-7B-v0.2
    parameters:
      density: 0.6    # keep the 60% most significant changes
      weight: 0.6
parameters:
  int8_mask: true
  normalize: true
```

Each merge took ~5 minutes on the RTX 4060 (models already downloaded locally).

---

## 5. Benchmark

### Design
25 questions, **22 objective** (auto-scored) + 3 qualitative:

| Category | Count | Scoring |
|---|---|---|
| CVSS scoring | 7 | numeric value within accept-range |
| CVE facts | 6 | keyword match (CVE ID + technology) |
| Graph reasoning | 5 | keyword + manual review |
| Attack classification | 4 | keyword + manual review |
| Reasoning (qualitative) | 3 | rubric, reviewed by eye |

### Critical inference settings
- **4-bit quantization** (bitsandbytes nf4) — without it, the 14 GB fp16 model doesn't fit in 8 GB VRAM, spills over PCIe into system RAM, and runs at ~0.8 tok/s (10 min per answer). With 4-bit: ~3.8 GB VRAM, 16.8 tok/s. **A 21× speedup.**
- **`do_sample=False`** — deterministic, reproducible outputs.
- **Chat template + system prompt** — `[INST]...[/INST]` instead of a raw prompt (a Gen 1 mistake).
- All models evaluated identically for a fair comparison.

> Quantization note: 4-bit slightly reduces quality vs. fp16, but since **every model** is quantized the same way, the comparison remains fair.

---

## 6. Results

### Auto-scoring (before manual review)

| Model | Objective score |
|---|---|
| Gen 1 flat SLERP | 14/22 (63.6%) |
| Gen 2 gradient | 14/22 (63.6%) |
| Gen 2 DARE-TIES | 15/22 (68.2%) |

### After a fair manual review

Manual review uncovered auto-scoring errors in both directions:

- **#14 (graph):** the auto-scorer matched "b" inside unrelated words → false positive. Reality: Gen 1 and gradient correctly identified chokepoint B; **DARE-TIES named Host D instead (wrong — D is the target, not the chokepoint).**
- **#20 (attack):** every model invented a non-existent MITRE category; the keyword "lateral movement" slipped through by accident. Fair result: nobody actually got this one right.
- **#17 (graph):** DARE-TIES named the load balancer instead of the backend (wrong).

| Category | Gen 1 | Gradient | DARE-TIES |
|---|---|---|---|
| CVSS | 0/7 | 0/7 | 2/7 |
| CVE facts | 5/6 | 5/6 | 5/6 |
| Graph reasoning | 5/5 | 5/5 | 3/5 |
| Attack classification | 3/4 | 3/4 | 3/4 |
| **TOTAL** | **13/22** | **13/22** | **13/22** |

**Result: a three-way tie at 13/13/13.** DARE-TIES gained 2 points on CVSS but lost 2 on graph reasoning.

---

## 7. Interpretation — what the data actually says

### Merging didn't change capability
All three strategies landed identically. Factual and reasoning questions were answered equally well across the board, because that knowledge already existed in **both seed models** before merging — merging just blends it. The gradient hypothesis (per-layer ratio) was technically sound, but there was no room for it to show up in these categories, since weight distribution wasn't the ceiling.

### CVSS is a hard limit
Every variant failed at CVSS (0–2/7). The answers show "eyeballing it": #1 → 10.0 instead of 9.8 (close), #5 → 7.5 instead of 5.3 (way off). The model can't **apply the CVSS formula** — and that's not something merging fixes, because CVSS is an algorithm, not knowledge encoded in weights.

### Number hallucination
The model occasionally invents a plausible-looking but wrong number — e.g. question #12 (Spectre V1) returned "CVE-2018-36934" instead of the correct CVE-2017-5753. Confident, but wrong.

---

## 8. Direction for Gen 3

The data points clearly to where the problem is — and it isn't the merge strategy:

1. **CVSS fine-tuning** — a small dataset (vulnerability description → vector + score), LoRA fine-tune on top of the DARE-TIES model. This is the only real path to teaching the model to *compute*, not guess.
2. **Tool-use alternative** — have the model extract CVSS metrics (AV, AC, PR…) and compute the score with a deterministic function instead. More accurate than any model.
3. **A stronger/more specialized seed** — if broader security knowledge is the goal, consider a stronger security-focused seed model.

Gen 3 isn't "one more merge" — it's a **fine-tune or tool-use fix targeted at the specific weakness the benchmark exposed.**

---

## 9. What I learned

- **Model merging is geometry, not training** — interpolating task vectors in weight space.
- **Merging doesn't create new capability** — it combines existing capability. If no seed model knows X, the merge won't know X either.
- **A benchmark needs an objective ground truth** — otherwise "sounds right" quietly replaces "is correct".
- **Auto-scoring needs a manual pass** — keyword matching produces both false positives and false negatives.
- **An honest negative result beats a pretended win** — proving a method's limit with data is more valuable than claiming victory.
- **Hardware: quantization is decisive** — the difference between 10 minutes and 12 seconds per answer.

---

*Reproducible artifacts included in this repo: `eval_dataset.json`, `evaluate.py`, three `config-*.yaml` files, `requirements.txt`.*
