# Double Charge Club — Your step-by-step playbook (IBM Bob 2.0 Hackathon)

**Team:** Double Charge Club  
**Product:** Lane — one orchestrator, five agent apps, one sample repo (Harbor Stay)  
**Deadline:** Sunday, 27 Sep 2026, **8:30 PM IST** (15:00 UTC)

Use this document top to bottom. Check off each step as you finish.

---

## Part A — Accounts and team (you, ~30 minutes)

### Step 1 — Confirm you are in the hackathon

| What | Why |
|------|-----|
| Log in to [lablab IBM Bob 2.0](https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon) | You must be enrolled to submit |
| Open the [live dashboard](https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon/live) | See countdown and submission link |

**How:** Browser → lablab.ai → your profile → hackathon page. Status should show you are building.

---

### Step 2 — Team profile

| What | Why |
|------|-----|
| Team name: **Double Charge Club** | Already chosen |
| Upload **cover image** | Team spirit on lablab |

**How:**

1. On lablab, open **Teams** for this hackathon.
2. Create or open team **Double Charge Club**.
3. Upload: `submission/cover-double-charge-club.png`  
   (If missing, open `submission/cover-double-charge-club.html` in Chrome, screenshot the dark 1280×720 area, save as PNG.)
4. Short team description (≤20 chars): e.g. `5-agent orchestrator`

---

### Step 3 — Discord and Bob access

| What | Why |
|------|-----|
| Join lablab Discord from the hackathon page | Access instructions and help |
| Get **IBM Bob 2.0** login | Required to build and for submission screenshots |

**How:**

1. Click **Join Discord** on the hackathon page.
2. Read pinned messages / #announcements for **Bob 2.0 access** (link or invite).
3. Install/open Bob, sign in, run one tiny task (e.g. “explain this folder”).
4. Find **task session summary** in Bob UI — note where it appears (you will screenshot this often).

---

### Step 4 — GitHub

| What | Why |
|------|-----|
| New **public** repository | Judges need code + MIT license |
| MIT `LICENSE` in repo | Hackathon rules |

**How:**

1. github.com → **New repository** → name e.g. `lane-harbor-stay` → Public → Create.
2. On your PC:  
   `git clone https://github.com/YOUR_USER/lane-harbor-stay.git`  
   Copy your `PROJECT-02` work into that folder (or clone into `PROJECT-02`).
3. Add MIT license (GitHub offers “Add license” → MIT).

---

## Part B — What you are building (picture in your head)

```
You trigger Lane (alert / ticket / release / onboard / advisory)
        ↓
   ORCHESTRATOR (your Python code — the main originality)
        ↓
   Agent 1 … Agent 5 (each solves one real dev problem)
        ↓
   Same repo: Harbor Stay (fictional hotel booking API with a planted bug)
```

**You are NOT building five separate products.** You are building **one orchestrator** that runs **five apps** on **one repo**.

---

## Part C — Build order (Saturday → Sunday morning)

### Step 5 — Create Harbor Stay (`sample-service/`)

| What | Why |
|------|-----|
| Small Python API + tests + docs + fixtures | All agents read this repo |

**How (with Bob in Agent mode):**

1. In Bob, open your cloned repo folder.
2. Paste a prompt like:  
   *“Create `sample-service/` Harbor Stay: fictional inn API. Plant idempotency double-charge bug in `billing.py`. Add openapi drift, stale runbook, advisory JSON. MIT. Stdlib only. Tests pass before fix; `python -m harborstay.demo` shows 2 charges.”*  
3. Run locally:  
   `cd sample-service && python -m unittest discover -s tests`  
   `python -m harborstay.demo`
4. `git add` → `git commit` → `git push`

**Or:** Ask Cursor in this project: *“Execute Harbor Stay sample-service from the plan.”*

---

### Step 6 — Orchestrator core (`lane/`)

| What | Why |
|------|-----|
| `HandoffPacket` (JSON) | Data between apps — not chat text |
| `Orchestrator` class | Decides what runs, when, errors, done |
| CLI | Demo for judges |

**How:**

1. Create folder `lane/` with e.g. `orchestrator.py`, `packet.py`, `registry.py`, `cli.py`.
2. In Bob (or Cursor), implement:
   - **Packet fields:** `runId`, `trigger`, `status`, `artifacts`, `repoPath`
   - **Registry:**  
     - `alert` → incident → ticket → release  
     - `ticket` → ticket only  
     - `release` → release only  
     - `onboard` → onboard only  
     - `advisory` → advisory only
   - **Error rules:** missing input → stop; test fail → retry patch once; then escalate
3. Test:  
   `python -m lane run --trigger ticket --fixture sample-service/fixtures/tickets/SUP-1187.md`  
   (exact CLI name can match what you implement)

**Screenshot Bob** after this step → save to `submission/bob-screenshots/`.

---

### Step 7 — Five agent apps (one at a time)

Do **not** jump between all five. Finish one, test, commit.

