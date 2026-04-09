import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatCard from './components/StatCard';
import Controls from './components/Controls';
import AgentList from './components/AgentList';
import EventTimeline from './components/EventTimeline';
import { fetchWorldState, fetchAgents, fetchEvents, fetchStatus } from './api';
import './index.css';

function App() {
  const [world, setWorld] = useState(null);
  const [agents, setAgents] = useState([]);
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState({ running: false, tick: 0 });
  const [error, setError] = useState(null);

  const pollData = async () => {
    try {
      const w = await fetchWorldState();
      if (w.error) {
        setError(w.error);
        return;
      }
      setWorld(w);
      
      const ag = await fetchAgents();
      setAgents(ag);
      
      const evs = await fetchEvents();
      setEvents(evs.events || []);
      
      const stat = await fetchStatus();
      setStatus(stat);
      
      setError(null);
    } catch (err) {
      setError("Cannot connect to AI Simulation Server at http://localhost:8000.");
    }
  };

  useEffect(() => {
    pollData();
    const interval = setInterval(pollData, 3000); // Reduced polling to save API calls
    return () => clearInterval(interval);
  }, []);

  if (error || !world) {
    return (
      <div className="app-container" style={{ alignItems: 'center', justifyContent: 'center', height: '100vh', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        <Header />
        <div className="glass-panel" style={{ padding: '4rem', textAlign: 'center', maxWidth: '600px' }}>
          <h2 style={{ color: error ? 'var(--accent-red)' : 'var(--text-main)' }}>
            {error ? "Backend Disconnected" : "Initializing Link..."}
          </h2>
          <p style={{ color: 'var(--text-muted)', marginTop: '1rem', lineHeight: '1.5' }}>
            {error || "Waiting for FastAPI server heartbeat..."}
          </p>
          {error && (
            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px', marginTop: '1.5rem', fontFamily: 'monospace', fontSize: '0.9rem', color: 'var(--accent-green)' }}>
              python main.py --server
            </div>
          )}
        </div>
      </div>
    );
  }
  
  return (
    <div className="app-container">
      <Header isConnected={true} isRunning={status.running} />
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
        <h2 style={{ paddingLeft: '0.5rem', color: 'var(--text-main)', fontSize: '1.5rem', margin: 0 }}>Global Telemetry</h2>
        <Controls isRunning={status.running} />
      </div>
      
      <div className="stats-grid">
        <StatCard 
          title="World Time" 
          value={`Day ${world.day}`} 
          subtitle={`${world.time_of_day} • ${world.weather}`} 
          color="var(--text-main)" 
        />
        <StatCard 
          title="Global Treasury" 
          value={`$${world.economy.treasury.toLocaleString(undefined, {maximumFractionDigits: 0})}`} 
          subtitle={`Inflation: ${world.economy.inflation_rate.toFixed(3)}x`} 
          color="var(--accent-green)" 
        />
        <StatCard 
          title="Population" 
          value={world.economy.population} 
          subtitle={`${world.economy.employed} Employed`} 
          color="var(--accent-blue)" 
        />
        <StatCard 
          title="Simulation Tick" 
          value={status.tick} 
          subtitle={status.running ? "Looping Active" : "Time Frozen"}
          color="var(--accent-purple)" 
        />
      </div>
      
      <div className="dashboard-grid">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <h2 style={{ paddingLeft: '0.5rem', color: 'var(--text-main)', fontSize: '1.5rem', margin: '1rem 0 0 0' }}>Agent Neural Network</h2>
          <AgentList agents={agents} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <h2 style={{ paddingLeft: '0.5rem', color: 'var(--text-main)', fontSize: '1.5rem', margin: '1rem 0 0 0' }}>Activity Ledger</h2>
          <EventTimeline events={events} />
        </div>
      </div>
    </div>
  );
}

export default App;
