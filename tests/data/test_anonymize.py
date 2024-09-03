from data_processing.anonymization.anonymize import (
    anonymize
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
    unittest.main()
