import kenlm
import math
import numpy as np
import pandas as pd
import pickle
import scipy
import sentencepiece  # type: ignore
from openthaigpt_pretraining_data.core.text_normalizer import normalize
from typing import List
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


class SentencesLM:
    """
    คลาสนี้ใช้ในการคำนวณคะแนน perplexity สำหรับแต่ละบรรทัดในเอกสาร
    """

    def __init__(self):
        """
        ฟังก์ชันนี้มีไว้เพื่อสร้างและกำหนดค่าเริ่มต้นให้กับคลาส SentencesLM
        โดยการโหลดโมเดลภาษา (language model) และตัวประมวลผลประโยค (sentence piece processor)
        """
        # กำหนดค่าเริ่มต้นสำหรับการโหลดโมเดลภาษา
        lm_config = kenlm.Config()
        lm_config.load_method = 2

        # โหลดโมเดลภาษา kenlm จากไฟล์
        lm_model_filename = "th.arpa.bin"
        self.lm = kenlm.Model(str(lm_model_filename), lm_config)

        # โหลดโมเดล sentence piece processor จากไฟล์
        self.sp = sentencepiece.SentencePieceProcessor()
        self.sp.load("th.sp.model")

    def pp(self, log_score: float, length: int) -> float:
        """
        ฟังก์ชันนี้มีไว้เพื่อคำนวณคะแนน perplexity จาก log score และความยาวของประโยค

        Parameters:
        log_score (float): ค่า log score ที่ได้จากโมเดลภาษา
        length (int): ความยาวของประโยค

        Returns:
        float: ค่า perplexity ที่คำนวณได้
        """
        power = min(30, -log_score / length)
        return 10.0**power

    def do(self, document: List[str]) -> float:
        """
        ฟังก์ชันนี้มีไว้เพื่อคำนวณคะแนน perplexity สำหรับแต่ละบรรทัดในเอกสาร

        Parameters:
        document (List[str]): รายการของบรรทัดในเอกสารที่ต้องการคำนวณคะแนน perplexity

        Returns:
        float: ค่า perplexity เฉลี่ยของเอกสาร
        """
        total_pp = 0
        total_length = 0

        # วนลูปผ่านแต่ละบรรทัดในเอกสาร
        for line in document:
            # ปรับแต่งบรรทัดให้เป็นรูปแบบมาตรฐาน
            line = normalize(line, accent=False)

            # แปลงบรรทัดให้เป็น token โดยใช้ sentence piece processor
            tokenized_line = " ".join(self.sp.encode_as_pieces(line))

            # คำนวณ log score สำหรับบรรทัด
            log_score = self.lm.score(tokenized_line)

            # คำนวณความยาวของบรรทัด
            length = len(line.split()) + 1

            # รวมความยาวและ log score ของบรรทัดเข้ากับค่า total
            total_length += length
            total_pp += log_score

        # คำนวณและส่งคืนค่า perplexity เฉลี่ยของเอกสาร
        return round(self.pp(total_pp, total_length), 1)


classifier_filename = "decision_tree.sav"
# โหลดโมเดล decision tree จากไฟล์
classifier = pickle.load(open(classifier_filename, "rb"))

# สร้างวัตถุ SentencesLM สำหรับการคำนวณ perplexity
lm = SentencesLM()


def classify_spam(text: str):
    """
    ฟังก์ชันนี้มีไว้เพื่อจัดประเภทข้อความว่ามีลักษณะเป็น spam หรือไม่
    โดยใช้คะแนน perplexity และโมเดล decision tree

    Parameters:
    text (str): ข้อความที่ต้องการจัดประเภท

    Returns:
    tuple:
        - prediction (array): ค่าที่ทำนายว่าเป็น spam หรือไม่ (1 คือ spam, 0 คือ non-spam)
        - log_pp_score (float): ค่าลอการิทึมของคะแนน perplexity
    """

    # คำนวณคะแนน perplexity สำหรับข้อความ
    pp_score = lm.do(text.split("\n"))

    # คำนวณลอการิทึมของคะแนน perplexity
    log_pp_score = math.log(pp_score)

    # ใช้โมเดล decision tree ในการทำนายประเภทของข้อความ
    prediction = classifier.predict(pd.DataFrame({"log_score": [log_pp_score]}))

    # ส่งคืนผลการทำนายและค่าลอการิทึมของคะแนน perplexity
    return prediction, log_pp_score


def sample_text_back(
    probs: np.ndarray,
    percentage: float = 0.1,
) -> List[int]:
    """
    ฟังก์ชันนี้มีไว้เพื่อสุ่มข้อความ spam กลับมาในชุดข้อมูล โดยใช้การกระจายคะแนน log perplexity ของโมเดลภาษา

    Parameters:
    probs (np.ndarray): อาเรย์ของความน่าจะเป็น (probability) ของคะแนน log perplexity
    percentage (float, optional): เปอร์เซ็นต์ของข้อมูลที่จะสุ่มกลับมา (ค่าเริ่มต้น: 0.1)

    Returns:
    List[int]: ดัชนีของข้อมูลที่ถูกสุ่มกลับมา
    """

    n = len(probs)
    if n <= 1:
        return []

    # นำค่าความน่าจะเป็นของ log perplexity มา normalize ด้วย softmax
    norm_probs = scipy.special.softmax(1 - probs)

    # ตั้งค่าการสุ่มเพื่อให้ผลลัพธ์คงที่
    np.random.seed(0)

    # สุ่มดัชนีของข้อมูลตามค่าความน่าจะเป็นที่ normalize แล้ว
    selected_idx = np.random.choice(
        n, p=norm_probs, size=int(percentage * n), replace=False
    )

    # ส่งคืนรายการของดัชนีที่ถูกสุ่ม
    return list(selected_idx)
