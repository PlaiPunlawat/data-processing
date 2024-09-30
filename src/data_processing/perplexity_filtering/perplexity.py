import kenlm
import math
import numpy as np
import pandas as pd
import pickle
import scipy
import sentencepiece  # type: ignore
from data_processing.core.text_normalizer import normalize
from typing import List
import warnings
import os

warnings.simplefilter(action="ignore", category=FutureWarning)

class SentencesLM:
    """
    This class is used to compute the perplexity scores for each line in a document.
    คลาสนี้ใช้ในการคำนวณคะแนน perplexity สำหรับแต่ละบรรทัดในเอกสาร
    """

    def __init__(self):
        """
        Initializes the SentencesLM class by loading the language model and sentence piece processor.
        ฟังก์ชันนี้มีไว้เพื่อสร้างและกำหนดค่าเริ่มต้นให้กับคลาส SentencesLM
        โดยการโหลดโมเดลภาษา (language model) และตัวประมวลผลประโยค (sentence piece processor)
        """
        # Set up the configuration for loading the language model
        # กำหนดค่าเริ่มต้นสำหรับการโหลดโมเดลภาษา
        lm_config = kenlm.Config()
        lm_config.load_method = 2  # Load method 2 is used for efficient loading

        # Construct the path to the kenlm language model file
        # สร้างเส้นทางไปยังไฟล์โมเดลภาษา kenlm
        lm_model_filename = os.path.join(os.path.dirname(__file__), 'th.arpa.bin')
        
        # Load the kenlm language model from the specified file
        # โหลดโมเดลภาษา kenlm จากไฟล์
        self.lm = kenlm.Model(str(lm_model_filename), lm_config)

        # Initialize the sentence piece processor
        # โหลดโมเดล sentence piece processor จากไฟล์
        self.sp = sentencepiece.SentencePieceProcessor()
        self.sp.load(os.path.join(os.path.dirname(__file__), "th.sp.model"))

    def pp(self, log_score: float, length: int) -> float:
        """
        Calculates the perplexity from the log score and the length of the sentence.
        ฟังก์ชันนี้มีไว้เพื่อคำนวณคะแนน perplexity จาก log score และความยาวของประโยค

        Parameters:
        log_score (float): The log probability score obtained from the language model.
                           ค่า log score ที่ได้จากโมเดลภาษา
        length (int): The length of the sentence in terms of number of tokens.
                      ความยาวของประโยค

        Returns:
        float: The calculated perplexity value.
               ค่า perplexity ที่คำนวณได้
        """
        # Calculate the exponent part for the perplexity formula
        # คำนวณส่วนยกกำลังสำหรับสูตร perplexity
        power = min(30, -log_score / length)
        
        # Compute the perplexity by raising 10 to the power calculated
        # คำนวณ perplexity โดยการยก 10 กำลังค่าที่คำนวณได้
        return 10.0 ** power

    def do(self, document: List[str]) -> float:
        """
        Computes the average perplexity for each line in the document.
        ฟังก์ชันนี้มีไว้เพื่อคำนวณคะแนน perplexity สำหรับแต่ละบรรทัดในเอกสาร

        Parameters:
        document (List[str]): A list of lines (sentences) from the document.
                              รายการของบรรทัดในเอกสารที่ต้องการคำนวณคะแนน perplexity

        Returns:
        float: The average perplexity of the document.
               ค่า perplexity เฉลี่ยของเอกสาร
        """
        total_pp = 0  # Initialize total log score
        total_length = 0  # Initialize total length of all sentences

        # Iterate over each line in the document
        # วนลูปผ่านแต่ละบรรทัดในเอกสาร
        for line in document:
            # Normalize the line (e.g., remove accents)
            # ปรับแต่งบรรทัดให้เป็นรูปแบบมาตรฐาน
            line = normalize(line, accent=False)

            # Tokenize the line using the sentence piece processor
            # แปลงบรรทัดให้เป็น token โดยใช้ sentence piece processor
            tokenized_line = " ".join(self.sp.encode_as_pieces(line))

            # Calculate the log score for the tokenized line using the language model
            # คำนวณ log score สำหรับบรรทัด
            log_score = self.lm.score(tokenized_line)

            # Determine the length of the line in terms of tokens (words)
            # คำนวณความยาวของบรรทัด
            length = len(line.split()) + 1  # +1 accounts for sentence end

            # Accumulate the total length and log score
            # รวมความยาวและ log score ของบรรทัดเข้ากับค่า total
            total_length += length
            total_pp += log_score

        # Compute the average perplexity over the entire document
        # คำนวณและส่งคืนค่า perplexity เฉลี่ยของเอกสาร
        return round(self.pp(total_pp, total_length), 1)  # Rounded to one decimal place


