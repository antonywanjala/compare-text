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

    def set_writer(self):
        self.writer = WriterMaker()

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

    def initialize_results(self):
        self.results = []

    def analyze(self):
        self.initialize_results()

        for n in range(1, self.get_max_order() + 1):
            with open(self.get_source_file(), 'r', encoding='utf-8') as f:
                source_text = f.read()

            with open(self.get_response_file(), 'r', encoding='utf-8') as f:
                response_text = f.read()

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
                    ngram_text = " ".join(ngram)

                    n_gram_text_remover = NonAlphaNumericCharacterRemoverMaker()
                    n_gram_text_remover.set_initial_string(ngram_text)
                    n_gram_text_remover.remove()

                    cleaned_ngram = n_gram_text_remover.get_final_string()

                    # Find the original n-gram in each text
                    source_index = source_ngrams.index(ngram) if ngram in source_ngrams else None
                    response_index = response_ngrams.index(ngram) if ngram in response_ngrams else None

                    self.results.append({
                        "n-gram order": n,
                        "n-gram": cleaned_ngram,
                        "original n-gram in piece 1": " ".join(
                            source_ngrams[source_index]) if source_index is not None else "",
                        "original n-gram in piece 2": " ".join(
                            response_ngrams[response_index]) if response_index is not None else "",
                        "frequency in piece 1": source_ngrams.count(ngram),
                        "frequency in piece 2": response_ngrams.count(ngram),
                        "frequency": frequency,
                        "appears in piece 1": ngram in source_ngrams,
                        "appears in piece 2": ngram in response_ngrams,
                        "Both": ngram in source_ngrams and ngram in response_ngrams
                    })
                    progress_bar.update(1)

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


class NonAlphaNumericCharacterRemoverMaker:
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

    def remove(self):
        self.set_final_string("")
        for char in self.get_initial_string():
            if char.isalnum() or char.isspace():
                self.final_string += char.lower()

if __name__ == "__main__":
    piece_one = "absolute\\path\\to\\first\\piece_one.txt"
    piece_two = "absolute\\path\\to\\first\\piece_two.txt"
    
    max_order = 10  # Adjust the maximum n-gram order as needed
    only_common = False  # Set to False to include all n-grams

    analyzer = AnalyzerMaker(piece_one, piece_two, max_order=max_order, only_common=only_common)
    analyzer.set_writer()
    analyzer.analyze()

    analyzer.set_writer_output_path("absolute\\path\\to\\output_\\" + str(analyzer.get_start_time()) + ".csv")

    analyzer.get_writer().write()
