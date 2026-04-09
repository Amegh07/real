const API_BASE = "http://localhost:8000/api";

const safeFetch = async (url) => {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
};

export const fetchWorldState     = () => safeFetch(`${API_BASE}/world`);
export const fetchAgents         = () => safeFetch(`${API_BASE}/agents`);
export const fetchAgent          = (id) => safeFetch(`${API_BASE}/agents/${id}`);
export const fetchEvents         = (limit = 60) => safeFetch(`${API_BASE}/events?limit=${limit}`);
export const fetchStatus         = () => safeFetch(`${API_BASE}/status`);
export const fetchEconomyHistory = (limit = 100) => safeFetch(`${API_BASE}/economy/history?limit=${limit}`);
export const fetchJobs           = () => safeFetch(`${API_BASE}/jobs`);

export const pauseSimulation  = () => fetch(`${API_BASE}/control/pause`,  { method: "POST" }).then(r => r.json());
export const resumeSimulation = () => fetch(`${API_BASE}/control/resume`, { method: "POST" }).then(r => r.json());
export const setSpeed         = (tps) => fetch(`${API_BASE}/control/speed?tps=${tps}`, { method: "POST" }).then(r => r.json());
