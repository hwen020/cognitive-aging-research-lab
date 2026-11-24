import { cohortSize, data, format, markerLabels, mean, trajectories, YEARS, type Marker, type Row } from './cohort';

function Stat({ label, value, hint }: { label: string; value: string; hint: string }) {
  return <div className="panel stat">
    <div className="label">{label}</div>
    <div className="value">{value}</div>
    <div className="hint">{hint}</div>
  </div>;
}

export function SummaryStats() {
  return <>
    <Stat label="Participants" value={cohortSize(data).toLocaleString()} hint="Unique synthetic IDs" />
    <Stat label="Repeated observations" value={data.length.toLocaleString()} hint="Five observations per participant" />
    <Stat label="Follow-up window" value={`${YEARS.at(-1)} years`} hint="Baseline and four follow-ups" />
    <Stat label="Biomarker proxies" value={String(Object.keys(markerLabels).length)} hint="CRP · p-tau · NfL" />
  </>;
}

export function CohortStats({ rows }: { rows: Row[] }) {
  return <>
    <Stat label="Visible observations" value={rows.length.toLocaleString()} hint="Matching filter criteria" />
    <Stat label="Unique participants" value={cohortSize(rows).toLocaleString()} hint="Distinct participant IDs" />
    <Stat label="Mean cognition" value={format(mean(rows, row => row.cognitive_score))} hint="Unadjusted synthetic score" />
    <Stat label="Mean age" value={format(mean(rows, row => row.age_at_visit))} hint="Years at selected visits" />
  </>;
}

export function CohortWaves({ rows }: { rows: Row[] }) {
  const counts = YEARS.map(year => rows.filter(row => row.visit_year === year).length);
  return <div className="wave-summary">
    <h3>Matching observations by visit</h3>
    {YEARS.map((year, index) => <div className="feature" key={year} data-count={counts[index]}>
      <span>Year {year}</span>
      <div className="bartrack" aria-hidden="true"><div className="barfill" style={{ width: `${counts[index] / (Math.max(...counts) || 1) * 100}%` }} /></div>
      <span className="right">{counts[index].toLocaleString()}</span>
    </div>)}
    <p className="footnote">Complete simulation. Matching observations have no missing fields.</p>
  </div>;
}

export function TrajectoryChart() {
  const values = trajectories.flatMap(series => series.points.map(point => point.mean));
  const low = Math.floor(Math.min(...values) / 5) * 5;
  const high = Math.ceil(Math.max(...values) / 5) * 5;
  const x = (year: number) => 44 + year / 8 * 288;
  const y = (score: number) => 12 + (high - score) / (high - low || 1) * 154;
  const ticks = Array.from({ length: 5 }, (_, index) => low + (high - low) * index / 4);

  return <>
    <svg viewBox="0 0 356 195" role="img" aria-label="Synthetic cognitive score means by visit year and deprivation group">
      {ticks.map(tick => <g key={tick}>
        <line x1="44" x2="332" y1={y(tick)} y2={y(tick)} stroke="#e4eaf1" />
        <text x="38" y={y(tick) + 4} textAnchor="end" fontSize="10">{format(tick)}</text>
      </g>)}
      {YEARS.map(year => <text key={year} x={x(year)} y="187" textAnchor="middle" fontSize="10">Year {year}</text>)}
      {trajectories.map(({ group, color, points }) => <g key={group}>
        <polyline points={points.map(point => `${x(point.year)},${y(point.mean)}`).join(' ')} fill="none" stroke={color} strokeWidth="2" />
        {points.map(point => <circle key={point.year} cx={x(point.year)} cy={y(point.mean)} r="3" fill={color}>
          <title>{`${group} deprivation, Year ${point.year}, mean ${format(point.mean)}, n = ${point.n}`}</title>
        </circle>)}
      </g>)}
    </svg>
    <details className="trajectory-values">
      <summary>Trajectory values</summary>
      <div className="scroll" tabIndex={0} role="region" aria-label="Trajectory values">
        <table>
          <thead><tr><th scope="col">Group</th><th scope="col">Year</th><th scope="col">Mean</th><th scope="col">n</th></tr></thead>
          <tbody>{trajectories.flatMap(({ group, points }) => points.map(point => <tr key={`${group}-${point.year}`}>
            <td>{group}</td><td>{point.year}</td><td>{format(point.mean)}</td><td>{point.n}</td>
          </tr>))}</tbody>
        </table>
      </div>
    </details>
  </>;
}

export function TrajectorySummary() {
  return <>
    {trajectories.map(({ group, points }) => <div key={group} className="rowline">
      <b>{group} deprivation change, baseline to Year 8</b>
      <span className="metric">{format(points[4].mean - points[0].mean)}</span>
    </div>)}
    <div className="rowline">
      <b>Year 8 difference, high minus low</b>
      <span className="metric">{format(trajectories[1].points[4].mean - trajectories[0].points[4].mean)}</span>
    </div>
    <p>Synthetic group means, without adjustment or uncertainty intervals.</p>
  </>;
}

export function Scatter({ rows, marker }: { rows: Row[]; marker: Marker }) {
  const markerValues = rows.map(row => row[marker]);
  const scores = rows.map(row => row.cognitive_score);
  const minX = Math.min(...markerValues);
  const minY = Math.min(...scores);
  const xRange = Math.max(...markerValues) - minX || 1;
  const yRange = Math.max(...scores) - minY || 1;
  const ticks = Array.from({ length: 5 }, (_, index) => index / 4);
  return <>
    <svg viewBox="0 0 356 195" role="img" aria-label={`${markerLabels[marker]} and synthetic cognitive score`}>
      <text x="4" y="12" fontSize="10">Cognition</text>
      {ticks.map(tick => <g key={tick}>
        <line x1={42 + tick * 290} x2={42 + tick * 290} y1="23" y2="149" stroke="#e4eaf1" />
        <line x1="42" x2="332" y1={149 - tick * 126} y2={149 - tick * 126} stroke="#e4eaf1" />
        <text x={42 + tick * 290} y="165" textAnchor="middle" fontSize="10">{format(minX + tick * xRange)}</text>
        <text x="36" y={152 - tick * 126} textAnchor="end" fontSize="10">{format(minY + tick * yRange)}</text>
      </g>)}
      {rows.filter((_, index) => index % 7 === 0).map(row => <circle key={row.participant_id}
        cx={42 + (row[marker] - minX) / xRange * 290} cy={149 - (row.cognitive_score - minY) / yRange * 126}
        r="2" fill="#138b8a" opacity=".55" />)}
      <text x="180" y="186" textAnchor="middle" fontSize="10">{markerLabels[marker]}</text>
    </svg>
    <p className="meta">The scatter shows every seventh row. Pearson r uses all selected observations.</p>
  </>;
}
