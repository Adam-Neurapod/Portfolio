from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from datetime import datetime

QUESTIONS = [
    {
        "id": 1,
        "category": "CVE knowledge",
        "prompt": "What is a SQL injection attack and how can it be prevented?"
    },
    {
        "id": 2,
        "category": "Graph reasoning",
        "prompt": "A network has 3 servers. Server A connects to B and C. Server B connects only to A. Server C connects to A and has an unpatched CVE. Which server is the highest risk entry point?"
    },
    {
        "id": 3,
        "category": "CVSS scoring",
        "prompt": "A vulnerability allows remote unauthenticated attackers to execute arbitrary code on a web server with root privileges. No user interaction is required. Estimate the CVSS v3 base score and explain your reasoning."
    },
    {
        "id": 4,
        "category": "Attack surface",
        "prompt": "A company has: a public web server, an internal database server, a VPN gateway, and an employee laptop with outdated antivirus. Rank these from highest to lowest attack surface and explain why."
    },
    {
        "id": 5,
        "category": "Threat analysis",
        "prompt": "What is the difference between a zero-day exploit and a known CVE, and why are zero-days more dangerous from a risk management perspective?"
    }
]

def test_model(model_path, model_name):
    print(f"\n{'='*60}")
    print(f"Testujem: {model_name}")
    print(f"{'='*60}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="cuda"
    )

    results = []
    for q in QUESTIONS:
        print(f"\n[{q['category']}] Generujem odpoveď...")
        inputs = tokenizer(q["prompt"], return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True
            )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        results.append({
            "id": q["id"],
            "category": q["category"],
            "prompt": q["prompt"],
            "answer": answer
        })
        print(f"✅ Hotovo")

    del model
    torch.cuda.empty_cache()

    return results

all_results = {}

all_results["merged-cybersec"] = test_model("./merged-cybersec", "Merged CyberSec Model")
all_results["lily"] = test_model("segolilylabs/Lily-Cybersecurity-7B-v0.2", "Lily Cybersecurity 7B")
all_results["mistral"] = test_model("mistralai/Mistral-7B-Instruct-v0.2", "Mistral 7B Instruct")

output_file = f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Výsledky uložené do {output_file}")
print("Hotovo! Môžeme porovnať.")