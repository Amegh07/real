import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatCard from './components/StatCard';
import Controls from './components/Controls';
import AgentList from './components/AgentList';
import EventTimeline from './components/EventTimeline';
import EconomyChart from './components/EconomyChart';
import JobMarket from './components/JobMarket';
import AgentModal from './components/AgentModal';
import OntologyPanel from './components/OntologyPanel';

import { fetchWorldState, fetchAgents, fetchEvents, fetchStatus, fetchEconomyHistory, fetchJobs, fetchOntology, fetchFeatures, fetchCausal, fetchInformation, fetchRelationships, fetchMarket, fetchPolitical, fetchFinancial } from './api';
import './index.css';

function App() {
  const [world, setWorld] = useState(null);
  const [agents, setAgents] = useState([]);
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState({ running: false, tick: 0 });
  const [economyHistory, setEconomyHistory] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [ontology, setOntology] = useState(null);
  const [features, setFeatures] = useState([]);
  const [causal, setCausal] = useState([]);
  const [information, setInformation] = useState({});
  const [relationships, setRelationships] = useState({});
  const [market, setMarket] = useState({});
  const [political, setPolitical] = useState({});
  const [financial, setFinancial] = useState({});
  const [error, setError] = useState(null);

  const [activeTab, setActiveTab] = useState('overview');
  const [selectedAgentId, setSelectedAgentId] = useState(null);

  const pollData = async () => {
    const fetchWithError = async (fn, fallback) => {
      try {
        return await fn();
      } catch (err) {
        console.warn('Fetch failed:', err.message);
        return fallback;
      }
    };
    try {
      const [wData, agData, evData, statData, ecoData, jobData, ontologyData, featureData, causalData, infoData, relData, marketData, polData, finData] = await Promise.all([
        fetchWithError(fetchWorldState, null),
        fetchWithError(fetchAgents, []),
        fetchWithError(fetchEvents, { events: [] }),
        fetchWithError(fetchStatus, { running: false, tick: 0 }),
        fetchWithError(fetchEconomyHistory, { history: [] }),
        fetchWithError(fetchJobs, { jobs: [] }),
        fetchWithError(fetchOntology, null),
        fetchWithError(fetchFeatures, { features: [] }),
        fetchWithError(fetchCausal, { records: [] }),
        fetchWithError(fetchInformation, {}),
        fetchWithError(fetchRelationships, { stats: {} }),
        fetchWithError(fetchMarket, {}),
        fetchWithError(fetchPolitical, {}),
        fetchWithError(fetchFinancial, {})
      ]);

      if (wData?.error) {
        setError(wData.error);
        return;
      }

      setWorld(wData);
      setAgents(Array.isArray(agData) ? agData : []);
      setEvents(Array.isArray(evData?.events) ? evData.events : []);
      setStatus(statData || { running: false, tick: 0 });
      setEconomyHistory(Array.isArray(ecoData?.history) ? ecoData.history : []);
      setJobs(Array.isArray(jobData?.jobs) ? jobData.jobs : []);
      setOntology(ontologyData);
      setFeatures(Array.isArray(featureData?.features) ? featureData.features : []);
      setCausal(Array.isArray(causalData?.records) ? causalData.records : []);
      setInformation(infoData || {});
      setRelationships(relData || {});
      setMarket(marketData || {});
      setPolitical(polData || {});
      setFinancial(finData || {});
      setError(null);
    } catch (err) {
      setError("Cannot connect to server.");
    }
  };

  useEffect(() => {
    pollData();
    const interval = setInterval(pollData, 1500);
    return () => clearInterval(interval);
  }, []);

  if (error || !world) {
    return (
      <div className="app-shell" style={{ alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <Header status={null} isConnected={false} isRunning={false} />
        <div className="glass" style={{ padding: '4rem', textAlign: 'center', maxWidth: '600px', marginTop: '2rem' }}>
          <h2 style={{ color: error ? 'var(--accent-red)' : 'var(--text-main)', fontSize: '1.5rem', marginBottom: '1rem' }}>
            {error ? "Backend Disconnected" : "Initializing..."}
          </h2>
          <p style={{ color: 'var(--text-muted)' }}>{error || "Waiting for server..."}</p>
        </div>
      </div>
    );
  }

  const { stats, economy, dimensions } = world;
  const worldDimensions = dimensions?.dimensions || {};
  const avgStress = worldDimensions.biophysical?.avg_stress_load ?? 0;
  const activeCases = worldDimensions.pathology?.active_cases ?? 0;

  return (
    <div className="app-shell">
      <Header status={status} isConnected={true} isRunning={status.running} />

      <div className="glass" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.5rem' }}>
        <div className="nav-tabs">
          <button className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>Overview</button>
          <button className={`tab-btn ${activeTab === 'agents' ? 'active' : ''}`} onClick={() => setActiveTab('agents')}>Agents</button>
          <button className={`tab-btn ${activeTab === 'economy' ? 'active' : ''}`} onClick={() => setActiveTab('economy')}>Economy</button>
          <button className={`tab-btn ${activeTab === 'market' ? 'active' : ''}`} onClick={() => setActiveTab('market')}>Market</button>
          <button className={`tab-btn ${activeTab === 'events' ? 'active' : ''}`} onClick={() => setActiveTab('events')}>Events</button>
          <button className={`tab-btn ${activeTab === 'network' ? 'active' : ''}`} onClick={() => setActiveTab('network')}>Network</button>
          <button className={`tab-btn ${activeTab === 'ontology' ? 'active' : ''}`} onClick={() => setActiveTab('ontology')}>Ontology</button>
        </div>
        <Controls isRunning={status.running} onToggle={pollData} />
      </div>

      {activeTab === 'overview' && (
        <div className="fade-in-up" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="stats-grid">
            <StatCard title="Avg Happiness" value={`${stats.avg_happiness || 0}%`} subtitle={`Stress: ${avgStress}`} color="var(--accent-green)" />
            <StatCard title="Treasury" value={`$${Math.round(economy.treasury).toLocaleString()}`} subtitle={`Infl: ${economy.inflation_rate.toFixed(3)}`} color="var(--accent-yellow)" />
            <StatCard title="In Crisis" value={stats.agents_in_crisis || 0} subtitle={activeCases > 0 ? `${activeCases} cases` : "All OK"} color={stats.agents_in_crisis > 0 ? "var(--accent-red)" : "var(--accent-cyan)"} />
            <StatCard title="Top Earner" value={`$${Math.round(stats.top_earner_cash || 0).toLocaleString()}`} subtitle={stats.top_earner || 'None'} color="var(--accent-purple)" />
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
            <StatCard title="Population" value={agents.length} color="var(--accent-blue)" />
            <StatCard title="Avg Energy" value={`${stats.avg_energy || 0}%`} color="var(--accent-blue)" />
            <StatCard title="Avg Hunger" value={`${stats.avg_hunger || 0}%`} color="var(--accent-red)" />
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
              <StatCard title="Employment" value={`${Math.round((economy.employed / Math.max(economy.population, 1)) * 100)}%`} subtitle={`${economy.employed}/${Math.max(economy.population, 1)}`} color="var(--accent-purple)" />
            </div>
            <EconomyChart history={economyHistory} />
          </div>
          <JobMarket jobs={jobs} />
        </div>
      )}

      {activeTab === 'market' && (
        <div className="fade-in-up">
          <div className="stats-grid">
            <StatCard title="Price" value={`$${market.price || 0}`} color="var(--accent-yellow)" />
            <StatCard title="Volume" value={market.volume || 0} color="var(--accent-blue)" />
            <StatCard title="Buy Orders" value={market.buy_orders || 0} color="var(--accent-green)" />
            <StatCard title="Sell Orders" value={market.sell_orders || 0} color="var(--accent-red)" />
          </div>
          <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(0,0,0,0.3)', borderRadius: 8 }}>
            <h3>Political System</h3>
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
              <StatCard title="Stability" value={political.state_formation?.stability_score || 'N/A'} color="var(--accent-cyan)" />
              <StatCard title="Democracy" value={political.democratic_mechanics?.democracy_score || 'N/A'} color="var(--accent-blue)" />
              <StatCard title="Balance" value={political.international_relations?.balance_of_power_score || 'N/A'} color="var(--accent-purple)" />
            </div>
            <h3 style={{ marginTop: '1rem' }}>Financial System</h3>
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
              <StatCard title="Volatility" value={financial.market?.volatility || 'N/A'} color="var(--accent-red)" />
              <StatCard title="Inflation" value={financial.inflation_rate || 'N/A'} color="var(--accent-yellow)" />
              <StatCard title="Reserve" value={financial.banking?.reserve_ratio || 'N/A'} color="var(--accent-cyan)" />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'events' && (
        <div className="fade-in-up" style={{ height: 'calc(100vh - 200px)' }}>
          <EventTimeline events={events} />
        </div>
      )}

      {activeTab === 'network' && (
        <div className="fade-in-up">
          <div className="stats-grid">
            <StatCard title="Info Packets" value={information.packets || 0} color="var(--accent-blue)" />
            <StatCard title="Relationships" value={relationships.stats?.total_relationships || 0} color="var(--accent-purple)" />
            <StatCard title="Friends" value={relationships.stats?.friends || 0} color="var(--accent-green)" />
            <StatCard title="Rivals" value={relationships.stats?.rivals || 0} color="var(--accent-red)" />
          </div>
        </div>
      )}

      {activeTab === 'ontology' && (
        <div className="fade-in-up">
          <OntologyPanel ontology={ontology} features={features} causal={causal} />
        </div>
      )}

      {selectedAgentId && <AgentModal agentId={selectedAgentId} onClose={() => setSelectedAgentId(null)} />}
    </div>
  );
}

export default App;