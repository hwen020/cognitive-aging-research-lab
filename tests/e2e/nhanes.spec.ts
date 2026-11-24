import { expect, test } from '@playwright/test';

test('real NHANES reports and HRS status stay separate from the synthetic demo', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: /NHANES 2011–2014/ }).click();
  await expect(page.getByRole('heading', { level: 1, name: 'NHANES 2011–2014' })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Social factors/ })).toBeVisible();
  await expect(page.getByRole('img', { name: /Binned DSST residuals for biological/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Predictive performance/ })).toBeVisible();
  for (const track of ['Social', 'Biological']) {
    const download = page.waitForEvent('download');
    await page.getByRole('link', { name: `NHANES ${track} Report` }).click();
    expect((await download).suggestedFilename()).toBe(`${track.toLowerCase()}.md`);
  }
  await expect(page.getByRole('button', { name: 'Export CSV' })).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
  await page.getByRole('link', { name: /HRS Longitudinal —/ }).click();
  await expect(page.getByText('Longitudinal Analysis Framework — Awaiting Authorized Data Execution')).toBeVisible();
  await expect(page.getByRole('heading', { name: /Predictive performance/ })).toHaveCount(0);
  await page.getByRole('link', { name: 'Synthetic Demo' }).click();
  await expect(page.getByRole('button', { name: 'Export CSV' })).toBeVisible();
});
