from data_processing.anonymization.anonymize import (
    anonymize,
    ner_tag_transformer
)
import pandas as pd
from datasets import Dataset
import unittest



class TestAnonymize(unittest.TestCase):

    def test_person(self):
        text_test = "สมเด็จพระเทพรัตนราชสุดาฯ สยามบรมราชกุมารี ทรงเสด็จไปเยือนประเทศญี่ปุ่นเมื่อวันที่ 5 เมษายน 2564"
        result = anonymize(text_test)
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<person>", result)

    def test_person_manual_model(self):
        text_test = "ฉันชื่อ นางสาวมะลิวา บุญสระดี อาศัยอยู่ที่อำเภอนางรอง จังหวัดบุรีรัมย์ อายุ 23 ปี เพิ่งเรียนจบจาก มหาวิทยาลัยขอนแก่น และนี่คือข้อมูลปลอมชื่อคนไม่มีอยู่จริง อายุ 23 ปี"
        result = anonymize(text_test, "thainer-v2")
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<person>", result)

    def test_ner_tag_transformer_model(self):
        text_test = "ฉันชื่อ นางสาวมะลิวา บุญสระดี อาศัยอยู่ที่อำเภอนางรอง จังหวัดบุรีรัมย์ อายุ 23 ปี เพิ่งเรียนจบจาก มหาวิทยาลัยขอนแก่น และนี่คือข้อมูลปลอมชื่อคนไม่มีอยู่จริง อายุ 23 ปี"
        result = anonymize(text_test, ner_corpus="pythainlp/thainer-corpus-v2-base-model", NER_TAG=True)
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<person>", result)

    def test_org(self):
        text_test = "NECTEC เป็นหน่วยงานที่ดูแลเรื่อง AI เครือข่าย AIS ให้บริการโทรษัพ บริษัทซีพีจำกัด"
        result = anonymize(text_test)
        print("text_test", text_test)
        print("result", result)

        # self.assertIn("<person>", result)

    def test_email(self):
        text_test = "โปรดส่ง email มาหาฉันที่ email nectec@gmail.com"
        result = anonymize(text_test)
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<email>", result)

    def test_phone(self):
        text_test = "เบอร์โทรของฉันคือ 0890340123"
        result = anonymize(text_test)
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<phone_number>", result)

    def test_id(self):
        text_test = "บัตรประชาชนของฉันคือ 1-1996-99999-94-1"
        result = anonymize(text_test)
        print("text_test", text_test)
        print("result", result)

        self.assertIn("<id no.>", result)


if __name__ == "__main__":
    TestAnonymize.NER_TAG_TRANSFORMER_MODEL = "pythainlp/thainer-corpus-v2-base-model"
    unittest.main()
