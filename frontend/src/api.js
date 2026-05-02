const API_BASE = "http://localhost:8000/api";

const FETCH_TIMEOUT = 10000;
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

const safeFetch = async (url, retries = MAX_RETRIES) => {
    let lastError;
    for (let attempt = 0; attempt <= retries; attempt++) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT);
        try {
            const res = await fetch(url, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        } catch (err) {
            clearTimeout(timeoutId);
            lastError = err;
            if (attempt < retries && (err.name === 'AbortError' || err.message.includes('network') || err.message.includes('Failed to fetch'))) {
                await new Promise(r => setTimeout(r, RETRY_DELAY * (attempt + 1)));
                continue;
            }
            throw err;
        }
    }
    throw lastError || new Error('Fetch failed after retries');
};

export const fetchWorldState     = () => safeFetch(`${API_BASE}/world`);
export const fetchAgents         = () => safeFetch(`${API_BASE}/agents`);
export const fetchAgent          = (id) => safeFetch(`${API_BASE}/agents/${id}`);
export const fetchEvents         = (limit = 60) => safeFetch(`${API_BASE}/events?limit=${limit}`);
export const fetchStatus         = () => safeFetch(`${API_BASE}/status`);
export const fetchEconomyHistory = (limit = 100) => safeFetch(`${API_BASE}/economy/history?limit=${limit}`);
export const fetchJobs           = () => safeFetch(`${API_BASE}/jobs`);
export const fetchOntology      = () => safeFetch(`${API_BASE}/ontology`);
export const fetchFeatures      = () => safeFetch(`${API_BASE}/features`);
export const fetchCausal        = (limit = 60) => safeFetch(`${API_BASE}/causal?limit=${limit}`);
export const fetchHealth        = () => safeFetch(`${API_BASE}/health`);

export const pauseSimulation  = () => fetch(`${API_BASE}/control/pause`,  { method: "POST" }).then(r => r.json());
export const resumeSimulation = () => fetch(`${API_BASE}/control/resume`, { method: "POST" }).then(r => r.json());
export const setSpeed         = (tps) => fetch(`${API_BASE}/control/speed?tps=${tps}`, { method: "POST" }).then(r => r.json());

// New endpoints for missing features
export const fetchInformation = () => safeFetch(`${API_BASE}/information/state`);
export const fetchRelationships = () => safeFetch(`${API_BASE}/relationships`);
export const fetchSnapshots = () => safeFetch(`${API_BASE}/snapshots`);
export const saveSnapshot = (name) => fetch(`${API_BASE}/snapshots/save?name=${name}`, { method: "POST" }).then(r => r.json());
export const loadSnapshot = (tick) => safeFetch(`${API_BASE}/snapshots/load?tick=${tick}`);
export const fetchMarket = () => safeFetch(`${API_BASE}/market/state`);
export const fetchPolitical = () => safeFetch(`${API_BASE}/political/summary`);
export const fetchFinancial = () => safeFetch(`${API_BASE}/financial/summary`);
