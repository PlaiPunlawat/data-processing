from datetime import datetime
import pandas as pd
from typing import List, Dict, Pattern
import re

# flake8: noqa:
from .words_pattern import (
    GAMBLE_RE,
    GAMBLE_THRESHOLD,
    FOOTBALL_RE,
    FOOTBALL_THRESHOLD,
    HOTEL_AD_RE,
    HOTEL_AD_THRESHOLD,
    SALE_URL_RE,
    SALE_URL_THERSHOLD,
    SALE_SKIP_RE,
    SALE_SKIP_THRESHOLD,
    SALE_RE,
    SALE_THRESHOLD,
    RENT_SKIP_RE,
    RENT_SKIP_THRESHOLD,
    RENT_RE,
    RENT_THRESHOLD,
    SCRIPT_RE,
    SCRIPT_THRESHOLD,
    GARBAGE_RE,
    GARBAGE_THRESHOLD
)

from .regex_pattern import (
    PAGE_RE,
    TOOLARGE_RE,
    TOOLARGE_THRESHOLD,
    NONECHAR_RE,
    NONECHAR_THRESHOLD,
    NONE_TONE_MARK_RE,
    NONE_TONE_MARK_THRESHOLD,
    JSON_RE,
    JSON_THRESHOLD,
    GHOST_RE,
    GHOST_THRESHOLD,
    HEX_RE,
    HEX_THRESHOLD,
    TOOLARGE_RE,
    NONECHAR_RE,
    NONE_TONE_MARK_RE,
    JSON_RE,
    EMBEDDED_SERVER_RE,
    U_RE,
    EMAIL_RE,
    URL_RE,
    MENU1_RE,
    MENU2_RE,
    MENU3_RE,
    MENU4_RE,
    SIDEBAR_RE,
    BLOCK_RE,
    HASHTAG_RE,
    MARKUP_RE,
    IFRAME_RE,
    IP_RE,
    TEL_RE,
    DATE1_RE,
    DATE2_RE,
    HTML_RE,
    REFINE1_RE,
    REFINE2_RE,
    REFINE3_RE,
    REFINE4_RE,
    REFINE5_RE,
    REFINE6_RE,
    REFINE7_RE,
    REFINE8_RE,
    REFINE9_RE,
    REFINE10_RE,
    REFINE11_RE,
    REFINE12_RE,
    REFINE13_RE,
    REFINE14_RE,

)

LIST_WORD_PATTERN = [
        { "KEY":"GAMBLE", "VALUE":{"PATTERN": GAMBLE_RE, "THRESHOLD": GAMBLE_THRESHOLD} },
        { "KEY":"FOOTBALL", "VALUE": {"PATTERN": FOOTBALL_RE, "THRESHOLD": FOOTBALL_THRESHOLD} },
        { "KEY":"HOTEL_AD", "VALUE": {"PATTERN": HOTEL_AD_RE, "THRESHOLD": HOTEL_AD_THRESHOLD} },
        # { "KEY":"SALE_URL", "VALUE": {"PATTERN": SALE_URL_RE, "THRESHOLD": SALE_URL_THERSHOLD} },
        { "KEY":"SALE_SKIP", "VALUE": {"PATTERN": SALE_SKIP_RE, "THRESHOLD": SALE_SKIP_THRESHOLD} },
        { "KEY":"SALE", "VALUE": {"PATTERN": SALE_RE, "THRESHOLD": SALE_THRESHOLD} },
        { "KEY":"RENT_SKIP", "VALUE": {"PATTERN": RENT_SKIP_RE, "THRESHOLD": RENT_SKIP_THRESHOLD} },
        { "KEY":"RENT", "VALUE": {"PATTERN": RENT_RE, "THRESHOLD": RENT_THRESHOLD} },
        { "KEY":"SCRIPT", "VALUE": {"PATTERN": SCRIPT_RE, "THRESHOLD": SCRIPT_THRESHOLD} },
        { "KEY":"GARBAGE", "VALUE": {"PATTERN": GARBAGE_RE, "THRESHOLD": GARBAGE_THRESHOLD} },
        { "KEY":"TOOLARGE", "VALUE": {"PATTERN": TOOLARGE_RE, "THRESHOLD": TOOLARGE_THRESHOLD} },
        { "KEY":"NONECHAR", "VALUE": {"PATTERN": NONECHAR_RE, "THRESHOLD": NONECHAR_THRESHOLD} },
        { "KEY":"NONE_TONE_MARK", "VALUE": {"PATTERN": NONE_TONE_MARK_RE, "THRESHOLD": NONE_TONE_MARK_THRESHOLD} },
        { "KEY":"JSON", "VALUE": {"PATTERN": JSON_RE, "THRESHOLD": JSON_THRESHOLD} },
        { "KEY":"GHOST", "VALUE": {"PATTERN": GHOST_RE, "THRESHOLD": GHOST_THRESHOLD} },
        { "KEY":"HEX", "VALUE": {"PATTERN": HEX_RE, "THRESHOLD": HEX_THRESHOLD} },
]

