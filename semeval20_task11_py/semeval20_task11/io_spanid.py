import logging
import numpy as np
import pandas as pd

# File article820791520.txt is the longest one, with 12596 chars. We use the current value because team Fragarach has that value for span
# 781672902       16552   16568
MAXIMUM_LENGTH = 16568

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

def vectors_to_file(df, output):
    """
    Reads the Boolean vectors and stores them into a tsv file.
    :param df:
            Pandas dataframe with [doc_id, snippet_start, snippet_end]
    :param output: path to the output file
    :return: None
    """

    df.to_csv(output, sep='\t', header=False, index=False)
    logger.info("Snippets written to %s", output)


# vectors = file_to_vectors(ONE_PARTICIPANT_FILE)
