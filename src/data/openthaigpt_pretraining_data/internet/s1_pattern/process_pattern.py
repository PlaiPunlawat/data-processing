import re
import pandas as pd
from typing import List, Dict, Pattern

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

LIST_WORD_PATTERN = {
        "GAMBLE": {"PATTERN": GAMBLE_RE, "THRESHOLD": GAMBLE_THRESHOLD},
        "FOOTBALL": {"PATTERN": FOOTBALL_RE, "THRESHOLD": FOOTBALL_THRESHOLD},
        "HOTEL_AD": {"PATTERN": HOTEL_AD_RE, "THRESHOLD": HOTEL_AD_THRESHOLD},
        "SALE_URL": {"PATTERN": SALE_URL_RE, "THRESHOLD": SALE_URL_THERSHOLD},
        "SALE_SKIP": {"PATTERN": SALE_SKIP_RE, "THRESHOLD": SALE_SKIP_THRESHOLD},
        "SALE": {"PATTERN": SALE_RE, "THRESHOLD": SALE_THRESHOLD},
        "RENT_SKIP": {"PATTERN": RENT_SKIP_RE, "THRESHOLD": RENT_SKIP_THRESHOLD},
        "RENT": {"PATTERN": RENT_RE, "THRESHOLD": RENT_THRESHOLD},
        "SCRIPT": {"PATTERN": SCRIPT_RE, "THRESHOLD": SCRIPT_THRESHOLD},
        "GARBAGE": {"PATTERN": GARBAGE_RE, "THRESHOLD": GARBAGE_THRESHOLD}
    }

# Arg parse
WORD_PATTERN_FILTER = ["GAMBLE", "FOOTBALL"]
WORD_PATTERN_FILTER = None

def clean_with_remove_document(WORD_PATTERN: Pattern, WORD_THRESHOLD: int, text: str) -> bool:

    matches = WORD_PATTERN.findall(text)[:WORD_THRESHOLD]
    if len(matches) == WORD_THRESHOLD:
        return True
    
def clean_with_remove_document2(WORD_PATTERN: Pattern, WORD_THRESHOLD: int, text: str) -> bool:

    # Apply all word pattern filter
    if WORD_PATTERN_FILTER == None:
        for WP in LIST_WORD_PATTERN:
            matches = WP['WORD_PATTERN'].findall(text)[:WP['WORD_THRESHOLD']]
            if len(matches) == WP['WORD_THRESHOLD']:
                return True
    else:
    # Specific word pattern
        for WP in LIST_WORD_PATTERN:
            if WP['WORD_PATTERN'] in WORD_PATTERN_FILTER:
                matches = WP['WORD_PATTERN'].findall(text)[:WP['WORD_THRESHOLD']]
                if len(matches) == WP['WORD_THRESHOLD']:
                    return True
    
    return False
        

# if __name__ == "__main__":
#     print("Hello")

