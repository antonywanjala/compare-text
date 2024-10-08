import pandas as pd
import nltk
import time
from collections import Counter
from tqdm import tqdm


class AnalyzerMaker:
    def __init__(self, source_file, response_file, max_order=5, only_common=True):
        self.start_time = time.time()

        self.source_file = source_file
        self.response_file = response_file

        self.max_order = max_order

        self.only_common = only_common

        self.results = None
        self.writer = None

        self.source_file_remover = None
        self.response_file_remover = None

    def get_writer(self):
        return self.writer

    def get_results(self):
        return self.results

    def get_start_time(self):
        return self.start_time

    def get_source_file(self):
        return self.source_file

    def get_response_file(self):
        return self.response_file

    def get_max_order(self):
        return self.max_order

    def get_only_common(self):
        return self.only_common

    def get_source_file_remover_final_string(self):
        return self.source_file_remover.get_final_string()

    def get_response_file_remover_final_string(self):
        return self.response_file_remover.get_final_string()


    def set_writer(self):
        self.writer = WriterMaker()

    def set_source_file_remover(self):
        self.source_file_remover = NonAlphaNumericRemoverMaker()

    def set_response_file_remover(self):
        self.response_file_remover = NonAlphaNumericRemoverMaker()

    def set_results_dataframe(self, value):
        self.results_dataframe = pd.DataFrame(value)

    def set_writer_dataframe(self, value):
        self.writer.set_dataframe(value)

    def set_results(self, value):
        self.results = value

    def set_start_time(self, value):
        self.start_time = value

    def set_source_file(self, value):
        self.source_file = value

    def set_response_file(self, value):
        self.response_file = value

    def set_max_order(self, value):
        self.max_order = value

    def set_only_common(self, value):
        self.only_common = value

    def set_writer_output_path(self, value):
        self.writer.set_output_path(value)

    def remove_all_non_alphanumeric_from_source_file(self, value):
        self.source_file_remover.remove(value)

    def remove_all_non_alphanumeric_from_response_file(self, value):
        self.response_file_remover.remove(value)

    def initialize_results(self):
        self.results = []

    def analyze(self, switch=1):
        self.initialize_results()

        for n in range(1, self.get_max_order() + 1):
            with open(self.get_source_file(), 'r', encoding='utf-8') as f:
                source_text = f.read()

            with open(self.get_response_file(), 'r', encoding='utf-8') as f:
                response_text = f.read()

            if switch == 1:
                source_text = source_text.lower()
                response_text = response_text.lower()
                self.remove_all_non_alphanumeric_from_source_file(source_text)
                self.remove_all_non_alphanumeric_from_response_file(response_text)
                source_text = self.get_source_file_remover_final_string()
                response_text = self.get_response_file_remover_final_string()

            source_ngrams = list(nltk.ngrams(source_text.split(), n))
            response_ngrams = list(nltk.ngrams(response_text.split(), n))

            if self.get_only_common():
                common_ngrams = set(source_ngrams) & set(response_ngrams)
            else:
                common_ngrams = source_ngrams + response_ngrams

            ngram_frequencies = Counter(common_ngrams)

            # Calculate the total number of n-grams to process
            total_ngrams = len(ngram_frequencies)

            with tqdm(total=total_ngrams, desc=f"Analyzing n-grams (order {n})") as progress_bar:
                for ngram, frequency in ngram_frequencies.items():
                    self.results.append({
                        "n-gram order": n,
                        "n-gram": " ".join(ngram),
                        "frequency": frequency,
                        "appears in piece 1": ngram in source_ngrams,
                        "appears in piece 2": ngram in response_ngrams,
                        "Both": ngram in source_ngrams and ngram in response_ngrams
                    })
                    progress_bar.update(1)
        # print('results=')
        # print(self.get_results())

        self.set_writer_dataframe(self.get_results())


class WriterMaker:
    def __init__(self):
        self.start_time = time.time()
        self.dataframe = None
        self.output_path = None

    def get_start_time(self):
        return self.start_time

    def get_dataframe(self):
        return self.dataframe

    def get_output_path(self):
        return self.output_path

    def set_dataframe(self, value):
        self.dataframe = pd.DataFrame(value)

    def set_output_path(self, value):
        self.output_path = value

    def write(self):
        self.get_dataframe().to_csv(self.get_output_path())
        print("OUTPUT PATH: " + str(self.get_output_path()))


class NonAlphaNumericRemoverMaker:
    def __init__(self):
        self.start_time = time.time()
        self.initial_string = None
        self.final_string = None

    def get_start_time(self):
        return self.start_time

    def get_final_string(self):
        return self.final_string

    def get_initial_string(self):
        return self.initial_string

    def set_initial_string(self, value):
        self.initial_string = value

    def set_final_string(self, value):
        self.final_string = value

    def remove(self, string):
        self.set_final_string(''.join(ch for ch in string if ch.isalnum() or ch.isspace()))

if __name__ == "__main__":
    piece_one = "absolute\\path\\to\\first\\piece_one.txt"
    piece_two = "absolute\\path\\to\\first\\piece_two.txt"

    max_order = 10  # Adjust the maximum n-gram order as needed
    only_common = False  # Set to False to include all n-grams

    analyzer = AnalyzerMaker(piece_one, piece_two, max_order=max_order, only_common=only_common)
    analyzer.set_writer()
    analyzer.set_source_file_remover()
    analyzer.set_response_file_remover()
    analyzer.analyze(switch=1)

    analyzer.set_writer_output_path("absolute\\path\\to\\output_" + "\\" + str(self.get_start_time()) + ".csv")

    analyzer.get_writer().write()