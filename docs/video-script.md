# §3.9 — Recorded demonstration: speaking script

**Target length:** 8–10 minutes. **Name:** Dharmin Patel. **Course:** IT 7075C.

How to use this: lines in **[brackets]** are stage directions — what to have on screen or
what to type. Everything else is what you say out loud. Don't read it word for word; the
phrasing is there so you never have to stall and think.

Before you hit record:
- Docker Desktop running, `juice-shop` container up.
- Colab notebook open in a tab, already executed.
- VS Code Insiders open on `ai-tools-setup`, all other windows closed.
- Turn on Do Not Disturb. A Teams banner in the middle of a graded recording looks bad.
- One terminal window, font size bumped up so it's readable at 1080p.

---

## 0. Opening (~30 s)

**[Screen: VS Code Insiders open on the `ai-tools-setup` folder.]**

Hi, I'm Dharmin Patel, and this is my mini project for IT 7075C — configuring AI tools and
environments.

I'm working on a MacBook Pro with an Apple M2 Pro — 12 cores, 16 gigabytes of unified
memory, running macOS 26.5. That hardware detail matters more than you'd expect, and it
comes back twice later in this demo.

I'll go through the competencies in order: the editor, the isolated environment, version
control, hosted notebooks, model access with managed credentials, virtualization, and the
resource inventory. Jetstream2 was announced as unavailable, so section 3.6 isn't included.

---

## 1. §3.1 — Integrated development environment (~1 min)

**[Screen: VS Code Insiders, Explorer showing the project tree.]**

This is Visual Studio Code Insiders with the project folder open as the workspace root.

**[Open a terminal, run the extensions listing.]**

Let me show the extensions are actually installed rather than just claiming it.

```
"/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code" \
  --list-extensions --show-versions | grep -E 'ms-python|ms-toolsai|github'
```

There they are — Python, Pylance, the Python Debugger, Jupyter, and GitHub Pull Requests,
with version numbers.

**[Open `hello.py`. Run it in the integrated terminal.]**

Now a script running inside the editor.

```
source .venv/bin/activate && python hello.py
```

Two lines of output. "Hello from the isolated environment" — and then the interpreter path.
Notice it resolves to `.venv/bin/python` inside the project, not a system Python. That's the
same proof section 3.2 needs, so I'm getting both at once.

**[Open `demo.ipynb`. Point at the executed cells.]**

And the same thing in a notebook — a cell executed in the editor, printing the kernel's
interpreter path, and it's that same `.venv`.

---

## 2. §3.2 — Isolated Python environment (~1 min 30 s)

**[Screen: terminal.]**

The environment is a standard `venv` in the project root. Here's how I built it:

