import pandas as pd
import nltk
import time
from collections import Counter
from tqdm import tqdm

class NGramAnalyzerMaker:

    def __init__(self, source_file, response_file, max_order=5, only_common=True):
        self.start_time = time.time()
        self.source_file = source_file
        self.response_file = response_file
        self.max_order = max_order
        self.only_common = only_common
        self.results = None
        self.results_dataframe = None
        self.output_path = None

    def get_output_path(self):
        return self.output_path
    def get_results_dataframe(self):
        return self.results_dataframe

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
    def set_results_dataframe(self, value):
        self.results_dataframe = pd.DataFrame(value)

    def set_results(self, value):
        return self.results

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

    def set_output_path(self):
        self.output_path = "absolute\\path\\to\\output_" + "\\" + str(self.get_start_time()) + ".csv"

    def initialize_results(self):
        self.results = []

    def remove_asterisks_and_hashtags(self, text):
        # Replace asterisks with empty strings
        text = text.replace('*', '')

        # Replace hashtags with empty strings
        text = text.replace('#', '')

        return text

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
                source_text = self.remove_asterisks_and_hashtags(source_text)
                response_text = self.remove_asterisks_and_hashtags(response_text)

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

        self.set_results_dataframe(self.get_results())

    def output(self):
        self.get_results_dataframe().to_csv(self.get_output_path())

if __name__ == "__main__":
    piece_one = "absolute\\path\\to\\first\\piece_one.txt"
    piece_two = "absolute\\path\\to\\first\\piece_two.txt"

    max_order = 10
    only_common = False  # Set to False to include all n-grams

    analyzer = NGramAnalyzerMaker(piece_one, piece_two, max_order, only_common)

    analyzer.analyze()
    analyzer.set_output_path()
    analyzer.output()
