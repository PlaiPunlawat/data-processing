import re
# from pythainlp.tag.named_entity import NER
from pythainlp.tag import NER

from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from pythainlp.tokenize import word_tokenize  # pip install pythainlp
import torch
import argparse

# prepare params for blinding data
NER_CORPUS = "thainer"
PERSON_SUB = "<person>"
ORG_SUB = "<org>"
ID_SUB = "<id no.>"
BLANK = ""
NUMBER_SUB = "<phone_number>"
EMAIL_SUB = "<email>"
THAI_ID_SUB = "<id no.>"
NER_TAG_TRANSFORMER_MODEL = None


def anonymize(src_text, ner_corpus=NER_CORPUS, NER_TAG=False):
    
    # Declare regex patterns for sensitive information
    # ประกาศรูปแบบ regex สำหรับข้อมูลที่เป็นความลับ
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

    # If transformer-based NER tagging is enabled, use that
    # ถ้าใช้ NER ที่ใช้โมเดล transformer ให้เรียกใช้ฟังก์ชันแท็ก NER แบบ transformer
    if NER_TAG_TRANSFORMER_MODEL is not None or NER_TAG:
        print("-----NER_TAG")
        result = ner_tag_transformer(src_text, ner_corpus)
    else:
        print("-----Default")
        # Use default NER tagger
        # ใช้การแท็ก NER แบบทั่วไป
        ner = NER(ner_corpus)
        result = ner.tag(src_text, tag=True, pos=True)

    # Replace identified entities and sensitive information with placeholders
    # แทนที่เอนทิตีและข้อมูลที่เป็นความลับที่ระบุด้วยข้อมูลแทนที่
    result = PERSON_TAG.sub(PERSON_SUB, result)
    result = ORG_TAG.sub(ORG_SUB, result)
    result = OTHERS_TAG.sub(BLANK, result)
    result = ID_PATTERN.sub(ID_SUB, result)
    result = NUMBER_PATTERN.sub(NUMBER_SUB, result)
    result = EMAIL_PATTERN.sub(EMAIL_SUB, result)
    result = THAI_ID_PATTERN.sub(THAI_ID_SUB, result)

    # Return the anonymized text
    # ส่งคืนข้อความที่ปกปิดข้อมูลแล้ว
    return result

def ner_tag_transformer(sentence, ner_corpus=NER_TAG_TRANSFORMER_MODEL):
    # Load the pre-trained tokenizer and model from the specified corpus
    # โหลด tokenizer และโมเดลที่ฝึกมาแล้วจาก ner_corpus
    tokenizer = AutoTokenizer.from_pretrained(ner_corpus)
    model = AutoModelForTokenClassification.from_pretrained(ner_corpus)

    # Tokenize the input sentence while replacing spaces with a placeholder
    # ทำการแยกคำในประโยคและแทนที่ช่องว่างด้วย "<_>"
    cut = word_tokenize(sentence.replace(" ", "<_>"))
    inputs = tokenizer(cut, is_split_into_words=True, return_tensors="pt")

    # Extract input ids and attention mask
    # ดึงข้อมูล ids และ attention mask จาก input ที่เตรียมไว้
    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]

    # Pass inputs through the model (forward pass)
    # ส่ง input ผ่านโมเดลเพื่อคำนวณ logits
    outputs = model(ids, attention_mask=mask)
    logits = outputs[0]

    # Get the predicted token classes (NER labels)
    # คำนวณค่าการจำแนกประเภทเอนทิตีจาก logits
    predictions = torch.argmax(logits, dim=2)
    predicted_token_class = [model.config.id2label[t.item()] for t in predictions[0]]

    # Fix span errors in the NER output
    # ฟังก์ชันนี้แก้ไขข้อผิดพลาดของช่วงเอนทิตีในผลลัพธ์
    def fix_span_error(words, ner):
        _ner = ner
        _new_tag = []
        for i, j in zip(words, _ner):
            # Decode the tokens into human-readable text
            # แปลงคำที่ถูกแยกออกมาเป็นข้อความที่มนุษย์อ่านได้
            i = tokenizer.decode(i)
            if i.isspace() and j.startswith("B-"):
                j = "O"  # Correct labeling for space tokens
            if i == '' or i == '<s>' or i == '</s>':
                continue
            if i == "<_>":
                i = " "
            _new_tag.append((i, j))
        return _new_tag

    # Fix entity tagging for the sentence
    # แก้ไขแท็กเอนทิตีสำหรับประโยคที่จำแนกได้
    sent_ner = fix_span_error(inputs['input_ids'][0], predicted_token_class)

    # Build the final sentence with entity tags
    # สร้างประโยคสุดท้ายที่มีแท็กเอนทิตี
    temp = ""
    sent = ""
    for idx, (word, ner) in enumerate(sent_ner):
        if ner.startswith("B-") and temp != "":
            sent += "</" + temp + ">"
            temp = ner[2:]
            sent += "<" + temp + ">"
        elif ner.startswith("B-"):
            temp = ner[2:]
            sent += "<" + temp + ">"
        elif ner == "O" and temp != "":
            sent += "</" + temp + ">"
            temp = ""
        sent += word

        if idx == len(sent_ner) - 1 and temp != "":
            sent += "</" + temp + ">"

    # Return the sentence with the NER tags inserted
    # ส่งคืนประโยคที่มีการเพิ่มแท็กเอนทิตี
    return sent


def main():
    parser = argparse.ArgumentParser(description='Process anonymization')

    # Adding an argument to accept an string pattern
    parser.add_argument(
        '-ntt', '--ner_tag_transformer',
        nargs='+',
        type=str,
        required=False,
        help='Name of repo for NER tag transformer. Example: -ntt pythainlp/thainer-corpus-v2-base-model'
    )

    args = parser.parse_args()

    # Arg parse
    if args.ner_tag_transformer is not None:
        NER_TAG_TRANSFORMER_MODEL = args.ner_tag_transformer
    else:
        NER_TAG_TRANSFORMER_MODEL = None


if __name__ == "__main__":
    main()
