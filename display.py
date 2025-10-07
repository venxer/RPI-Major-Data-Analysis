import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- Config --------------------
CSV_PATH = "./filtered_data/decoded.csv"
EXCLUDE_CIPCODES = {"Total"}      
TOP_N = 10
RANK_METHOD = "slope"              
PCT_MULTIPLIER = 100.0             
# ------------------------------------------------

# Load
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip().upper() for c in df.columns]

# Identify columns
year_col  = next((c for c in df.columns if "YEAR" in c), None)
grad_col  = next((c for c in df.columns if "CTOTALT" in c), None)
major_col = next((c for c in df.columns if "CIPCODE" in c or "MAJOR" in c), None)
if not all([year_col, grad_col, major_col]):
    raise ValueError("Columns YEAR, CTOTALT, and CIPCODE/MAJOR not found.")

# Ensure numeric year and grads
df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
df[grad_col] = pd.to_numeric(df[grad_col], errors="coerce")
df = df.dropna(subset=[year_col, grad_col, major_col])

mask_total = df[major_col].isin(["Total"])
totals = (
    df[mask_total]
    .groupby(year_col, as_index=False)[grad_col]
    .sum()
    .rename(columns={grad_col: "TOTAL_YEAR"})
)

if totals.empty:
    raise ValueError("No rows found for CIPCODE Total to compute per-year totals.")

majors = (
    df.groupby([year_col, major_col], as_index=False)[grad_col]
      .sum()
)
majors = majors.merge(totals, on=year_col, how="inner")

majors = majors[majors["TOTAL_YEAR"] > 0].copy()
majors["PCT"] = (majors[grad_col] / majors["TOTAL_YEAR"]) * PCT_MULTIPLIER

majors_no_total = majors[~majors[major_col].isin(EXCLUDE_CIPCODES)].copy()

def fit_slope(x, y):
    if len(x) < 2:
        return 0.0
    coeffs = np.polyfit(x, y, 1)
    return float(coeffs[0])

def abs_growth(y, x):
    if len(x) < 2:
        return 0.0
    order = np.argsort(x)
    return float(y[order[-1]] - y[order[0]])

def cagr(y, x):
    if len(x) < 2:
        return 0.0
    order = np.argsort(x)
    y0 = float(y[order[0]])
    y1 = float(y[order[-1]])
    n_years = int(x[order[-1]] - x[order[0]])
    if y0 <= 0 or n_years <= 0:
        return 0.0
    return (y1 / y0) ** (1 / n_years) - 1

metrics = []
for major, g in majors_no_total.groupby(major_col):
    xs = g[year_col].to_numpy()
    ys = g["PCT"].to_numpy()
    metrics.append({
        "major": major,
        "slope": fit_slope(xs, ys),
        "abs_growth": abs_growth(ys, xs),
        "cagr": cagr(ys, xs)
    })
met = pd.DataFrame(metrics)

if RANK_METHOD not in {"slope", "abs_growth", "cagr"}:
    raise ValueError("RANK_METHOD must be 'slope', 'abs_growth', or 'cagr'.")

top_majors = (
    met.sort_values(RANK_METHOD, ascending=False)
       .head(TOP_N)["major"]
       .tolist()
)

top_df = majors_no_total[majors_no_total[major_col].isin(top_majors)].copy()
top_df.sort_values([major_col, year_col], inplace=True)

# ---- Plot ----
plt.figure(figsize=(12, 6))
for major, g in top_df.groupby(major_col):
    plt.plot(g[year_col], g["PCT"], marker='o', label=str(major))

ylabel = "% of Total Graduates"
plt.title(f"Top {TOP_N} Growing Majors by Trend Slope")
plt.xlabel("Year")
plt.ylabel(ylabel)
plt.legend(title="Major", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize="small")
plt.grid(True)
plt.tight_layout()
plt.savefig("./output/graph.png", dpi=300, bbox_inches="tight")
plt.show()


print(met.sort_values(RANK_METHOD, ascending=False).head(TOP_N))
