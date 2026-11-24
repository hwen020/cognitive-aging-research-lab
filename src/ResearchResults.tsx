import results from './generated/results.json';
import { format } from './cohort';

type Mode = 'complete' | 'incomplete';
export const modes: Mode[] = ['complete', 'incomplete'];
export { results };

export function LongitudinalResults() {
  return <article className="panel card research-results">
    <h2>Adjusted longitudinal model</h2>
    <p>R nlme random participant intercept, with interactions between follow-up time and baseline covariates. The contrast is the high-minus-low deprivation difference in annual cognition slope.</p>
    <div className="scroll" role="region" aria-label="Adjusted longitudinal estimates" tabIndex={0}>
      <table>
        <thead><tr><th scope="col">Synthetic cohort</th><th scope="col">Participants</th><th scope="col">Rows</th><th scope="col">Slope difference</th><th scope="col">95% CI</th><th scope="col">Residual lag-1 ACF</th></tr></thead>
        <tbody>{modes.map(mode => {
          const model = results.cohort[mode].social;
          const coefficient = model.coefficients.find(row => row.term === 'visit_year:deprivationHigh');
          const diagnostic = model.diagnostics[0];
          if (!coefficient) return <tr key={mode}><td>{mode}</td><td colSpan={5}>Estimate unavailable</td></tr>;
          return <tr key={mode}>
            <th scope="row">{mode}</th><td>{diagnostic.participants}</td><td>{diagnostic.n}</td>
            <td>{format(coefficient.estimate, 3)}</td>
            <td>{format(coefficient.ci_lower, 3)} to {format(coefficient.ci_upper, 3)}</td>
            <td>{format(diagnostic.residual_lag1_acf, 3)}</td>
          </tr>;
        })}</tbody>
      </table>
    </div>
    <p>Intervals use the fitted model's independent residual assumption. Residual autocorrelation is reported as a model diagnostic. The incomplete-mode fit uses observed outcomes and complete covariates.</p>
  </article>;
}
