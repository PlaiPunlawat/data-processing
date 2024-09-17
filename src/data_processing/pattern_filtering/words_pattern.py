# coding: utf-8
# flake8: noqa
import re
import os

# Gamble Clean Words
GAMBLE_WORDS = None
GAMBLE_PATH = os.path.join(os.path.dirname(
    __file__), 'config/GAMBLE_WORDS.txt')
with open(GAMBLE_PATH) as my_file:
    GAMBLE_WORDS = my_file.read().splitlines()

GAMBLE_PATTERN = "|".join(GAMBLE_WORDS)
GAMBLE_RE = re.compile(GAMBLE_PATTERN, re.MULTILINE)
GAMBLE_THRESHOLD = 2

# Sale Clean Words
SALE_SKIP_WORDS = None
SALE_SKIP_PATH = os.path.join(os.path.dirname(
    __file__), 'config/SALE_SKIP_WORDS.txt')
with open(SALE_SKIP_PATH) as my_file:
    SALE_SKIP_WORDS = my_file.read().splitlines()

SALE_SKIP_PATTERN = "|".join(SALE_SKIP_WORDS)
SALE_SKIP_RE = re.compile(SALE_SKIP_PATTERN, re.MULTILINE)
SALE_SKIP_THRESHOLD = 3

# Sale URL
SALE_URL_WORDS = None
SALE_URL_PATH = os.path.join(os.path.dirname(
    __file__), 'config/SALE_URL_WORDS.txt')
with open(SALE_URL_PATH) as my_file:
    SALE_URL_WORDS = my_file.read().splitlines()

SALE_URL_PATTERN = "|".join(SALE_URL_WORDS)
SALE_URL_RE = re.compile(SALE_URL_PATTERN, re.MULTILINE)
SALE_URL_THERSHOLD = None

# Sales
SALE_WORDS = None
SALE_PATH = os.path.join(os.path.dirname(__file__), 'config/SALE_WORDS.txt')
with open(SALE_PATH) as my_file:
    SALE_WORDS = my_file.read().splitlines()

SALE_PATTERN = "|".join(SALE_WORDS)
SALE_RE = re.compile(SALE_PATTERN, re.MULTILINE)
SALE_THRESHOLD = 3

# Rent Clean Words
RENT_SKIP_WORDS = None
RENT_SKIP_PATH = os.path.join(os.path.dirname(
    __file__), 'config/RENT_SKIP_WORDS.txt')
with open(RENT_SKIP_PATH) as my_file:
    RENT_SKIP_WORDS = my_file.read().splitlines()

RENT_SKIP_PATTERN = "|".join(RENT_SKIP_WORDS)
RENT_SKIP_RE = re.compile(RENT_SKIP_PATTERN, re.MULTILINE)
RENT_SKIP_THRESHOLD = 2

# Rent words
RENT_WORDS = None
RENT_PATH = os.path.join(os.path.dirname(__file__), 'config/RENT_WORDS.txt')
with open(RENT_PATH) as my_file:
    RENT_WORDS = my_file.read().splitlines()

RENT_PATTERN = "|".join(RENT_WORDS)
RENT_RE = re.compile(RENT_PATTERN, re.MULTILINE)
RENT_THRESHOLD = 2

# Script Clean Words
SCRIPT_WORDS = None
SCRIPT_PATH = os.path.join(os.path.dirname(
    __file__), 'config/SCRIPT_WORDS.txt')
with open(SCRIPT_PATH) as my_file:
    SCRIPT_WORDS = my_file.read().splitlines()

SCRIPT_PATTERN = r"\b" + "|".join(SCRIPT_WORDS) + r"\b"
SCRIPT_RE = re.compile(SCRIPT_PATTERN, re.MULTILINE)
SCRIPT_THRESHOLD = 10

# Garbage Clean Words
GARBAGE_WORDS = None
GARBAGE_PATH = os.path.join(os.path.dirname(
    __file__), 'config/GARBAGE_WORDS.txt')
with open(GARBAGE_PATH) as my_file:
    GARBAGE_WORDS = my_file.read().splitlines()

GARBAGE_PATTERN = "|".join(GARBAGE_WORDS)
GARBAGE_RE = re.compile(GARBAGE_PATTERN, re.MULTILINE)
GARBAGE_THRESHOLD = 4

# Football teams
FOOTBALL_TEAMS = None
FOOTBALL_TEAMS_PATH = os.path.join(
    os.path.dirname(__file__), 'config/FOOTBALL_TEAMS.txt')
with open(FOOTBALL_TEAMS_PATH) as my_file:
    FOOTBALL_TEAMS = my_file.read().splitlines()

FOOTBALL_PATTERN = "|".join(FOOTBALL_TEAMS)
FOOTBALL_RE = re.compile(FOOTBALL_PATTERN, re.MULTILINE)
FOOTBALL_THRESHOLD = 4

# Hotels Advertising
HOTEL_AD = None
HOTEL_AD_PATH = os.path.join(os.path.dirname(__file__), 'config/HOTEL_AD.txt')
with open(HOTEL_AD_PATH) as my_file:
    HOTEL_AD = my_file.read().splitlines()

HOTEL_AD_PATTERN = "|".join(HOTEL_AD)
HOTEL_AD_RE = re.compile(HOTEL_AD_PATTERN, re.MULTILINE)
HOTEL_AD_THRESHOLD = 4
