"""
evaluate.py — Gen 2 evaluačný skript pre cybersecurity merge projekt.

Čo robí:
  1. Načíta eval_dataset.json (25 otázok, 22 objektívnych + 3 kvalitatívne)
  2. Pre každý zadaný model: načíta ho 4-bit (aby sa zmestil do 8GB VRAM),
     spustí všetkých 25 otázok s CHAT TEMPLATE + system promptom
  3. Auto-skóruje objektívne otázky (CVSS range check + keyword match)
  4. Uloží kompletné odpovede + skóre do JSON pre ďalšiu analýzu

Spustenie:
  python evaluate.py

Modely na test uprav v zozname MODELS nižšie.
"""

import json
import re
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODELS = {
    "gen1-slerp":      "./merged-cybersec",
    "gen2-gradient":   "./merged-gen2-gradient",
    "gen2-dareties":   "./merged-gen2-dareties",

}

DATASET_PATH = "eval_dataset.json"
OUTPUT_PATH  = f"eval_gen2_results_{time.strftime('%Y%m%d_%H%M')}.json"
MAX_NEW_TOKENS = 400

SYSTEM_PROMPT = (
    "You are a cybersecurity analyst. Answer precisely and concisely. "
    "When asked for a CVSS score, give the numeric base score explicitly. "
    "When asked for a CVE identifier, state it in full (e.g. CVE-2021-44228)."
)
BNB = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)


def build_prompt(tokenizer, question):
    """Zabalí otázku do chat template modelu (Mistral [INST] formát).
    Toto bol gen 2 fix — gen 1 posielala holý text bez template."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    try:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    except Exception:
        merged = f"{SYSTEM_PROMPT}\n\n{question}"
        return tokenizer.apply_chat_template(
            [{"role": "user", "content": merged}],
            tokenize=False, add_generation_prompt=True
        )


def score_cvss(answer, q):
    """CVSS otázka: nájdi v odpovedi číslo ktoré padne do accept_range.
    Berieme PRVÉ číslo v rozsahu 0-10 ktoré sedí — modely občas vypíšu
    viac čísel (napr. metriky), tak hľadáme to ktoré je v accept_range."""
    lo, hi = q["accept_range"]
    nums = re.findall(r"\b(\d{1,2}(?:\.\d)?)\b", answer)
    for n in nums:
        val = float(n)
        if lo <= val <= hi:
            return True, val
    return False, None


def score_keywords(answer, q):
    """CVE / klasifikačná otázka: všetky keywords_required musia byť v odpovedi.
    Vráti (bol_uspech, kolko_bonus_slov_naslo)."""
    low = answer.lower()
    required = q.get("keywords_required", [])
    got_all = all(kw.lower() in low for kw in required)
    bonus = sum(1 for kw in q.get("keywords_bonus", []) if kw.lower() in low)
    return got_all, bonus


def score_answer(answer, q):
    """Rozhodne podľa typu otázky ako skórovať."""
    cat = q["category"]
    scoring = q["scoring"]

    if scoring == "qualitative":
        return {"type": "qualitative", "auto": None, "note": "manual review"}

    if cat == "cvss":
        ok, found = score_cvss(answer, q)
        return {"type": "cvss", "correct": ok, "found_value": found,
                "expected": q["expected_score"]}

    ok, bonus = score_keywords(answer, q)
    result = {"type": "keyword", "correct": ok, "bonus_hits": bonus}
    if q.get("manual_check"):
        result["manual_check"] = True
    return result


def run_model(name, path, dataset, tokenizer_cache):
    print(f"\n{'='*64}\n  MODEL: {name}  ({path})\n{'='*64}")

    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        path, quantization_config=BNB, device_map="cuda"
    )
    print(f"  Načítaný za {time.time()-t0:.1f}s, "
          f"VRAM {torch.cuda.memory_allocated()/1024**3:.1f}GB")

    results = []
    for q in dataset["questions"]:
        prompt = build_prompt(tok, q["prompt"])
        inputs = tok(prompt, return_tensors="pt").to("cuda")

        t0 = time.time()
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                pad_token_id=tok.eos_token_id,
            )
        gen_time = time.time() - t0

        full = tok.decode(out[0], skip_special_tokens=True)
        answer = full[len(tok.decode(inputs.input_ids[0], skip_special_tokens=True)):].strip()

        score = score_answer(answer, q)
        results.append({
            "id": q["id"],
            "category": q["category"],
            "scoring": q["scoring"],
            "prompt": q["prompt"],
            "answer": answer,
            "score": score,
            "gen_time_s": round(gen_time, 1),
        })
        mark = "?" if q["scoring"] == "qualitative" else ("OK" if score.get("correct") else "X")
        print(f"  [{mark}] #{q['id']:>2} {q['category']:<22} {gen_time:>5.1f}s")

    del model
    torch.cuda.empty_cache()
    return results


def summarize(all_results):
    """Spočítaj skóre po kategóriách pre každý model."""
    summary = {}
    for model_name, results in all_results.items():
        by_cat = {}
        obj_correct = obj_total = 0
        for r in results:
            cat = r["category"]
            by_cat.setdefault(cat, {"correct": 0, "total": 0})
            if r["scoring"] == "objective":
                by_cat[cat]["total"] += 1
                obj_total += 1
                if r["score"].get("correct"):
                    by_cat[cat]["correct"] += 1
                    obj_correct += 1
        summary[model_name] = {
            "objective_score": f"{obj_correct}/{obj_total}",
            "objective_pct": round(100*obj_correct/obj_total, 1) if obj_total else 0,
            "by_category": by_cat,
        }
    return summary


def main():
    with open(DATASET_PATH, encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"Načítaných {len(dataset['questions'])} otázok z {DATASET_PATH}")

    all_results = {}
    for name, path in MODELS.items():
        try:
            all_results[name] = run_model(name, path, dataset, {})
        except Exception as e:
            print(f"  !! CHYBA pri modeli {name}: {e}")
            all_results[name] = {"error": str(e)}

    summary = summarize(all_results)

    output = {"summary": summary, "detailed": all_results}
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*64}\n  VÝSLEDKY\n{'='*64}")
    for model_name, s in summary.items():
        print(f"  {model_name:<18} {s['objective_score']:>7}  ({s['objective_pct']}%)")
    print(f"\nUložené do {OUTPUT_PATH}")


if __name__ == "__main__":
    main()