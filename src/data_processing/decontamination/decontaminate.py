import pickle

import numpy as np
from tqdm.auto import tqdm
from datasets import load_from_disk, Features, Sequence, Value
from datasketch import MinHashLSH, LeanMinHash
import pandas as pd

from data_processing.core.constants import MINHASH_SEED
from data_processing.core.minhash import generate_minhash_signature
from data_processing.decontamination.utils import (
    load_data,
)


def query_func(item, idx, index):
    """
    This function is designed to find similar text for a given document by utilizing MinHash signatures and a MinHashLSH index.
    ฟังก์ชันนี้มีไว้เพื่อค้นหาข้อความที่คล้ายคลึงกันสำหรับเอกสารที่ได้รับมา โดยใช้ลายเซ็น MinHash และ MinHashLSH index

    Parameters:
    item (dict): The document to search for, which includes various information such as hashvalues.
                 เอกสารที่ต้องการค้นหาข้อความ ประกอบด้วยข้อมูลต่าง ๆ รวมถึง hashvalues
    idx (int): The index of the document in the dataset.
               ดัชนีของเอกสารในชุดข้อมูล
    index (MinHashLSH): The MinHashLSH index used to find similar documents.
                        ดัชนี MinHashLSH ที่ใช้ในการค้นหาข้อความ

    Returns:
    dict: A dictionary containing the list of similar documents found and the index of the document.
          พจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
    """

    # Search for similar documents using MinHash signatures and the MinHashLSH index.
    # ค้นหาข้อความที่คล้ายคลึงกันโดยใช้ลายเซ็น MinHash และ MinHashLSH index
    neighbors = [
        str(dup_idx)  # Convert the index of the similar document to a string.
        # แปลงดัชนีของข้อความเป็นสตริง
        for dup_idx in index.query(
            LeanMinHash(
                seed=MINHASH_SEED, hashvalues=item["hashvalues"]
            ),  # Create a LeanMinHash object using the document's hashvalues.
            # สร้าง LeanMinHash จาก hashvalues ของเอกสาร
        )
    ]

    # Return a dictionary with the similar documents and the index of the document.
    # ส่งคืนพจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
    return {"__neighbors__": neighbors, "idx": idx}

