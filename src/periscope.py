#!/usr/bin/env python

"""This program shows `hyperfine` benchmark results as a box and whisker plot.

Quoting from the matplotlib documentation:
    The box extends from the lower to upper quartile values of the data, with
    a line at the median. The whiskers extend from the box to show the range
    of the data. Flier points are those past the end of the whiskers.
"""

import argparse

import matplotlib.pyplot as plt

import whiskers
import histogram
import periscope_result


def main(
    periscope_results: list[periscope_result.BenchResult], args: argparse.Namespace
):
    figure = plt.figure(figsize=(20, 12), constrained_layout=True)

    match args.type:
        case "whisker":
            whiskers.plot_whiskers(args, periscope_results, figure)
        case "histogram":
            histogram.plot_histogram(args, periscope_results, figure, of_dump=False)
        case "histogram-after-dump":
            histogram.plot_histogram(args, periscope_results, figure, of_dump=True)
        case _:
            print("Unknown type passed.")
            return

    if args.output:
        plt.savefig(args.output)
    else:
        plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="JSON file with benchmark results")
    parser.add_argument("--title", help="Plot Title")
    parser.add_argument("--sort-by", choices=["median", "wc"], help="Sort method")
    parser.add_argument(
        "--labels", help="Comma-separated list of entries for the plot legend"
    )
    parser.add_argument(
        "--type",
        choices=["whisker", "histogram", "histogram-after-dump"],
        help="Creates a histogram with word count of \
        (dump of ) the model on y axis and the time on x axis \
        for each file.",
    )
    parser.add_argument("-o", "--output", help="Save image to the given filename.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    periscope_results = periscope_result.results_from_file(args.file)
    main(periscope_results, args)