# Arg parse
WORD_PATTERN_FILTER = ["GAMBLE", "FOOTBALL"]
WORD_PATTERN_FILTER = None
    

def clean_with_remove_document(text: str) -> bool:
    # print(text)
    # Apply all word pattern filter
    if WORD_PATTERN_FILTER == None:
        for WP in LIST_WORD_PATTERN:
            # print(WP)
            WORD_THRESHOLD = int(WP["VALUE"]['THRESHOLD'])
            WORD_PATTERN = WP["VALUE"]['PATTERN']
            matches = WORD_PATTERN.findall(text)[:WORD_THRESHOLD]
            print(len(matches), WORD_THRESHOLD)
            if len(matches) == WORD_THRESHOLD:
                return True
    else:
        # Specific word pattern
        for WP in LIST_WORD_PATTERN:
            if WP['KEY'] in WORD_PATTERN_FILTER:
                WORD_THRESHOLD = int(WP["VALUE"]['THRESHOLD'])
                WORD_PATTERN = WP["VALUE"]['PATTERN']
                matches = WORD_PATTERN.findall(text)[:WORD_THRESHOLD]
                if len(matches) == WORD_THRESHOLD:
                    return True

    return False


def clean_text(text: str) -> str:
    text = PAGE_RE.sub(" ", text)
    text = EMBEDDED_SERVER_RE.sub(" ", text)
    text = U_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = MENU1_RE.sub(" ", text)
    text = MENU2_RE.sub(" ", text)
    text = MENU3_RE.sub(" ", text)
    text = MENU4_RE.sub(" ", text)
    text = SIDEBAR_RE.sub(" ", text)
    text = BLOCK_RE.sub(" ", text)
    text = HASHTAG_RE.sub(" ", text)
    text = MARKUP_RE.sub(" ", text)
    text = IFRAME_RE.sub(" ", text)
    text = IP_RE.sub(" ", text)
    text = TEL_RE.sub(" ", text)
    text = DATE1_RE.sub(" ", text)
    text = DATE2_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)

    # --- Refinements (in sequence)
    text = REFINE1_RE.sub(" ", text)
    text = REFINE2_RE.sub(" ", text)
    text = REFINE3_RE.sub(" ", text)
    text = REFINE4_RE.sub(" ", text)
    text = REFINE5_RE.sub(" ", text)
    text = REFINE6_RE.sub(" ", text)
    text = REFINE7_RE.sub(" ", text)
    text = REFINE8_RE.sub(" ", text)
    text = REFINE9_RE.sub(" ", text)
    text = REFINE10_RE.sub(" ", text)
    text = REFINE11_RE.sub(" ", text)
    text = REFINE12_RE.sub(" ", text)
    text = REFINE13_RE.sub(" ", text)
    text = REFINE14_RE.sub(" ", text)

    # Split the text into lines and remove any empty lines
    lines = [line for line in text.split("\n") if line]

    # Initialize the list with the first line
    deduplicated_list = [lines[0]]

    # Iterate over the rest of the lines
    for i in range(1, len(lines)):
        # Find the common prefix between this line and the previous line
        common_prefix = ""
        for char1, char2 in zip(lines[i], lines[i - 1]):
            if char1 == char2:
                common_prefix += char1
            else:
                break

        # Remove the common prefix from this line and add it to the list
        deduplicated_list.append(lines[i][len(common_prefix):])

    text = "\n".join(deduplicated_list)

    # Clean short lines
    # ( len(line) <= 30 characters , cut this line off)
    text = "\n".join(line for line in text.split("\n") if len(line) > 30)

    # ---- The scan row that passes all filter is written to disk
    # before write to disk, get rid of spaces by change them to single space (' ').

    text = re.sub("[ ]+", " ", text, 0, re.MULTILINE)
    text = re.sub("^[ ]", "", text, 0, re.MULTILINE)
    text = re.sub(r"\n\s*", "\n", text, 0, re.MULTILINE)

    return text


def clean_dataset(dataset: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Description : Call function clean_text to process the whole dataset.
    Input text : An input dataset having each element as a document in the dataset.
    Output : A clean dataset.
    """

    for i, data_point in enumerate(dataset):
        cleaned_text = clean_text(data_point["text"])
        if cleaned_text != dataset[i]["text"]:
            dataset[i]["text"] = cleaned_text
            dataset[i]["updated_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return [data_point for data_point in dataset if data_point["text"] != ""]
