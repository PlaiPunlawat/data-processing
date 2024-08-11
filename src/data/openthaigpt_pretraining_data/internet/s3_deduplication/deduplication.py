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
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับข้อความที่ได้รับมา
    โดยการใช้ n-gram และแฮชจำนวน permutations ที่กำหนดไว้

    Parameters:
    text (str): ข้อความที่ต้องการสร้างลายเซ็น
    num_perm (int): จำนวน permutations ที่จะใช้ในการสร้าง MinHash

    Returns:
    MinHash: วัตถุ MinHash ที่มีลายเซ็นที่สร้างขึ้นจากข้อความ
    """

    # สร้างวัตถุ MinHash โดยกำหนดค่า seed และจำนวนการแฮช (num_perm)
    minhash = MinHash(seed=MINHASH_SEED, num_perm=num_perm)

    # แบ่งข้อความออกเป็น tokens โดยใช้ตัวแบ่งคำแบบ "newmm"
    tokens = segment(text, "newmm")

    # กำหนดจำนวน n-gram ที่จะใช้
    n_gram = N_GRAM

    # วนลูปผ่าน tokens เพื่อสร้าง n-gram และอัปเดต MinHash ด้วย n-gram เหล่านั้น
    for i in range(len(tokens) - n_gram + 1):
        token_gram = "".join(tokens[i : i + n_gram])  # สร้าง n-gram จาก tokens
        minhash.update(
            token_gram.encode("utf-8")
        )  # อัปเดต MinHash ด้วย n-gram ที่เข้ารหัสเป็น UTF-8

    # ส่งคืน MinHash object ที่สร้างขึ้น
    return minhash


def generate_minhash_signature_hf(
    doc, num_perm=DEFAULT_NUM_PERMUTATION, col_name=DEFAULT_MINHASH_COL_NAME
):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับเอกสารที่ได้รับมา
    โดยใช้จำนวน permutations ที่กำหนดและคอลัมน์ของข้อความที่ต้องการ

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้างลายเซ็น MinHash
    num_perm (int, optional): จำนวน permutations ที่จะใช้ในการสร้าง MinHash (ค่าเริ่มต้น: DEFAULT_NUM_PERMUTATION)
    col_name (str, optional): ชื่อคอลัมน์ที่มีข้อความที่ต้องการสร้างลายเซ็น (ค่าเริ่มต้น: DEFAULT_MINHASH_COL_NAME)

    Returns:
    dict: พจนานุกรมที่มีลายเซ็น MinHash ที่สร้างขึ้นจากข้อความในเอกสาร
    """

    # สร้างลายเซ็น MinHash สำหรับข้อความในคอลัมน์ที่กำหนด
    minhash = generate_minhash_signature(doc[col_name], num_perm)

    # ส่งคืนพจนานุกรมที่มี hashvalues ของ MinHash
    return {"hashvalues": minhash.hashvalues}


def query_func(item, idx, index):
    """
    ฟังก์ชันนี้มีไว้เพื่อค้นหาข้อคยามที่คล้ายคลึงกันสำหรับเอกสารที่ได้รับมา
    โดยใช้ลายเซ็น MinHash และ MinHashLSH index

    Parameters:
    item (dict): เอกสารที่ต้องการค้นหา
    idx (int): ดัชนีของเอกสารในชุดข้อมูล
    index (MinHashLSH): ดัชนี MinHashLSH ที่ใช้ในการค้นหาข้อความ

    Returns:
    dict: พจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
    """

    # ค้นหาข้อความที่คล้ายคลึงกันโดยใช้ลายเซ็น MinHash และ MinHashLSH index
    neighbors = [
        str(dup_idx)
        for dup_idx in index.query(
            LeanMinHash(seed=MINHASH_SEED, hashvalues=item["hashvalues"]),
        )
        if dup_idx != idx  # ตรวจสอบว่าข้อความที่พบไม่ใช่ตัวเอง
    ]

    # ส่งคืนพจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
    return {"__neighbors__": neighbors, "idx": idx}


