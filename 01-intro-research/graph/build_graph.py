import json
import re
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

HERE = Path(__file__).parent
REPORT = HERE.parent / "genai_applications_report.md"

TERMS = {
    "LLM": ([r"\bLLMs?\b"], [r"\bthe model\b", r"\blanguage model"]),
    "Token": ([r"\btokens?\b"], [r"\bburn money\b"]),
    "Tokenomics": ([r"\btokenomics\b"], [r"\bcost control\b", r"\bcost per ticket\b", r"\bcompute cost\b"]),
    "Context window": ([r"\bcontext window\b"], [r"\bdon'?t fit into (the )?context\b", r"\bcodebase-wide context\b"]),
    "Prompt": ([r"\bprompts?\b(?! injection)"], [r"\bnatural language\b", r"\bfrom comments\b"]),
    "Prompt injection": ([r"\bprompt injection\b"], [r"\bmalicious\b"]),
    "Hallucination": ([r"\bhallucinat\w*"], [r"\binvented\b", r"\bconfident(ly)? but wrong\b", r"\banswers confidently anyway\b", r"\bplausible but wrong\b"]),
    "Grounding": ([r"\bground(ed|ing)\b"], [r"\bmatch actual policies\b", r"\bbased on internal docs\b"]),
    "RAG": ([r"\bRAG\b", r"\bretrieval-augmented\b"], [r"\bknowledge base\b", r"\bretriev(al|ed)\b"]),
    "Embedding": ([r"\bembed(ding|ded)s?\b"], [r"\bvectors?\b"]),
    "Vector database": ([r"\bvector DB\b", r"\bvector database\b"], [r"\bindex(es|ing)\b"]),
    "Chunking": ([r"\bchunk(ed|ing|s)?\b"], [r"\bsplit\w* .{0,20}documents\b"]),
    "Multimodal": ([r"\bmultimodal\b"], [r"\btext-to-(image|video|speech)\b", r"\bvoice synthesis\b"]),
    "Agent": ([r"\bagents?\b"], [r"\bautonomous\b", r"\bplans? (changes|multi-step)\b"]),
    "Agentic workflow": ([r"\bagentic\b"], [r"\bmulti-step\b", r"\bworkflows?\b", r"\bcoordinate with other\b"]),
    "Tool calling": ([r"\btool call\w*", r"\bfunction calling\b"], [r"\bcall tools\b", r"\bcode execution\b", r"\bruns? (python|tests)\b"]),
    "Copilot": ([r"\bcopilot\b"], [r"\bassistants?\b", r"\bpair programmer\b"]),
    "AI-native tool": ([r"\bAI-native\b"], [r"\bVS Code fork\b"]),
    "Guardrails": ([r"\bguardrails?\b"], [r"\bsafely\b", r"\baccess control\b", r"\bsecurity of tool access\b"]),
    "Human-in-the-loop": ([r"\bhuman-in-the-loop\b"], [r"\breview is still mandatory\b", r"\bhuman review\b", r"\bhand\w* off to a human\b"]),
    "Fine-tuning": ([r"\bfine-tun\w*"], [r"\btrained on licensed\b", r"\bbrand voice\b"]),
    "Deepfake": ([r"\bdeepfakes?\b"], [r"\bvoice cloning\b"]),
    "PoC": ([r"\bPoCs?\b", r"\bproof of concept\b"], [r"\bprototypes?\b", r"\bmockups?\b"]),
}


def count(patterns, text):
    return sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in patterns)


def main():
    text = REPORT.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
    sections = {p.splitlines()[0].strip(): p for p in parts}

    stats = {}
    used_in = {}
    for term, (exp, imp) in TERMS.items():
        e = count(exp, text)
        i = count(imp, text)
        stats[term] = {"explicit": e, "implicit": i}
        used_in[term] = [name for name, body in sections.items()
                         if count(exp, body) + count(imp, body) > 0]

    edges = []
    for a, b in combinations(TERMS, 2):
        shared = set(used_in[a]) & set(used_in[b])
        if shared:
            edges.append({"source": a, "target": b, "weight": len(shared)})

    data = {"terms": stats, "sections": used_in, "edges": edges}
    (HERE / "vocabulary_stats.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    G = nx.Graph()
    for term, s in stats.items():
        G.add_node(term, **s)
    for e in edges:
        if e["weight"] >= 2:
            G.add_edge(e["source"], e["target"], weight=e["weight"])

    pos = nx.spring_layout(G, k=1.1, seed=7, weight="weight")
    fig, (ax_g, ax_b) = plt.subplots(1, 2, figsize=(22, 11), gridspec_kw={"width_ratios": [3, 2]})

    widths = [0.4 + (G[u][v]["weight"] - 2) * 0.8 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax_g, width=widths, edge_color="#b0b0b0", alpha=0.7)
    total = [stats[n]["explicit"] + stats[n]["implicit"] for n in G.nodes()]
    expl = [stats[n]["explicit"] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax_g, node_size=[200 + t * 60 for t in total], node_color="#f2b25c", alpha=0.9)
    nx.draw_networkx_nodes(G, pos, ax=ax_g, node_size=[60 + t * 60 for t in expl], node_color="#3b6fb6")
    nx.draw_networkx_labels(G, pos, ax=ax_g, font_size=10)
    ax_g.set_title("Vocabulary relations (edge = terms used in same report section, >=2 sections)\n"
                   "blue core = explicit usage, orange ring = implicit usage", fontsize=12)
    ax_g.axis("off")

    order = sorted(stats, key=lambda t: stats[t]["explicit"] + stats[t]["implicit"])
    y = range(len(order))
    ax_b.barh([v - 0.2 for v in y], [stats[t]["explicit"] for t in order], height=0.4, color="#3b6fb6", label="explicit")
    ax_b.barh([v + 0.2 for v in y], [stats[t]["implicit"] for t in order], height=0.4, color="#f2b25c", label="implicit")
    ax_b.set_yticks(list(y))
    ax_b.set_yticklabels(order)
    ax_b.set_xlabel("mentions in report")
    ax_b.set_title("Usage frequency per term", fontsize=12)
    ax_b.legend(loc="lower right")
    ax_b.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(HERE / "vocabulary_graph.png", dpi=110)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
