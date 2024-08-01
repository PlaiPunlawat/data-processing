import numpy as np
from tqdm.auto import tqdm
from datasets import load_from_disk, Features, Sequence, Value
from datasketch import MinHashLSH, LeanMinHash, MinHash
from nlpo3 import segment

DEFAULT_MINHASH_COL_NAME = "text"
DEFAULT_NUM_PERMUTATION = 128
N_GRAM = 5
MINHASH_SEED = 1


def generate_minhash_signature(text, num_perm):
    minhash = MinHash(seed=MINHASH_SEED, num_perm=num_perm)
    tokens = segment(text, "newmm")
    n_gram = N_GRAM

    for i in range(len(tokens) - n_gram + 1):
        token_gram = "".join(tokens[i : i + n_gram])

        minhash.update(token_gram.encode("utf-8"))

    return minhash


def generate_minhash_signature_hf(
    doc, num_perm=DEFAULT_NUM_PERMUTATION, col_name=DEFAULT_MINHASH_COL_NAME
):
    minhash = generate_minhash_signature(doc[col_name], num_perm)
    return {"hashvalues": minhash.hashvalues}


def query_func(item, idx, index):
    neighbors = [
        str(dup_idx)
        for dup_idx in index.query(
            LeanMinHash(seed=MINHASH_SEED, hashvalues=item["hashvalues"]),
        )
        if dup_idx != idx
    ]
    return {"__neighbors__": neighbors, "idx": idx}


def process_data(batch, idx, pretrain_dataset_minhash, thresold):
    duplicate_results = []
    hashvalues = batch["hashvalues"]
    for j in range(len(idx)):
        key = idx[j]
        doc_hash_value = hashvalues[j]

        minhash = LeanMinHash(seed=MINHASH_SEED, hashvalues=doc_hash_value)
        neighbors = set(batch["__neighbors__"][j])

        for neighbor in neighbors:
            if neighbor == key:
                continue
            reference = pretrain_dataset_minhash[int(neighbor)]
            reference_signature = LeanMinHash(
                seed=MINHASH_SEED, hashvalues=reference["hashvalues"]
            )
            score = minhash.jaccard(reference_signature)
            if score > thresold:
                duplicate_results.append(
                    {
                        # "duplicate_id": neighbor,
                        "duplicate_text": reference["text"],
                        # "duplicate_dataset": reference["source"],
                        # "original_dataset": batch["source"][j],
                        # "original_text": batch["text"][j],
                        "original_id": str(key),
                        # "score": score,
                    }
                )
                break

    dict_of_lists = {}

    for dictionary in duplicate_results:
        for key, value in dictionary.items():
            if key not in dict_of_lists:
                dict_of_lists[key] = []

            dict_of_lists[key].append(value)

    return dict_of_lists


def deduplicate(
    pretrain_dataset, pretrain_dataset_minhash, num_perm=128, batch_size=100
):

    # print(pretrain_dataset_minhash, "pretrain_dataset_minhash")

    empty_hashvalues = generate_minhash_signature("", num_perm).hashvalues

    globals()["minhash_index"] = MinHashLSH(
        threshold=0.9,
        num_perm=num_perm,
    )
    with globals()["minhash_index"].insertion_session() as session:
        for i in tqdm(
            range(0, len(pretrain_dataset_minhash), batch_size),
            dynamic_ncols=True,
            desc="Iterating MinHashes...",  # noqa: E501
        ):
            batch = pretrain_dataset_minhash[i : i + batch_size]
            for j, hash_value in enumerate(batch["hashvalues"]):
                key = i + j
                session.insert(
                    key, LeanMinHash(seed=MINHASH_SEED, hashvalues=hash_value)
                )

    pretrain_dataset_minhash_result = pretrain_dataset_minhash.map(
        lambda doc, idx: query_func(doc, idx, index=globals()["minhash_index"]),
        desc="Querying...",
        num_proc=2,
        features=Features(
            {
                **pretrain_dataset_minhash.features,
                "__neighbors__": Sequence(Value("string")),
                "idx": Value("int32"),
            }
        ),
        load_from_cache_file=False,
        with_indices=True,
    ).filter(
        lambda x: len(x["__neighbors__"]) > 0
        and not np.array_equal(x["hashvalues"], empty_hashvalues),
        desc="Filtering...",
        num_proc=2,
    )

    print(pretrain_dataset_minhash_result, "pretrain_dataset_minhash_result")

    duplicate_results = pretrain_dataset_minhash_result.map(
        lambda batch, idx: process_data(batch, idx, pretrain_dataset_minhash, 0.9),
        batched=True,
        with_indices=True,
        num_proc=2,
        remove_columns=pretrain_dataset_minhash_result.column_names,
        load_from_cache_file=False,
        features=Features(
            {
                # "duplicate_id": Value("int32"),
                "duplicate_text": Value("string"),
                # "duplicate_dataset": Value("string"),
                # "original_dataset": Value("string"),
                # "original_text": Value("string"),
                "original_id": Value("string"),
                # "score": Value("float32"),
            }
        ),
    )

    print(duplicate_results, "duplicate_results")

    original_ids_to_remove = set()

    for i in tqdm(
        range(0, len(duplicate_results), batch_size),
        dynamic_ncols=True,
        desc="Collecting index to remove...",  # noqa: E501
    ):
        batch = duplicate_results[i : i + batch_size]
        for idx in batch["original_id"]:
            original_ids_to_remove.add(idx)

    pretrain_dataset = pretrain_dataset.filter(
        lambda _, idx: str(idx) not in original_ids_to_remove,
        desc="Filtering...",
        num_proc=2,
        with_indices=True,
    )

    print(pretrain_dataset, "pretrain_dataset")

    return duplicate_results, pretrain_dataset
