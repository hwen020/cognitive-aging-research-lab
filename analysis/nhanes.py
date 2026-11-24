"""Fetch and validate the two official NHANES waves; keep row data in ignored storage."""

import argparse
import hashlib
import html
import json
import re
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"
CYCLES = ((2011, "G"), (2013, "H"))
FIELDS = {
    "DEMO": ["RIDAGEYR", "RIAGENDR", "RIDRETH3", "DMDEDUC2", "INDFMPIR",
             "WTMEC2YR", "SDMVSTRA", "SDMVPSU", "RIDSTATR"],
    "CFQ": ["CFDCSR", "CFDCST1", "CFDCST2", "CFDCST3", "CFDAST", "CFDDS"],
    "BPX": [f"BPX{kind}{i}" for kind in ("SY", "DI") for i in range(1, 5)],
    "GHB": ["LBXGH"],
}
KEY = ["cycle", "SEQN"]
ROOT = Path(".analysis-work/nhanes")
PIN = Path("analysis/nhanes_sources.json")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retrieve(root, pins):
    root.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for year, suffix in CYCLES:
        for component, columns in FIELDS.items():
            name = f"{component}_{suffix}"
            entry = {}
            for ext in ("XPT", "htm"):
                url = f"{BASE}/{year}/DataFiles/{name}.{ext}"
                path = root / f"{name}.{ext}"
                if not path.exists():
                    request = urllib.request.Request(url, headers={"User-Agent": "CognitiveAgingResearch/1.1"})
                    with urllib.request.urlopen(request, timeout=45) as response:
                        body = response.read()
                    if ext == "XPT" and not body.startswith(b"HEADER RECORD"):
                        raise ValueError(f"Invalid SAS transport download: {url}")
                    path.write_bytes(body)
                checksum = digest(path)
                if pins and checksum != pins[name][ext]["sha256"]:
                    raise ValueError(f"Source checksum differs from reviewed version: {name}.{ext}")
                entry[ext] = {"url": url, "sha256": checksum, "bytes": path.stat().st_size}
            dictionary = (root / f"{name}.htm").read_text(encoding="utf-8-sig")
            entry["fields"] = {}
            for field in ["SEQN", *columns]:
                label = re.search(r'<h3[^>]*id="' + field + r'"[^>]*>(.*?)</h3>', dictionary, re.I | re.S)
                if not label:
                    raise ValueError(f"{field} missing from {name} official codebook")
                entry["fields"][field] = html.unescape(label.group(1)).strip()
            for version in ("First Published", "Last Revised"):
                match = re.search(version + r":\s*([^<]+)", dictionary, re.I)
                if match:
                    entry[version] = html.unescape(match.group(1)).strip()
            manifest[name] = entry
    return manifest


def merge_components(left, right):
    return left.merge(right, on=KEY, how="left", validate="one_to_one")


def load(root):
    waves = []
    for year, suffix in CYCLES:
        components = {}
        for component, columns in FIELDS.items():
            frame = pd.read_sas(root / f"{component}_{suffix}.XPT", format="xport")
            frame = frame[["SEQN", *columns]].copy()
            if not all(pd.api.types.is_numeric_dtype(frame[column]) for column in frame):
                raise ValueError(f"Non-numeric XPT schema: {component}_{suffix}")
            if frame.SEQN.isna().any() or not frame.SEQN.mod(1).eq(0).all() or frame.SEQN.duplicated().any():
                raise ValueError(f"Invalid survey identifiers: {component}_{suffix}")
            frame["cycle"] = year
            components[component] = frame
        wave = components.pop("DEMO")
        for frame in components.values():
            if not frame.SEQN.isin(wave.SEQN).all():
                raise ValueError(f"Orphan component record in {year}")
            wave = merge_components(wave, frame)
        waves.append(wave)
    data = pd.concat(waves, ignore_index=True)
    if data.SEQN.duplicated().any():
        raise ValueError("Expected disjoint NHANES cycle IDs")
    ranges = {"CFDDS": (0, 133), "CFDCSR": (0, 10), "CFDCST1": (0, 10),
              "CFDCST2": (0, 10), "CFDCST3": (0, 10), "CFDAST": (0, 100),
              "LBXGH": (0, 25), "RIDAGEYR": (0, 80)}
    ranges.update({field: (0, 300) for field in FIELDS["BPX"]})
    for field, (lo, hi) in ranges.items():
        if not data[field].dropna().between(lo, hi).all():
            raise ValueError(f"Values outside analytical range: {field}")
    data["education"] = data.DMDEDUC2.where(data.DMDEDUC2.isin(range(1, 6)))
    data["pir"] = data.INDFMPIR.where(data.INDFMPIR.between(0, 5))
    data["immediate"] = data[["CFDCST1", "CFDCST2", "CFDCST3"]].sum(axis=1, min_count=3)
    data["delayed"] = data.CFDCSR
    data["fluency"] = data.CFDAST
    data["dsst"] = data.CFDDS
    data["hba1c"] = data.LBXGH
    for short, kind in (("sbp", "SY"), ("dbp", "DI")):
        readings = data[[f"BPX{kind}{i}" for i in range(1, 5)]]
        data[short] = readings.mean(axis=1)
        data[short + "_n"] = readings.notna().sum(axis=1)
    positive = data.WTMEC2YR.gt(0)
    if data.loc[positive, ["SDMVSTRA", "SDMVPSU"]].isna().any().any():
        raise ValueError("Missing design identifiers for positive MEC weights")
    data["mec4"] = data.WTMEC2YR / 2
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-reviewed-sources", action="store_true")
    args = parser.parse_args()
    pins = None if args.record_reviewed_sources else json.loads(PIN.read_text(encoding="utf8"))
    manifest = retrieve(ROOT, pins)
    data = load(ROOT)
    if args.record_reviewed_sources:
        PIN.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8")
    data.to_csv(ROOT / "cohort.csv", index=False)
    older = data.RIDAGEYR.ge(60) & data.mec4.gt(0)
    print(data.loc[older].groupby("cycle")[["dsst", "immediate", "delayed", "fluency", "hba1c", "sbp"]].count().to_string())
