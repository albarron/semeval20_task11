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

TITLES= [
    "Overall",
    "Loaded language",
    "Name calling, labeling",
    "Repetition",
    "Exaggeration, minimisation",
    "Doubt",
    "Appeal to fear-prejudice",
    "Flag-waving",
    "Causal oversimplification",
    "Slogans",
    "Appeal to authority",
    "Black-and-white fallacy",
    "Thought-terminating clichés",
    "Whataboutism, straw men, red_herring",
    "Bandwagon, reductio ad hitlerum"
    ]

def plot(df, title, bar=True):
    if bar:
        plot_bar(df, title)
    else:
        plot_lines(df, title)

def plot_bar(df, file_title):
    fig, axs = plt.subplots(5, 3, sharex=True, figsize=(10, 8), )

    plt.tight_layout(pad=1.3)
    plt.subplots_adjust(hspace=0.45, wspace=0.05)
    font = {'family': 'normal',
            # 'weight': 'bold',
            'size': 9}

    plt.rc('font', **font)
    # fig.suptitle("x")
    for title in TITLES:
        df[title] = df[title]*100
    m = 0

    for i in range(5):
        for j in range(3):
            axs[i][j].set_ylim([0, 85])
            axs[i][j].set_title(TITLES[m])
            axs[i][j].set_alpha(0.4)
            axs[i][j].tick_params('y', )



            df.plot.bar(x="top n", y=TITLES[m], ax=axs[i][j], width=0.7, color=(0.2, 0.4, 0.6, 0.5), legend=None)

            if j != 0:
                axs[i][j].tick_params(axis='y',  # changes apply to the x-axis
                                      # which='both',  # both major and minor ticks are affected
                                      left='on',
                                      right='off',
                                      labelsize=1,
                                      labelcolor="white")
            # else:
            #     axs[i][j].set_ylabel("F$_1$")

            for k in axs[i][j].patches:

                label = str(round((k.get_height()), 2))
                if len(label.split(".")[1]) < 2:
                    label +="0"
                if len(label.split(".")[0]) < 2:
                    label = "  " + label
                axs[i][j].text(k.get_x()+0.8, 50, #k.get_height() - 20.9, \
                            label,
                            color='black', rotation=90, horizontalalignment='right')

            m+= 1

    for j in range(3):
        axs[4][j].tick_params('x', rotation=0)

        axs[4][j].set_xticklabels(
            ['1', '','','',
             '5', '','','','',
             '10','','','','',
             '15','','','','',
             '20','','','','',
             '25'])
    # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
    plt.savefig("tc_plot_{}.png".format(file_title.replace(" ", "_")), format="png")
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

    plot(df, title, bar=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest='input', required=True,
                       help="TSV input file with number and F overall and for each class")

    parser.add_argument("-t", "--title", dest='title', required=True,
                        help="Title for the plot")

    arguments = parser.parse_args()

    param = OrderedDict()
    param['input'] = arguments.input
    param['title'] = arguments.title
    main(param)