import React from 'react';

const JOB_ICONS = {
  Farmer: '🌾', Merchant: '💰', Guard: '⚔️', Teacher: '📚', Laborer: '🔨',
};

export default function JobMarket({ jobs }) {
  if (!jobs || jobs.length === 0) {
    return (
      <div className="glass" style={{ padding: '1.5rem' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>Job Market</h2>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '2rem 0' }}>
          Loading job data…
        </div>
      </div>
    );
  }

  return (
    <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
      <h2>Job Market</h2>

      {jobs.map(job => {
        const fillRate  = job.filled / Math.max(job.slots, 1);
        const fillColor = fillRate >= 0.9 ? 'var(--accent-red)'
                        : fillRate >= 0.6 ? 'var(--accent-yellow)'
                        : 'var(--accent-green)';
        const unstaffed = job.slots - job.filled;

        return (
          <div
            key={job.name}
            style={{
              padding: '1rem',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: 10,
              border: '1px solid var(--border-subtle)',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.6rem',
            }}
          >
            {/* Title row */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.6rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '1.1rem' }}>{JOB_ICONS[job.name] ?? '💼'}</span>
                <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>{job.name}</span>
              </div>
              <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                <span className="badge badge-green" style={{ fontSize: '0.68rem' }}>
                  ${job.wage}/tick
                </span>
                <span className="badge" style={{
                  fontSize: '0.68rem',
                  background: `${fillColor}22`,
                  color: fillColor,
                  border: `1px solid ${fillColor}44`,
                }}>
                  {job.filled}/{job.slots === 99 ? '∞' : job.slots}
                </span>
              </div>
            </div>

            {/* Bar */}
            <div className="progress-track">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min(100, fillRate * 100)}%`,
                  background: `linear-gradient(90deg, ${fillColor}88, ${fillColor})`,
                }}
              />
            </div>

            {/* Footer */}
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
              <span>{job.description}</span>
              <span style={{ color: unstaffed > 0 ? 'var(--accent-green)' : 'var(--text-dim)' }}>
                {unstaffed > 0 ? `${unstaffed} opening${unstaffed > 1 ? 's' : ''}` : 'Full'}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
