import argparse
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd

from collections import OrderedDict
from datetime import timedelta, date




FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger()

def plot_multiple(data_frames):
    # TODO currently not very useful, as the 2,2 has to be recalculated
    # define number of rows and columns for subplots
    nrow = 2
    ncol = 2
    # make a list of all dataframes
    provinces = [x for x in data_frames.keys()]
    fig, axes = plt.subplots(nrow, ncol, sharey=True)
    fig.subplots_adjust(bottom=0.2)
    # plot counter
    count = 0
    for r in range(nrow):
        if count == len(provinces):
            break
        for c in range(ncol):
            if count == len(provinces):
                break
            print(r, c, provinces[count])
            data_frames[provinces[count]].plot(
                ax=axes[r, c],
                x="data",
                y="totale_casi",
                kind="bar")
            data_frames[provinces[count]].plot(
                ax=axes[r, c],
                x='data',
                y="nuovi",
                kind='bar',
                color="C2",
                title = provinces[r + c]
            )


            count += 1
    for ax in fig.get_axes():
        ax.label_outer()
        ax.set_yscale('log')

    plt.show()


def plot(df, title, bar=True):
    if bar:
        plot_bar(df, title)
    else:
        plot_lines(df, title)

def plot_bar(df, title):
    fig, axs = plt.subplots(4, sharex=True,  figsize=(4,4))
    # fig.suptitle("x")

    # F
    axs[0].set_ylim([20, 64])
    axs[0].set_ylabel('F$_1$')
    axs[0].set_alpha(0.4)
    axs[0].tick_params('y', )

    # P
    axs[1].set_ylim([28, 100])
    axs[1].set_ylabel('Prec')
    axs[1].set_alpha(0.4)
    axs[1].tick_params('y', )

    # R
    axs[2].set_ylim([12, 100])
    axs[2].set_ylabel('Rec')
    axs[2].set_alpha(0.4)
    axs[2].tick_params('y', )

    # chars
    # for i in range(1, 3):
    # # setting the ranges
    #     axs[i].set_ylim([15, 100])
    #     axs[i].set_ylabel(ylabels[i])
    #     axs[i].set_alpha(0.4)
    #     axs[i].tick_params('y', )

    axs[3].set_xlim([0, 8])
    axs[3].set_ylim([5, 133])
    axs[3].set_ylabel("chars")
    axs[3].set_alpha(0.4)

    df.plot.bar(x="top n", y="F", ax=axs[0], rot=90, title=title, width=0.7, legend=None)
    for i in axs[0].patches:
        axs[0].text(i.get_x(), i.get_height() + .3, \
                str(round((i.get_height()), 2)), fontsize=9,
            color='black')

    # axs[2].set_xticks([0, 5, 10, 15, 20])
    df.plot.bar(x='top n', y="P", ax=axs[1], color="C2", width=0.7, legend=None)
    for i in axs[1].patches:
        axs[1].text(i.get_x(), i.get_height() + .5, \
                str(round((i.get_height()), 2)), fontsize=9,
            color='black')

    df.plot.bar(x='top n', y="R",  ax=axs[2], color="C3", rot=90, width=0.7, legend=None)
    for i in axs[2].patches:
        axs[2].text(i.get_x(), i.get_height() + .5, \
                str(round((i.get_height()), 2)), fontsize=9,
            color='black')

    # mirar por que esta desplazado
    df.plot.bar(x='top n', y="chars",  ax=axs[3], width=0.7, color="C4",  legend=None)
    for i in axs[3].patches:
        axs[3].text(i.get_x(), i.get_height() + .5, \
                "{}k".format(int(i.get_height())), fontsize=9,
            color='black')


    axs[3].tick_params(axis="x", labelsize=9)

    plt.tight_layout(pad=0.2, w_pad=0.5, h_pad=1.0)
    plt.xticks(rotation=0)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
    plt.savefig("plot_{}.png".format(title), format="png")
    plt.show()
    plt.close()


def plot_lines(df, title):
    fig, axs = plt.subplots(4, sharex=True,  figsize=(4,4))
    # fig.suptitle("x")

    ylabels = ['F$_1$', 'Prec', "Rec"]

    axs[0].set_ylim([0, 64])
    axs[0].set_ylabel(ylabels[0])
    axs[0].set_alpha(0.4)
    axs[0].tick_params('y', )


    for i in range(1, 3):
    # setting the ranges
        axs[i].set_ylim([0, 100])
        axs[i].set_ylabel(ylabels[i])
        axs[i].set_alpha(0.4)
        axs[i].tick_params('y', )

    axs[3].set_xlim([0, 9])
    axs[3].set_ylim([0, 153])
    axs[3].set_ylabel("chars")
    axs[3].set_alpha(0.4)

    df.plot.line(x="top n", y="F", ax=axs[0], rot=90, title=title, legend=None)
    df.plot.scatter(x='top n', y="F", ax=axs[0], legend=None)
    for i, v in enumerate(df.F):
        axs[0].text(i+1, v + 5, "%d" % v, ha="center")

    # axs[2].set_xticks([0, 5, 10, 15, 20])
    df.plot.line(x='top n', y="P", ax=axs[1], color="C2", legend=None)
    df.plot.scatter(x='top n', y="P", ax=axs[1], color="C2", legend=None)
    for i, v in enumerate(df.P):
        axs[1].text(i+1, v + 10, "%d" % v, ha="center")

    df.plot.line(x='top n', y="R",  ax=axs[2], color="C3", rot=90, legend=None)
    df.plot.scatter(x='top n', y="R", ax=axs[2], color="C3", legend=None)
    for i, v in enumerate(df.R):
        axs[2].text(i+1, v + 10, "%d" % v, ha="center")

    df.plot.line(x='top n', y="chars",  ax=axs[3], color="C4",  legend=None)
    df.plot.scatter(x='top n', y="chars", ax=axs[3], color="C4", legend=None)
    for i, v in enumerate(df.chars):
        axs[3].text(i+1, v + 10, "%dk" % v, ha="center")

    # axs[3].set_xticklabels(df["top n"])


    # axs[3].tick_params(axis="x", labelsize=9)
    axs[3].set_xticks(ticks=[1,2,3,4,5,6,7,8])
    plt.tight_layout(pad=0.2, w_pad=0.5, h_pad=1.0)
    # plt.xticks(rotation=0)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
    plt.savefig("plot_{}.png".format(title), format="png")
    plt.show()
    plt.close()


def main(param):
    input = param['input']
    title = param['title']
    logger.info("Processing data for %s ", input)

    df = pd.read_csv(input, sep="\t")
    print(df)

    # print(data_frames[province])
    plot(df, title, bar=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest='input', required=True,
                       help="TSV input file with number, F, P and R (and to add number of chars)")

    parser.add_argument("-t", "--title", dest='title', required=True,
                        help="Title for the plot")

    arguments = parser.parse_args()

    param = OrderedDict()
    param['input'] = arguments.input
    param['title'] = arguments.title
    main(param)