export const seed = 20261123;
export const YEARS = [0, 2, 4, 6, 8] as const;
export const columns = ['participant_id', 'visit_year', 'age_at_baseline', 'age_at_visit', 'sex', 'deprivation', 'education_years', 'hypertension', 'crp', 'ptau', 'nfl', 'cognitive_score'] as const;

export type Marker = 'crp' | 'ptau' | 'nfl';
export type Row = {
  participant_id: string;
  visit_year: number;
  age_at_baseline: number;
  age_at_visit: number;
  sex: 'Female' | 'Male';
  deprivation: 'Low' | 'High';
  education_years: number;
  hypertension: 'Yes' | 'No';
  crp: number;
  ptau: number;
  nfl: number;
  cognitive_score: number;
};

export function generateCohort(): Row[] {
  let rngState = seed;
  function random() {
    rngState = (1664525 * rngState + 1013904223) >>> 0;
    return rngState / 4294967296;
  }
  function normal() {
    return Math.sqrt(-2 * Math.log(Math.max(random(), 1e-12))) * Math.cos(2 * Math.PI * random());
  }
  const round = (value: number, digits = 1) => Number(value.toFixed(digits));
  const rows: Row[] = [];
  for (let participant = 1; participant <= 2400; participant++) {
    const age = round(54 + random() * 30);
    const sex = random() < .54 ? 'Female' : 'Male';
    const high = random() < .49;
    const education = round(9 + random() * 11);
    const hypertension = random() < (age - 48) / 65 + (high ? .12 : 0);
    const personNoise = normal() * 3.1;
    const baseCognition = 111 - .21 * (age - 55) + .43 * (education - 12)
      - (high ? 2.8 : 0) - (hypertension ? 1.5 : 0) + personNoise;
    const inflammation = Math.max(.15, 1.3 + normal() * .35 + (hypertension ? .47 : 0) + (high ? .38 : 0));
    for (const year of YEARS) {
      const change = -.52 * year - .033 * year * (age - 55) - (high ? .24 * year : 0) - (hypertension ? .12 * year : 0);
      const crp = Math.max(.1, inflammation + year * .06 + normal() * .25);
      const ptau = Math.max(0, 12 + .18 * (age - 55) + .48 * year + normal() * 2.5);
      const nfl = Math.max(0, 16 + .26 * (age - 55) + .51 * year + normal() * 3.4);
      const cognition = round(baseCognition + change - .2 * crp - .055 * ptau + normal() * .9);
      rows.push({
        participant_id: 'P' + String(participant).padStart(4, '0'),
        visit_year: year,
        age_at_baseline: age,
        age_at_visit: round(age + year),
        sex,
        deprivation: high ? 'High' : 'Low',
        education_years: education,
        hypertension: hypertension ? 'Yes' : 'No',
        crp: round(crp, 2),
        ptau: round(ptau, 2),
        nfl: round(nfl, 2),
        cognitive_score: cognition,
      });
    }
  }
  return rows;
}

export const data = generateCohort();
export const cohortSize = (rows: Row[]) => new Set(rows.map(row => row.participant_id)).size;
export const mean = (rows: Row[], value: (row: Row) => number) =>
  rows.length ? rows.reduce((sum, row) => sum + value(row), 0) / rows.length : NaN;
export const format = (value: number, precision = 1) => Number.isFinite(value) ? value.toFixed(precision) : '—';

type FilterKey = 'visit_year' | 'sex' | 'deprivation' | 'hypertension';
export function filterRows(rows: Row[], { education = 'all', ...filters }: Record<FilterKey, string> & { education?: string }) {
  return rows.filter(row => Object.entries(filters).every(([key, value]) =>
    value === 'all' || String(row[key as FilterKey]) === value)
    && (education === 'all' || (education === 'below14' ? row.education_years < 14 : row.education_years >= 14)));
}

export const trajectories = (['Low', 'High'] as const).map((group, index) => ({
  group,
  color: ['#5479d7', '#138b8a'][index],
  points: YEARS.map(year => {
    const rows = data.filter(row => row.deprivation === group && row.visit_year === year);
    return { year, n: rows.length, mean: mean(rows, row => row.cognitive_score) };
  }),
}));

export function pearson(rows: Row[], marker: Marker) {
  const xMean = mean(rows, row => row[marker]);
  const yMean = mean(rows, row => row.cognitive_score);
  let cross = 0;
  let xx = 0;
  let yy = 0;
  for (const row of rows) {
    const x = row[marker] - xMean;
    const y = row.cognitive_score - yMean;
    cross += x * y;
    xx += x * x;
    yy += y * y;
  }
  return rows.length < 3 || xx === 0 || yy === 0 ? NaN : cross / Math.sqrt(xx * yy);
}

export const markerLabels: Record<Marker, string> = {
  crp: 'CRP proxy (simulated mg/L)',
  ptau: 'p-tau proxy (arbitrary units)',
  nfl: 'NfL proxy (arbitrary units)',
};

const fields: Record<(typeof columns)[number], string> = {
  participant_id: 'Non-identifying artificial participant key',
  visit_year: 'Years since baseline, one of 0, 2, 4, 6, 8',
  age_at_baseline: 'Synthetic baseline age in years, 54–84',
  age_at_visit: 'Synthetic age in years, baseline age plus visit year',
  sex: 'Simulated Female or Male category',
  deprivation: 'Simulated baseline High or Low neighborhood deprivation',
  education_years: 'Simulated baseline years of education, 9–20',
  hypertension: 'Simulated Yes or No baseline hypertension proxy',
  ...markerLabels,
  cognitive_score: 'Simulated unitless cognition-like score',
};

export const dictionary = { dataset_type: 'DETERMINISTIC_SYNTHETIC', seed, missingness: 'None injected in the complete cohort', fields };
export const reportCounts = `${cohortSize(data).toLocaleString()} synthetic participants contribute ${data.length.toLocaleString()} rows across five scheduled visits. The generator uses seed ${seed}. This complete cohort has no injected missingness.`;
export const report = () => ({
  title: 'Cognitive Aging Research Lab',
  schema_version: 1,
  provenance: dictionary,
  participants: cohortSize(data),
  observations: data.length,
  visit_years: YEARS,
  descriptive_trajectories: trajectories.map(({ group, points }) => ({ group, points })),
  limitations: ['Synthetic data and arbitrary cognition scale', 'Analyses characterize the specified simulations', 'No real-world generalization'],
});

export function csv(rows: Row[]) {
  return [columns.join(','), ...rows.map(row => columns.map(column => row[column]).join(','))].join('\n') + '\n';
}

function download(body: string, name: string, type: string) {
  const url = URL.createObjectURL(new Blob([body], { type }));
  const link = document.createElement('a');
  link.href = url;
  link.download = name;
  document.body.append(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 2_000);
}

export function downloadCohort(rows: Row[], filtered = false) {
  download(csv(rows), filtered ? 'cognitive_aging_filtered_synthetic.csv' : 'cognitive_aging_synthetic_cohort.csv', 'text/csv;charset=utf-8');
}

export function downloadJson(value: unknown, name: string) {
  download(JSON.stringify(value, null, 2), name, 'application/json;charset=utf-8');
}
