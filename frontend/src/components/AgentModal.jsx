import React, { useEffect, useState } from 'react';
import { fetchAgent } from '../api';

const EMOTION_ICONS = {
  happy: '😃', neutral: '😐', sad: '😢', fearful: '😨', angry: '😠'
};

const EMOTION_COLORS = {
  happy: 'var(--accent-green)', neutral: 'var(--text-muted)',
  sad: 'var(--accent-blue)', fearful: 'var(--accent-yellow)', angry: 'var(--accent-red)'
};

const PERSONALITY_ICONS = {
  industrious: '⚙️', lazy: '😴', social: '🤝',
  reclusive: '🔮', reckless: '⚡', cautious: '🛡️',
};

const PERSONALITY_COLORS = {
  industrious: 'var(--accent-blue)', lazy: 'var(--accent-yellow)',
  social: 'var(--accent-purple)', reclusive: 'var(--accent-cyan)',
  reckless: 'var(--accent-red)', cautious: 'var(--accent-green)',
};

export default function AgentModal({ agentId, onClose }) {
  const [agent, setAgent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await fetchAgent(agentId);
        setAgent(data);
        setError(null);
      } catch (e) {
        setError("Failed to load agent details: " + e.message);
      } finally {
        setLoading(false);
      }
    };
    load();
    const interval = setInterval(load, 3000);
    return () => clearInterval(interval);
  }, [agentId]);

  if (!agentId) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        {loading && !agent ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
            Loading Neural Net…
          </div>
        ) : error ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--accent-red)' }}>
            {error}
          </div>
        ) : (
          <>
            {/* Header / Top profile */}
            <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'flex-start' }}>
              <div style={{
                width: 80, height: 80, borderRadius: 20,
                background: `linear-gradient(135deg, ${PERSONALITY_COLORS[agent.personality]}44, ${PERSONALITY_COLORS[agent.personality]})`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '2.5rem', flexShrink: 0,
                boxShadow: `0 0 30px ${PERSONALITY_COLORS[agent.personality]}44`,
                border: `2px solid ${PERSONALITY_COLORS[agent.personality]}`,
              }}>
                {PERSONALITY_ICONS[agent.personality] ?? '👤'}
              </div>

              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h1 style={{ margin: 0, fontSize: '2.2rem' }}>{agent.name}</h1>
                  <button className="btn btn-ghost" onClick={onClose} style={{ padding: '0.4rem 0.6rem' }}>✕</button>
                </div>
                
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                  <span className="badge" style={{ background: `${PERSONALITY_COLORS[agent.personality]}33`, color: PERSONALITY_COLORS[agent.personality], border: `1px solid ${PERSONALITY_COLORS[agent.personality]}66` }}>
                    {agent.personality}
                  </span>
                  <span className="badge badge-cyan">💼 {agent.job || 'Unemployed'}</span>
                  <span className="badge badge-green">💰 ${agent.money.toLocaleString()}</span>
                  <span className="badge badge-blue">🕰️ Age {agent.age_ticks}</span>
                </div>
              </div>
            </div>

            {/* Reflection / Goal Box */}
            <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '1.2rem' }}>
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
                Inner Reflection (Phase 5 AI)
              </div>
              <div style={{ fontSize: '1.05rem', fontStyle: 'italic', color: 'var(--text-main)', lineHeight: 1.5, marginBottom: '0.8rem' }}>
                "{agent.memory.reflection || 'No thoughts formulated yet.'}"
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.8rem', fontSize: '0.85rem' }}>
                <div style={{ color: 'var(--text-muted)' }}>Current Action: <span style={{ color: 'var(--text-main)', textTransform: 'capitalize' }}>{agent.current_action.replace('_', ' ')}</span></div>
                <div style={{ color: 'var(--accent-blue)', fontWeight: 500 }}>Goal: {agent.goal}</div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
              {/* Needs & Traits */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                
                <div>
                  <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.4rem', marginBottom: '0.8rem' }}>Current Needs</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    {[
                      { label: 'Hunger', value: agent.hunger, color: 'var(--accent-red)' },
                      { label: 'Energy', value: agent.energy, color: 'var(--accent-blue)' },
                      { label: 'Happiness', value: agent.happiness, color: 'var(--accent-green)' },
                    ].map(n => (
                      <div key={n.label}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '3px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>{n.label}</span>
                          <span style={{ fontWeight: 600, color: n.color }}>{n.value.toFixed(0)}</span>
                        </div>
                        <div className="progress-track">
                          <div className="progress-fill" style={{ width: `${n.value}%`, background: n.color }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.4rem', marginBottom: '0.8rem' }}>Personality Traits</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                    {Object.entries(agent.traits || {}).map(([key, val]) => (
                      <div key={key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <span style={{ textTransform: 'capitalize', fontSize: '0.8rem', color: 'var(--text-dim)' }}>{key.replace('_', ' ')}</span>
                        <div style={{ width: '50%', background: 'rgba(0,0,0,0.4)', height: 6, borderRadius: 3 }}>
                          <div style={{ width: `${val * 100}%`, background: 'var(--text-muted)', height: '100%', borderRadius: 3 }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.4rem', marginBottom: '0.8rem' }}>Relationships</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {agent.relationships?.length === 0 ? (
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No connections yet.</span>
                    ) : (
                      agent.relationships.sort((a,b) => b.bond - a.bond).map(r => (
                        <div key={r.target} className={`badge ${r.status === 'friend' ? 'badge-green' : r.status === 'rival' ? 'badge-red' : 'badge-blue'}`}>
                          {r.status === 'friend' ? '💖' : r.status === 'rival' ? '⚔️' : '👤'} {r.target} ({r.bond > 0 ? '+' : ''}{r.bond.toFixed(0)})
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>

              {/* Memory Logs */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
                <div>
                  <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.4rem', marginBottom: '0.8rem', color: 'var(--accent-purple)' }}>Core Memories</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {agent.memory.significant?.length === 0 && <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No significant memories.</span>}
                    {agent.memory.significant?.map((m, i) => (
                      <div key={i} style={{ padding: '0.5rem 0.6rem', background: 'rgba(139,92,246,0.1)', borderLeft: '3px solid var(--accent-purple)', borderRadius: '4px', fontSize: '0.8rem' }}>
                        <span className="mono" style={{ color: 'var(--text-muted)', marginRight: '6px' }}>T{m.tick}</span>
                        {m.text}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.4rem', marginBottom: '0.8rem' }}>Recent Log</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                    {agent.memory.recent?.length === 0 && <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>No recent events.</span>}
                    {agent.memory.recent?.slice().reverse().map((m, i) => (
                      <div key={i} style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start', fontSize: '0.8rem', padding: '4px 0' }}>
                        <span title={m.emotion} style={{ fontSize: '1rem', marginTop: '-2px' }}>{EMOTION_ICONS[m.emotion] ?? '⚪'}</span>
                        <div>
                          <span className="mono" style={{ color: 'var(--text-dim)', marginRight: '6px' }}>T{m.tick}</span>
                          <span style={{ color: EMOTION_COLORS[m.emotion] || 'var(--text-main)' }}>{m.text}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
