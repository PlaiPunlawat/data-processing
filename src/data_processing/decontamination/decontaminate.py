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


def prepare_dataset(pretrain_data_args, decontaminate_args):
    """
    This function is used to load and prepare the pretraining dataset and its corresponding MinHash signatures 
    for further processing, such as decontamination or deduplication.

    ฟังก์ชันนี้มีไว้เพื่อโหลดและเตรียมชุดข้อมูลการฝึกอบรมล่วงหน้าและลายเซ็น MinHash ที่เกี่ยวข้อง
    สำหรับการประมวลผลเพิ่มเติม เช่น การกำจัดข้อมูลซ้ำหรือการล้างข้อมูลที่ปนเปื้อน

    Input:
    - pretrain_data_args (Namespace): Arguments related to the pretraining dataset, including its location.
    - decontaminate_args (Namespace): Arguments related to decontamination, including the path to the MinHash signatures.

    Output:
    - tuple: A tuple containing:
      1. pretrain_dataset: The loaded pretraining dataset.
      2. pretrain_dataset_minhash: The loaded MinHash signatures corresponding to the dataset.

    """

    # Load the pretraining dataset using the provided arguments.
    # โหลดชุดข้อมูลการฝึกอบรมล่วงหน้าจากข้อมูลที่ระบุใน pretrain_data_args
    pretrain_dataset = load_data(pretrain_data_args)

    # Load the MinHash signatures for the dataset from the specified path.
    # โหลดลายเซ็น MinHash ของชุดข้อมูลจากเส้นทางที่ระบุใน decontaminate_args
    pretrain_dataset_minhash = load_from_disk(decontaminate_args.minhash_path)

    # Return both the pretraining dataset and its corresponding MinHash signatures.
    # ส่งคืนชุดข้อมูลการฝึกอบรมล่วงหน้าและลายเซ็น MinHash ที่เกี่ยวข้อง
    return pretrain_dataset, pretrain_dataset_minhash


def prepare_dataset_group(dataset_groups, dataset_key, decontaminate_args, global_config):
    """
    This function prepares a group of datasets by loading MinHash signatures and the corresponding dataset,
    and inserting the signatures into a MinHashLSH index for similarity searching.

    ฟังก์ชันนี้เตรียมกลุ่มชุดข้อมูลโดยการโหลดลายเซ็น MinHash และชุดข้อมูลที่เกี่ยวข้อง
    และเพิ่มลายเซ็นเหล่านั้นลงในดัชนี MinHashLSH เพื่อการค้นหาความคล้ายคลึงกัน

    Input:
    - dataset_groups (dict): A dictionary containing different dataset groups.
                             พจนานุกรมที่มีชุดข้อมูลหลายกลุ่ม
    - dataset_key (str): The key used to access a specific dataset group from dataset_groups.
                         คีย์ที่ใช้ในการเข้าถึงกลุ่มชุดข้อมูลเฉพาะจาก dataset_groups
    - decontaminate_args (Namespace): Arguments related to decontamination, including threshold and paths.
                                      อาร์กิวเมนต์ที่เกี่ยวข้องกับการกำจัดการปนเปื้อน รวมถึงเกณฑ์และเส้นทางต่างๆ
    - global_config (Namespace): Configuration settings such as number of permutations for MinHash.
                                 การตั้งค่าการกำหนดค่าทั่วไป เช่น จำนวน permutations สำหรับ MinHash

    Output:
    - tuple: A tuple containing:
        1. data: The dataset loaded from the temporary file.
                 ชุดข้อมูลที่โหลดจากไฟล์ชั่วคราว
        2. signature: The MinHash signatures loaded from the temporary file.
                      ลายเซ็น MinHash ที่โหลดจากไฟล์ชั่วคราว
    """

    # Define the number of permutations to be used in MinHash creation.
    # กำหนดจำนวน permutations ที่จะใช้ในการสร้าง MinHash
    num_perm = global_config.num_perm

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

    return data, signature


def generate_minhash_pretrain_dataset(pretrain_dataset_minhash, empty_hashvalues, dataset_key, global_config):
    """
    This function generates a pretraining dataset by identifying and filtering similar documents
    using a MinHashLSH index. It returns the resulting dataset after filtering.

    ฟังก์ชันนี้สร้างชุดข้อมูลการฝึกโดยการระบุและกรองเอกสารที่คล้ายกัน
    โดยใช้ดัชนี MinHashLSH และส่งคืนชุดข้อมูลที่ได้หลังจากการกรอง

    Input:
    - pretrain_dataset_minhash (Dataset): The dataset containing MinHash signatures to process.
                                          ชุดข้อมูลที่มีลายเซ็น MinHash สำหรับการประมวลผล
    - empty_hashvalues (ndarray): The empty hashvalues used for comparison to filter out incomplete entries.
                                  ลายเซ็น MinHash ว่างที่ใช้เปรียบเทียบเพื่อกรองข้อมูลที่ไม่สมบูรณ์
    - dataset_key (str): The key used to access the MinHashLSH index in the global variables.
                         คีย์ที่ใช้ในการเข้าถึงดัชนี MinHashLSH ในตัวแปร global
    - global_config (Namespace): Configuration settings including number of processes to use for parallel execution.
                                 การตั้งค่าการกำหนดค่า รวมถึงจำนวน process สำหรับการประมวลผลขนาน

    Output:
    - pretrain_dataset_minhash_result (Dataset): The filtered dataset containing documents with non-empty hashvalues 
                                                 and identified neighbors from the MinHashLSH index.
                                                 ชุดข้อมูลที่ผ่านการกรอง ซึ่งมีเอกสารที่มีลายเซ็นไม่ว่างเปล่าและมีเพื่อนบ้านที่ระบุจากดัชนี MinHashLSH
    """

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

    return pretrain_dataset_minhash_result


