import { format } from './cohort';
import { results } from './ResearchResults';

export function CausalResults() {
  const complete = results.cohort.complete.iptw;
  const incomplete = results.cohort.incomplete.iptw;
  return <>
    <div className="gridhalf">
      <article className="panel card">
        <h2>Directed graph of the simulator</h2>
        <p>Age and education precede assignment. The simulator draws deprivation independently at time zero.</p>
        <ul>
          <li>Deprivation → hypertension, CRP proxy, and Year-8 cognition</li>
          <li>Age → hypertension, p-tau proxy, and Year-8 cognition</li>
          <li>Education → Year-8 cognition</li>
          <li>Hypertension → CRP proxy and Year-8 cognition</li>
          <li>CRP, p-tau, and independent individual variation → Year-8 cognition</li>
        </ul>
      </article>
      <article className="panel card">
        <h2>Target estimand</h2>
        <p>{complete.estimand}, in synthetic score points. The propensity model includes age, education, and sex. Hypertension and CRP are generated downstream of assignment.</p>
        <p>Real observational identification would require a defensible intervention, adequate overlap, exchangeability, and a censoring design. Omitted residential history or early-life factors could invalidate a real-world interpretation.</p>
      </article>
    </div>
    <article className="panel card">
      <h2>Stabilized IPTW in the complete simulation</h2>
      {complete.status === 'computed' ? <>
        <p>{complete.n.toLocaleString()} participants, {complete.n_high.toLocaleString()} assigned high deprivation. The percentile intervals refit the propensity model in each of {complete.bootstrap_replications} participant resamples.</p>
        <p>Common support contains {format(100 * complete.diagnostics.fraction_in_common_support, 2)}% of participants. Effective sample sizes (low/high) are {complete.diagnostics.ess_low_high.map(value => format(value, 1)).join(' / ')}.</p>
        <div className="scroll" role="region" aria-label="Covariate balance" tabIndex={0}>
          <table>
            <thead><tr><th scope="col">Covariate</th><th scope="col">Unweighted SMD</th><th scope="col">Weighted SMD</th></tr></thead>
            <tbody>{complete.diagnostics.balance.map(row => <tr key={row.covariate}>
              <th scope="row">{row.covariate}</th><td>{format(row.smd_before, 3)}</td><td>{format(row.smd_after, 3)}</td>
            </tr>)}</tbody>
          </table>
        </div>
        <div className="scroll" role="region" aria-label="Weight truncation sensitivity" tabIndex={0}>
          <table>
            <thead><tr><th scope="col">Symmetric weight truncation</th><th scope="col">Weighted difference</th><th scope="col">95% CI</th></tr></thead>
            <tbody>{complete.weight_sensitivity.map(row => <tr key={row.tail_quantile}>
              <th scope="row">{row.tail_quantile === 0 ? 'None (primary)' : `${row.tail_quantile * 100}% per tail`}</th>
              <td>{row.diagnostics.passes ? format(row.estimate, 3) : 'Withheld'}</td>
              <td>{row.diagnostics.passes ? row.ci95.map(value => format(value, 3)).join(' to ') : 'Withheld'}</td>
            </tr>)}</tbody>
          </table>
        </div>
      </> : <p>Effect estimate withheld. Diagnostics failed the reporting thresholds.</p>}
      <p className="callout"><strong>Incomplete simulation effect withheld.</strong> {incomplete.reason}</p>
    </article>
  </>;
}
