import { useEffect, useState } from 'react';
import { LongitudinalResults, results } from './ResearchResults';
import { BiomarkerModels, PredictionResults } from './BiologicalResults';
import { MarkerProfile } from './MarkerProfile';
import { CausalResults } from './CausalResults';
import { CohortStats, Scatter, SummaryStats, TrajectoryChart, TrajectorySummary } from './charts';
import { columns, data, dictionary, downloadCohort, downloadJson, filterRows, format, pearson, report, reportCounts, type Marker } from './cohort';
import './style.css';

const pages = [
  ['overview', 'Overview'],
  ['cohort', 'Cohort Explorer'],
  ['longitudinal', 'Longitudinal Analysis'],
  ['causal', 'Causal Inference'],
  ['biomarkers', 'Biomarker Explorer'],
  ['prediction', 'Prediction Modeling'],
  ['report', 'Research Report'],
] as const;

const currentPage = () => pages.find(([id]) => location.hash === '#' + id) ?? pages[0];
const initialFilters = { visit_year: 'all', sex: 'all', deprivation: 'all', hypertension: 'all' };
const pageSize = 80;

export function App() {
  const [[page, label], setPage] = useState(currentPage);
  const [filters, setFilters] = useState(initialFilters);
  const [pageIndex, setPageIndex] = useState(0);
  const [marker, setMarker] = useState<Marker>('crp');
  const [markerYear, setMarkerYear] = useState(0);

  useEffect(() => {
    const navigate = () => {
      setPage(currentPage());
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', navigate);
    return () => window.removeEventListener('hashchange', navigate);
  }, []);

  function updateFilter(key: keyof typeof initialFilters, value: string) {
    setFilters(previous => ({ ...previous, [key]: value }));
    setPageIndex(0);
  }

  const filtered = filterRows(data, filters);
  const offset = pageIndex * pageSize;
  const pageRows = filtered.slice(offset, offset + pageSize);
  const rowNote = filtered.length
    ? `Showing ${offset + 1}–${offset + pageRows.length} of ${filtered.length.toLocaleString()} matching rows. CSV includes every matching row.`
    : 'No observations match these filters.';
  const markerRows = data.filter(row => row.visit_year === markerYear);
  const correlation = pearson(markerRows, marker);

  return (
    <div className="app">
      <a className="skip" href="#main" onClick={event => {
        event.preventDefault();
        document.getElementById('main')?.focus();
      }}>Skip to research content</a>
      <aside className="sidebar">
        <div className="brand">
          <div className="brandmark" aria-hidden="true">◈</div>
          <strong>Cognitive Aging<br />Research Lab</strong>
        </div>
        <nav className="nav" aria-label="Research sections">
          {pages.map(([id, title]) => <a key={id} href={`#${id}`} aria-current={page === id ? 'page' : undefined}>{title}</a>)}
        </nav>
      </aside>
      <main className="main" id="main" tabIndex={-1}>
        <div className="topbar">
          <div className="crumb">Research / <b>{label}</b></div>
          <div className="top-actions"><span className="tag">Synthetic data</span><button className="button" onClick={() => downloadCohort(data)}>Export CSV</button></div>
        </div>
        <p className="notice"><strong>Research integrity.</strong> All records are simulated from a fixed seed. The results characterize this simulation and its analytical workflow.</p>
        <section id="overview" hidden={page !== 'overview'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Research intelligence workspace</div>
          <h1>Studying cognitive aging, together.</h1>
          <div className="subtitle">One harmonized longitudinal cohort for social determinants and biological pathways.</div>
          </div>
          <div className="tabs">
          <span className="tab selected">Social determinants</span>
          <span className="tab selected">Biological markers</span>
          </div>
          </div>
          <div className="stats" id="summaryStats">
          <SummaryStats />
          </div>
          <div className="grid2">
          <article className="panel card">
          <div className="cardhead">
          <div>
          <h2>Cognitive score by follow-up visit</h2>
          <div className="meta">Synthetic cohort · group means with shared timeline</div>
          </div>
          <span className="pill shared">Shared</span>
          </div>
          <div id="overviewChart" className="plot">
          <TrajectoryChart />
          </div>
          <div className="legend">
          <span>
          <i className="dot" style={{background: '#5479d7'}}>
          </i>Lower deprivation</span>
          <span>
          <i className="dot" style={{background: '#138b8a'}}>
          </i>Higher deprivation</span>
          </div>
          </article>
          <article className="panel card">
          <div className="cardhead">
          <h2>Research tracks</h2>
          </div>
          <div className="rowline">
          <div>
          <b>Social research</b>
          <small>Deprivation, education, vascular risks</small>
          </div>
          <span className="pill social">Social DS</span>
          </div>
          <div className="rowline">
          <div>
          <b>Biological research</b>
          <small>CRP, p-tau, NfL, cognition</small>
          </div>
          <span className="pill bio">Biological DS</span>
          </div>
          <div className="rowline">
          <div>
          <b>Shared methods</b>
          <small>Cohort QC, longitudinal analysis, reproducibility</small>
          </div>
          <span className="pill shared">Both roles</span>
          </div>
          <div className="callout">Explore the same people and visits across both tracks. Outcomes and predictors follow a single harmonized schema.</div>
          </article>
          </div>
          <div className="gridhalf">
          <article className="panel card">
          <div className="cardhead">
          <h2>Analysis coverage</h2>
          <span className="pill social">Social research</span>
          </div>
          <div className="flowlist">
          <div className="flowbox">
          <b>Social exposure → cognitive trajectory</b>
          <small>Exploratory stratification and confounder-aware analysis plan</small>
          </div>
          <div className="flowbox">
          <b>Observational causal framework</b>
          <small>Directed graph, estimand and simulated IPTW diagnostics</small>
          </div>
          </div>
          </article>
          <article className="panel card">
          <div className="cardhead">
          <h2>Analysis coverage</h2>
          <span className="pill bio">Biological research</span>
          </div>
          <div className="flowlist">
          <div className="flowbox">
          <b>Biomarker → cognition associations</b>
          <small>Descriptive Pearson correlations on synthetic records</small>
          </div>
          <div className="flowbox">
          <b>Held-out prediction experiment</b>
          <small>Baseline-only features and participant-grouped validation</small>
          </div>
          </div>
          </article>
          </div>
        </section>
        <section id="cohort" hidden={page !== 'cohort'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Shared foundation</div>
          <h1>Cohort Explorer</h1>
          <div className="subtitle">Slice an analysis-ready, synthetic longitudinal cohort.</div>
          </div>
          <span className="pill shared">Both roles</span>
          </div>
          <div className="panel card">
          <div className="formrow">
          <div className="field">
          <label htmlFor="visitFilter">Visit year</label>
          <select id="visitFilter" value={filters.visit_year} onChange={event => updateFilter('visit_year', event.target.value)}>
          <option value="all">All visits</option>
          <option value="0">Baseline</option>
          <option value="2">Year 2</option>
          <option value="4">Year 4</option>
          <option value="6">Year 6</option>
          <option value="8">Year 8</option>
          </select>
          </div>
          <div className="field">
          <label htmlFor="sexFilter">Sex (synthetic)</label>
          <select id="sexFilter" value={filters.sex} onChange={event => updateFilter('sex', event.target.value)}>
          <option value="all">All</option>
          <option value="Female">Female</option>
          <option value="Male">Male</option>
          </select>
          </div>
          <div className="field">
          <label htmlFor="deprivationFilter">Deprivation group</label>
          <select id="deprivationFilter" value={filters.deprivation} onChange={event => updateFilter('deprivation', event.target.value)}>
          <option value="all">All</option>
          <option value="Low">Low</option>
          <option value="High">High</option>
          </select>
          </div>
          <div className="field">
          <label htmlFor="htnFilter">Hypertension</label>
          <select id="htnFilter" value={filters.hypertension} onChange={event => updateFilter('hypertension', event.target.value)}>
          <option value="all">All</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          </select>
          </div>
          </div>
          <div className="stats" id="cohortStats" style={{marginBottom: '10px'}}>
          <CohortStats rows={filtered} />
          </div>
          <div className="cardhead">
          <h2>Observation records</h2>
          <div className="downloadrow">
          <button className="button" onClick={() => downloadCohort(filtered, true)}>Export filtered CSV</button>
          <button className="button" onClick={() => downloadJson(dictionary, 'data_dictionary.json')}>Data dictionary JSON</button>
          </div>
          </div>
          <div className="scroll" tabIndex={0} role="region" aria-label="Observation records">
          <table>
          <thead>
          <tr>{columns.map(column => <th key={column} scope="col">{column}</th>)}</tr>
          </thead>
          <tbody id="cohortTable">{pageRows.map(row => <tr key={`${row.participant_id}-${row.visit_year}`}>{columns.map(column => <td key={column}>{row[column]}</td>)}</tr>)}</tbody>
          </table>
          </div>
          <p className="footnote" role="status">{rowNote}</p>
          <div className="downloadrow">
          <button className="button" disabled={pageIndex === 0} onClick={() => setPageIndex(index => index - 1)}>Previous page</button>
          <button className="button" disabled={offset + pageSize >= filtered.length} onClick={() => setPageIndex(index => index + 1)}>Next page</button>
          </div>
          </div>
        </section>
        <section id="longitudinal" hidden={page !== 'longitudinal'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Trajectory analysis</div>
          <h1>Longitudinal Analysis</h1>
          <div className="subtitle">Observe synthetic within-cohort changes over five follow-ups spanning eight years.</div>
          </div>
          <span className="pill shared">Both roles</span>
          </div>
          <div className="grid2">
          <article className="panel card">
          <div className="cardhead">
          <h2>Mean cognitive score over time</h2>
          <span className="pill shared">Descriptive</span>
          </div>
          <div id="longChart" className="plot">
          <TrajectoryChart />
          </div>
          <div className="legend">
          <span>
          <i className="dot" style={{background: '#5479d7'}}>
          </i>Lower deprivation</span>
          <span>
          <i className="dot" style={{background: '#138b8a'}}>
          </i>Higher deprivation</span>
          </div>
          </article>
          <article className="panel card">
          <div className="cardhead">
          <h2>Interpretation</h2>
          </div>
          <div id="trajectoryText">
          <TrajectorySummary />
          </div>
          <div className="callout">These means summarize the complete cohort without adjustment. The fitted repeated-measures model appears below.</div>
          </article>
          </div>
          <article className="panel card">
          <div className="cardhead">
          <h2>Longitudinal workflow</h2>
          <span className="pill shared">Codex implementation</span>
          </div>
          <div className="flowlist">
          <div className="flowbox">
          <b>1 · Long-format validation</b>
          <small>Unique (participant_id, visit_year), time ordering, missingness and range checks</small>
          </div>
          <div className="flowbox">
          <b>2 · Mixed-effects regression (R/lme4)</b>
          <small>Random participant intercept; time × deprivation interaction; baseline age, sex, education, vascular risks</small>
          </div>
          <div className="flowbox">
          <b>3 · Uncertainty and sensitivity</b>
          <small>Confidence intervals, diagnostics, missingness analyses and reproducible report</small>
          </div>
          </div>
          </article>
          <LongitudinalResults />
        </section>
        <section id="causal" hidden={page !== 'causal'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Social research track</div>
          <h1>Causal Inference</h1>
          <div className="subtitle">Specify a question before estimating an effect.</div>
          </div>
          <span className="pill social">Social DS</span>
          </div>
          <CausalResults />
        </section>
        <section id="biomarkers" hidden={page !== 'biomarkers'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Biological research track</div>
          <h1>Biomarker Explorer</h1>
          <div className="subtitle">Explore associations between inflammatory/neurodegeneration proxies and cognition.</div>
          </div>
          <span className="pill bio">Biological DS</span>
          </div>
          <div className="grid2">
          <article className="panel card">
          <div className="cardhead">
          <h2>Marker vs. cognitive score</h2>
          <span className="pill bio">Synthetic data</span>
          </div>
          <div className="formrow">
          <div className="field">
          <label htmlFor="markerSelect">Biomarker</label>
          <select id="markerSelect" value={marker} onChange={event => setMarker(event.target.value as Marker)}>
          <option value="crp">CRP (mg/L)</option>
          <option value="ptau">p-tau (arbitrary demo units)</option>
          <option value="nfl">NfL (arbitrary demo units)</option>
          </select>
          </div>
          <div className="field">
          <label htmlFor="markerVisit">Timepoint</label>
          <select id="markerVisit" value={markerYear} onChange={event => setMarkerYear(Number(event.target.value))}>
          <option value="0">Baseline</option>
          <option value="2">Year 2</option>
          <option value="4">Year 4</option>
          <option value="6">Year 6</option>
          <option value="8">Year 8</option>
          </select>
          </div>
          </div>
          <div id="scatterChart" className="plot">
          <Scatter rows={markerRows} marker={marker} />
          </div>
          </article>
          <article className="panel card">
          <div className="cardhead">
          <h2>Descriptive association</h2>
          <span className="pill bio">Unadjusted</span>
          </div>
          <div className="stat" style={{padding: '0'}}>
          <div className="label">Pearson correlation (r)</div>
          <div className="value" id="corrValue">{format(correlation, 3)}</div>
          <div className="hint" id="corrSample">{`n = ${markerRows.length.toLocaleString()} synthetic observations at Year ${markerYear}`}</div>
          </div>
          <div className="callout">Correlations are computed from deterministic synthetic observations. They do not show biological causation, clinical utility, or predictive performance.</div>
          <div className="flowlist">
          <div className="flowbox">
          <b>Adjusted marker models</b>
          <small>Separate baseline levels and within-person change with mixed effects and BH adjustment.</small>
          </div>
          <div className="flowbox">
          <b>Real-world data boundary</b>
          <small>Only use biomarker / imaging data when licensed and authorized. Synthetic proxies must remain clearly labeled.</small>
          </div>
          </div>
          </article>
          </div>
          <MarkerProfile rows={markerRows} marker={marker} />
          <BiomarkerModels />
        </section>
        <section id="prediction" hidden={page !== 'prediction'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Biological research track</div>
          <h1>Prediction Modeling</h1>
          <div className="subtitle">Baseline-only prediction of simulated Year-8 cognitive scores.</div>
          </div>
          <span className="pill bio">Biological DS</span>
          </div>
          <PredictionResults />
        </section>
        <section id="report" hidden={page !== 'report'}>
          <div className="heading">
          <div>
          <div className="eyebrow">Reproducible research</div>
          <h1>Research Report</h1>
          <div className="subtitle">Methods-first summaries for both research tracks.</div>
          </div>
          <span className="pill shared">Both roles</span>
          </div>
          <article className="panel report">
          <h2>Cognitive Aging Research Lab — Demo Report</h2>
          <p>
          <b>Study type:</b> deterministic synthetic longitudinal cohort; five visits across eight years; no patient records.</p>
          <h3>Objective</h3>
          <p>Demonstrate a shared technical workflow for analyzing social determinants of cognitive aging and biological markers in longitudinal observational datasets.</p>
          <h3>Data provenance and quality</h3>
          <p id="reportCounts">{reportCounts}</p>
          <h3>Social research workstream</h3>
          <p>Stratified synthetic cognitive trajectories are visualized for neighborhood deprivation groups. The complete mode includes IPTW balance and overlap diagnostics, bootstrap uncertainty, and truncation sensitivity. The incomplete-mode effect is withheld because attrition requires a censoring design.</p>
          <h3>Biological research workstream</h3>
          <p>Three synthetic biomarker variables are explored using unadjusted Pearson associations with cognitive scores. These are demo variables, not medical measurements. Adjusted models distinguish baseline marker level and change since baseline, with six terms per mode adjusted for multiple tests.</p>
          <h3>Prediction protocol</h3>
          <p>The baseline-to-Year-8 experiment reports held-out regression metrics, paired marker comparisons, subgroup error, and permutation importance.</p>
          <h3>Reproducibility and limitations</h3>
          <p>Records are generated using a fixed seeded algorithm. Screens and exports derive from one data source. This artifact is intended to demonstrate application architecture and research workflow only. No real-world effect sizes, causal conclusions, biomarker validity or model generalization should be inferred.</p>
          <div className="downloadrow">
          <button className="button primary" onClick={() => downloadJson({ ...report(), analyses: results }, 'research_demo_report.json')}>Download report JSON</button>
          <button className="button" onClick={() => window.print()}>Print / PDF</button>
          <button className="button" onClick={() => downloadCohort(data)}>Download cohort CSV</button>
          </div>
          </article>
        </section>
      </main>
    </div>
  );
}
