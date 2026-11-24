import { format } from './cohort';
import { modes, results } from './ResearchResults';

const interval = (bounds: number[]) => bounds.map(value => format(value, 3)).join(' to ');

export function BiomarkerModels() {
  return <article className="panel card">
    <h2>Adjusted biomarker associations</h2>
    <p>Separate R random-intercept models distinguish baseline marker level from change since baseline. Each coefficient is a score-point difference per one synthetic marker unit. Benjamini–Hochberg q-values cover six marker terms within each simulation mode.</p>
    <div className="scroll" tabIndex={0} role="region" aria-label="Adjusted biomarker estimates">
      <table>
        <thead><tr><th scope="col">Mode</th><th scope="col">Marker</th><th scope="col">Term</th><th scope="col">Rows</th><th scope="col">Estimate</th><th scope="col">95% CI</th><th scope="col">BH q</th></tr></thead>
        <tbody>{modes.flatMap(mode => {
          const model = results.cohort[mode].biological;
          return model.coefficients.filter(row => row.q_bh !== null).map(row => <tr key={`${mode}-${row.model}-${row.term}`}>
            <td>{mode}</td><th scope="row">{row.model}</th><td>{row.term === 'marker_baseline' ? 'Baseline level' : 'Change since baseline'}</td>
            <td>{model.diagnostics.find(diagnostic => diagnostic.model === row.model)?.n.toLocaleString()}</td>
            <td>{format(row.estimate, 3)}</td><td>{interval([row.ci_lower, row.ci_upper])}</td><td>{row.q_bh?.toPrecision(3)}</td>
          </tr>);
        })}</tbody>
      </table>
    </div>
    <p>Models use available complete rows for each marker. Missing a baseline marker removes that participant from its model. Values were left on the original simulated scale without winsorization.</p>
  </article>;
}

export function PredictionResults() {
  return <>
    {modes.map(mode => {
      const experiment = results.cohort[mode].prediction;
      return <article className="panel card" key={mode}>
        <h2>{mode === 'complete' ? 'Complete simulation' : 'Simulated attrition and missing markers'}</h2>
        <p>{experiment.eligible.toLocaleString()} of {experiment.enrolled.toLocaleString()} enrolled participants had a Year-8 target. Train {experiment.n_train.toLocaleString()} · test {experiment.n_test.toLocaleString()} · overlapping IDs {experiment.participant_overlap}.</p>
        <div className="scroll" tabIndex={0} role="region" aria-label={`${mode} held-out model metrics`}>
          <table>
            <thead><tr><th scope="col">Model</th><th scope="col">MAE (95% CI)</th><th scope="col">RMSE (95% CI)</th><th scope="col">R² (95% CI)</th></tr></thead>
            <tbody>{Object.entries(experiment.models).map(([label, model]) => <tr key={label}>
              <th scope="row">{label}</th>
              {(['mae', 'rmse', 'r2'] as const).map(metric => <td key={metric}>${''}{format(model.metrics[metric].estimate, 3)} ({interval(model.metrics[metric].ci95)})</td>)}
            </tr>)}</tbody>
          </table>
        </div>
        <h3>Paired change in MAE from adding marker proxies</h3>
        <ul>{Object.entries(experiment.paired_marker_comparisons).map(([model, value]) => (
          <li key={model}>{model} {format(value.delta_mae, 3)} points (95% CI {interval(value.ci95)})</li>
        ))}</ul>
        <details>
          <summary>Subgroup errors and held-out permutation importance</summary>
          <ul>{Object.entries(experiment.models).map(([label, model]) => <li key={label}>
            <strong>{label}</strong>
            <ul>
              {Object.entries(model.by_synthetic_sex).map(([group, metric]) => <li key={group}>{group} category, n = {metric.n}, MAE {format(metric.mae, 3)}</li>)}
              {'permutation_mae_increase' in model && Object.entries(model.permutation_mae_increase).map(([feature, value]) => (
                <li key={feature}>{feature} permutation ΔMAE {format(value, 3)}</li>
              ))}
            </ul>
          </li>)}</ul>
        </details>
      </article>;
    })}
    <p className="callout">Only baseline predictors enter the model. Median imputation, scaling and model selection are fit within participant-grouped training folds. The holdout is used for evaluation and permutation importance. Intervals resample held-out participants conditional on fitted models. All metrics apply to the synthetic data only.</p>
  </>;
}