# Construct the path to the decision tree classifier file
# สร้างเส้นทางไปยังไฟล์โมเดล decision tree
classifier_filename = os.path.join(os.path.dirname(__file__), 'decision_tree.sav')

# Load the decision tree classifier from the specified file
# โหลดโมเดล decision tree จากไฟล์
classifier = pickle.load(open(classifier_filename, "rb"))

# Create an instance of the SentencesLM class for perplexity calculations
# สร้างวัตถุ SentencesLM สำหรับการคำนวณ perplexity
lm = SentencesLM()



def classify_spam(text: str, threshold=0.5):
    """
    This function classifies a given text as either spam or not spam.
    It uses perplexity scores and a decision tree model to make the prediction.

    ฟังก์ชันนี้มีไว้เพื่อจัดประเภทข้อความว่ามีลักษณะเป็น spam หรือไม่
    โดยใช้คะแนน perplexity และโมเดล decision tree

    Parameters:
    text (str): The text to be classified as spam or not.
                ข้อความที่ต้องการจัดประเภท
    threshold (float): default=0.5 If the proba > threshold returns 1 else 0.

    Returns:
    tuple:
        - prediction (array): The predicted classification (1 for spam, 0 for non-spam).
                              ค่าที่ทำนายว่าเป็น spam หรือไม่ (1 คือ spam, 0 คือ non-spam)
        - log_pp_score (float): The logarithm of the perplexity score.
                                ค่าลอการิทึมของคะแนน perplexity
    """

    # Calculate the perplexity score for the text by splitting it into lines
    # คำนวณคะแนน perplexity สำหรับข้อความ
    pp_score = lm.do(text.split("\n"))

    # Calculate the logarithm of the perplexity score
    # คำนวณลอการิทึมของคะแนน perplexity
    log_pp_score = math.log(pp_score)

    # Use the decision tree model to predict whether the text is spam
    # ใช้โมเดล decision tree ในการทำนายประเภทของข้อความ
    predicted_proba = classifier.predict_proba(pd.DataFrame({"log_score": [log_pp_score]}))
    prediction = (predicted_proba [:,1] >= threshold).astype('int')

    # Return the prediction and the log perplexity score
    # ส่งคืนผลการทำนายและค่าลอการิทึมของคะแนน perplexity
    return prediction, log_pp_score



def sample_text_back(
    probs: np.ndarray,
    percentage: float = 0.1,
) -> List[int]:
    """
    This function is designed to randomly sample spam text back into the dataset
    using the distribution of log perplexity scores from a language model.

    ฟังก์ชันนี้มีไว้เพื่อสุ่มข้อความ spam กลับมาในชุดข้อมูล โดยใช้การกระจายคะแนน log perplexity ของโมเดลภาษา

    Parameters:
    probs (np.ndarray): An array of probability values corresponding to the log perplexity scores.
                        อาเรย์ของความน่าจะเป็น (probability) ของคะแนน log perplexity
    percentage (float, optional): The percentage of data to be sampled back (default is 0.1).
                                  เปอร์เซ็นต์ของข้อมูลที่จะสุ่มกลับมา (ค่าเริ่มต้น: 0.1)

    Returns:
    List[int]: A list of indices of the sampled data.
               ดัชนีของข้อมูลที่ถูกสุ่มกลับมา
    """

    n = len(probs)  # Get the number of probabilities
    if n <= 1:
        return []  # If there is only one or no probability, return an empty list

    # Normalize the log perplexity probabilities using the softmax function
    # นำค่าความน่าจะเป็นของ log perplexity มา normalize ด้วย softmax
    norm_probs = scipy.special.softmax(1 - probs)

    # Set the random seed for reproducibility
    # ตั้งค่าการสุ่มเพื่อให้ผลลัพธ์คงที่
    np.random.seed(0)

    # Randomly select indices based on the normalized probabilities
    # สุ่มดัชนีของข้อมูลตามค่าความน่าจะเป็นที่ normalize แล้ว
    selected_idx = np.random.choice(
        n, p=norm_probs, size=int(percentage * n), replace=False
    )

    # Return the list of sampled indices
    # ส่งคืนรายการของดัชนีที่ถูกสุ่ม
    return list(selected_idx)

