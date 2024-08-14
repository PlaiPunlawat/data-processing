from datetime import datetime
import pandas as pd
from typing import List, Dict, Pattern
import re

# Word Pattern
from data_processing.pattern_filtering.words_pattern import (
    GAMBLE_RE,
    GAMBLE_THRESHOLD,
    FOOTBALL_RE,
    FOOTBALL_THRESHOLD,
    HOTEL_AD_RE,
    HOTEL_AD_THRESHOLD,
    # SALE_URL_RE,
    # SALE_URL_THERSHOLD,
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
    GARBAGE_THRESHOLD,
)

# Regular Expression Pattern
from data_processing.pattern_filtering.regex_pattern import (
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

# Default Word Pattern
LIST_WORD_PATTERN = [
    {"KEY": "GAMBLE", "VALUE": {"PATTERN": GAMBLE_RE, "THRESHOLD": GAMBLE_THRESHOLD}},
    {
        "KEY": "FOOTBALL",
        "VALUE": {"PATTERN": FOOTBALL_RE, "THRESHOLD": FOOTBALL_THRESHOLD},
    },
    {
        "KEY": "HOTEL_AD",
        "VALUE": {"PATTERN": HOTEL_AD_RE, "THRESHOLD": HOTEL_AD_THRESHOLD},
    },
    # { "KEY":"SALE_URL", "VALUE": {"PATTERN": SALE_URL_RE, "THRESHOLD": SALE_URL_THERSHOLD} },
    {
        "KEY": "SALE_SKIP",
        "VALUE": {"PATTERN": SALE_SKIP_RE, "THRESHOLD": SALE_SKIP_THRESHOLD},
    },
    {"KEY": "SALE", "VALUE": {"PATTERN": SALE_RE, "THRESHOLD": SALE_THRESHOLD}},
    {
        "KEY": "RENT_SKIP",
        "VALUE": {"PATTERN": RENT_SKIP_RE, "THRESHOLD": RENT_SKIP_THRESHOLD},
    },
    {"KEY": "RENT", "VALUE": {"PATTERN": RENT_RE, "THRESHOLD": RENT_THRESHOLD}},
    {"KEY": "SCRIPT", "VALUE": {"PATTERN": SCRIPT_RE, "THRESHOLD": SCRIPT_THRESHOLD}},
    {
        "KEY": "GARBAGE",
        "VALUE": {"PATTERN": GARBAGE_RE, "THRESHOLD": GARBAGE_THRESHOLD},
    },
    {
        "KEY": "TOOLARGE",
        "VALUE": {"PATTERN": TOOLARGE_RE, "THRESHOLD": TOOLARGE_THRESHOLD},
    },
    {
        "KEY": "NONECHAR",
        "VALUE": {"PATTERN": NONECHAR_RE, "THRESHOLD": NONECHAR_THRESHOLD},
    },
    {
        "KEY": "NONE_TONE_MARK",
        "VALUE": {"PATTERN": NONE_TONE_MARK_RE, "THRESHOLD": NONE_TONE_MARK_THRESHOLD},
    },
    {"KEY": "JSON", "VALUE": {"PATTERN": JSON_RE, "THRESHOLD": JSON_THRESHOLD}},
    {"KEY": "GHOST", "VALUE": {"PATTERN": GHOST_RE, "THRESHOLD": GHOST_THRESHOLD}},
    {"KEY": "HEX", "VALUE": {"PATTERN": HEX_RE, "THRESHOLD": HEX_THRESHOLD}},
]

# Arg parse
WORD_PATTERN_FILTER = ["GAMBLE", "FOOTBALL"]
WORD_PATTERN_FILTER = None

def clean_with_remove_document(text: str) -> bool:
    """
    This function is designed to check and filter text based on predefined word patterns.
    It examines whether the text contains a certain number of matches for each pattern,
    as determined by the threshold. If the text meets or exceeds the threshold for any
    pattern, the function returns True, indicating that the text should be removed. If
    none of the patterns reach their threshold, the function returns False.
    
    ฟังก์ชันนี้มีไว้เพื่อตรวจสอบและกรองข้อความที่ตรงกับรูปแบบคำที่กำหนด
    โดยจะตรวจสอบว่ามีจำนวนคำที่ตรงกับรูปแบบ (pattern) ถึงเกณฑ์ที่กำหนดหรือไม่
    ถ้าตรงเกณฑ์จะคืนค่า True ซึ่งหมายความว่าข้อความนั้นควรถูกลบออก
    ถ้าไม่มีคำที่ตรงกับรูปแบบและเกณฑ์ที่กำหนด คืนค่า False
    
    Parameters:
    text (str): ข้อความที่ต้องการตรวจสอบ / The text to be checked
    
    Returns:
    bool: True ถ้าข้อความควรถูกลบออก (ตรงกับรูปแบบคำและเกณฑ์ที่กำหนด), False ถ้าไม่ตรง
          True if the text should be removed; False otherwise.
    """

    # If no specific word pattern filter is provided, process all patterns in the list
    # ถ้าไม่มีการกำหนดตัวกรองรูปแบบคำ (WORD_PATTERN_FILTER == None)
    if WORD_PATTERN_FILTER == None:
        # Loop through each word pattern in the LIST_WORD_PATTERN
        # วนลูปผ่านรายการรูปแบบคำใน LIST_WORD_PATTERN
        for WP in LIST_WORD_PATTERN:
            # Extract the threshold value for the current pattern
            # กำหนดเกณฑ์จำนวนคำที่ตรงกับรูปแบบ
            WORD_THRESHOLD = int(WP["VALUE"]["THRESHOLD"])
            
            # Extract the pattern (regular expression) for the current word pattern
            # กำหนดรูปแบบคำ (pattern)
            WORD_PATTERN = WP["VALUE"]["PATTERN"]
            
            # Find all matches in the text up to the threshold
            # หาคำที่ตรงกับรูปแบบในข้อความและเก็บใน matches
            matches = WORD_PATTERN.findall(text)
            
            # If the number of matches meets the threshold, return True
            # ถ้าจำนวนคำที่ตรงกับรูปแบบถึงเกณฑ์ที่กำหนด คืนค่า True
            print(len(matches), WORD_THRESHOLD)
            if len(matches) >= WORD_THRESHOLD:
                return True
    else:
        # If specific word pattern filters are provided, process only those
        # ถ้ามีการกำหนดตัวกรองรูปแบบคำ (WORD_PATTERN_FILTER)
        for WP in LIST_WORD_PATTERN:
            if WP["KEY"] in WORD_PATTERN_FILTER:
                # Extract the threshold and pattern for the current word pattern
                # กำหนดเกณฑ์จำนวนคำที่ตรงกับรูปแบบ
                WORD_THRESHOLD = int(WP["VALUE"]["THRESHOLD"])
                
                # กำหนดรูปแบบคำ (pattern)
                WORD_PATTERN = WP["VALUE"]["PATTERN"]
                
                # Find all matches in the text up to the threshold
                # หาคำที่ตรงกับรูปแบบในข้อความและเก็บใน matches
                matches = WORD_PATTERN.findall(text)
                
                # If the number of matches meets the threshold, return True
                # ถ้าจำนวนคำที่ตรงกับรูปแบบถึงเกณฑ์ที่กำหนด คืนค่า True
                if len(matches) >= WORD_THRESHOLD:
                    return True

    # If no patterns meet their threshold, return False
    # ถ้าไม่มีคำที่ตรงกับรูปแบบและเกณฑ์ที่กำหนด คืนค่า False
    return False


def clean_text(text: str, cutoff_character_length = 30) -> str:
    """
    This function is designed to clean and sanitize text by removing unnecessary data
    and formatting the text to make it more organized. It uses multiple regex patterns
    to find and remove unwanted content such as URLs, emails, HTML tags, etc. It also
    removes lines that are partially duplicated and any lines shorter than a specified
    length (default is 30 characters).
    
    ฟังก์ชันนี้มีไว้เพื่อล้างและทำความสะอาดข้อความ โดยการลบสิ่งที่ไม่จำเป็นออก
    และปรับแต่งข้อความให้เหมาะสม
    
    Parameters:
    text (str): ข้อความที่ต้องการล้างและทำความสะอาด / The text that needs to be cleaned and sanitized
    cutoff_character_length (int, optional): จำนวนตัวอักษรขั้นต่ำที่บรรทัดควรมี ถ้าบรรทัดใดมีความยาวน้อยกว่าค่านี้จะถูกลบออก (ค่าเริ่มต้นคือ 30)
                                             The minimum number of characters a line should have. (default is 30)
    
    Returns:
    str: ข้อความที่ผ่านการล้างและทำความสะอาดแล้ว / The cleaned and sanitized text
    """

    # Use various regex patterns to remove unwanted content from the text
    # ใช้ regex ต่าง ๆ เพื่อลบข้อความที่ไม่ต้องการออก
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

    # Apply additional regex patterns to refine the text further
    # ใช้ regex ต่าง ๆ เพื่อปรับแต่งข้อความเพิ่มเติม (เรียงตามลำดับ)
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
    # แยกข้อความเป็นบรรทัดและลบบรรทัดที่ว่าง
    lines = [line for line in text.split("\n") if line]

    # Initialize the deduplicated list with the first line
    # เริ่มต้นรายการด้วยบรรทัดแรก
    deduplicated_list = [lines[0]]

    # Iterate over the rest of the lines
    # วนลูปผ่านบรรทัดที่เหลือ
    for i in range(1, len(lines)):
        # Find the common prefix between this line and the previous line
        # หาคำนำร่วมระหว่างบรรทัดนี้และบรรทัดก่อนหน้า
        common_prefix = ""
        for char1, char2 in zip(lines[i], lines[i - 1]):
            if char1 == char2:
                common_prefix += char1
            else:
                break

        # Remove the common prefix from this line and add it to the deduplicated list
        # ลบคำนำร่วมออกจากบรรทัดนี้และเพิ่มลงในรายการ
        deduplicated_list.append(lines[i][len(common_prefix) :])

    # Join the lines back together
    # รวมบรรทัดเข้าด้วยกัน
    text = "\n".join(deduplicated_list)

    # Remove lines that are shorter than the cutoff length
    # ลบบรรทัดที่สั้นกว่า cutoff_character_length ตัวอักษร
    text = "\n".join(line for line in text.split("\n") if len(line) > cutoff_character_length)

    # Remove extra spaces before writing the text to disk
    # ลบช่องว่างเพิ่มเติมก่อนเขียนลงดิสก์
    text = re.sub("[ ]+", " ", text, 0, re.MULTILINE)
    text = re.sub("^[ ]", "", text, 0, re.MULTILINE)
    text = re.sub(r"\n\s*", "\n", text, 0, re.MULTILINE)

    return text



def clean_dataset(dataset: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    This function is designed to clean and sanitize the text in an entire dataset.
    The function iterates through each document in the dataset and applies the clean_text
    function to clean the text. If the text in a document is modified during cleaning, the
    function updates the text and records the current timestamp. Finally, the function
    returns the cleaned dataset, excluding any documents where the text has been emptied.
    
    ฟังก์ชันนี้มีไว้เพื่อล้างและทำความสะอาดข้อความในชุดข้อมูลทั้งหมด
    โดยเรียกใช้ฟังก์ชัน clean_text สำหรับแต่ละเอกสารในชุดข้อมูล
    
    Parameters:
    dataset (List[Dict[str, str]]): ชุดข้อมูลที่แต่ละองค์ประกอบเป็นเอกสารในรูปแบบของพจนานุกรม (dictionary)
    The dataset where each element is a document represented as a dictionary.
    
    Returns:
    List[Dict[str, str]]: ชุดข้อมูลที่ผ่านการล้างและทำความสะอาดแล้ว
    The cleaned dataset where text has been sanitized and empty documents removed.
    """

    # Iterate through each document in the dataset
    # วนลูปผ่านเอกสารแต่ละรายการในชุดข้อมูล
    for i, data_point in enumerate(dataset):
        # Clean and sanitize the text in each document
        # ล้างและทำความสะอาดข้อความในเอกสารแต่ละรายการ
        cleaned_text = clean_text(data_point["text"])
        
        # If the text has been modified, update the text and the update date
        # ถ้าข้อความหลังจากทำความสะอาดไม่เหมือนเดิม ให้ปรับปรุงข้อความและวันที่
        if cleaned_text != dataset[i]["text"]:
            dataset[i]["text"] = cleaned_text
            dataset[i]["updated_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Return the dataset with non-empty text
    # ส่งคืนชุดข้อมูลที่ข้อความไม่ว่างเปล่า
    return [data_point for data_point in dataset if data_point["text"] != ""]