def contaminated_pretrain_dataset(pretrain_dataset_minhash_result, data, signature, dataset_key, pretrain_data_args, decontaminate_args):

    contaminated_results = []

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

    return contaminated_results


def save_dataset_to_disk(dataset, save_path):
    """
    This function saves a given dataset to a specified location on the disk.
    ฟังก์ชันนี้มีไว้เพื่อบันทึกชุดข้อมูลที่กำหนดไปยังที่ตั้งที่ระบุบนดิสก์

    Parameters:
    dataset: The dataset to be saved. It must be compatible with the save_to_disk method.
             ชุดข้อมูลที่จะถูกบันทึก จะต้องเป็นวัตถุที่รองรับวิธี save_to_disk
    save_path (str): The file path where the dataset should be saved.
                     เส้นทางไฟล์ที่ชุดข้อมูลจะถูกบันทึก
    """

    # Save the dataset to the specified path on the disk.
    # บันทึกชุดข้อมูลไปยังเส้นทางที่ระบุบนดิสก์
    dataset.save_to_disk(save_path)


def indentify_decontaminate_pretrain_dataset(contaminated_results, pretrain_dataset, pretrain_data_args, global_config):

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

    return pretrain_dataset


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

    # Get the number of permutations from global_config
    # ดึงจำนวนการแฮช MinHash จาก global_config
    num_perm = global_config.num_perm

    # Initialize a list to store contaminated results
    # สร้างรายการเพื่อเก็บข้อมูลที่ปนเปื้อน
    contaminated_results = []

    # Generate an empty MinHash signature to compare with real signatures later
    # สร้างลายเซ็น MinHash ว่างเพื่อใช้ในการเปรียบเทียบกับลายเซ็นจริงในภายหลัง
    empty_hashvalues = generate_minhash_signature("", num_perm).hashvalues

    # Load pretraining dataset and MinHash dataset from disk
    # โหลดชุดข้อมูลการฝึกและชุดข้อมูล MinHash จากดิสก์
    pretrain_dataset, pretrain_dataset_minhash = prepare_dataset(
        pretrain_data_args, decontaminate_args)

    # Iterate over each dataset group.
    # วนลูปผ่านกลุ่มข้อมูลแต่ละกลุ่ม
    for dataset_key in tqdm(dataset_groups.keys()):
        print(dataset_key)

        # Prepare data and signatures for each dataset group
        # เตรียมข้อมูลและลายเซ็นสำหรับแต่ละกลุ่มข้อมูล
        data, signature = prepare_dataset_group(
            dataset_groups, dataset_key, decontaminate_args, global_config)

        # Generate MinHash results for the pretraining dataset
        # สร้างผลลัพธ์ MinHash สำหรับชุดข้อมูลการฝึก
        pretrain_dataset_minhash_result = generate_minhash_pretrain_dataset(
            pretrain_dataset_minhash, empty_hashvalues, dataset_key, global_config)
        print(pretrain_dataset_minhash_result,
              "pretrain_dataset_minhash_result")

        # Calculate Jaccard distance and identify contaminated data.
        # คำนวณระยะทาง Jaccard และระบุข้อมูลที่ปนเปื้อน
        contaminated_pretrain = contaminated_pretrain_dataset(
            pretrain_dataset_minhash_result, data, signature, decontaminate_args)

        # Add contaminated data to the results list
        # เพิ่มข้อมูลที่ปนเปื้อนเข้าไปในรายการผลลัพธ์
        contaminated_results.extend(contaminated_pretrain)
        print(len(contaminated_results), "len(contaminated_results)")

    # Save contaminated results to a CSV file.
    # บันทึกผลลัพธ์ที่ปนเปื้อนไปยังไฟล์ CSV
    df = pd.DataFrame(contaminated_results)
    save_dataset_to_disk(df, f"contaminated_results_{num_perm}.csv")

    # Identify and remove contaminated data from the pretraining dataset
    # ระบุและลบข้อมูลที่ปนเปื้อนออกจากชุดข้อมูลการฝึก
    prepare_dataset = indentify_decontaminate_pretrain_dataset(
        contaminated_results, pretrain_dataset, pretrain_data_args, global_config)
    print(pretrain_dataset)

    # Save the cleaned pretraining dataset to the specified storage.
    # บันทึกชุดข้อมูลที่ถูกล้างข้อมูลแล้วไปยังที่เก็บข้อมูลที่กำหนด
    save_dataset_to_disk(pretrain_dataset, decontaminate_args.save_path)
