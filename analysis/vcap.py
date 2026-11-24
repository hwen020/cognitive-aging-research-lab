from pathlib import Path
import json
import argparse
from collections import Counter
import pandas as pd
from openpyxl import load_workbook

ROOT = Path(".analysis-work/vcap")
BOOK = ROOT / "Virginia Cognitive Aging Project Datasets 2001-2019.xlsx"
KEY = ["id", "occasion"]

def load(path):
    book = load_workbook(path, read_only=True, data_only=True, keep_links=False)
    try:
        tables = {}
        key_audit = {}
        for sheet, fields in {
            "Demographics": {"Age": "age", "Educ": "educ", "Sex": "sex"},
            "Test Dates": {"Session 1": "date"},
            "DigSym1": {"Score": "score"},
        }.items():
            rows = book[sheet].values
            fields = {"SubjID": "id", "Occasion": "occasion", **fields}
            header = next(rows)
            positions = [header.index(name) for name in fields]
            tab = pd.DataFrame.from_records(([row[i] for i in positions] for row in rows), columns=list(fields.values()))
            tab = tab.dropna(subset=KEY, how="all")
            key_audit[sheet] = {"partial_keys": int(tab[KEY].isna().any(axis=1).sum()),
                                "exact_duplicates": int(tab.duplicated().sum())}
            tab = tab.dropna(subset=KEY).drop_duplicates()
            conflict = tab.duplicated(KEY, keep=False)
            key_audit[sheet]["conflicting_key_rows"] = int(conflict.sum())
            tab = tab.loc[~conflict]
            tables[sheet] = tab
        info = tables["Demographics"]
        quality = {"sheets": len(book.sheetnames), "key_audit": key_audit, "demographic_rows": len(info)}
        for name in ["Test Dates", "DigSym1"]:
            other = tables[name]
            quality[name + "_unmatched"] = int(len(other.merge(info[KEY], how="left", on=KEY, indicator=True).query('_merge == "left_only"')))
            info = info.merge(other, on=KEY, how="left", validate="one_to_one")
        return info, quality
    finally:
        book.close()

def clean(info, quality):
    info = info.copy()
    for col, lo, hi in [("age", 18, 100), ("educ", 10, 35), ("score", 0, 133)]:
        parsed = pd.to_numeric(info[col], errors="coerce")
        info[col] = parsed.where(parsed.between(lo, hi))
        quality["missing_" + col] = int(info[col].isna().sum())
    info["sex"] = pd.to_numeric(info.sex, errors="coerce").where(lambda s: s.isin([0, 1]))
    info["occasion"] = pd.to_numeric(info.occasion, errors="coerce")
    invalid = ~info.occasion.ge(1) | ~info.occasion.mod(1).eq(0)
    quality["invalid_occasion"] = int(invalid.sum())
    info = info.loc[~invalid].copy()
    info["date"] = pd.to_datetime(info.date.where(info.date.map(lambda value: not isinstance(value, (int, float)))), errors="coerce")
    quality["missing_date"] = int(info.date.isna().sum())
    count = info.groupby("id").size()
    quality.update(participants=len(count), two_occasions=int((count >= 2).sum()), three_occasions=int((count >= 3).sum()))
    dated = info.dropna(subset=["date"]).sort_values(KEY).copy()
    bad = dated.loc[dated.groupby("id").date.diff().dt.days.le(0), "id"]
    quality["nonincreasing_date_participants"] = int(bad.nunique())
    dated = dated.loc[~dated.id.isin(bad)]
    dated = dated.loc[dated.occasion.ge(1)]
    base = dated.loc[dated.occasion.eq(1), ["id", "age", "educ", "sex", "date", "score"]].rename(columns={
        "age": "age0", "educ": "educ0", "sex": "sex0", "date": "date0", "score": "score0"})
    analytic = dated.merge(base, how="inner", on="id", validate="many_to_one")
    analytic["years"] = (analytic.date - analytic.date0).dt.days / 365.2425
    analytic = analytic.dropna(subset=["score", "score0", "age0", "educ0", "sex0"])
    analytic = analytic.loc[analytic.years.ge(0)].copy()
    sizes = analytic.groupby("id").size()
    quality.update(eligible_people=len(sizes), eligible_rows=len(analytic), repeated_people=int((sizes >= 2).sum()),
                   eligible_three=int((sizes >= 3).sum()))
    last = analytic.groupby("id").years.max()
    quality["followup_years_quantiles"] = last[last.gt(0)].quantile([0,.25,.5,.75,1]).tolist()
    quality["baseline_profiles"] = {
        str(label): {"n": len(group), **group[["age0","educ0","score0"]].mean().to_dict()}
        for label, group in analytic.loc[analytic.occasion.eq(1)].groupby(analytic.id.map(sizes).gt(1))
    }
    return analytic, quality

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, default=BOOK)
    args = parser.parse_args()
    data, audit = clean(*load(args.workbook))
    data[["id", "occasion", "years", "age0", "educ0", "sex0", "score"]].to_csv(ROOT / "analysis-private.csv", index=False)
    (ROOT / "audit.json").write_text(json.dumps(audit, indent=2, allow_nan=False), encoding="utf8")
    print(json.dumps(audit, indent=2))
