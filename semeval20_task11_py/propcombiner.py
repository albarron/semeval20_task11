import os
import logging

from semeval20_task11 import io_spanid

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


ONE_PARTICIPANT_FILE = "/Users/albarron/publications/semeval20_propaganda/data/submission/teams/Hitachi/test_si_Hitachi___2020-March-2__4_11_13.txt"

SI_SUBMISSIONS_PATH = "submissions_test_si"

TOP = 5

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


def file_from_team(team):
    path = os.path.join(SI_SUBMISSIONS_PATH, "si_" + team + ".tsv")
    return path

for i in range(TOP):
    # print(file_from_team(SI_RANKING_IDS[i]))
    # TODO align the vectors for each of the document IDs
    # TODO for each vector set, sum
    # TODO apply a filter to identify final predictions
    # TODO return to the submission format
    x = io_spanid.file_to_vectors(file_from_team(SI_RANKING_IDS[i]))



