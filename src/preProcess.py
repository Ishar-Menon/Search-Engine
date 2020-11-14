import re
from collections import defaultdict
from string import punctuation
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from contractions import contractions_dict
from autocorrect import Speller


def preProcess(text, queryType=-1):
    """ 
    Performs pre processing on the given query

    Arguments:
    text - The text data that is to be preprocessed
    queryType - Indicative of whether the text is a query, or part of the corpora

    Returns:
    List of terms
    """
    def strip_punctuation(s):
        return ''.join(c for c in s if c not in punctuation)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contractions_dict.get(match) \
            if contractions_dict.get(match) \
            else contractions_dict.get(match.lower())
        expanded_contraction = expanded_contraction
        return expanded_contraction

    def lemmatize_tokens(tokens):
        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV

        lemma_function = WordNetLemmatizer()
        lemmatized_tokens = []
        for token, tag in pos_tag(tokens):
            lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
            lemmatized_tokens.append(lemma)

        return lemmatized_tokens

    metadata = defaultdict(int)
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    text = expanded_text

    text = text.lower()

    if queryType > 0:
        tokens = text.split()

        token_list = []

        otherIndex = 0
        for index,token in enumerate(tokens):
            if re.findall('/[0-9]+', token):
                metadata[(otherIndex - 1, otherIndex)] = int(tokens[index].lstrip('/'))
            else:
                otherIndex += 1
                token_list.append(token)

        for i in range(len(token_list)):
            if token_list[i][0] == '*':
                metadata[i] = 1
                token_list[i] = token_list[i].lstrip('*')
            elif token_list[i][-1] == '*':
                metadata[i] = 2
                token_list[i] = token_list[i].rstrip('*')

        lemmatized_tokens = lemmatize_tokens(token_list)
        return (lemmatized_tokens, metadata)

    text = strip_punctuation(text)
    tokens = word_tokenize(text)

    if queryType != -1:
        spell = Speller(lang='en')
        tokens = [spell(w) for w in tokens]

    stopword = stopwords.words('english')
    tokens_removed_stopwords = []
    tokens_with_pos = []
    pos = 0

    for token in tokens:
        if token in stopword:
            pos += 1
            continue

        tokens_removed_stopwords.append(token)
        if queryType == -1:
            tokens_with_pos.append((token, pos))

        pos += 1

    lemmatized_tokens = lemmatize_tokens(tokens_removed_stopwords)

    if queryType != -1:
        return (lemmatized_tokens, metadata)

    for idx in range(len(lemmatized_tokens)):
        lemmatized_tokens[idx] = (
            lemmatized_tokens[idx], tokens_with_pos[idx][1])

    return (lemmatized_tokens, metadata)
