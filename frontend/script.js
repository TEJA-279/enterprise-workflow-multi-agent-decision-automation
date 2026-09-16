const STORAGE_KEYS = {
    users: "ai_workflow_users",
    activeUser: "ai_workflow_active_user",
    history: "ai_workflow_history_"
};

const API_URL = window.WORKFLOW_API_URL || (
    window.location.port === "5500"
        ? "http://127.0.0.1:8000/workflow"
        : "/api/workflow"
);

const authModal = document.getElementById("authModal");
const closeAuthModal = document.getElementById("closeAuthModal");
const openAuthModal = document.getElementById("openAuthModal");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const authError = document.getElementById("authError");
const authTitle = document.getElementById("authTitle");
const authSubtitle = document.getElementById("authSubtitle");
const showLoginTab = document.getElementById("showLoginTab");
const showRegisterTab = document.getElementById("showRegisterTab");
const logoutButton = document.getElementById("logoutButton");
const userBadge = document.getElementById("userBadge");
const historyList = document.getElementById("historyList");
const clearHistoryButton = document.getElementById("clearHistoryButton");

const messageInput = document.getElementById("message");
const submitButton = document.getElementById("submitButton");
const buttonText = document.getElementById("buttonText");
const responseContainer = document.getElementById("responseContainer");
const loading = document.getElementById("loading");
const errorContainer = document.getElementById("errorContainer");
const sessionInfo = document.getElementById("sessionInfo");
const characterCount = document.getElementById("characterCount");

const state = {
    activeUser: localStorage.getItem(STORAGE_KEYS.activeUser) || "",
    sessionId: "session-" + Date.now(),
    authMode: "login"
};

function getUsers() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEYS.users) || "{}");
    } catch (error) {
        return {};
    }
}

function saveUsers(users) {
    localStorage.setItem(STORAGE_KEYS.users, JSON.stringify(users));
}

function ensureDemoUser() {
    const users = getUsers();
    if (!users.admin) {
        users.admin = {
            username: "admin",
            password: "admin123",
            role: "admin"
        };
        saveUsers(users);
    }
}

function setAuthMode(mode) {
    state.authMode = mode;
    const isLogin = mode === "login";
    loginForm.classList.toggle("hidden", !isLogin);
    registerForm.classList.toggle("hidden", isLogin);
    showLoginTab.classList.toggle("active", isLogin);
    showRegisterTab.classList.toggle("active", !isLogin);

    authTitle.textContent = isLogin ? "Welcome back" : "Create account";
    authSubtitle.textContent = isLogin
        ? "Sign in to access your enterprise workflow dashboard."
        : "Register to create a secure personal workspace.";
    authError.classList.add("hidden");
    authError.textContent = "";
}

function getHistoryKey(username) {
    return `${STORAGE_KEYS.history}${username}`;
}

function getHistoryForUser(username) {
    try {
        return JSON.parse(localStorage.getItem(getHistoryKey(username)) || "[]");
    } catch (error) {
        return [];
    }
}

function saveHistoryForUser(username, entries) {
    localStorage.setItem(getHistoryKey(username), JSON.stringify(entries));
}

function renderHistory() {
    const currentUser = state.activeUser;
    if (!currentUser) {
        historyList.innerHTML = "";
        return;
    }

    const entries = getHistoryForUser(currentUser);
    if (!entries.length) {
        historyList.innerHTML = '<div class="history-empty">No saved activity yet.</div>';
        return;
    }

    historyList.innerHTML = entries.map((entry) => `
        <div class="history-item" data-query="${escapeHtml(entry.query)}">
            <div class="history-topline"><span>${escapeHtml(entry.timestamp)}</span></div>
            <div class="history-question">${escapeHtml(entry.query)}</div>
            <div class="history-answer">${escapeHtml(entry.decision)}</div>
        </div>
    `).join("");

    historyList.querySelectorAll(".history-item").forEach((item) => {
        item.addEventListener("click", () => {
            messageInput.value = item.dataset.query;
            updateCharacterCount();
            messageInput.focus();
        });
    });
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function setSessionInfo() {
    sessionInfo.textContent = `Session: ${state.sessionId}`;
    userBadge.textContent = state.activeUser || "Guest";
}

function updateAuthButtons() {
    const isLoggedIn = !!state.activeUser;
    openAuthModal.classList.toggle("hidden", isLoggedIn);
    logoutButton.classList.toggle("hidden", !isLoggedIn);
    logoutButton.textContent = isLoggedIn ? `Logout (${state.activeUser})` : "Logout";
}

function showAuthModal() {
    authModal.classList.remove("hidden");
    authError.classList.add("hidden");
    authError.textContent = "";
}

function hideAuthModal() {
    authModal.classList.add("hidden");
    authError.classList.add("hidden");
    authError.textContent = "";
}

function login(username, password) {
    const users = getUsers();
    const normalizedUsername = String(username || "").trim();
    const normalizedPassword = String(password || "").trim();

    if (!normalizedUsername || !normalizedPassword) return false;

    ensureDemoUser();

    const user = users[normalizedUsername];
    if (user && user.password === normalizedPassword) {
        state.activeUser = normalizedUsername;
        localStorage.setItem(STORAGE_KEYS.activeUser, normalizedUsername);
        setSessionInfo();
        updateAuthButtons();
        renderHistory();
        hideAuthModal();
        return true;
    }

    if (normalizedUsername === "admin" && normalizedPassword === "admin123") {
        users.admin = { username: "admin", password: "admin123", role: "admin" };
        saveUsers(users);
        state.activeUser = "admin";
        localStorage.setItem(STORAGE_KEYS.activeUser, "admin");
        setSessionInfo();
        updateAuthButtons();
        renderHistory();
        hideAuthModal();
        return true;
    }

    return false;
}

function register(username, password, confirmPassword) {
    const users = getUsers();
    const normalizedUsername = String(username || "").trim();
    const normalizedPassword = String(password || "").trim();
    const normalizedConfirmPassword = String(confirmPassword || "").trim();

    if (!normalizedUsername || !normalizedPassword || !normalizedConfirmPassword) {
        return "Please fill in all fields.";
    }

    if (normalizedPassword.length < 6) return "Password must be at least 6 characters.";
    if (normalizedPassword !== normalizedConfirmPassword) return "Passwords do not match.";
    if (users[normalizedUsername]) return "That username already exists.";

    users[normalizedUsername] = {
        username: normalizedUsername,
        password: normalizedPassword,
        role: "user"
    };
    saveUsers(users);

    state.activeUser = normalizedUsername;
    localStorage.setItem(STORAGE_KEYS.activeUser, normalizedUsername);
    setSessionInfo();
    updateAuthButtons();
    renderHistory();
    hideAuthModal();
    return "";
}

function logout() {
    state.activeUser = "";
    localStorage.removeItem(STORAGE_KEYS.activeUser);
    setSessionInfo();
    renderHistory();
    updateAuthButtons();
    showAuthModal();
}

function addHistoryEntry(query, decision) {
    if (!state.activeUser) return;

    const entries = getHistoryForUser(state.activeUser);
    entries.unshift({
        query,
        decision,
        timestamp: new Date().toLocaleString()
    });

    saveHistoryForUser(state.activeUser, entries.slice(0, 12));
    renderHistory();
}

function updateCharacterCount() {
    characterCount.textContent = `${messageInput.value.length} / 2000`;
}

loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    if (!login(username, password)) {
        authError.textContent = "Invalid username or password.";
        authError.classList.remove("hidden");
        return;
    }

    loginForm.reset();
});

registerForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;
    const confirmPassword = document.getElementById("registerConfirmPassword").value;

    const error = register(username, password, confirmPassword);
    if (error) {
        authError.textContent = error;
        authError.classList.remove("hidden");
        return;
    }

    registerForm.reset();
    authError.classList.add("hidden");
    authError.textContent = "";
});

showLoginTab.addEventListener("click", () => setAuthMode("login"));
showRegisterTab.addEventListener("click", () => setAuthMode("register"));
closeAuthModal.addEventListener("click", hideAuthModal);
openAuthModal.addEventListener("click", showAuthModal);
logoutButton.addEventListener("click", logout);
clearHistoryButton.addEventListener("click", () => {
    if (!state.activeUser) return;
    saveHistoryForUser(state.activeUser, []);
    renderHistory();
});

submitButton.addEventListener("click", runWorkflow);
messageInput.addEventListener("input", updateCharacterCount);
messageInput.addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key === "Enter") {
        event.preventDefault();
        runWorkflow();
    }
});

function setWorkflowPhase(phaseName) {
    const phases = ["planning", "research", "analysis", "decision"];
    phases.forEach((phase) => {
        const element = document.getElementById(`step${phase.charAt(0).toUpperCase() + phase.slice(1)}`);
        if (!element) return;

        const isActive = phase === phaseName;
        const isCompleted = phases.indexOf(phase) < phases.indexOf(phaseName);
        element.classList.toggle("is-active", isActive);
        element.classList.toggle("is-complete", isCompleted);
        element.classList.toggle("is-pending", !isActive && !isCompleted);
    });
}

function animateWorkflowProcess() {
    const phases = ["planning", "research", "analysis", "decision"];
    phases.forEach((phase, index) => {
        window.setTimeout(() => setWorkflowPhase(phase), index * 600);
    });
}

async function runWorkflow() {
    if (!state.activeUser) {
        showAuthModal();
        authError.textContent = "Please log in or register before running a workflow.";
        authError.classList.remove("hidden");
        return;
    }

    const message = messageInput.value.trim();

    if (!message) {
        showError("Please enter a question.");
        return;
    }

    responseContainer.innerHTML = "";
    clearError();
    loading.classList.remove("hidden");
    submitButton.disabled = true;
    buttonText.textContent = "Processing...";
    animateWorkflowProcess();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: state.sessionId,
                message: message
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Backend request failed.");
        }

        if (data.decision && data.decision.trim()) {
            responseContainer.innerHTML = "";
            const answer = document.createElement("div");
            answer.className = "ai-response";
            answer.textContent = data.decision;
            responseContainer.appendChild(answer);
            addHistoryEntry(message, data.decision);
        } else {
            responseContainer.innerHTML = "No answer was returned.";
        }

        if (data.errors && data.errors.length > 0) {
            showError(data.errors.join("\n"));
        }

        setWorkflowPhase("decision");
    } catch (error) {
        console.error("ERROR:", error);
        showError("Unable to connect to the AI system: " + error.message);
        responseContainer.textContent = "Unable to get an AI response.";
        setWorkflowPhase("planning");
    } finally {
        loading.classList.add("hidden");
        submitButton.disabled = false;
        buttonText.textContent = "Run Analysis";
    }
}

function showError(message) {
    errorContainer.textContent = message;
    errorContainer.classList.remove("hidden");
}

function clearError() {
    errorContainer.textContent = "";
    errorContainer.classList.add("hidden");
}

ensureDemoUser();
setAuthMode("login");
setSessionInfo();
updateCharacterCount();
setWorkflowPhase("planning");
updateAuthButtons();
renderHistory();

if (!state.activeUser) {
    showAuthModal();
}
