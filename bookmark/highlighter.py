"""
Reference: https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
"""
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests


def _create_dictionary_table(text_string) -> dict:
    try:
        stop_words = set(stopwords.words("english"))
    except LookupError:
        download("stopwords")
        stop_words = set(stopwords.words("english"))
    try:
        words = word_tokenize(text_string)
    except LookupError:
        download("punkt")
        words = word_tokenize(text_string)
    stem = PorterStemmer()
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1
    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    # algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> float:
    # calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold, max_sentences=0) -> str:
    sentence_counter = 0
    article_summary = ""

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= threshold:
            # article_summary += " " + sentence
            article_summary += sentence + "\n"
            sentence_counter += 1
            if sentence_counter == max_sentences:
                break

    return article_summary


def _run_article_summary(article) -> str:
    frequency_table = _create_dictionary_table(article)
    sentences = sent_tokenize(article)
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)
    avg_score = _calculate_average_score(sentence_scores)
    article_summary = _get_article_summary(sentences, sentence_scores, threshold=1.5*avg_score, max_sentences=5)
    return article_summary


def main():
    fetched_data = requests.get("https://en.wikipedia.org/wiki/20th_century")
    article_read = fetched_data.text
    article_parsed = BeautifulSoup(article_read, "html.parser")
    paragraphs = article_parsed.find_all("p")
    article_content = ""
    for p in paragraphs:
        article_content += p.text

    summary_results = _run_article_summary(article_content)
    print(summary_results)


if __name__ == "__main__":
    main()
