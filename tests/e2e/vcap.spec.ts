import { expect, test } from '@playwright/test';
import { readFile } from 'node:fs/promises';

test('VCAP is separate and exports only validated aggregate data', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'VCAP Longitudinal Research' }).click();
  await expect(page.getByRole('heading', { name: 'VCAP Longitudinal Research' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Mixed-Effects Results' })).toBeVisible();
  await expect(page.getByText(/participant overlap 0/i)).toBeVisible();
  const download = page.waitForEvent('download');
  await page.getByRole('link', { name: 'VCAP aggregate JSON' }).click();
  const aggregate = JSON.parse(await readFile((await (await download).path())!, 'utf8'));
  expect(aggregate.audit.repeated_people).toBeGreaterThan(0);
  expect(aggregate.prediction.max_id_overlap).toBe(0);
  expect(JSON.stringify(aggregate)).not.toMatch(/"SubjID"|"date0"|"score0raw"/);
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
  await page.getByRole('link', { name: /NHANES 2011/ }).click();
  await expect(page.getByRole('heading', { name: 'NHANES 2011–2014', exact: true })).toBeVisible();
});
