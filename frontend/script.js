const state = {
  running: false,
  route: "IDLE"
};

const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const chatMessages = document.getElementById("chatMessages");
const activityLog = document.getElementById("activityLog");
const routeBadge = document.getElementById("routeBadge");
const sqlViewer = document.getElementById("sqlViewer");
const mcpTool = document.getElementById("mcpTool");
const mcpStatus = document.getElementById("mcpStatus");
const mcpRows = document.getElementById("mcpRows");
const sourceList = document.getElementById("sourceList");

const demoResponses = {
  "What are our total sales?": {
    route: "SQL",
    sql: "SELECT SUM(total_amount) AS total_sales FROM orders WHERE status = 'Completed';",
    tool: "execute_readonly_sql",
    rows: 1,
    answer: "Our total completed sales are ₹7.13 crore.",
    sources: [],
    events: [
      "Orchestrator selected SQL",
      "SQL Agent generated a read-only query",
      "MCP tool execute_readonly_sql called",
      "SQLite returned 1 row",
      "Response Agent synthesized the result"
    ]
  },
  "What is our refund policy?": {
    route: "RAG",
    sql: "Waiting for SQL Agent...",
    tool: "-",
    rows: "-",
    answer: "Our refund policy allows refunds within the documented eligibility window. The final policy details are retrieved from the company knowledge base.",
    sources: [
      { document: "refund_policy.pdf", page: 1 },
      { document: "faq.pdf", page: 1 }
    ],
    events: [
      "Orchestrator selected RAG",
      "RAG Agent searched ChromaDB",
      "Retrieved refund_policy.pdf",
      "Retrieved faq.pdf",
      "Response Agent synthesized the evidence"
    ]
  },
  "Which product generated the highest revenue?": {
    route: "SQL",
    sql: "SELECT p.product_name, SUM(oi.quantity * oi.unit_price) AS total_revenue FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_id, p.product_name ORDER BY total_revenue DESC LIMIT 1;",
    tool: "execute_readonly_sql",
    rows: 1,
    answer: "The product with the highest revenue is the 4K Monitor.",
    sources: [],
    events: [
      "Orchestrator selected SQL",
      "SQL Agent generated a revenue aggregation query",
      "MCP tool execute_readonly_sql called",
      "SQLite returned the top product",
      "Response Agent synthesized the result"
    ]
  }
};

