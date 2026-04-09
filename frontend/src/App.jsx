import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatCard from './components/StatCard';
import Controls from './components/Controls';
import AgentList from './components/AgentList';
import EventTimeline from './components/EventTimeline';
import EconomyChart from './components/EconomyChart';
import JobMarket from './components/JobMarket';
import AgentModal from './components/AgentModal';

import { fetchWorldState, fetchAgents, fetchEvents, fetchStatus, fetchEconomyHistory, fetchJobs } from './api';
import './index.css';

function App() {
  const [world, setWorld] = useState(null);
  const [agents, setAgents] = useState([]);
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState({ running: false, tick: 0 });
  const [economyHistory, setEconomyHistory] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState(null);

  // UI State
  const [activeTab, setActiveTab] = useState('overview'); // overview, agents, economy, events
  const [selectedAgentId, setSelectedAgentId] = useState(null);

  const pollData = async () => {
    try {
      const [wData, agData, evData, statData, ecoData, jobData] = await Promise.all([
        fetchWorldState(),
        fetchAgents(),
        fetchEvents(),
        fetchStatus(),
        fetchEconomyHistory(),
        fetchJobs()
      ]);

      if (wData.error) {
        setError(wData.error);
        return;
      }

      setWorld(wData);
      setAgents(agData);
      setEvents(evData.events || []);
      setStatus(statData);
      setEconomyHistory(ecoData.history || []);
      setJobs(jobData.jobs || []);
      setError(null);
    } catch (err) {
      setError("Cannot connect to AI Simulation Server at http://localhost:8000.");
    }
  };

  useEffect(() => {
    pollData();
    const interval = setInterval(pollData, 1500); // Poll slightly faster for smoother charts
    return () => clearInterval(interval);
  }, []);

  if (error || !world) {
    return (
      <div className="app-shell" style={{ alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <Header status={null} isConnected={false} isRunning={false} />
        <div className="glass" style={{ padding: '4rem', textAlign: 'center', maxWidth: '600px', marginTop: '2rem' }}>
          <h2 style={{ color: error ? 'var(--accent-red)' : 'var(--text-main)', fontSize: '1.5rem', marginBottom: '1rem' }}>
            {error ? "Backend Disconnected" : "Initializing Link..."}
          </h2>
          <p style={{ color: 'var(--text-muted)', lineHeight: '1.5' }}>
            {error || "Waiting for FastAPI server heartbeat..."}
          </p>
          {error && (
            <div style={{ background: 'rgba(0,0,0,0.4)', padding: '1rem', borderRadius: 8, marginTop: '1.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--accent-green)', letterSpacing: '0.05em' }}>
              &gt; python start.py
            </div>
          )}
        </div>
      </div>
    );
  }

  const { stats, economy } = world;

  return (
    <div className="app-shell">
      <Header status={status} isConnected={true} isRunning={status.running} />

      {/* Main Control Strip */}
      <div className="glass" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.5rem' }}>
        <div className="nav-tabs">
          <button className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>🌍 Overview</button>
          <button className={`tab-btn ${activeTab === 'agents' ? 'active' : ''}`}   onClick={() => setActiveTab('agents')}>🤖 Agents</button>
          <button className={`tab-btn ${activeTab === 'economy' ? 'active' : ''}`}  onClick={() => setActiveTab('economy')}>💹 Economy</button>
          <button className={`tab-btn ${activeTab === 'events' ? 'active' : ''}`}   onClick={() => setActiveTab('events')}>📜 Event Ledger</button>
        </div>
        <Controls isRunning={status.running} onToggle={pollData} />
      </div>

      {/* Dynamic Content Area */}
      {activeTab === 'overview' && (
        <div className="fade-in-up" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="stats-grid">
            <StatCard title="Avg Happiness" value={`${stats.avg_happiness || 0}%`} subtitle={`Gini Index: ${stats.wealth_gini || 0}`} color="var(--accent-green)" icon="😊" />
            <StatCard title="Treasury"      value={`$${Math.round(economy.treasury).toLocaleString()}`} subtitle={`Inf: ${economy.inflation_rate.toFixed(3)}×`} color="var(--accent-yellow)" icon="🏦" />
            <StatCard title="Agents in Crisis" value={stats.agents_in_crisis || 0} subtitle={stats.agents_in_crisis > 0 ? "Intervention needed" : "All optimal"} color={stats.agents_in_crisis > 0 ? "var(--accent-red)" : "var(--accent-cyan)"} icon="🚨" />
            <StatCard title="Top Earner"    value={`$${Math.round(stats.top_earner_cash || 0).toLocaleString()}`} subtitle={stats.top_earner || 'None'} color="var(--accent-purple)" icon="🏆" />
          </div>
          <div className="dashboard-split">
            <EconomyChart history={economyHistory} />
            <EventTimeline events={events} />
          </div>
        </div>
      )}

      {activeTab === 'agents' && (
        <div className="fade-in-up" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="stats-grid">
            <StatCard title="Total Population" value={agents.length} color="var(--accent-blue)" icon="👥" />
            <StatCard title="Avg Energy"    value={`${stats.avg_energy || 0}%`} color="var(--accent-blue)" icon="⚡" />
            <StatCard title="Avg Hunger"    value={`${stats.avg_hunger || 0}%`} color="var(--accent-red)" icon="🍔" />
          </div>
          <AgentList agents={agents} onSelect={a => setSelectedAgentId(a.id)} />
        </div>
      )}

      {activeTab === 'economy' && (
        <div className="fade-in-up dashboard-split">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
               <StatCard title="GDP Spending" value={`$${Math.round(economy.tick_spending).toLocaleString()}`} subtitle="This tick" color="var(--accent-green)" />
               <StatCard title="Wages Paid" value={`$${Math.round(economy.tick_wages).toLocaleString()}`} subtitle="This tick" color="var(--accent-blue)" />
               <StatCard title="Employment" value={`${Math.round((economy.employed / economy.population)*100)}%`} subtitle={`${economy.employed}/${economy.population}`} color="var(--accent-purple)" />
            </div>
            <EconomyChart history={economyHistory} />
          </div>
          <JobMarket jobs={jobs} />
        </div>
      )}

      {activeTab === 'events' && (
        <div className="fade-in-up" style={{ height: 'calc(100vh - 200px)' }}>
          <EventTimeline events={events} />
        </div>
      )}

      {/* Modals */}
      {selectedAgentId && <AgentModal agentId={selectedAgentId} onClose={() => setSelectedAgentId(null)} />}
    </div>
  );
}

export default App;
