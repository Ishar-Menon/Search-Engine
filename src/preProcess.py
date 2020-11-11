import re
from collections import defaultdict
from string import punctuation
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from contractions import contractions_dict
from autocorrect import spell


def preProcess(text, isQuery=False):
    """ 
    Performs pre processing on the given query

    Arguments:
    text - The text data that is to be preprocessed
    isQuery - Indicative of whether the text is a query

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

    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    text = expanded_text

    text = strip_punctuation(text)
    tokens = word_tokenize(text)

    stopword = stopwords.words('english')
    # print(sorted(stopword))
    tokens_removed_stopwords = []
    tokens_with_pos = []
    pos = 0

    for token in tokens:
        if token in stopword:
            pos += 1
            continue

        tokens_removed_stopwords.append(token)
        if not isQuery:
            tokens_with_pos.append((token, pos))

        pos += 1

    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    lemmatized_tokens = []
    lemma_function = WordNetLemmatizer()
    for token, tag in pos_tag(tokens_removed_stopwords):
        lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
        lemmatized_tokens.append(lemma)

    if isQuery:
        return lemmatized_tokens

    for idx in range(len(lemmatized_tokens)):
        lemmatized_tokens[idx] = (
            lemmatized_tokens[idx], tokens_with_pos[idx][1])

    return lemmatized_tokens
