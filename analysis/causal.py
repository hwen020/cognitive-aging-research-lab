"""IPTW demonstration for an exposure randomly assigned by the simulator."""

import numpy as np
from sklearn.linear_model import LogisticRegression

from analysis.cohort import SEED

ADJUSTMENT = ["age_at_baseline", "education_years", "sex_female"]


def weighted_difference(y, a, weights):
    return float(np.average(y[a], weights=weights[a]) - np.average(y[~a], weights=weights[~a]))


def propensity(x, a):
    fit = LogisticRegression(C=1e6, solver="lbfgs", tol=1e-8)
    return fit.fit(x, a).predict_proba(x)[:, 1]


def stabilized(a, p):
    return np.where(a, a.mean() / p, (1 - a.mean()) / (1 - p))


def diagnostics(x, a, p, weights):
    sd = np.sqrt((x[a].var(axis=0) + x[~a].var(axis=0)) / 2)
    before = (x[a].mean(axis=0) - x[~a].mean(axis=0)) / sd
    after = (np.average(x[a], axis=0, weights=weights[a])
             - np.average(x[~a], axis=0, weights=weights[~a])) / sd
    ess = [float(group.sum() ** 2 / (group @ group)) for group in (weights[~a], weights[a])]
    overlap = [float(max(p[a].min(), p[~a].min())), float(min(p[a].max(), p[~a].max()))]
    support = float(np.mean((p >= overlap[0]) & (p <= overlap[1])))
    passes = bool(np.isfinite(after).all() and np.abs(after).max() <= .10
                  and min(ess) >= 50 and support >= .90 and p.min() >= .05 and p.max() <= .95)
    return {
        "passes": passes, "ess_low_high": ess, "common_support": overlap,
        "fraction_in_common_support": support,
        "propensity_range": [float(p.min()), float(p.max())],
        "weight_range": [float(weights.min()), float(weights.max())],
        "balance": [
            {"covariate": name, "smd_before": float(b), "smd_after": float(c)}
            for name, b, c in zip(ADJUSTMENT, before, after)
        ],
    }


def analyze(frame, replications=500):
    baseline = frame.loc[frame.visit_year.eq(0)].set_index("participant_id")
    year8 = frame.loc[frame.visit_year.eq(8)].set_index("participant_id")
    if len(year8) != len(baseline):
        return {"status": "withheld", "reason": "Year-8 attrition requires a separate censoring design."}
    baseline = baseline.loc[year8.index]
    a = baseline.deprivation.eq("High").to_numpy()
    y = year8.cognitive_score.to_numpy()
    x = np.column_stack(((baseline.age_at_baseline - 69) / 10,
                         (baseline.education_years - 14) / 5,
                         baseline.sex.eq("Female").astype(float)))
    if min(a.sum(), (~a).sum()) < 50 or np.any(x[a].var(axis=0) + x[~a].var(axis=0) == 0):
        return {"status": "withheld", "reason": "Insufficient treatment-group size or covariate variation."}
    p = propensity(x, a)
    if p.min() < .05 or p.max() > .95:
        return {"status": "withheld", "reason": "Positivity threshold failed.",
                "propensity_range": [float(p.min()), float(p.max())]}
    weights = stabilized(a, p)
    primary = diagnostics(x, a, p, weights)
    result = {"n": len(y), "n_high": int(a.sum()), "diagnostics": primary,
              "estimand": "Simulated baseline population ATE of high versus low assignment on Year-8 cognition"}
    if not primary["passes"]:
        return {**result, "status": "withheld", "reason": "Balance or overlap threshold failed."}

    rng = np.random.default_rng(SEED + 2)
    trims = [0, .01, .05]
    bootstrap = {trim: [] for trim in trims}
    for _ in range(replications):
        idx = rng.integers(len(y), size=len(y))
        ai, xi, yi = a[idx], x[idx], y[idx]
        wi = stabilized(ai, propensity(xi, ai))
        for trim in trims:
            bootstrap[trim].append(weighted_difference(yi, ai, wi.clip(*np.quantile(wi, [trim, 1 - trim]))))
    sensitivity = []
    for trim in trims:
        w = weights.clip(*np.quantile(weights, [trim, 1 - trim]))
        audit = diagnostics(x, a, p, w)
        entry = {"tail_quantile": trim, "diagnostics": audit}
        if audit["passes"]:
            entry.update(estimate=weighted_difference(y, a, w),
                         ci95=np.quantile(bootstrap[trim], [.025, .975]).tolist())
        sensitivity.append(entry)

    return {**result, "status": "computed", "bootstrap_replications": replications,
            "adjustment": ADJUSTMENT, "weight_sensitivity": sensitivity,
            "assumptions": ["Synthetic exposure draw is independent of pre-exposure attributes.",
                            "Baseline clinical proxies and biomarkers are excluded from the adjustment set.",
                            "No transport to observed neighborhood interventions or populations."]}
