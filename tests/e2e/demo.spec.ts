import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';

async function download(page: Page, name: string) {
  const pending = page.waitForEvent('download');
  await page.getByRole('button', { name, exact: true }).click();
  return readFile((await (await pending).path())!, 'utf8');
}

test('navigation, accessible chart values, and browser history', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Studying cognitive aging, together.');
  for (const name of ['Cohort Explorer', 'Longitudinal Analysis', 'Causal Inference', 'Biomarker Explorer', 'Prediction Modeling', 'Research Report']) {
    await page.getByRole('link', { name, exact: true }).click();
    await expect(page.getByRole('heading', { name, exact: true })).toBeVisible();
    await expect(page.getByRole('link', { name, exact: true })).toHaveAttribute('aria-current', 'page');
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
  }
  await page.goBack();
  await expect(page.getByRole('heading', { name: 'Prediction Modeling' })).toBeVisible();
  await page.getByRole('link', { name: 'Longitudinal Analysis' }).click();
  await page.locator('#longitudinal').getByText('Trajectory values', { exact: true }).click();
  await expect(page.getByRole('region', { name: 'Trajectory values' }).getByRole('row')).toHaveCount(11);
  await expect(page.getByRole('region', { name: 'Adjusted longitudinal estimates' })).toBeVisible();
  await page.getByRole('link', { name: 'Causal Inference' }).click();
  await expect(page.getByRole('region', { name: 'Covariate balance' })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Weight truncation sensitivity' }).getByRole('row')).toHaveCount(4);
  await expect(page.getByText('Incomplete simulation effect withheld.')).toBeVisible();
  expect(errors).toEqual([]);
});

test('cohort pagination, filtered CSV, dictionary, report, and print', async ({ page }) => {
  await page.goto('/#cohort');
  await page.getByRole('button', { name: 'Next page' }).click();
  await expect(page.getByRole('status')).toContainText('81–160');
  await page.getByLabel('Visit year', { exact: true }).selectOption('8');
  await page.getByLabel('Sex (synthetic)').selectOption('Female');
  await page.getByLabel('Deprivation group', { exact: true }).selectOption('High');
  await page.getByLabel('Hypertension', { exact: true }).selectOption('Yes');
  const status = await page.getByRole('status').textContent();
  const [header, ...rows] = (await download(page, 'Export filtered CSV')).trim().split('\n');
  expect(header).toContain('participant_id,visit_year,age_at_baseline,age_at_visit');
  expect(status).toContain(`of ${rows.length.toLocaleString()} matching rows`);
  expect(rows.every(row => /^P\d{4},8,[\d.]+,[\d.]+,Female,High,[\d.]+,Yes,/.test(row))).toBe(true);
  const dictionary = JSON.parse(await download(page, 'Data dictionary JSON'));
  expect(Object.keys(dictionary.fields).sort()).toEqual(header.split(',').sort());
  await page.getByRole('link', { name: 'Research Report', exact: true }).click();
  const report = JSON.parse(await download(page, 'Download report JSON'));
  expect(report.observations).toBe(12_000);
  expect(report.analyses.cohort.complete.iptw.status).toBe('computed');
  expect(report.analyses.cohort.incomplete.iptw.status).toBe('withheld');
  expect(report.analyses.cohort.complete.prediction.participant_overlap).toBe(0);
  const cohort = await download(page, 'Download cohort CSV');
  expect(cohort.trim().split('\n')).toHaveLength(12_001);
  expect(await download(page, 'Export CSV')).toBe(cohort);
  await page.evaluate(() => { window.print = () => document.body.setAttribute('data-printed', 'true'); });
  await page.getByRole('button', { name: 'Print / PDF' }).click();
  await expect(page.locator('body')).toHaveAttribute('data-printed', 'true');
});

test('biomarker wave and marker selection recompute the association', async ({ page }) => {
  await page.goto('/#biomarkers');
  const r = page.locator('#biomarkers #corrValue');
  const baseline = await r.textContent();
  await page.getByLabel('Timepoint').selectOption('8');
  await expect(r).not.toHaveText(baseline!);
  const crp = await r.textContent();
  await page.getByLabel('Biomarker', { exact: true }).selectOption('nfl');
  await expect(r).not.toHaveText(crp!);
  await expect(page.getByRole('img', { name: /NfL proxy/ })).toBeVisible();
  await expect(page.locator('#corrSample')).toContainText('Year 8');
  await page.getByLabel('Synthetic participant ID', { exact: false }).fill('P0001');
  await expect(page.getByRole('img', { name: /across visits for P0001/ })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Adjusted biomarker estimates' }).getByRole('row')).toHaveCount(13);
  await page.getByRole('link', { name: 'Prediction Modeling' }).click();
  await expect(page.getByRole('region', { name: 'complete held-out model metrics', exact: true }).getByRole('row')).toHaveCount(6);
  await expect(page.getByText(/Train 1,800 · test 600 · overlapping IDs 0/)).toBeVisible();
});
