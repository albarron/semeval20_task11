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

DATA_FILE = "data/si_eval_all.tsv"


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


def plot(df, bar=True):
    if bar:
        plot_bar(df)
    else:
        plot_lines(df)

def plot_bar(df):
    fig, axs = plt.subplots(4, 3, sharex=True,  figsize=(11, 4))
    # fig.suptitle("x")

    plt.tight_layout(pad=1.8)
    plt.subplots_adjust(hspace=0.45, wspace=0.05)
    font = {'family': 'normal',
            # 'weight': 'bold',
            'size': 9}

    plt.rc('font', **font)
    TITLES = ['union', 'intersection', 'majority voting']
    YS = ['F$_1$', 'Prec', 'Rec', 'chars']
    for r in range(4):
        # axs[0][r].set_ylim([0, 85])
        axs[r][0].set_ylabel(YS[r])
        axs[r][0].set_alpha(0.4)
        # axs[r][0].tick_params('y', which="major")

    for c in range(3):
        # Ranges
        axs[0][c].set_ylim([20, 64])    # F
        axs[1][c].set_ylim([28, 100])   # Prec
        axs[2][c].set_ylim([12, 100])   # Rec
        axs[3][c].set_xlim([0, 8])      # chars
        axs[3][c].set_ylim([5, 135])    # chars
        axs[1][1].tick_params('y', which="major")


        cols_pref = ["F_", "P_", "R_", "chars_", "chars_"]

        if c == 0:  # union
            cols = ["{}u".format(col) for col in cols_pref]
        elif c==1:  # intersection
            cols = ["{}i".format(col) for col in cols_pref]
        else:       # majority voting
            cols = ["{}v".format(col) for col in cols_pref]


        df.plot.bar(x="top n", y=cols[0], ax=axs[0][c], rot=90, title=TITLES[c], width=0.7, legend=None)
        for i in axs[0][c].patches:
            axs[0][c].text(i.get_x(), i.get_height() + 1, \
                get_label(i.get_height()),
                color='black')

        # axs[2].set_xticks([0, 5, 10, 15, 20])
        df.plot.bar(x='top n', y=cols[1], ax=axs[1][c], color="C2", width=0.7, legend=None)
        for i in axs[1][c].patches:
            axs[1][c].text(i.get_x(), i.get_height() + 1, \
                get_label(i.get_height()),
                color='black')

        df.plot.bar(x='top n', y=cols[2],  ax=axs[2][c], color="C3", rot=90, width=0.7, legend=None)
        for i in axs[2][c].patches:
            axs[2][c].text(i.get_x(), i.get_height() + 1, \
                get_label(i.get_height()),
                color='black')

        # mirar por que esta desplazado
        df.plot.bar(x='top n', y=cols[3],  ax=axs[3][c], width=0.7, color="C4",  legend=None)
        for i in axs[3][c].patches:
            axs[3][c].text(i.get_x(), i.get_height() + 3, \
                " {}k".format(int(i.get_height())),
                color='black')

        if c != 0:
            for r in range(4):
                axs[r][c].tick_params(axis='y',  # changes apply to the x-axis
                                  # which='both',  # both major and minor ticks are affected
                                  left='on',
                                  right='off',
                                  labelsize=1,
                                  labelcolor="white")

        axs[3][c].tick_params(axis="x", labelsize=9, rotation=0)

    #######

    # plt.tight_layout(pad=0.2, w_pad=0.5, h_pad=1.0)
    # plt.xticks(rotation=0)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
    plt.savefig("si_plot_{}.png".format("all"), format="png")
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

def get_label(k):
    label = str(round(k, 2))
    if len(label.split(".")[1]) < 2:
        label += "0"
    if len(label.split(".")[0]) < 2:
        label = "  " + label
    return label

def main(param):
    title = param['title']
    logger.info("Processing data for %s ", input)

    df = pd.read_csv(DATA_FILE, sep="\t")
    print(df)

    # print(data_frames[province])
    plot(df, bar=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input", dest='input', required=False,
    #                    help="TSV input file with number, F, P and R (and to add number of chars)")

    parser.add_argument("-t", "--title", dest='title', required=True,
                        help="Title for the plot")

    arguments = parser.parse_args()

    param = OrderedDict()

    # param['input'] = arguments.input
    param['title'] = arguments.title
    main(param)