from bs4 import BeautifulSoup as bs
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import rapidjson as rj

download("stopwords")
download("punkt")


def sanitize(raw):
    parsed = bs(raw, "html.parser")
    paragraphs = parsed.find_all("p")
    sanitized = ""
    for p in paragraphs:
        sanitized += p.text
    return sanitized


def get_title(raw):
    parsed = bs(raw, "html.parser")
    return parsed.find("title").text


def determine_word_frequency(content):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(content)
    stemmer = PorterStemmer()
    frequency_table = dict()
    for word in words:
        word = stemmer.stem(word)
        if word in stop_words:
            continue
        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1
    return frequency_table


def generate_highlights(content, frequency_table, num_highlights=1):
    sentences = sent_tokenize(content)

    sentence_scores = {}
    for sentence in sentences:
        sentence_key = sentence[:10]
        sentence_word_count = 0
        for word in frequency_table:
            if word in sentence.lower():
                word_score = frequency_table[word]
                sentence_word_count += 1
                if sentence_key in sentence_scores:
                    sentence_scores[sentence_key] += word_score
                else:
                    sentence_scores[sentence_key] = word_score

        sentence_scores[sentence_key] = sentence_scores[sentence_key] / sentence_word_count

    score_sum = 0
    for entry in sentence_scores:
        score_sum += sentence_scores[entry]

    average_score = score_sum / len(sentence_scores)

    highlight_counter = 0
    content_highlights = []
    min_score_threshold = 1.5*average_score

    for sentence in sentences:
        sentence_key = sentence[:10]
        if sentence_key in sentence_scores and sentence_scores[sentence_key] >= min_score_threshold:
            content_highlights.append(sentence)
            highlight_counter += 1

            if highlight_counter == num_highlights:
                break

    return rj.dumps(content_highlights)



