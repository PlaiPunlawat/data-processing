import re
import pandas as pd
from datasketch import MinHash, MinHashLSH


def create_minhash(text, num_perm=128):
    m = MinHash(num_perm=num_perm)
    for word in re.findall(r"\w+", text.lower()):
        m.update(word.encode("utf8"))
    return m


def deduplicate_data(data, threshold=0.8, num_perm=128):
    df = pd.DataFrame(data)
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    minhashes = {}

    for idx, text in enumerate(df["text"]):
        minhash = create_minhash(text, num_perm=num_perm)
        minhashes[idx] = minhash
        lsh.insert(f"doc_{idx}", minhash)

    duplicates = set()
    for idx, minhash in minhashes.items():
        result = lsh.query(minhash)
        if len(result) > 1:
            duplicates.add(idx)

    df["is_duplicate"] = df.index.isin(duplicates)
    df = df[~df["is_duplicate"]]
    return df


if __name__ == "__main__":
    data = {
        "text": [
            "This is a good sentence.",
            "This is a good sentence.",
            "Another clean sentence.",
            "Yet another sentence.",
            "Another clean sentence.",
            "A completely different sentence.",
        ]
    }
    df_cleaned = deduplicate_data(data)
    print(df_cleaned)
