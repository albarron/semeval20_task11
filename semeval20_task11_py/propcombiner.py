import logging
import numpy as np
import pandas as pd
import os

from semeval20_task11 import io_spanid

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


ONE_PARTICIPANT_FILE = "/Users/albarron/publications/semeval20_propaganda/data/submission/teams/Hitachi/test_si_Hitachi___2020-March-2__4_11_13.txt"

SI_SUBMISSIONS_PATH = "submissions_test_si"

TOP = 1

SI_RANKING_IDS = [
    "Hitachi",
    "ApplicaAI",
    "aschern",
    "LTIatCMU",
   "UPB",
    # "Fragarach",  # This team has one annotation longer than the current limit
    "NoPropaganda",
    "CyberWallE",
    "Transformers",
    "SWEAT",
    "YNUtaoxin",
    "DREAM",
    "newsSweeper",
    "PsuedoProp",
    "Solomon",
    # "YNUHPCC", # This team has one annotation longer than the current limit
    "NLFIIT",
    "PALI",
    "UESTCICSA",
    "TTUI",
    "BPGC",
    "DoNotDistribute",
    "UTMNandOCAS",
    "Entropy",
    "syrapropa",
    "SkoltechNLP",
    "NTUAAILS",
    "UAIC1860",
    "CCNI",
    "NCCU-SMRG",
    "3218IR",
    "WMD",
    "LS",
    "HunAlize",
    "YOLO",
    "Baseline",
    "Murgila",
    "TakeLab",
    "atulcst",
    "AAA",
    "CUNLP",
    "IIITD",
    "UoB",
    "UOfBirmingham",
    "SocCogCom",
    "Inno",
    "Raghavan",
    "California",
    ]

SI_FILES_IDS = [
    813452859,
    813494037,
    813547724,
    813552066,
    813601978,
    813602345,
    813603860,
    813623212,
    813714967,
    813949697,
    813953273,
    813953435,
    813992175,
    814251296,
    814371058,
    814403543,
    814403783,
    814403875,
    814404002,
    814427361,
    814435435,
    814630609,
    814777937,
    815412286,
    815858385,
    816460196,
    816720060,
    817147979,
    817176202,
    817190270,
    817408115,
    817449755,
    818141325,
    820419869,
    820791520,
    821040551,
    821744708,
    822220578,
    822295249,
    822942601,
    824256050,
    824350729,
    824658990,
    824684605,
    828866387,
    829267754,
    829815104,
    830153674,
    830274102,
    830359136,
    830359423,
    830821478,
    832269185,
    832918490,
    832920387,
    832926076,
    832931332,
    832933796,
    832934428,
    832940138,
    832941978,
    832947554,
    832947600,
    832947852,
    832948083,
    832956618,
    832959523,
    832971448,
    832984694,
    833013834,
    833018464,
    833021113,
    833024133,
    833024696,
    833028146,
    833028680,
    833028932,
    833032366,
    833032367,
    833036176,
    833036489,
    833039623,
    833040400,
    833041409,
    833042063,
    833050243,
    833052347,
    833053628,
    833053676,
    833067493
]

def file_from_team(team):
    path = os.path.join(SI_SUBMISSIONS_PATH, "si_" + team + ".tsv")
    return path

def merge_vectors(vectors, wanted_teams):
    merged = {}

    for file_id in SI_FILES_IDS:
        merged[file_id] = np.zeros(io_spanid.MAXIMUM_LENGTH, dtype=int)
        for team in wanted_teams:
            try:
                merged[file_id] += vectors[team][file_id]
            except:
                logging.debug("%s lacks an input for %i", team, file_id)
        # relevant = [vector[file_id] for vector in ]
        # vector = vectors
        # None
    return merged
        # merged[file_id] =

def compute_union(merged_vectors):
    # TODO check that this is working well
    boolean_vectors = {}
    df = pd.DataFrame(columns=[
        0,  # document id
        1,  # span beginning (incl)
        2  # span ending (excl)
    ])
    for file_id in SI_FILES_IDS:
        try:
            positive_tokens = np.where(merged_vectors[file_id] > 0)
            boolean_vectors[file_id] = merged_vectors[file_id] > 0
            df = df.append(positives_to_ranges(file_id, positive_tokens))
        except:
            logging.debug("No vector for $s exists", file_id)    # should never be exectuted
    print(df)
    print(df.ndim)
    return df

def positives_to_ranges(file_id, vector_of_positives):
    """
    Takes the file_id and the vector
    :param file_id:
                unique file identifier
    :param vector_of_positives:
                A vector which values represent the indexes where
                a character belongs to the positive class.
    :return:
                Pandas dataframe with columns file_id, range_start, range_end.
                As usual, the start is inclusive, whereas the end is exclusive.
    """
    into = False    # whether I am inside of an instance
    ranges = []
    # current = vector_of_positives[0][0]
    for value in np.nditer(vector_of_positives):
        new = int(value)
        if not into:
            # Beginning of the process. Get the starting position for the first snippet
            snippet_start = new
            into = True

        elif new - current == 1:
            # Nothing to do. Still in the same snippet
            pass

        else:
            # Record the new range and reset the starting snippet
            snippet_end = current
            # The end is exclusive (hence + 1)
            ranges.append([file_id, snippet_start, snippet_end+1])
            snippet_start = new

        # Update the current value
        current = new

    if snippet_start > snippet_end:   # TODO the conditional shouldn't be necessary. In all cases we should add a final one
        # End of the process. Add the final snippet
        ranges.append([file_id, snippet_start, new + 1])

    df = pd.DataFrame(ranges)
    # print(df)
    return df
    # TODO add the test that giving only one element should result in an identical file
    # (this has been checked manually, by setting TOP = 1)


def compute_inter(merged_vectors):
    # TODO check that this is working well
    boolean_vectors = {}
    for file_id in SI_FILES_IDS:
        try:
            boolean_vectors[file_id] = merged_vectors[file_id] == TOP
        except:
            logging.debug("No vector for $s exists", file_id)    # should never be exectuted
    return boolean_vectors

def compute_voting(merged_vectors):
    threshold = round(TOP * 0.6)
    # TODO check that this is working well
    boolean_vectors = {}
    for file_id in SI_FILES_IDS:
        try:
            boolean_vectors[file_id] = merged_vectors[file_id] >= threshold
        except:
            logging.info("No vector for $s exists", file_id)    # should never be exectuted
    return boolean_vectors

def get_output_name(operation):
    return str.format("si_%s_top_%s.tsv", (operation, TOP))

wanted_teams = SI_RANKING_IDS[:TOP]
all_vectors= {}

for team in wanted_teams:
    # print(file_from_team(SI_RANKING_IDS[i]))
    # TODO apply a filter to identify final predictions -> check that this works
    # TODO return to the submission format
    all_vectors[team] = io_spanid.file_to_vectors(file_from_team(team))

merged_vectors = merge_vectors(all_vectors, wanted_teams)

df_union = compute_union(merged_vectors)
# inter_vectors = compute_inter(merged_vectors)
# voting_vectors = compute_voting(merged_vectors)

io_spanid.vectors_to_file(df_union, get_output_name("union"))
# io_spanid.vectors_to_file(inter_vectors, get_output_name("intersection"))
# io_spanid.vectors_to_file(voting_vectors, get_output_name("voting"))
print(len(all_vectors["Hitachi"]))