def decontaminate(
    dataset_groups, pretrain_data_args, decontaminate_args, global_config
):
    """
    This function is used to remove contaminated data from a pretraining dataset by using MinHash and MinHashLSH techniques.
    It identifies and removes similar text from the dataset to ensure data cleanliness.

    ฟังก์ชันนี้มีไว้เพื่อกำจัดข้อมูลปนเปื้อนจากชุดข้อมูลการฝึก โดยใช้เทคนิค MinHash และ MinHashLSH
    เพื่อค้นหาและระบุข้อความที่คล้ายคลึงกันและลบออกจากชุดข้อมูล

    Parameters:
    dataset_groups (dict): A collection of dataset groups to be processed.
                           กลุ่มของชุดข้อมูลที่ต้องการประมวลผล
    pretrain_data_args (Namespace): Arguments used to load the pretraining dataset.
                                    อาร์กิวเมนต์ที่ใช้ในการโหลดชุดข้อมูลการฝึก
    decontaminate_args (Namespace): Arguments used for decontaminating the data.
                                    อาร์กิวเมนต์ที่ใช้ในการกำจัดข้อมูลปนเปื้อน
    global_config (Namespace): General settings like the number of permutations and the number of processes.
                               การตั้งค่าทั่วไป เช่น จำนวน permutations และจำนวน process

    Returns:
    None
    ไม่มีค่าออกมา
    """

    # Define the number of permutations to be used in MinHash creation.
    # กำหนดจำนวน permutations ที่จะใช้ในการสร้าง MinHash
    num_perm = global_config.num_perm

    # Generate empty hash values for comparison purposes.
    # สร้างค่า hashvalues ที่ว่างเปล่าเพื่อใช้เปรียบเทียบ
    empty_hashvalues = generate_minhash_signature("", num_perm).hashvalues

    # Load the pretraining dataset.
    # โหลดชุดข้อมูลการฝึก
    pretrain_dataset = load_data(pretrain_data_args)

    # Load the saved MinHash dataset.
    # โหลดชุดข้อมูล MinHash ที่บันทึกไว้
    pretrain_dataset_minhash = load_from_disk(decontaminate_args.minhash_path)

    contaminated_results = []  # A list to store contaminated data results.
    # รายการเก็บผลลัพธ์ของข้อมูลที่ปนเปื้อน

    # Iterate over each dataset group.
    # วนลูปผ่านกลุ่มข้อมูลแต่ละกลุ่ม
    for dataset_key in tqdm(dataset_groups.keys()):
        print(dataset_key)

        dataset_arg = dataset_groups[dataset_key]

        # Paths to temporary signature and data files.
        # เส้นทางไปยังไฟล์ลายเซ็นและไฟล์ข้อมูลที่เก็บไว้ชั่วคราว
        signature_path = (
            f"./temp/{dataset_key}_{dataset_arg.split}_signature_{num_perm}.pickle"
        )
        file_path = f"./temp/{dataset_key}_{dataset_arg.split}_file_{num_perm}.pickle"

        # Load data and signatures from temporary files.
        # โหลดข้อมูลและลายเซ็นจากไฟล์ที่เก็บไว้ชั่วคราว
        with open(file_path, "rb") as file:
            data = pickle.load(file)

        with open(signature_path, "rb") as file:
            signature = pickle.load(file)

        # Create a MinHashLSH index for similarity searching.
        # สร้าง MinHashLSH index สำหรับการค้นหาความคล้ายคลึงกัน
        globals()[dataset_key] = MinHashLSH(
            threshold=decontaminate_args.thresold,
            num_perm=num_perm,
        )
        
        # Add MinHash signatures to the MinHashLSH index.
        # เพิ่มลายเซ็น MinHash เข้าไปใน MinHashLSH index
        with globals()[dataset_key].insertion_session() as session:
            for i, item in enumerate(signature):
                session.insert(i, item)

        # Search for similar text in the MinHashLSH index.
        # ค้นหาข้อความที่คล้ายคลึงกันใน MinHashLSH index
        pretrain_dataset_minhash_result = pretrain_dataset_minhash.map(
            lambda doc, idx: query_func(doc, idx, index=globals()[dataset_key]),
            desc="Querying...",
            num_proc=global_config.num_process,
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
            # Filter out documents that have text and non-empty signatures.
            # กรองข้อมูลที่มีข้อความและไม่ใช่ลายเซ็นที่ว่างเปล่า
            lambda x: len(x["__neighbors__"]) > 0
            and not np.array_equal(x["hashvalues"], empty_hashvalues),
            desc="Filtering...",
            num_proc=global_config.num_process,
        )
        print(pretrain_dataset_minhash_result, "pretrain_dataset_minhash_result")

        # Calculate Jaccard distance and identify contaminated data.
        # คำนวณระยะทาง Jaccard และระบุข้อมูลที่ปนเปื้อน
        for doc in tqdm(
            pretrain_dataset_minhash_result, desc="Calculation Jaccard Distance..."
        ):
            neighbors = set(doc["__neighbors__"])
            minhash = LeanMinHash(seed=MINHASH_SEED, hashvalues=doc["hashvalues"])
            for neighbor in neighbors:
                reference = data[int(neighbor)]
                reference_signature = signature[int(neighbor)]
                score = minhash.jaccard(reference_signature)
                if score > decontaminate_args.thresold:
                    contaminated_results.append(
                        {
                            "duplicate_id": neighbor,
                            "duplicate_text": reference,
                            "duplicate_dataset": dataset_key,
                            "original_dataset": doc["source"],
                            "original_text": doc[pretrain_data_args.col_name],
                            "original_id": doc["idx"],
                            "score": score,
                        }
                    )
                    break
        print(len(contaminated_results), "len(contaminated_results)")

    # Save contaminated results to a CSV file.
    # บันทึกผลลัพธ์ที่ปนเปื้อนไปยังไฟล์ CSV
    df = pd.DataFrame(contaminated_results)
    df.to_csv(f"contaminated_results_{num_perm}.csv")

    # Identify the IDs to remove from the original dataset.
    # ระบุ ID ที่ต้องการลบออกจากข้อมูลต้นฉบับ
    original_ids_to_remove = set()
    for item in contaminated_results:
        original_ids_to_remove.add(item["original_id"])

    # Filter out the contaminated data from the pretraining dataset.
    # กรองข้อมูลปนเปื้อนออกจากชุดข้อมูลฝึก
    pretrain_dataset[pretrain_data_args.split] = pretrain_dataset[
        pretrain_data_args.split
    ].filter(
        lambda _, idx: idx not in original_ids_to_remove,
        desc="Filtering...",
        num_proc=global_config.num_process,
        with_indices=True,
    )
    print(pretrain_dataset)

    # Save the cleaned pretraining dataset to the specified storage.
    # บันทึกชุดข้อมูลที่ถูกล้างข้อมูลแล้วไปยังที่เก็บข้อมูลที่กำหนด
    pretrain_dataset.save_to_disk(decontaminate_args.save_path)