def process_data(batch, idx, pretrain_dataset_minhash, thresold):
    """
    ฟังก์ชันนี้มีไว้เพื่อประมวลผลข้อมูลในแต่ละ batch และค้นหาข้อความที่ซ้ำกันในชุดข้อมูลการฝึก
    โดยใช้ลายเซ็น MinHash และคำนวณระยะทาง Jaccard

    Parameters:
    batch (dict): กลุ่มข้อมูลที่ต้องการประมวลผล
    idx (list): รายการของดัชนีที่เกี่ยวข้องกับข้อมูลใน batch
    pretrain_dataset_minhash (Dataset): ชุดข้อมูลการฝึกที่มีลายเซ็น MinHash
    thresold (float): เกณฑ์ที่ใช้ในการตัดสินว่าข้อความสองข้อความมีความคล้ายคลึงกันพอที่จะถือว่าซ้ำกัน

    Returns:
    dict: พจนานุกรมของรายการที่ซ้ำกันพร้อมข้อมูลรายละเอียด
    """

    duplicate_results = []  # สร้างรายการเก็บผลลัพธ์ของข้อมูลที่ซ้ำกัน
    hashvalues = batch["hashvalues"]  # ดึงค่า hashvalues จาก batch

    # วนลูปผ่านแต่ละดัชนีใน batch
    for j in range(len(idx)):
        key = idx[j]  # ดัชนีของเอกสารในชุดข้อมูล
        doc_hash_value = hashvalues[j]  # ค่า hashvalue ของเอกสาร

        # สร้าง LeanMinHash สำหรับเอกสาร
        minhash = LeanMinHash(seed=MINHASH_SEED, hashvalues=doc_hash_value)
        neighbors = set(batch["__neighbors__"][j])  # รายการข้อความที่คล้ายคลึงกัน

        # วนลูปผ่านข้อความแต่ละคน
        for neighbor in neighbors:
            if neighbor == key:  # ถ้าข้อความเป็นตัวเอง ให้ข้ามไป
                continue
            # ดึงเอกสารข้อความจากชุดข้อมูลการฝึก
            reference = pretrain_dataset_minhash[int(neighbor)]
            # สร้าง LeanMinHash สำหรับข้อความ
            reference_signature = LeanMinHash(
                seed=MINHASH_SEED, hashvalues=reference["hashvalues"]
            )
            # คำนวณระยะทาง Jaccard ระหว่างเอกสารและข้อความ
            score = minhash.jaccard(reference_signature)
            if score > thresold:  # ถ้าคะแนน Jaccard มากกว่าเกณฑ์ที่กำหนด
                # เพิ่มผลลัพธ์ที่ซ้ำกันในรายการ
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
                break  # หยุดการวนลูปเพราะพบข้อความซ้ำแล้ว

    dict_of_lists = {}  # สร้างพจนานุกรมสำหรับเก็บผลลัพธ์

    # วนลูปผ่านผลลัพธ์ที่ซ้ำกันและเพิ่มเข้าในพจนานุกรม
    for dictionary in duplicate_results:
        for key, value in dictionary.items():
            if key not in dict_of_lists:
                dict_of_lists[key] = []

            dict_of_lists[key].append(value)

    return dict_of_lists  # ส่งคืนพจนานุกรมของรายการที่ซ้ำกันพร้อมข้อมูลรายละเอียด


def deduplicate(
    pretrain_dataset, pretrain_dataset_minhash, num_perm=128, batch_size=100
):
    """
    ฟังก์ชันนี้มีไว้เพื่อกำจัดข้อมูลที่ซ้ำกันในชุดข้อมูลการฝึก โดยใช้ MinHash และ MinHashLSH
    เพื่อค้นหาและระบุข้อความที่ซ้ำกัน

    Parameters:
    pretrain_dataset (Dataset): ชุดข้อมูลการฝึกที่ต้องการกำจัดข้อมูลซ้ำ
    pretrain_dataset_minhash (Dataset): ชุดข้อมูลการฝึกที่มีลายเซ็น MinHash
    num_perm (int, optional): จำนวน permutations ที่ใช้ในการสร้าง MinHash (ค่าเริ่มต้น: 128)
    batch_size (int, optional): ขนาดของแต่ละ batch สำหรับการประมวลผล (ค่าเริ่มต้น: 100)

    Returns:
    tuple: พจนานุกรมของผลลัพธ์ที่ซ้ำกัน และชุดข้อมูลการฝึกที่ถูกล้างข้อมูลแล้ว
    """

    # สร้างค่า hashvalues ที่ว่างเปล่าเพื่อใช้เปรียบเทียบ
    empty_hashvalues = generate_minhash_signature("", num_perm).hashvalues

    # สร้าง MinHashLSH index สำหรับการค้นหาความคล้ายคลึงกัน
    globals()["minhash_index"] = MinHashLSH(
        threshold=0.9,
        num_perm=num_perm,
    )

    # เพิ่มลายเซ็น MinHash เข้าไปใน MinHashLSH index
    with globals()["minhash_index"].insertion_session() as session:
        for i in tqdm(
            range(0, len(pretrain_dataset_minhash), batch_size),
            dynamic_ncols=True,
            desc="Iterating MinHashes...",
        ):
            batch = pretrain_dataset_minhash[i : i + batch_size]
            for j, hash_value in enumerate(batch["hashvalues"]):
                key = i + j
                session.insert(
                    key, LeanMinHash(seed=MINHASH_SEED, hashvalues=hash_value)
                )

    # ค้นหาข้อความที่คล้ายคลึงกันใน MinHashLSH index
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
        # กรองข้อมูลที่มีข้อความและไม่ใช่ลายเซ็นที่ว่างเปล่า
        lambda x: len(x["__neighbors__"]) > 0
        and not np.array_equal(x["hashvalues"], empty_hashvalues),
        desc="Filtering...",
        num_proc=2,
    )

    print(pretrain_dataset_minhash_result, "pretrain_dataset_minhash_result")

    # ประมวลผลข้อมูลใน batch เพื่อตรวจสอบข้อมูลที่ซ้ำกัน
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

    # รวบรวมดัชนีของข้อมูลที่ต้องการลบออก
    for i in tqdm(
        range(0, len(duplicate_results), batch_size),
        dynamic_ncols=True,
        desc="Collecting index to remove...",
    ):
        batch = duplicate_results[i : i + batch_size]
        for idx in batch["original_id"]:
            original_ids_to_remove.add(idx)

    # กรองข้อมูลที่ซ้ำกันออกจากชุดข้อมูลการฝึก
    pretrain_dataset = pretrain_dataset.filter(
        lambda _, idx: str(idx) not in original_ids_to_remove,
        desc="Filtering...",
        num_proc=2,
        with_indices=True,
    )

    print(pretrain_dataset, "pretrain_dataset")

    return duplicate_results, pretrain_dataset
