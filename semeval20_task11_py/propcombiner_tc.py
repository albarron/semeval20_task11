import logging
import numpy as np
import pandas as pd
import os

from semeval20_task11 import io_techclass

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


ONE_PARTICIPANT_FILE = "/Users/albarron/publications/semeval20_propaganda/data/submission/teams/Hitachi/test_si_Hitachi___2020-March-2__4_11_13.txt"

TC_SUBMISSIONS_PATH = "submissions_test_tc"

TOP = 25

TC_RANKING_IDS = [
    "ApplicaAI",
    "aschern",
    "Hitachi",
    "Solomon",
    "newsSweeper",
    "NoPropaganda",
    "Inno",
    "CyberWallE",
    "PALI",
    "Duth",
    "DiSaster",
    "djichen",
    "SocCogCom",
    "TTUI",
    "JUST",
    "NLFIIT",
    "UMSIForeseer",
    "BPGC",
    "UPB",
    "syrapropa",
    "WMD",
    "YNUHPCC",
    "UESTCICSA",
    "DoNotDistribute",
    "NTUAAILS",
    "UAIC1860",
    "UNTLing",
    "HunAlize",
    # I am ignoring submissions Transformers and Entropy because the
    # order of the entries is different from the rest and they are
    # low in the ranking anyway (we wont do majority voting with them)
    # "Transformers",
    # "Entropy",
    "IJSE8"
    ]

# The order os that of the frequency of predictions
# on the test set. In that way, in case of tie the most
# frequent element is returned
TC_TECHNIQUES_TO_IDX = {
    "Loaded_Language":                  0,
    "Name_Calling,Labeling":            1,
    "Doubt":                            2,
    "Exaggeration,Minimisation":        3,
    "Appeal_to_fear-prejudice":         4,
    "Flag-Waving":                      5,
    "Repetition":                       6,
    "Causal_Oversimplification":        7,
    "Appeal_to_Authority":              8,
    "Slogans":                          9,
    "Black-and-White_Fallacy":          10,
    "Thought-terminating_Cliches":      11,
    "Whataboutism,Straw_Men,Red_Herring":12,
    "Bandwagon,Reductio_ad_hitlerum":   13
    }

TC_IDX_TO_TECHNIQUES = dict([reversed(i) for i in TC_TECHNIQUES_TO_IDX.items()])


def file_from_team(team):
    path = os.path.join(TC_SUBMISSIONS_PATH, "tc_" + team + ".tsv")
    return path


def count_predictions(all_predictions):
    """
    Counts the predictions by all desired teams into a matrix of counters:
    (instances x classes). That should be 1790x14
    :param all_predictions:
            list of lists with all the predictions. We assume they
            all stick to the same order
    :return:
            numpy matrix with the sum of the amount of
            classes predicted for each instance
    """
    instances = len(all_predictions[0])
    merged = np.zeros((instances, len(TC_TECHNIQUES_TO_IDX)), dtype=int)
    logging.info("Creating counting matrix of  %s instances times techniques", merged.shape)

    for team_predictions in all_predictions:
        for i in range(instances):
            merged[i][TC_TECHNIQUES_TO_IDX[team_predictions[i]]] +=1
    print(sum(merged))

    return merged


def compute_voting(counting_matrix):
    print(counting_matrix)
    # threshold = round(TOP * 0.5)
    predictions = []

    for i in range(len(counting_matrix)):
        print (counting_matrix[i])
        # print (counting_matrix[i].argmax())
        index = counting_matrix[i].argmax()
        # if we want to decide ties in a different way (now it's by
        # frequency, as argmax gets the first value and the classes
        # are ordered by frequency), we need an if/else here.
        decision = TC_IDX_TO_TECHNIQUES[index]
        predictions.append(decision)
        print("{}\t{}/{}".format(decision, counting_matrix[i][index], TOP))
    return predictions


# def positives_to_ranges(file_id, vector_of_positives):
#     """
#     Takes the file_id and the vector
#     :param file_id:
#                 unique file identifier
#     :param vector_of_positives:
#                 A vector which values represent the indexes where
#                 a character belongs to the positive class.
#     :return:
#                 Pandas dataframe with columns file_id, range_start, range_end.
#                 As usual, the start is inclusive, whereas the end is exclusive.
#     """
#     into = False    # whether I am inside of an instance
#     ranges = []
#     # current = vector_of_positives[0][0]
#     for value in np.nditer(vector_of_positives):
#         new = int(value)
#         if not into:
#             # Beginning of the process. Get the starting position for the first snippet
#             snippet_start = new
#             into = True
#
#         elif new - current == 1:
#             # Nothing to do. Still in the same snippet
#             pass
#
#         else:
#             # Record the new range and reset the starting snippet
#             snippet_end = current
#             # The end is exclusive (hence + 1)
#             ranges.append([file_id, snippet_start, snippet_end+1])
#             snippet_start = new
#
#         # Update the current value
#         current = new
#
#     # End of the process. Add the final snippet
#     ranges.append([file_id, snippet_start, new + 1])
#
#     df = pd.DataFrame(ranges)
#     # TODO add the test that giving only one element should result in an identical file
#     # (this has been checked manually, by setting TOP = 1, for many of the teams)
#     return df

def substitute_predictions(new_predictions, df):
    # print(df)
    # print(df.groupby(1).count())
    df[1] = new_predictions
    # print(df)
    # print(df.groupby(1).count())
    return df

def get_output_name(operation):
    return "tc_{}_top_{}.tsv".format(operation, TOP)

wanted_teams = TC_RANKING_IDS[:TOP]
all_vectors= []

for team in wanted_teams:
    # print(file_from_team(SI_RANKING_IDS[i]))
    all_vectors.append(io_techclass.file_to_vectors(file_from_team(team)))

# print(all_vectors)

counting_matrix = count_predictions(all_vectors)

# df_union = compute_union(merged_vectors)
# df_inter = compute_inter(merged_vectors)
voting = compute_voting(counting_matrix)

# TODO still need to catch the ids and add them to the output

# io_.vectors_to_file(df_union, get_output_name("union"))
# io_spanid.vectors_to_file(df_inter, get_output_name("intersection"))
io_techclass.vectors_to_file(
    substitute_predictions(voting, io_techclass.file_to_df(file_from_team(wanted_teams[0]))),
                           get_output_name("voting"))
# print(len(all_vectors["Hitachi"]))

