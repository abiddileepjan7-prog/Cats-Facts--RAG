const form = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const conversation = document.getElementById("conversation");
const submitButton = document.getElementById("submit-button");
const statusPill = document.getElementById("status-pill");
const promptChips = document.querySelectorAll(".prompt-chip");

function setStatus(text, busy = false) {
  statusPill.textContent = text;
  statusPill.dataset.busy = busy ? "true" : "false";
}

function appendMessage(role, content) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "user" ? "You" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  const roleLabel = document.createElement("p");
  roleLabel.className = "message-role";
  roleLabel.textContent = role === "user" ? "You" : "Assistant";

  const body = document.createElement("p");
  body.textContent = content;

  bubble.append(roleLabel, body);
  article.append(avatar, bubble);
  conversation.appendChild(article);
  conversation.scrollTop = conversation.scrollHeight;
}

function autoResizeTextarea() {
  questionInput.style.height = "auto";
  questionInput.style.height = `${Math.min(questionInput.scrollHeight, 180)}px`;
}

async function askQuestion(query) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || "Something went wrong.");
  }

  return payload;
}

async function submitQuestion() {
  const query = questionInput.value.trim();

  if (!query) {
    setStatus("Enter a question");
    return;
  }

  appendMessage("user", query);
  questionInput.value = "";
  autoResizeTextarea();
  submitButton.disabled = true;
  setStatus("Searching...", true);

  try {
    const result = await askQuestion(query);
    appendMessage("assistant", result.answer);
    setStatus("Answered");
  } catch (error) {
    appendMessage("assistant", error.message);
    setStatus("Error");
  } finally {
    submitButton.disabled = false;
    questionInput.focus();
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitQuestion();
});

questionInput.addEventListener("keydown", async (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    if (!submitButton.disabled) {
      await submitQuestion();
    }
  }
});

questionInput.addEventListener("input", autoResizeTextarea);

promptChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    questionInput.value = chip.dataset.prompt || "";
    autoResizeTextarea();
    questionInput.focus();
  });
});

autoResizeTextarea();
