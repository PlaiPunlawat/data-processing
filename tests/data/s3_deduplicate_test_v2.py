import unittest
import pandas as pd
from openthaigpt_pretraining_data.internet.s3_deduplication_v2.dedup import (
    deduplicate_data,
)


class TestDeduplication(unittest.TestCase):

    def setUp(self):
        self.data = {
            "text": [
                "This is a good sentence.",
                "This is a good sentence.",
                "Another clean sentence.",
                "Yet another sentence.",
                "Another clean sentence.",
                "A completely different sentence.",
            ]
        }

    def test_deduplication(self):
        df_cleaned = deduplicate_data(self.data)
        expected_texts = ["Yet another sentence.", "A completely different sentence."]
        self.assertEqual(list(df_cleaned["text"]), expected_texts)

    def test_no_duplicates(self):
        unique_data = {
            "text": [
                "Unique sentence one.",
                "Unique sentence two.",
                "Unique sentence three.",
            ]
        }
        df_cleaned = deduplicate_data(unique_data)
        self.assertEqual(len(df_cleaned), len(unique_data["text"]))


if __name__ == "__main__":
    unittest.main()
