import logging
import numpy as np
import os

from semeval20_task11 import io_spanid

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


ONE_PARTICIPANT_FILE = "/Users/albarron/publications/semeval20_propaganda/data/submission/teams/Hitachi/test_si_Hitachi___2020-March-2__4_11_13.txt"

SI_SUBMISSIONS_PATH = "submissions_test_si"

TOP = 2

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
                logging.info("%s lacks an input for %i", team, file_id)
        # relevant = [vector[file_id] for vector in ]
        # vector = vectors
        # None
    return merged
        # merged[file_id] =

def compute_union(merged_vectors):
    # TODO check that this is working well
    boolean_vectors = {}
    for file_id in SI_FILES_IDS:
        # try:
        boolean_vectors[file_id] = merged_vectors[file_id] > 0
        # except:
        #     logging.info("No vector for $s exists", file_id)    # should never be exectuted
    return boolean_vectors

def compute_inter(merged_vectors):
    # TODO check that this is working well
    boolean_vectors = {}
    for file_id in SI_FILES_IDS:
        # try:
        boolean_vectors[file_id] = merged_vectors[file_id] == TOP
        # except:
        #     logging.info("No vector for $s exists", file_id)    # should never be exectuted
    return boolean_vectors

def compute_voting(merged_vectors):
    threshold = round(TOP * 0.6)
    # TODO check that this is working well
    boolean_vectors = {}
    for file_id in SI_FILES_IDS:
        # try:
        boolean_vectors[file_id] = merged_vectors[file_id] >= threshold
        # except:
        #     logging.info("No vector for $s exists", file_id)    # should never be exectuted
    return boolean_vectors


wanted_teams = SI_RANKING_IDS[:TOP]
all_vectors= {}

for team in wanted_teams:
    # print(file_from_team(SI_RANKING_IDS[i]))
    # TODO apply a filter to identify final predictions -> check that this works
    # TODO return to the submission format
    all_vectors[team] = io_spanid.file_to_vectors(file_from_team(team))

merged_vectors = merge_vectors(all_vectors, wanted_teams)

union_vectors = compute_union(merged_vectors)
inter_vectors = compute_inter(merged_vectors)
voting_vectors = compute_voting(merged_vectors)


print(len(all_vectors["Hitachi"]))

