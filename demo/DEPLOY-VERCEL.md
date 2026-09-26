# Deploy Lane demo to Vercel

This folder is a **small web demo**: visitors click workflow triggers and see **real orchestrator run JSON** captured from your project. It is not a full Python runtime (Vercel cannot run `lane` + file patches reliably).

## Prerequisites

- [Vercel account](https://vercel.com)
- [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`

## Deploy

```bash
cd ~/Downloads/PROJECT-02/demo
vercel login
vercel --prod
```

When linking the project:

- **Root Directory:** `demo` (if importing from GitHub monorepo, set this in Vercel project settings)

## After deploy

- **Application URL** for lablab: `https://your-project.vercel.app`
- Test: open the site → click **alert (hero chain)** → JSON appears

## Refresh demo data (after you change Lane)

From repo root:

```bash
cd ~/Downloads/PROJECT-02
for t in alert ticket release onboard advisory; do
  python3 -m lane run --trigger $t > /tmp/lane-$t.out 2>&1
  LOG=$(grep '^Log:' /tmp/lane-$t.out | awk '{print $2}')
  cp "$LOG" "demo/public/data/${t}.json"
done
cd demo && vercel --prod
```

## Full local testing (for developers)

```bash
git clone https://github.com/Ravi-Saxena-kronos/lane-harbor-stay.git
cd lane-harbor-stay
python3 -m lane run --trigger alert
```
