#!/usr/bin/env python3
"""Generate native profiles from the single agent registry; does not install them."""
import json
from pathlib import Path


def sync(root):
    agents = json.loads((root / "skills/pd-orchestrator/references/agents.json").read_text())["agents"]
    out = root / "agents"
    out.mkdir(exist_ok=True)
    expected = set()
    for key, agent in agents.items():
        if key == "orchestrator":
            continue
        name = "pd_" + key
        instructions = ("Receba caminho explícito do projeto, ID da tarefa, objetivo, fontes e critérios de saída. "
                        "Leia " + agent["skill"] + "/SKILL.md e aplique seus contratos. " + agent["purpose"] +
                        " Use pd-grilling para decisões pendentes e pd-methods para escolher técnicas. "
                        "Só leia contexto do projeto indicado; não grave dados de projeto nas skills. "
                        "Acione especialistas quando a tarefa justificar: " + ", ".join(agent["subagents"]) +
                        ". Consolide suas contribuições e retorne artefatos e perguntas ao orquestrador. "
                        "Nunca aprove gates. O reviewer deve avaliar em instância distinta, sem editar o artefato de origem.")
        profile = {"name": name, "description": agent["purpose"], "developer_instructions": instructions}
        file = out / ("pd-" + key + ".toml")
        file.write_text("\n".join(k + " = " + json.dumps(v, ensure_ascii=False) for k, v in profile.items()) + "\n")
        expected.add(file.name)
        for specialist in agent["subagents"]:
            name = "pd_" + specialist.replace("-", "_")
            profile = {"name": name, "description": "Especialista em " + specialist + ", acionado pelo owner " + key + ".", "developer_instructions": "Atue exclusivamente no recorte " + specialist + ", sob o owner " + key + ". Leia " + agent["skill"] + "/SKILL.md. Receba projeto, fontes e critérios. Use pd-grilling se houver decisão pendente e devolva perguntas ao owner. Não assuma ownership global, não aprove gates nem invente coleta ou falas reais. Entregue contribuição rastreável."}
            file = out / ("pd-" + specialist + ".toml")
            file.write_text("\n".join(k + " = " + json.dumps(v, ensure_ascii=False) for k, v in profile.items()) + "\n")
            expected.add(file.name)
    extra = {p.name for p in out.glob("*.toml")} - expected
    if extra:
        raise ValueError("Unexpected native profiles; reconcile before release: " + str(extra))


if __name__ == "__main__":
    sync(Path(__file__).resolve().parents[1])
