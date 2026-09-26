const TRIGGERS = [
  { id: "alert", label: "alert (hero chain)" },
  { id: "ticket", label: "ticket" },
  { id: "release", label: "release" },
  { id: "onboard", label: "onboard" },
  { id: "advisory", label: "advisory" },
];

const out = document.getElementById("output");
const container = document.getElementById("triggers");

async function run(trigger, btn) {
  document.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  out.textContent = "Loading…";
  try {
    const res = await fetch(`/api/run?trigger=${encodeURIComponent(trigger)}`);
    const text = await res.text();
    if (!res.ok) throw new Error(text);
    const data = JSON.parse(text);
    out.textContent = JSON.stringify(data, null, 2);
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