```
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**[Run the verification commands.]**

```
python -V
which python
```

Python 3.11.2, and the interpreter lives inside the project's `.venv`.

**[Run `deactivate`, then `which python3`.]**

And here's the contrast — deactivate, and now `python3` is Homebrew's, at
`/opt/homebrew/bin/python3`, version 3.14.7. Two different interpreters, and the project
one is only reachable when the environment is active. That prefix difference *is* the
isolation.

Now, why 3.11 and not the newest? This is the first place the hardware bit comes back.
PyTorch hasn't published wheels for Python 3.14 yet, and I need `torch` for the section 3.8
inventory. So the constraint came from the dependency, not from wanting an old Python. The
whole point of an isolated environment is that holding 3.11 for this project costs nothing
everywhere else on the machine.

**[Show `pip list` filtered to the key packages.]**

Anthropic, numpy, torch 2.14, ipykernel, notebook, python-dotenv.

**[VS Code: Command Palette → "Python: Select Interpreter".]**

And in the editor, the interpreter picker shows the same `.venv` marked Recommended, right
next to the global 3.14.7.

**[Command Palette → "Notebook: Select Notebook Kernel".]**

Same for the notebook kernel — I registered the environment as a named Jupyter kernel so it
shows up in the picker, and the notebook is bound to it.

---

## 3. §3.3 — Version control and remote repositories (~1 min 30 s)

**[Screen: VS Code Source Control panel.]**

The repository is public on GitHub at `github.com/patel5d2/ai-tools-setup`.

**[Point at the commit graph.]**

Here's the commit history — more than the two substantive commits required. You can see
real work: scaffolding the venv, adding numpy because torch needs it, rebuilding the
environment, adding the report.

**[Make a small edit — e.g. a line in README.md. Stage, write a message, commit, push.]**

Let me make a change and push it live so you can see the whole loop, not just the result.

**[Switch to the terminal for the credential part.]**

Now the part that actually matters for security. There's a real `.env` file on this machine
with a live API key in it.

```
ls -l .env
```

It exists — 127 bytes. And now:

```
git check-ignore -v .env
```

Git tells me exactly which rule excludes it: line 2 of `.gitignore`.

```
git ls-files | grep env
```

The only env file git tracks is `.env.example` — the template, with placeholder values. So
the repository documents what variables you need without leaking any of them.

```
git status --short
```

And `.env` never shows up. It can't be committed by accident, because git doesn't consider
it a candidate at all.

---

## 4. §3.4 — Hosted notebooks and persistent storage (~1 min 30 s)

**[Screen: switch to the browser, Colab notebook open.]**

This is `colab_evidence.ipynb` running in Google Colab.

One thing worth saying up front: this notebook only runs in Colab. `google.colab` doesn't
exist in a local kernel — I found that out the direct way, by running it locally first and
getting `ModuleNotFoundError: No module named 'google'`. So the first cell now fails with a
plain message telling you to upload it, instead of a traceback.

**[Point at the mount cell and its output.]**

First cell mounts Google Drive at `/content/drive`, and there's the mount confirmation.

**[Point at the write cell.]**

Then I write a file to `MyDrive/IT7075C/persistence.txt` with a timestamp, and read it back
to confirm it's there.

**[Runtime ▸ Restart session. Let it restart on camera.]**

Now the actual test. I restart the runtime.

That gives me a completely fresh virtual machine. The local disk is gone.

**[Run the post-restart cell.]**

This cell first lists `/content` before mounting anything — and you can see the local
filesystem is empty. Then it remounts Drive and reads the file back.

`survived restart: True`, and the contents are the original timestamp from before the
restart.

That's the competency in one line: Colab's local filesystem is ephemeral and dies with the
runtime. Drive is durable storage that lives outside it. Anything that has to outlive a
session has to be written to mounted Drive.

---

## 5. §3.5 — Programmatic model access with managed credentials (~1 min 30 s)

**[Screen: VS Code, `src/model_test.py` open.]**

I'm using Anthropic, with the model `claude-opus-5`.

**[Scroll to the credential loading.]**

The important thing is what's *not* here. There is no API key anywhere in this source file.
`load_dotenv()` reads the local `.env`, and then `Anthropic()` is constructed with no
arguments at all — the SDK picks up `ANTHROPIC_API_KEY` from the process environment
itself.

**[Terminal.]**

```
python src/model_test.py
```

And there's a live response from the model.

**[Switch to Colab.]**

Now the same code path in Colab. The difference is only where the environment variable
comes from.

**[Point at the userdata cell.]**

`userdata.get('ANTHROPIC_API_KEY')` pulls it from Colab's Secrets store and puts it into
`os.environ`. Same three lines of Anthropic code after that.

**[Point at the response output.]**

Live response in Colab too.

**[Open the Secrets panel — the key icon in the left sidebar.]**

And here's where the key actually lives — the Secrets sidebar. The name is
`ANTHROPIC_API_KEY`, Notebook access is on, and the value is hidden. I'm deliberately
leaving the eye toggle off so nothing sensitive ends up in this recording.

The key is stored against my Google account, not inside the notebook file. So I could share
or commit this notebook and the credential doesn't travel with it. That's the Colab
equivalent of `.env` plus `.gitignore` — same principle, different mechanism.

---

## 6. §3.7 — Virtualization and isolated targets (~2 min)

**[Screen: terminal.]**

For the vulnerable target I'm using Docker with OWASP Juice Shop, not a Metasploitable2 VM.

That's a deliberate choice, and here's the second place the hardware comes back. This
machine is Apple Silicon — arm64. VirtualBox has no arm64 host build, and Metasploitable2
ships only as a 32-bit x86 image. You can't virtualize it here without full CPU emulation.
The assignment allows a containerized target for exactly this situation.

```
docker ps
```

The container is up, and look at the port binding: `127.0.0.1:3000`, not `0.0.0.0:3000`.

```
docker network inspect pentest-lab --format '...'
```

It's on a user-defined bridge network in NAT mode, subnet `172.28.0.0/16`.

Three reasons for that configuration. First, this target is deliberately vulnerable — on a
bridge it has no address on my physical LAN, so nothing outside this machine can route to
it. Host networking would put it straight onto my Wi-Fi interface. Second, binding the
publish to loopback explicitly means only this machine can reach the service — that's the
smallest exposure that still lets me test it. Third, a user-defined bridge gives me
container-name DNS, so lab hosts can address each other by name instead of by an IP that
changes on restart.

**[Reachability commands.]**

```
nc -zv 127.0.0.1 3000
curl -sI http://127.0.0.1:3000
```

Port's open, and the server answers 200 with its security headers.

```
curl -s http://127.0.0.1:3000 | grep -io '<title>.*</title>'
```

OWASP Juice Shop.

```
docker run --rm --network pentest-lab busybox ping -c 3 juice-shop
```

Three packets, zero loss, resolved by container name.

Now I want to be honest about something, because it cost me time. If I ping
`172.28.0.2` *directly from macOS*, I get one hundred percent packet loss — and that is not
a misconfiguration. Docker on macOS doesn't run containers on the host kernel; it runs them
inside a Linux VM. That subnet only exists inside that VM's network namespace, so macOS has
no route to it and ICMP has nowhere to go. TCP still works because Docker's userland proxy
forwards the published port across the VM boundary.

I confirmed that diagnosis by pinging the same container successfully from a second
container on the same bridge — which is what you just saw. So I demonstrate ICMP where it's
meaningful, on the lab network, and host-to-guest reachability at layer 4 and layer 7
through the published port, which is the path an attack tool would actually use.

The lesson I took from it: check the platform's architecture before re-checking your
network settings.

**[Browser: `127.0.0.1:3000`.]**

And here's the application in the browser.

---

## 7. §3.8 — Computational resource inventory (~1 min 30 s)

**[Screen: terminal.]**

Last competency — inventory the hardware on both platforms, using a system utility and a
framework query.

```
system_profiler SPHardwareDataType SPDisplaysDataType
```

MacBook Pro, M2 Pro, 12 CPU cores — 8 performance and 4 efficiency — 16 gigabytes of
memory, and 19 GPU cores with Metal support.

**[Framework query.]**

```
python src/resource_inventory.py
```

`CUDA available: False`. `MPS available: True`.

This is the part that's easy to misread, so let me interpret it properly. CUDA is NVIDIA's
API. This machine has an Apple integrated GPU, not an NVIDIA discrete card, so `False` is
the correct answer — it is not a failure and it is not a missing driver. The GPU is very
much present and usable; PyTorch reaches it through Metal, which it exposes as the MPS
backend, and that reports `True`.

If you only read the CUDA line you'd wrongly conclude there's no GPU here. There are 19 GPU
cores available for acceleration, just through a different backend.

One more thing worth noting: this memory is *unified*. The 16 gigabytes is shared between
CPU and GPU — there's no separate block of dedicated VRAM the way there would be on a
discrete card.

**[Switch to Colab.]**

Same two questions on the Colab runtime.

**[Point at the nvidia-smi cell.]**

`nvidia-smi: command not found` — this is a CPU-only runtime, so the tool isn't even
installed. Again, a correct result, not an error.

`lscpu` shows an Intel Xeon at 2.2 gigahertz with 2 virtual CPUs, and `free -h` shows about
12 gigabytes of memory. Then the framework query: torch 2.11 CPU build, `CUDA available:
False`.

So: two platforms, two completely different answers, and neither of them has CUDA — for two
entirely different reasons. On the Mac it's the wrong vendor's API for a GPU that's
present. On Colab it's a runtime with no GPU attached at all, which I could change under
Runtime, Change runtime type.

---

## 8. Closing (~45 s)

**[Screen: back to VS Code or the repo page.]**

That covers all the competencies attempted. A quick word on what I'd do differently.

I'd create `.env` from `.env.example` on day one, before writing any code. No key was ever
committed in this project — but the ordering was luck as much as design. The ignore rule
and the example file went in alongside the first real credential, not ahead of it. The
right discipline is to commit `.gitignore` and `.env.example` in the very first commit, so
the repository is structurally incapable of accepting a secret before one exists to leak.
Once a key is committed, `git rm --cached` and a rewritten history are the only remedy, and
a rotated key is the only safe assumption.

Smaller one: I'd pin the environment with `pip freeze > requirements.txt` rather than bare
package names, so the versions in my report are reproducible instead of drifting to
whatever's current at the next install.

The full write-up, all the evidence screenshots, and the code are in the repository linked
in the report. Thanks for watching.

---

## Quick reference — commands in order

```sh
# §3.1
"/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code" \
  --list-extensions --show-versions | grep -E 'ms-python|ms-toolsai|github'
source .venv/bin/activate && python hello.py

# §3.2
python -V
which python
pip list | grep -E 'anthropic|numpy|torch|ipykernel|notebook|dotenv'
deactivate; which python3; python3 -V

# §3.3
ls -l .env
git check-ignore -v .env
git ls-files | grep env
git status --short

# §3.5
python src/model_test.py

# §3.7
docker ps
docker network inspect pentest-lab \
  --format 'driver={{.Driver}} subnet={{range .IPAM.Config}}{{.Subnet}} gw={{.Gateway}}{{end}}'
nc -zv 127.0.0.1 3000
curl -sI http://127.0.0.1:3000
curl -s http://127.0.0.1:3000 | grep -io '<title>.*</title>'
docker run --rm --network pentest-lab busybox ping -c 3 juice-shop

# §3.8
system_profiler SPHardwareDataType SPDisplaysDataType
python src/resource_inventory.py
```

