from bs4 import BeautifulSoup as bs
from string import punctuation
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import rapidjson as rj
import math

from bookworm import database

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


def determine_word_scores():
    stop_words = set(stopwords.words("english") + list(punctuation))
    stemmer = PorterStemmer()

    scores = {}
    corpus = []

    with database.con.cursor() as cur:
        query = "select id, sanitized_data from bookmarks"
        cur.execute(query)
        for row in cur.fetchall():
            corpus.append({"bookmark_id": row[0], "content": row[1]})

    num_documents = len(corpus)

    for x in corpus:
        bookmark_id = x["bookmark_id"]
        content = x["content"].tobytes().decode('utf-8')

        words = word_tokenize(content)
        frequency_table = {}
        for word in words:
            stemmed_word = stemmer.stem(word)
            if stemmed_word in stop_words:
                continue
            if stemmed_word in frequency_table:
                frequency_table[stemmed_word][1] += 1
            else:
                frequency_table[stemmed_word] = [word, 1]

        df_scores = {k: 1 for k in frequency_table.keys()}
        with database.con.cursor() as cur:
            query = cur.mogrify("""select count(distinct bookmark_id), stem from keywords
                                   where stem in %s 
                                       and bookmark_id != {}
                                   group by stem
            """.format(bookmark_id), (tuple(frequency_table.keys()),))
            cur.execute(query)
            for row in cur.fetchall():
                df_scores[row[1]] += int(row[0])

        scores[bookmark_id] = []

        for stem, (word, count) in frequency_table.items():
            tf = count / float(len(words))
            idf = math.log10(num_documents / (float(df_scores[stem]) + 1))
            scores[bookmark_id].append({
                "stem": stem,
                "word": word,
                "count": count,
                "tf_idf_score": tf*idf
            })

    return scores


def generate_highlights(content, frequency_table, num_highlights=3):
    sentences = sent_tokenize(content)

    sentence_scores = {}
    for sentence in sentences:
        sentence_key = sentence[:10]
        sentence_word_count = 0
        for word, score in frequency_table.items():
            if word in sentence.lower():
                word_score = score
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


def word_stemmer(text):
    words = word_tokenize(text)
    stemmer = PorterStemmer()
    stemmed_words = []
    for word in words:
        stemmed_words.append(stemmer.stem(word))

    return stemmed_words


def get_matching_sentences(text, search_term):
    keywords = word_tokenize(search_term)
    sentences = sent_tokenize(text)
    matching_sentences = []
    match_count = 0
    for s in sentences:
        for w in keywords:
            if w.lower() in s.lower():
                if s not in matching_sentences:
                    matching_sentences.append(s)
                    match_count += 1
        if match_count >= 3:
            break
    return matching_sentences

