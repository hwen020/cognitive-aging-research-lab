import result from '../public/vcap/results.json';

export function VcapResearch() {
  const { audit, model, prediction } = result;
  const table = (rows: Record<string, string | number>[]) => <div className="research-table" tabIndex={0}><table>
    <thead><tr>{Object.keys(rows[0]).map(key => <th scope="col" key={key}>{key.replaceAll('_', ' ')}</th>)}</tr></thead>
    <tbody>{rows.map((row, i) => <tr key={i}>{Object.values(row).map((value, j) => <td key={j}>{typeof value === 'number' ? value.toLocaleString('en-US', { maximumFractionDigits: 3 }) : value}</td>)}</tr>)}</tbody>
  </table></div>;
  return <main className="real-research">
    <p className="data-origin">UVA Dataverse VCAP V1.0 · Real longitudinal analysis</p>
    <h1>VCAP Longitudinal Research</h1>
    <section><h2>Longitudinal Cohort Overview</h2>
      <p>{audit.participants.toLocaleString()} participants after key checks. {audit.two_occasions.toLocaleString()} have two or more occasions and {audit.three_occasions.toLocaleString()} have three or more.</p>
      <p>The analytic sample includes {model.participants.toLocaleString()} participants and {model.n.toLocaleString()} eligible observations.</p>
    </section>
    <section><h2>Repeated Cognitive Assessments</h2>
      <p>The study uses the first-session Digit Symbol score (correct matches in 120 seconds) from each occasion. {audit.repeated_people.toLocaleString()} participants have repeat eligible scores.</p>
    </section>
    <section><h2>Follow-up Trajectories</h2>
      <p>Grouped observed scores are descriptive. The people observed can differ across follow-up bins.</p>
      {table(Object.entries(model.trajectory).map(([bin, row]) => ({time_bin_years: bin, ...row})))}
    </section>
    <section><h2>Mixed-Effects Results</h2><p>Baseline age centered at 60 and education centered at 16. Follow-up is measured in elapsed years.</p>{table(model.coefficients)}</section>
    <section><h2>Missingness and Attrition</h2>
      <p>{audit.missing_score} scores and {audit.missing_educ} education observations are missing or outside accepted ranges in the linked extract.</p>
      <p>Observed repeat assessment is a coverage measure. Return pathways and reasons for missingness are unknown.</p>
      {table(Object.entries(audit.baseline_profiles).map(([key, row]) => ({observed_repeat: key === 'True' ? 'Yes' : 'No', ...row})))}
    </section>
    <section><h2>Longitudinal Prediction</h2>
      <p>Predict the next observed score from baseline information. Train {prediction.train}; validation {prediction.validation}; test {prediction.test}; participant overlap {prediction.max_id_overlap}.</p>
      {table(Object.entries(prediction.metrics).map(([name, row]) => ({model: name, mae: row.mae, mae_ci: row.mae_ci.map(x => x.toFixed(3)).join(' to '), rmse: row.rmse, rmse_ci: row.rmse_ci.map(x => x.toFixed(3)).join(' to ')})))}
    </section>
    <section><h2>Model Diagnostics</h2><p>Primary model: {model.primary}. Intercept AIC {model.intercept_aic.toFixed(1)}; slope AIC {model.slope_aic?.toFixed(1) ?? 'unavailable'}. Lag-one residual ACF {model.residual_lag1.toFixed(3)}.</p></section>
    <section><h2>Research Reports</h2>
      <ul>{['longitudinal', 'methods', 'data_quality', 'model_diagnostics', 'prediction', 'limitations', 'reproducibility'].map(name =>
        <li key={name}><a href={`/vcap/${name}.md`} download>{name.replaceAll('_', ' ')} report</a></li>)}
        <li><a href="/vcap/results.json" download>VCAP aggregate JSON</a></li></ul>
      <p>Results describe observational change and prediction of test scores. <a href="https://doi.org/10.18130/V3/QRCQ08">Official VCAP source</a></p>
    </section>
  </main>;
}
