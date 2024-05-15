#!/usr/bin/env python

"""This program shows `hyperfine` benchmark results as a box and whisker plot.

Quoting from the matplotlib documentation:
    The box extends from the lower to upper quartile values of the data, with
    a line at the median. The whiskers extend from the box to show the range
    of the data. Flier points are those past the end of the whiskers.
"""

import argparse
import json
from functools import cmp_to_key
from pathlib import Path

import matplotlib.pyplot as plt


def cmp_median(medians: list[float], labels: list[str]):
    def compare(i, j):
        med_cmp = medians[i] - medians[j]
        if med_cmp == 0:
            return labels[i] < labels[j]
        else:
            return med_cmp

    return compare


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("file", help="JSON file with benchmark results")
parser.add_argument("--title", help="Plot Title")
parser.add_argument("--sort-by", choices=["median"], help="Sort method")
parser.add_argument(
    "--labels", help="Comma-separated list of entries for the plot legend"
)
parser.add_argument("-o", "--output", help="Save image to the given filename.")

args = parser.parse_args()

with open(args.file, encoding="utf-8") as f:
    results_file = json.load(f)

periscope_results: list[tuple[str, list[dict]]] = []

# collect results
for result_name in results_file:
    result: dict = results_file[result_name]
    if result.get("Success"):
        run_results = result["Success"]["hyperfine"]["results"]
    else:
        run_results = result["Failed"]["hyperfine"]["results"]

    periscope_results.append((result_name, run_results))

if args.labels:
    labels = args.labels.split(",")
else:
    labels = [b[0] for b in periscope_results]
times = [b["times"] for pr in periscope_results for b in pr[1]]

if args.sort_by == "median":
    medians = [b["median"] for pr in periscope_results for b in pr[1]]
    indices = sorted(range(len(labels)), key=cmp_to_key(cmp_median(medians, labels)))
    labels = [labels[i] for i in indices]
    times = [times[i] for i in indices]

plt.figure(figsize=(20, 12), constrained_layout=True)
boxplot = plt.boxplot(times, vert=True, patch_artist=True)
cmap = plt.get_cmap("rainbow")
colors = [cmap(val / len(times)) for val in range(len(times))]

for patch, color in zip(boxplot["boxes"], colors):
    patch.set_facecolor(color)

if args.title:
    plt.title(args.title)
# plt.legend(handles=boxplot["boxes"], labels=labels, loc="best", fontsize="medium")
plt.title(Path(args.file).stem)
plt.ylabel("Time [s]")
plt.ylim(0, None)
plt.xticks(list(range(1, len(labels) + 1)), labels, rotation=65)
if args.output:
    plt.savefig(args.output)
else:
    plt.show()
