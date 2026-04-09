import React, { useState } from 'react';

const FILTERS = [
  { key: 'all',     label: 'All' },
  { key: 'alert',   label: '🚨 Alerts' },
  { key: 'economy', label: '💰 Economy' },
  { key: 'social',  label: '🗣️ Social' },
  { key: 'ai',      label: '🧠 AI' },
  { key: 'day',     label: '📅 Days' },
];

function classify(text) {
  if (text.includes('[ALERT]'))            return 'alert';
  if (text.includes('🗣️'))               return 'social';
  if (text.includes('[AI]') || text.includes('🧠')) return 'ai';
  if (text.includes('Economy') || text.includes('Treasury') || text.includes('Treasury')) return 'economy';
  if (text.includes('Day') && text.includes('begun')) return 'day';
  if (text.includes('became friends') || text.includes('rivals')) return 'social';
  if (text.includes('job'))               return 'economy';
  return 'other';
}

const CATEGORY_STYLE = {
  alert:   { border: 'var(--accent-red)',    text: 'var(--accent-red)' },
  economy: { border: 'var(--accent-green)',  text: 'var(--text-main)' },
  social:  { border: 'var(--accent-purple)', text: 'var(--text-main)' },
  ai:      { border: 'var(--accent-blue)',   text: 'var(--accent-blue)' },
  day:     { border: 'var(--accent-yellow)', text: 'var(--accent-yellow)' },
  other:   { border: 'var(--border-dim)',    text: 'var(--text-main)' },
};

export default function EventTimeline({ events }) {
  const [filter, setFilter] = useState('all');
  const [locked, setLocked] = useState(true);

  const filtered = (events || []).filter(ev => {
    if (filter === 'all') return true;
    const match = ev.match(/^\[T\d+\]\s*(.*)/s);
    const text = match ? match[1] : ev;
    return classify(text) === filter;
  });

  return (
    <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2>Activity Ledger</h2>
        <button
          className="btn btn-ghost"
          style={{ padding: '0.3rem 0.7rem', fontSize: '0.75rem' }}
          onClick={() => setLocked(l => !l)}
          title={locked ? 'Scroll freely' : 'Auto-scroll to latest'}
        >
          {locked ? '🔒 Live' : '🔓 Scroll'}
        </button>
      </div>

      {/* Filter tabs */}
      <div style={{ display: 'flex', gap: '0.3rem', flexWrap: 'wrap' }}>
        {FILTERS.map(f => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            style={{
              padding: '0.28rem 0.65rem',
              border: filter === f.key ? '1px solid var(--border-glow-blue)' : '1px solid var(--border-subtle)',
              borderRadius: 20,
              background: filter === f.key ? 'var(--accent-blue-dim)' : 'transparent',
              color: filter === f.key ? 'var(--accent-blue)' : 'var(--text-muted)',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.15s',
              fontFamily: 'var(--font-body)',
            }}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Events list */}
      <div
        style={{
          flex: 1,
          overflowY: locked ? 'hidden' : 'auto',
          display: 'flex',
          flexDirection: locked ? 'column-reverse' : 'column',
          gap: '0.5rem',
          minHeight: 200,
          maxHeight: 480,
          paddingRight: 4,
        }}
      >
        {filtered.length === 0 && (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', paddingTop: '2rem' }}>
            No events in this category yet…
          </div>
        )}
        {[...filtered].reverse().map((ev, i) => {
          const match = ev.match(/^\[T(\d+)\]\s*(.*)/s);
          if (!match) return <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>{ev}</div>;
          const tick = match[1];
          const text = match[2];
          const cat = classify(text);
          const style = CATEGORY_STYLE[cat] || CATEGORY_STYLE.other;

          return (
            <div
              key={i}
              className="fade-in-up"
              style={{
                fontSize: '0.82rem',
                padding: '0.55rem 0.75rem',
                background: 'rgba(255,255,255,0.02)',
                borderRadius: 8,
                borderLeft: `3px solid ${style.border}`,
                lineHeight: 1.45,
                display: 'flex',
                gap: '0.6rem',
                alignItems: 'flex-start',
              }}
            >
              <span className="mono" style={{ color: 'var(--text-dim)', fontSize: '0.72rem', marginTop: '1px', flexShrink: 0 }}>T{tick}</span>
              <span style={{ color: style.text }}>{text}</span>
            </div>
          );
        })}
      </div>

      {/* Count */}
      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textAlign: 'right' }}>
        {filtered.length} event{filtered.length !== 1 ? 's' : ''} shown
      </div>
    </div>
  );
}