function addMessage(role, text) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role === "user" ? "user-avatar" : "assistant-avatar"}`;
  avatar.textContent = role === "user" ? "YOU" : "BI";

  const body = document.createElement("div");
  body.className = "message-body";

  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "You" : "BizInsight AI";

  const content = document.createElement("div");
  content.className = "message-text";
  content.textContent = text;

  body.append(meta, content);
  wrapper.append(avatar, body);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function clearActivity() {
  activityLog.innerHTML = "";
}

function addActivity(text) {
  const item = document.createElement("div");
  item.className = "activity-item";

  const dot = document.createElement("span");
  dot.className = "activity-dot";

  const content = document.createElement("div");
  content.className = "activity-text";
  content.textContent = text;

  item.append(dot, content);
  activityLog.appendChild(item);
  activityLog.scrollTop = activityLog.scrollHeight;
}

function setNode(node, status, label) {
  const element = document.querySelector(`[data-node="${node}"]`);
  if (!element) return;

  element.classList.remove("active", "done");
  if (status === "active") element.classList.add("active");
  if (status === "done") element.classList.add("done");

  const stateLabel = element.querySelector(".node-state");
  if (stateLabel && label) stateLabel.textContent = label;
}

function resetNodes() {
  ["orchestrator", "sql", "mcp", "rag", "chroma", "response"].forEach((node) => {
    setNode(node, "idle", node === "mcp" ? "execute_readonly_sql" : node === "chroma" ? "Vector retrieval" : "Waiting");
  });
}

function updateInspector(response) {
  sqlViewer.textContent = response.sql || "No SQL generated.";
  mcpTool.textContent = response.tool || "-";
  mcpStatus.textContent = response.tool && response.tool !== "-" ? "Success" : "Not used";
  mcpRows.textContent = response.rows ?? "-";

  sourceList.innerHTML = "";

  if (!response.sources || response.sources.length === 0) {
    sourceList.innerHTML = '<div class="empty-state">No documents retrieved.</div>';
    return;
  }

  response.sources.forEach((source) => {
    const item = document.createElement("div");
    item.className = "source-item";
    item.innerHTML = `
      <span class="source-name">${escapeHtml(source.document)}</span>
      <span class="source-page">Page ${escapeHtml(String(source.page))}</span>
    `;
    sourceList.appendChild(item);
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;"
  }[char]));
}

async function animateExecution(response) {
  clearActivity();
  resetNodes();

  routeBadge.textContent = response.route;
  routeBadge.className = "route-badge active";

  setNode("orchestrator", "active", `Route = ${response.route}`);
  addActivity(`Orchestrator selected ${response.route}`);
  await sleep(420);
  setNode("orchestrator", "done", `Route = ${response.route}`);

  const needsSql = response.route === "SQL" || response.route === "BOTH";
  const needsRag = response.route === "RAG" || response.route === "BOTH";

  if (needsSql) {
    setNode("sql", "active", "Generating SQL");
    addActivity("SQL Agent started");
    await sleep(520);
    setNode("sql", "done", "SQL generated");
    addActivity("SQL Agent generated a read-only query");

    setNode("mcp", "active", "Calling tool");
    addActivity(`MCP Tool: ${response.tool}`);
    await sleep(440);
    setNode("mcp", "done", `Success · ${response.rows} row(s)`);
    addActivity(`MCP tool returned ${response.rows} row(s)`);
  }

  if (needsRag) {
    setNode("rag", "active", "Retrieving evidence");
    addActivity("RAG Agent started");
    await sleep(520);
    setNode("rag", "done", "Retrieved evidence");
    addActivity(`RAG retrieved ${response.sources.length} source(s)`);

    setNode("chroma", "active", "Similarity search");
    await sleep(380);
    setNode("chroma", "done", `${response.sources.length} source(s)`);
    response.sources.forEach((source) => addActivity(`Source: ${source.document} · Page ${source.page}`));
  }

  setNode("response", "active", "Synthesizing answer");
  addActivity("Response Agent started");
  await sleep(580);
  setNode("response", "done", "Completed");
  addActivity("Response Agent completed");
  addMessage("assistant", response.answer);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sendQuestion(question) {
  const cleanQuestion = question.trim();
  if (!cleanQuestion || state.running) return;

  state.running = true;
  sendBtn.disabled = true;
  questionInput.value = "";
  addMessage("user", cleanQuestion);

  // Temporary local demo response. This will be replaced by the FastAPI /chat call next.
  const response = demoResponses[cleanQuestion] || {
    route: "BOTH",
    sql: "SELECT ...",
    tool: "execute_readonly_sql",
    rows: 0,
    answer: "This is the frontend demo mode. The next backend integration will send the real LangGraph execution details here.",
    sources: [
      { document: "loyalty_program.pdf", page: 1 }
    ],
    events: ["Demo execution"]
  };

  updateInspector(response);
  await animateExecution(response);

  state.running = false;
  sendBtn.disabled = false;
}

sendBtn.addEventListener("click", () => sendQuestion(questionInput.value));

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendQuestion(questionInput.value);
  }
});

document.querySelectorAll(".suggestion").forEach((button) => {
  button.addEventListener("click", () => sendQuestion(button.textContent));
});

document.getElementById("newChatBtn").addEventListener("click", () => {
  chatMessages.innerHTML = "";
  clearActivity();
  resetNodes();
  routeBadge.textContent = "IDLE";
  routeBadge.className = "route-badge neutral";
  sqlViewer.textContent = "Waiting for SQL agent...";
  mcpTool.textContent = "-";
  mcpStatus.textContent = "-";
  mcpRows.textContent = "-";
  sourceList.innerHTML = '<div class="empty-state">No documents retrieved yet.</div>';
  addMessage("assistant", "New conversation started. Ask a business question.");
});
