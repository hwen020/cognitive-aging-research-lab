import result from './generated/nhanes.json';

export function DatasetLinks() {
  return <nav className="dataset-links" aria-label="Research datasets">
    <a href="./">Synthetic Demo</a>
    <a href="?dataset=nhanes">NHANES 2011–2014 — Real-World Data</a>
    <a href="?dataset=vcap">VCAP Longitudinal Research</a>
    <a href="?dataset=hrs">HRS Longitudinal — Authorized Analysis Only</a>
  </nav>;
}

function Summary({ values }: { values: Record<string, number> }) {
  return <dl>{Object.entries(values).map(([name, count]) => <div key={name}>
    <dt>{name.replaceAll('_', ' ')}</dt><dd>{count.toLocaleString()}</dd>
  </div>)}</dl>;
}

function FitTable({ track }: { track: 'social' | 'biological' }) {
  return <div tabIndex={0} className="research-table"><table>
    <thead><tr><th>Outcome</th><th>Exposure</th><th>n</th><th>Estimate</th><th>95% CI</th><th>BH q</th></tr></thead>
    <tbody>{Object.entries(result[track]).flatMap(([outcome, fit]) => fit.coefficients
      .filter(row => row.q_bh !== null).map(row => <tr key={outcome + row.term}>
        <td>{outcome.toUpperCase()}</td><td>{row.term}</td><td>{fit.n}</td>
        <td>{row.estimate.toFixed(2)}</td><td>{row.lower.toFixed(2)} to {row.upper.toFixed(2)}</td>
        <td>{row.q_bh?.toPrecision(3)}</td>
      </tr>))}</tbody>
  </table></div>;
}

function Diagnostic({ track }: { track: 'social' | 'biological' }) {
  const bins = result[track].dsst.residual_bins;
  const extent = Math.max(...bins.map(bin => Math.abs(bin.residual)), 1);
  const min = bins[0].fitted_values;
  const max = bins[bins.length - 1].fitted_values;
  return <figure>
    <svg viewBox="0 0 320 125" role="img" aria-label={`Binned DSST residuals for ${track} model`}>
      <line x1="20" x2="300" y1="52" y2="52" stroke="currentColor" />
      {bins.map((bin, i) => <circle key={i} r="4" fill="#047d72"
        cx={26 + 268 * (bin.fitted_values - min) / (max - min)}
        cy={52 - 42 * bin.residual / extent}>
        <title>{bin.fitted_values.toFixed(1)} fitted, {bin.residual.toFixed(2)} mean residual</title>
      </circle>)}
      <text x="20" y="115">Fitted DSST score</text>
    </svg>
    <figcaption>Eight bins of fitted values. The horizontal line is zero residual.</figcaption>
  </figure>;
}

export function RealResearch({ dataset }: { dataset: 'nhanes' | 'hrs' }) {
  if (dataset === 'hrs') return <main className="real-research">
    <h1>HRS Longitudinal</h1>
    <p>Longitudinal Analysis Framework — Awaiting Authorized Data Execution</p>
    <p>Independent authorized execution and disclosure review are required before any HRS results appear here.</p>
  </main>;

  const p = result.prediction;
  return <main className="real-research">
    <header><p className="data-origin">Public CDC/NCHS data · Repeated cross-sectional survey</p>
      <h1>NHANES 2011–2014</h1>
      <p>Socioeconomic and cardiometabolic factors associated with cognitive performance in adults aged 60 and older.</p>
    </header>
    <section><h2>Cohort overview and sample selection</h2><Summary values={result.counts} />
      <p>Design accounts for {result.design.strata} cycle-nested strata and {result.design.psus} masked PSUs. MEC weights are halved for the four-year pool.</p></section>
    <section><h2>Data quality and missingness</h2>
      <p>Percent missing in the examined age-60+ analysis domain.</p>
      <dl>{Object.entries(result.missing_fraction).map(([key, value]) => <div key={key}>
        <dt>{key}</dt><dd>{(100 * value).toFixed(1)}%</dd>
      </div>)}</dl>
    </section>
    <section><h2>Social factors · Observational associations</h2><FitTable track="social" /><Diagnostic track="social" /></section>
    <section><h2>Biological indicators · Observational associations</h2>
      <p>HbA1c is measured in percentage points. SBP is scaled per 10 mm Hg. The models report associations with general cardiometabolic indicators.</p>
      <FitTable track="biological" /><Diagnostic track="biological" /></section>
    <section><h2>Predictive performance · Concurrent DSST score</h2>
      <p>2011–2012 training n = {p.train.toLocaleString()}. 2013–2014 test n = {p.test.toLocaleString()}. Participant overlap {p.overlap}.</p>
      <div className="research-table" tabIndex={0}><table>
        <thead><tr><th>Model</th><th>MAE</th><th>RMSE</th><th>R²</th></tr></thead>
        <tbody>{Object.entries(p.metrics).map(([name, m]) => <tr key={name}><td>{name.replaceAll('_', ' ')}</td><td>{m.mae.toFixed(2)}</td><td>{m.rmse.toFixed(2)}</td><td>{m.r2.toFixed(3)}</td></tr>)}</tbody>
      </table></div>
      <p>Paired augmented-minus-social MAE {p.paired_mae_difference.toFixed(3)} (95% CI {p.paired_ci95[0].toFixed(3)} to {p.paired_ci95[1].toFixed(3)}). Unweighted holdout metrics describe prediction of a concurrent test score.</p>
    </section>
    <section><h2>Research reports and methods</h2>
      <ul>
        <li><a download href="/nhanes/social.md">NHANES Social Report</a></li>
        <li><a download href="/nhanes/biological.md">NHANES Biological Report</a></li>
        <li><a download href="/nhanes/results.json">Aggregate results and provenance JSON</a></li>
      </ul>
      <p>Results depend on test and covariate availability, and potential residual confounding. This design does not estimate causal effects or follow individuals over time.</p>
    </section>
  </main>;
}
