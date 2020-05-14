import logging
import numpy as np
import pandas as pd

# This is the length of file
# propaganda-corpus-creation/data-created-before-annotations/semeval2020-test-raw-articles/selected_articles_anafora_format/batch4/Brexit/article820791520/article820791520
# no file should be longer than this one (UNLESS SOMETHING IS WRONG) and
# hence we are going to create vectors of this size
MAXIMUM_LENGTH = 12596 # TODO there is at least one file with more. 12722 in si_Fragarach.tsv

ONE_PARTICIPANT_FILE = "/Users/albarron/publications/semeval20_propaganda/data/submission/teams/Hitachi/test_si_Hitachi___2020-March-2__4_11_13.txt"

GOLD_FILE = "/Users/albarron/projects/propaganda/propaganda-corpus-creation/data-created-after-annotations/semeval2020-remove-inconsistent-annotations/gold-test/test-task-SI.labels"

logger = logging.getLogger()

def file_to_vectors(input):
    """
    Extracts the annotations from a submission file and
    returns vectorial representations

    :param input: path to a tsv file with [id, start_span, end_span]
    :return: dictionary with id as key and a binary vector (1 where a span is covered)
    """
    logger.info("Reading document %s", input)
    df = pd.read_csv(input, header=None, sep="\t")
    grouped = df.groupby(0)
    my_vectors = {}
    for name, group in grouped:
        counter = 0
        vector = np.zeros(MAXIMUM_LENGTH, dtype=int)
        df2 = group

        for index, row in df2.iterrows():
            counter += row[2] - row[1]
            for i in range(row[1], row[2]):
                # print(i)
                vector[i] = 1

        my_vectors[name] = vector
        logger.debug("Propagandist characters for id %s: %i", name, sum(vector))
    # print(my_vectors)
    return my_vectors

def vectors_to_file(vectors, output):
    """
    Reads the Boolean vectors and stores them into a tsv file.
    :param vectors: Dictionary with {doc_id: Boolean vector}
    :param output: path to the output file
    :return: None
    """
    logger.info("Writing vectors to %s", output)
    # Convert the vector to dataframe
    spans = []
    # current = False

    for id, vector in vectors.items():
        print(len(vector))
        print(np.where(vector == True))
    #     for value in vector:
    #         print(value)

        exit()
        # Find out if we can get the boundaries; otherwise, I need a for


    df = pd.DataFrame(columns=[
        0,  # document id
        1,  # span beginning (incl)
        2   # span ending (excl)
        ])
    # dfObj = dfObj.append({'User_ID': 23, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True)

    # Save the dataframe into a tsv
    # pd.


# vectors = file_to_vectors(ONE_PARTICIPANT_FILE)
