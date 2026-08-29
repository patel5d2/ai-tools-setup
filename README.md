# AI Tools & Environment Setup

Local scaffold for the environment-setup competencies. Maps files to the rubric:

| § | Competency | Where |
|---|---|---|
| 3.1 | IDE: script + notebook | `hello.py`, `demo.ipynb` |
| 3.2 | Isolated Python env | `.venv/` (python 3.11), `requirements.txt` |
| 3.3 | Version control | this git repo, `.gitignore` |
| 3.5 | Managed credentials | `.env` (gitignored), `src/model_test.py` |
| 3.8 | Resource inventory | `src/resource_inventory.py` |

Colab (3.4), Jetstream2 (3.6), virtualization (3.7), and the video (3.9) are done by hand — not scaffolded here.

## Setup

```bash
python3.11 -m venv .venv          # 3.11: torch has no 3.14 wheels yet
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # then paste your real key into .env

python -V && which python         # path must be inside .venv/ (§3.2 evidence)
python hello.py                   # §3.1
python src/resource_inventory.py  # §3.8
python src/model_test.py          # §3.5 — needs a key in .env
```

In VS Code: select `.venv` as the interpreter (Cmd+Shift+P → "Python: Select Interpreter") and as the notebook kernel.
