#!/usr/bin/env python3
"""Move uma categoria do catálogo do SKILL.md pro parking lot (CATALOG-removed.md).
Uso: python3 _remove_category.py "<### Categoria>" "<motivo>"
"""
import sys, os, re

cat_name = sys.argv[1]
reason = sys.argv[2] if len(sys.argv) > 2 else "não vou usar"
DATE = "2026-06-26"

skill = open("SKILL.md").read()
lines = skill.splitlines()

start = end = None
for i, ln in enumerate(lines):
    if ln.strip() == f"### {cat_name}":
        start = i
    elif start is not None and ln.startswith("### ") and i > start:
        end = i; break
if start is None:
    sys.exit(f"categoria '{cat_name}' não encontrada")
if end is None:
    # categoria é a última do catálogo: vai até a próxima H2 (## ...)
    for i in range(start+1, len(lines)):
        if lines[i].startswith("## "):
            end = i; break
    end = end or len(lines)

section = [l for l in lines[start:end] if l.strip()]

# backup append
bkp = "CATALOG-removed.md"
header = ("# Parking lot — entradas removidas do catálogo\n\n"
          "Removidas do SKILL.md mas guardadas aqui pra re-adicionar se necessário.\n"
          "(A matéria-prima crua segue em raw/docs-oficiais/.)\n")
prev = open(bkp).read() if os.path.exists(bkp) else header
entry = f'\n## Removido em {DATE} — categoria "{cat_name}" (motivo: {reason})\n\n' + "\n".join(section) + "\n"
open(bkp, "w").write(prev + entry)

# remove do SKILL.md
del lines[start:end]
out = []
for ln in lines:
    if ln == "" and out and out[-1] == "":
        continue
    out.append(ln)
skill = "\n".join(out)

# atualizar contagem "(all N — the map)"
m = re.search(r"\(all (\d+) — the map\)", skill)
if m:
    new = skill.count("→ products/")
    skill = skill.replace(m.group(0), f"(all {new} — the map)")

open("SKILL.md", "w").write(skill + ("\n" if not skill.endswith("\n") else ""))
print(f"removida: {cat_name} ({len(section)-1} produtos)")
print(f"catálogo agora: {skill.count('→ products/')} produtos | SKILL.md ~{len(skill)//4} tokens")