| App | Input | Output | How you build it |
|-----|--------|--------|------------------|
| **Ticket-patch** | Support ticket file | Fix + test OR `needs_input` | Bob reads ticket + `billing.py`, adds idempotency test, runs unittest |
| **Incident** | Alert JSON | Files + action + status note | Bob reads alert + runbook, points to `billing.py` |
| **Release-gate** | Git diff / repo | go / no-go | Bob subagents: OpenAPI vs code, migration, tests in parallel |
| **Onboarding** | Repo + docs | Map + task; stop if runbook lies | Bob compares `docs/runbook.md` to real tree |
| **Advisory** | Advisory JSON | bump dep + test | Bob reads `deps/manifest.json` |

**How for each app:**

1. Bob **Plan mode** — 5-line plan for that app.
2. Bob **Agent mode** — edit only files for that app under `lane/agents/`.
3. Run orchestrator CLI for that trigger.
4. Screenshot **task session summary**.
5. `git commit -m "Add ticket-patch agent"` (etc.)

---

### Step 8 — Hero demo chain

| What | Why |
|------|-----|
| Run `alert` trigger end-to-end | Best story for video |

**How:**

1. Use fixture `sample-service/fixtures/alerts/ALT-2041.json`.
2. Run orchestrator: incident → ticket-patch → release-gate.
3. Confirm run log JSON shows each step and final `complete` or `escalated`.
4. Record screen while you run this once (keep for video).

---

### Step 9 — Bob evidence folder

| What | Why |
|------|-----|
| Folder `submission/bob-screenshots/` | Required on submission form |

**How:** After every major Bob session, export/screenshot **task session summary**. Aim for **5–10 images** (kernel, each agent, hero chain).

---

## Part D — Sunday: presentation only (stop coding early)

### Step 10 — Video (~3 minutes)

| Section | Time | What to show |
|---------|------|----------------|
| Problem | 20 s | Five manual dev workflows |
| Product | 30 s | Diagram: orchestrator + 5 apps |
| Demo | 90 s | Hero chain in terminal + packet/log |
| Bob | 30 s | Flash 2–3 Bob screenshots |
| Impact | 20 s | “One desk, tested patch, release gate” |

**How:** OBS or Zoom “record screen” → export MP4 → keep under platform size limit.

---

### Step 11 — Slides (6 slides PDF)

1. Title — Lane + Double Charge Club  
2. Problem  
3. Architecture  
4. Five agents table  
5. Screenshot of demo  
6. GitHub link + next steps  

**How:** Google Slides → Download PDF.

---

### Step 12 — Write submission text (copy into lablab)

**Title:**  
`Lane: orchestrated dev-ops desk with five IBM Bob agent apps`

**Short (one line):**  
`One orchestrator routes five workflow agents over a shared codebase (Harbor Stay).`

**Long (paste and edit):**  
We built Lane for the IBM Bob 2.0 hackathon. Developer teams waste time on incidents, repeat tickets, unsafe releases, slow onboarding, and scattered security advisories. Lane provides a single orchestrator that decides which specialist agent runs, in what order, what data is passed, how errors are handled, and when the workflow is complete. Five agents (incident, ticket-patch, release-gate, onboarding, advisory) share the fictional Harbor Stay repository. IBM Bob 2.0 was used in Agent mode with subagents and document understanding to implement agents and fix the planted double-charge bug with regression tests. Repository: [YOUR_GITHUB_URL].

**Tags:** `IBM Bob`, `orchestration`, `developer workflow`, `Python`, `agents`

---

## Part E — Submit on lablab (last step)

### Step 13 — Upload project

**How:**

1. Hackathon page → **Submit project** (or team dashboard → Submission).
2. Fill every field:
   - Title, short + long description, tags
   - Cover image (can reuse team cover or a **Lane** product cover)
   - Video MP4
   - Slides PDF
   - **Application URL** — GitHub repo or GitHub Pages
   - **Repository URL** — same GitHub, public
3. Attach **Bob task session screenshots** (upload or zip per form).
4. Mention in description which paths Bob helped (`lane/`, `sample-service/`).
5. Click **Submit** before **8:30 PM IST Sunday**.
6. After event: complete **feedback form** for $100 participant reward.

---

## Part F — Who does what

| Task | You | IBM Bob 2.0 | Cursor (this chat) |
|------|-----|-------------|---------------------|
| lablab login, team, submit | Yes | — | — |
| Bob login + screenshots | Yes | Yes | — |
| Video voice + record | Yes | — | — |
| Write orchestrator + agents | Guide + review | Implement in Agent mode | Can generate code if you ask |
| Harbor Stay sample repo | Run tests | Build | Can generate if you ask |
| Git push | Yes | — | — |

---

## If you only have time for the minimum

1. Harbor Stay + ticket-patch + orchestrator (one trigger).  
2. One Bob screenshot.  
3. 2-minute video + GitHub link + submit.

You still qualify; for judging, add hero chain + more screenshots.

---

## Your next 3 actions (start now)

1. Upload `submission/cover-double-charge-club.png` to team profile.  
2. Create GitHub repo + clone; get Bob access from Discord.  
3. Message Cursor: **“Build sample-service Harbor Stay and lane orchestrator skeleton.”**

Good luck — Double Charge Club.
