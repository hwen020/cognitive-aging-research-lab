import { useState } from 'react';
import { data, format, markerLabels, type Marker, type Row } from './cohort';

function quantile(values: number[], share: number) {
  const index = (values.length - 1) * share;
  const lower = Math.floor(index);
  return values[lower] + (values[Math.ceil(index)] - values[lower]) * (index - lower);
}

export function MarkerProfile({ rows, marker }: { rows: Row[]; marker: Marker }) {
  const [participant, setParticipant] = useState('');
  const profile = data.filter(row => row.participant_id === participant.trim().toUpperCase());
  const values = rows.map(row => row[marker]).sort((left, right) => left - right);
  const profileValues = profile.map(row => row[marker]);
  const profileMin = Math.min(...profileValues);
  const profileRange = Math.max(...profileValues) - profileMin || 1;
  return <article className="panel card">
    <h2>Distribution and participant profile</h2>
    <p>{markerLabels[marker]} at Year {rows[0]?.visit_year}. Minimum {format(values[0], 2)} · Median {format(quantile(values, .5), 2)} · IQR {format(quantile(values, .25), 2)} to {format(quantile(values, .75), 2)} · Maximum {format(values.at(-1) ?? NaN, 2)}. Missing measurements in this complete cohort: 0.</p>
    <div className="field">
      <label htmlFor="marker-participant">Synthetic participant ID (P0001–P2400)</label>
      <input id="marker-participant" value={participant} onChange={event => setParticipant(event.target.value)} />
    </div>
    {participant.trim() && (profile.length ? <>
      <svg className="marker-profile" viewBox="0 0 350 100" role="img" aria-label={`${markerLabels[marker]} across visits for ${profile[0].participant_id}`}>
        <polyline points={profile.map(row => `${25 + row.visit_year * 37},${76 - (row[marker] - profileMin) / profileRange * 50}`).join(' ')} stroke="#138b8a" strokeWidth="3" fill="none" />
        {profile.map(row => <text key={row.visit_year} x={25 + row.visit_year * 37} y="95" textAnchor="middle" fontSize="11">Year {row.visit_year}</text>)}
      </svg>
      <ul>{profile.map(row => <li key={row.visit_year}>Year {row.visit_year}: {format(row[marker], 2)}</li>)}</ul>
    </> : <p role="status">No synthetic participant matches that ID.</p>)}
  </article>;
}
