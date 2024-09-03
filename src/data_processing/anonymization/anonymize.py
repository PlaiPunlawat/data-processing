import re
from pythainlp.tag.named_entity import NER

# prepare params for blinding data
NER_CORPUS = "thainer"
PERSON_SUB = "<person>"
ORG_SUB = "<org>"
ID_SUB = "<id no.>"
BLANK = ""
NUMBER_SUB = "<phone_number>"
EMAIL_SUB = "<email>"
THAI_ID_SUB = "<id no.>"

def anonymize(src_text, ner_corpus=NER_CORPUS):
    # declare regex pattern
    PERSON_TAG = re.compile(r'\(*<PERSON>.*?</PERSON>\)*')
    ORG_TAG = re.compile(r'\(*<ORG>.*?</ORG>\)*')
    OTHERS_TAG = re.compile(
        r'<(?!\/?(?:'+re.escape(PERSON_SUB[1:-1])+r')\b)[^>]*>')
    ID_PATTERN = re.compile(
        r'\b\d{13}\b|\b\d-\d{4}-\d{5}-\d{2}-\d\b|\b\d\s\d{4}\s\d{5}\s\d{2}\s\d\b')
    NUMBER_PATTERN = re.compile(
        r'\b\d{10}\b|\b\d-\d{2}-\d{3}-\d{4}-\d\b|\b\d-\d{3}-\d{3}-\d{4}-\d\b|\b\d\s\d{2}\s\d{3}\s\d{4}\s\d\b|\b\d\s\d{3}\s\d{3}\s\d{4}\s\d\b')
    EMAIL_PATTERN = re.compile(
        "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])")
    THAI_ID_PATTERN = re.compile(
        r"[0–9]-[0–9]{4}-[0–9]{5}-[0–9]{2}-[0–9]")

    # create NER tag
    ner = NER(ner_corpus)
    result = ner.tag(src_text, tag=True, pos=True)

    # # removed by NER tag
    result = PERSON_TAG.sub(PERSON_SUB, result)
    result = ORG_TAG.sub(ORG_SUB, result)
    result = OTHERS_TAG.sub(BLANK, result)
    result = ID_PATTERN.sub(ID_SUB, result)
    result = NUMBER_PATTERN.sub(NUMBER_SUB, result)
    result = EMAIL_PATTERN.sub(EMAIL_SUB, result)
    result = THAI_ID_PATTERN.sub(THAI_ID_SUB, result)

    return result
