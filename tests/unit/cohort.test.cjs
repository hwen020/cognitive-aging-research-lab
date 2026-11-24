const { createHash } = require('node:crypto');
const assert = require('node:assert/strict');
const { test } = require('node:test');
const { cohortSize, csv, data, filterRows, generateCohort, pearson, YEARS } = require('../../.test-build/cohort.js');

test('the seeded cohort regenerates the same CSV and has unique complete waves', () => {
  const hash = value => createHash('sha256').update(value).digest('hex');
  assert.equal(hash(csv(generateCohort())), hash(csv(data)));
  assert.equal(hash(csv(data)), '5104d2c3ca510a4f0ac537652c3f4b76f6b4e567d42cad9029c3b24b5297de74');
  assert.equal(cohortSize(data), 2400);
  assert.equal(data.length, 12000);
  assert.equal(new Set(data.map(({ participant_id, visit_year }) => `${participant_id}/${visit_year}`)).size, data.length);
  for (const wave of YEARS) assert.equal(data.filter(row => row.visit_year === wave).length, 2400);
});

test('filtering and Pearson handle deliberate edge cases', () => {
  const fixture = [0, 1, 2].map(index => ({ ...data[0], crp: index + 1, cognitive_score: 4 - index }));
  assert.ok(Math.abs(pearson(fixture, 'crp') + 1) < 1e-12);
  assert.ok(Number.isNaN(pearson(fixture.slice(0, 2), 'crp')));
  assert.deepEqual(filterRows(data, { visit_year: '3', sex: 'all', deprivation: 'all', hypertension: 'all' }), []);
});
