const TRIGGERS = [
  { id: "alert", label: "alert (hero chain)" },
  { id: "ticket", label: "ticket" },
  { id: "release", label: "release" },
  { id: "onboard", label: "onboard" },
  { id: "advisory", label: "advisory" },
];

const out = document.getElementById("output");
const container = document.getElementById("triggers");

async function loadTrigger(trigger) {
  const staticUrl = `/data/${trigger}.json`;
  let res = await fetch(staticUrl);
  if (res.ok) {
    return { data: await res.json(), source: staticUrl };
  }
  const apiUrl = `/api/run?trigger=${encodeURIComponent(trigger)}`;
  res = await fetch(apiUrl);
  const text = await res.text();
  if (!res.ok) {
    throw new Error(text || `HTTP ${res.status}`);
  }
  return { data: JSON.parse(text), source: apiUrl };
}

async function run(trigger, btn) {
  document.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  out.textContent = "Loading…";
  try {
    const { data, source } = await loadTrigger(trigger);
    out.textContent = `// ${source}\n\n${JSON.stringify(data, null, 2)}`;
  } catch (err) {
    out.textContent = String(err);
  }
}

TRIGGERS.forEach(({ id, label }) => {
  const btn = document.createElement("button");
  btn.textContent = label;
  btn.type = "button";
  btn.addEventListener("click", () => run(id, btn));
  container.appendChild(btn);
});
