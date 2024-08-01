import unittest
from openthaigpt_pretraining_data.internet.s2_perplexity_v2.perplexity_filtering import (
    perplexity_based_filtering,
    calculate_perplexity,
)


class TestPerplexityFiltering(unittest.TestCase):

    def setUp(self):
        self.data = {
            "text": [
                "This is a good sentence.",
                "asdklj12klj3!",
                "Another clean sentence.",
                "ajsdklasdjasd.",
                "Visit http://example.com for more info.",
                "This text is clear and understandable.",
            ]
        }

    def test_perplexity_calculation(self):
        text = "This is a good sentence."
        perplexity = calculate_perplexity(text)
        self.assertTrue(perplexity > 0)

    def test_perplexity_filtering(self):
        df_cleaned = perplexity_based_filtering(self.data, perplexity_threshold=50)
        self.assertTrue("asdklj12klj3!" not in df_cleaned["text"].values)
        self.assertTrue("ajsdklasdjasd." not in df_cleaned["text"].values)

    def test_all_pass(self):
        clean_data = {
            "text": [
                "Hello good morning.",
                "No bad words here.",
                "Everything looks good.",
            ]
        }
        for text in clean_data["text"]:
            perplexity = calculate_perplexity(text)
            print(f"Text: {text}, Perplexity: {perplexity}")

        df_cleaned = perplexity_based_filtering(clean_data, perplexity_threshold=500)
        self.assertEqual(len(df_cleaned), len(clean_data["text"]))


if __name__ == "__main__":
    unittest.main()
