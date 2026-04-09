const API_BASE = "http://localhost:8000/api";

export const fetchWorldState = async () => {
    const res = await fetch(`${API_BASE}/world`);
    return res.json();
};

export const fetchAgents = async () => {
    const res = await fetch(`${API_BASE}/agents`);
    return res.json();
};

export const fetchEvents = async () => {
    const res = await fetch(`${API_BASE}/events?limit=20`);
    return res.json();
};

export const fetchStatus = async () => {
    const res = await fetch(`${API_BASE}/status`);
    return res.json();
};

export const pauseSimulation = async () => {
    const res = await fetch(`${API_BASE}/control/pause`, { method: "POST" });
    return res.json();
};

export const resumeSimulation = async () => {
    const res = await fetch(`${API_BASE}/control/resume`, { method: "POST" });
    return res.json();
};
