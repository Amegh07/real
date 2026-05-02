import React from 'react';

export default function OntologyPanel({ ontology, features, causal }) {
  const dims = ontology?.dimensions || [];
  const records = causal || [];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.2rem' }}>
      <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div className="section-header">
          <h2>Ontology</h2>
          <span className="badge badge-blue">{dims.length} dimensions</span>
        </div>

        <div className="dimension-grid">
          {dims.map(dim => (
            <div key={dim.key} className="dimension-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.5rem', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.35rem' }}>{dim.name}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{dim.description}</div>
                </div>
                <span className="badge badge-purple">{dim.key}</span>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.75rem' }}>
                {(dim.examples || []).map(example => (
                  <span key={example} className="badge badge-cyan" style={{ textTransform: 'none' }}>{example}</span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="section-header" style={{ marginTop: '0.5rem' }}>
          <h2>Feature Families</h2>
          <span className="badge badge-green">{features.length} seeded</span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', maxHeight: 360, overflowY: 'auto', paddingRight: 4 }}>
          {features.map(feature => (
            <div key={feature.feature_id} className="feature-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.75rem', marginBottom: '0.4rem' }}>
                <div>
                  <div style={{ fontWeight: 700 }}>{feature.feature_name}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{feature.feature_id}</div>
                </div>
                <span className="badge badge-yellow">{feature.domain}</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.45, marginBottom: '0.5rem' }}>
                {feature.mechanism}
              </div>
              <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                <span className="badge badge-blue">{feature.scale}</span>
                <span className="badge badge-green">{feature.timescale}</span>
                <span className="badge badge-purple">{feature.emergence_class}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div className="section-header">
          <h2>Causal Ledger</h2>
          <span className="badge badge-red">{records.length} records</span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxHeight: 780, overflowY: 'auto', paddingRight: 4 }}>
          {records.length === 0 && (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', paddingTop: '1rem' }}>
              No causal records yet.
            </div>
          )}
          {[...records].reverse().map(record => (
            <div key={record.record_id} className="causal-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.5rem', marginBottom: '0.35rem' }}>
                <span className="badge badge-purple">{record.category}</span>
                <span className="mono" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>T{record.tick}</span>
              </div>
              <div style={{ fontWeight: 700, lineHeight: 1.35, marginBottom: '0.35rem' }}>{record.summary}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.45, marginBottom: '0.5rem' }}>
                {record.mechanism}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.75rem', fontSize: '0.72rem', color: 'var(--text-dim)', marginBottom: '0.4rem' }}>
                <span>{record.source} → {record.target}</span>
                <span>confidence {Math.round((record.confidence || 0) * 100)}%</span>
              </div>
              <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                {(record.evidence || []).map(item => (
                  <span key={item} className="badge badge-cyan" style={{ textTransform: 'none' }}>{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
