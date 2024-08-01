import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

# โหลดโมเดลและ tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# model_path = "openthaigpt/openthaigpt-1.0.0-7b-chat"
# tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(
#     model_path, trust_remote_code=True, torch_dtype=torch.float16
# )


def calculate_perplexity(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        perplexity = torch.exp(loss)
    return perplexity.item()


def perplexity_based_filtering(data, perplexity_threshold=100):
    df = pd.DataFrame(data)
    df["perplexity"] = df["text"].apply(calculate_perplexity)
    df["is_spam"] = df["perplexity"] > perplexity_threshold
    df = df[~df["is_spam"]]
    return df


if __name__ == "__main__":
    data = {
        "text": [
            "This is a good sentence.",
            "asdklj12klj3!",
            "Another clean sentence.",
            "ajsdklasdjasd.",
            "Visit http://example.com for more info.",
            "This text is clear and understandable.",
        ]
    }
    df_cleaned = perplexity_based_filtering(data)
    print(df_cleaned)
