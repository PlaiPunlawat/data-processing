import numpy as np
from tqdm.auto import tqdm
from datasets import load_from_disk, Features, Sequence, Value
from datasketch import MinHashLSH, LeanMinHash

from data_processing.core.constants import MINHASH_SEED
from data_processing.core.minhash import generate_minhash_signature

DEFAULT_MINHASH_COL_NAME = "text"
DEFAULT_NUM_PERMUTATION = 128
N_GRAM = 5
MINHASH_SEED = 1


def query_func(item, idx, index):
    """
    ฟังก์ชันนี้มีไว้เพื่อค้นหาข้อคยามที่คล้ายคลึงกันสำหรับเอกสารที่ได้รับมา
    โดยใช้ลายเซ็น MinHash และ MinHashLSH index
    This function searches for similar documents to the given document using MinHash signature and MinHashLSH index.

    Parameters:
    item (dict): เอกสารที่ต้องการค้นหา
                 The document to search for, which includes the pre-generated MinHash signature.
    idx (int): ดัชนีของเอกสารในชุดข้อมูล
               The index of the document in the dataset.
    index (MinHashLSH): ดัชนี MinHashLSH ที่ใช้ในการค้นหาข้อความ
                        The MinHashLSH index used to find similar documents.

    Returns:
    dict: พจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
          A dictionary containing the list of similar documents found and the index of the document.
    """

    # ค้นหาข้อความที่คล้ายคลึงกันโดยใช้ลายเซ็น MinHash และ MinHashLSH index
    # Search for similar documents using MinHash signature and MinHashLSH index.
    neighbors = [
        str(dup_idx)
        for dup_idx in index.query(
            LeanMinHash(seed=MINHASH_SEED, hashvalues=item["hashvalues"]),
        )
        if dup_idx != idx  # ตรวจสอบว่าข้อความที่พบไม่ใช่ตัวเอง
                           # Ensure that the found document is not the same as the current document.
    ]

    # ส่งคืนพจนานุกรมที่มีข้อความที่ค้นพบและดัชนีของเอกสาร
    # Return a dictionary containing the list of similar documents found and the index of the document.
    return {"__neighbors__": neighbors, "idx": idx}


def process_data(batch, idx, pretrain_dataset_minhash, threshold):
    """
    This function processes a batch of data to find duplicate documents by comparing MinHash signatures
    and returns the detected duplicates.

    ฟังก์ชันนี้มีไว้เพื่อประมวลผลข้อมูลชุดหนึ่งเพื่อค้นหาข้อความที่ซ้ำกัน
    โดยใช้การเปรียบเทียบลายเซ็น MinHash และส่งคืนข้อมูลที่พบว่าซ้ำกัน

    Parameters:
    batch (dict): A batch of data to process, including MinHash signatures.
                  ข้อมูลที่ถูกแบ่งเป็นชุดย่อยเพื่อประมวลผล
    idx (list of int): A list of indices identifying the data in the dataset.
                       รายการของดัชนีที่ใช้ระบุข้อมูลในชุดข้อมูล
    pretrain_dataset_minhash (dict): The dataset containing MinHash signatures for the documents.
                                     ชุดข้อมูลที่ประกอบด้วยลายเซ็น MinHash สำหรับข้อมูลที่ต้องการตรวจสอบ
    threshold (float): The threshold value used to determine duplicates.
                       ค่าที่ใช้เป็นเกณฑ์ในการตัดสินว่าข้อมูลใดควรถูกพิจารณาว่าเป็นข้อมูลซ้ำ

    Returns:
    dict_of_lists (dict): A dictionary containing lists of duplicate data found.
                          พจนานุกรมที่ประกอบด้วยรายการของข้อมูลที่พบว่าซ้ำกัน
    """

    # Initialize a list to store the results of detected duplicates.
    duplicate_results = []
    # สร้างรายการเพื่อเก็บข้อมูลที่พบว่าซ้ำกัน
    # Retrieve the MinHash signatures from the batch.
    hashvalues = batch["hashvalues"]
    # ดึงค่าลายเซ็น MinHash จากข้อมูลที่รับมา

    # Loop over each document in the batch.
    # วนลูปผ่านแต่ละเอกสารใน batch
    for j in range(len(idx)):
        key = idx[j]
        doc_hash_value = hashvalues[j]

        # Create a LeanMinHash object for the current document.
        # สร้าง LeanMinHash สำหรับเอกสารปัจจุบัน
        minhash = LeanMinHash(seed=MINHASH_SEED, hashvalues=doc_hash_value)
        # Retrieve the list of similar documents.
        neighbors = set(batch["__neighbors__"][j])
        # ดึงรายการเอกสารที่คล้ายกัน

        # Loop through the similar documents (neighbors).
        # วนลูปผ่านเอกสารที่คล้ายกัน
        for neighbor in neighbors:
            if neighbor == key:
                continue  # Skip if the neighbor is the document itself.
                # ข้ามเอกสารที่เป็นตัวเอง
            reference = pretrain_dataset_minhash[int(neighbor)]
            reference_signature = LeanMinHash(
                seed=MINHASH_SEED, hashvalues=reference["hashvalues"]
            )
            # Calculate the Jaccard score.
            score = minhash.jaccard(reference_signature)
            # คำนวณคะแนน Jaccard

            # If the score exceeds the threshold, consider it a duplicate.
            # ถ้าคะแนนมากกว่าหรือเท่ากับเกณฑ์ที่กำหนด ให้ถือว่าเป็นข้อมูลซ้ำ
            if score > threshold:
                duplicate_results.append(
                    {
                        "duplicate_id": neighbor,
                        "duplicate_text": reference["text"],
                        "duplicate_dataset": reference["source"],
                        "original_dataset": batch["source"][j],
                        "original_text": batch["text"][j],
                        "original_id": str(key),
                        "score": score,
                    }
                )
                break  # Stop checking once a duplicate is found.
                # หยุดการตรวจสอบเมื่อพบข้อมูลซ้ำ

    # Initialize a dictionary to organize the duplicate results.
    dict_of_lists = {}
    # สร้างพจนานุกรมเพื่อนำผลลัพธ์ที่พบมาจัดเก็บ

    # Loop through the list of detected duplicates and organize them into the dictionary.
    # วนลูปผ่านข้อมูลซ้ำที่พบ และจัดเก็บในรูปแบบพจนานุกรม
    for dictionary in duplicate_results:
        for key, value in dictionary.items():
            if key not in dict_of_lists:
                dict_of_lists[key] = []

            dict_of_lists[key].append(value)

    # Return the dictionary of detected duplicates.
    # ส่งคืนพจนานุกรมที่มีข้อมูลซ้ำที่พบ
    return dict_of_lists


def prepare_dataset(pretrain_data_args, deduplicate_args):
    """
    This function loads the pretraining dataset and its corresponding MinHash signatures from disk.
    ฟังก์ชันนี้มีไว้เพื่อโหลดชุดข้อมูลการฝึกอบรมและลายเซ็น MinHash ที่เกี่ยวข้องจากดิสก์

    Parameters:
    pretrain_data_args (object/dict): Contains configuration details including the path to the pretraining dataset.
                                      มีรายละเอียดการกำหนดค่า รวมถึงเส้นทางไปยังชุดข้อมูลการฝึกอบรม
    deduplicate_args (object/dict): Contains configuration details including the path to the MinHash signatures.
                                    มีรายละเอียดการกำหนดค่า รวมถึงเส้นทางไปยังลายเซ็น MinHash

    Returns:
    tuple: A tuple containing the pretraining dataset and MinHash signatures.
           ทูเพิลที่ประกอบด้วยชุดข้อมูลการฝึกอบรมและลายเซ็น MinHash
    """

    # Load the pretraining dataset from the specified path in pretrain_data_args.
    # โหลดชุดข้อมูลการฝึกอบรมจากเส้นทางที่ระบุใน pretrain_data_args
    pretrain_dataset = load_from_disk(pretrain_data_args.path_name)

    # Load the MinHash signatures from the specified path in deduplicate_args.
    # โหลดลายเซ็น MinHash จากเส้นทางที่ระบุใน deduplicate_args
    pretrain_dataset_minhash = load_from_disk(deduplicate_args.minhash_path)

    # Return both the pretraining dataset and the MinHash signatures.
    # ส่งคืนทั้งชุดข้อมูลการฝึกอบรมและลายเซ็น MinHash
    return pretrain_dataset, pretrain_dataset_minhash


def generate_minhash_pretrain_dataset(pretrain_dataset_minhash, deduplicate_args, global_config):
    """
    This function generates and uses a MinHashLSH index to find similar documents in a pretraining dataset
    based on MinHash signatures, and returns the filtered dataset containing only those documents with similar neighbors.

    ฟังก์ชันนี้ใช้เพื่อสร้างและใช้งานดัชนี MinHashLSH เพื่อค้นหาเอกสารที่คล้ายกันในชุดข้อมูลการฝึกอบรม
    โดยอ้างอิงจากลายเซ็น MinHash และส่งคืนชุดข้อมูลที่กรองแล้วซึ่งมีเฉพาะเอกสารที่มีเพื่อนบ้านที่คล้ายกัน

    Parameters:
    pretrain_dataset_minhash (Dataset): A dataset containing MinHash signatures for each document.
                                        ชุดข้อมูลที่มีลายเซ็น MinHash สำหรับแต่ละเอกสาร
    deduplicate_args (object/dict): Arguments for deduplication, including threshold and batch size.
                                    อาร์กิวเมนต์สำหรับการกำจัดข้อมูลซ้ำ รวมถึงเกณฑ์และขนาดแบทช์
    global_config (object/dict): Global configuration settings, including num_perm and num_process.
                                 การตั้งค่าการกำหนดค่าทั่วไป รวมถึง num_perm และ num_process

    Returns:
    pretrain_dataset_minhash_result (Dataset): A filtered dataset containing only documents with similar neighbors.
                                               ชุดข้อมูลที่กรองแล้วซึ่งมีเฉพาะเอกสารที่มีเพื่อนบ้านที่คล้ายกัน
    """

    # Generate an empty MinHash signature for comparison purposes.
    # สร้างลายเซ็น MinHash ว่างสำหรับใช้ในการเปรียบเทียบ
    empty_hashvalues = generate_minhash_signature(
        "", global_config.num_perm).hashvalues

    # Initialize a MinHashLSH index for efficient similarity search.
    # เริ่มต้นดัชนี MinHashLSH สำหรับการค้นหาความคล้ายคลึงกันอย่างมีประสิทธิภาพ
    globals()["minhash_index"] = MinHashLSH(
        threshold=deduplicate_args.thresold,
        num_perm=global_config.num_perm,
    )

    # Insert the MinHash signatures into the LSH index in batches.
    # แทรกลายเซ็น MinHash ลงในดัชนี LSH เป็นชุดๆ
    with globals()["minhash_index"].insertion_session() as session:
        for i in tqdm(
            range(0, len(pretrain_dataset_minhash),
                  deduplicate_args.batch_size),
            dynamic_ncols=True,
            # Status message during MinHash iteration.
            desc="Iterating MinHashes...",
            # ข้อความสถานะระหว่างการทำซ้ำ MinHash
        ):
            batch = pretrain_dataset_minhash[i: i +
                                             deduplicate_args.batch_size]
            for j, hash_value in enumerate(batch["hashvalues"]):
                key = i + j
                session.insert(
                    key, LeanMinHash(seed=MINHASH_SEED, hashvalues=hash_value)
                )

    # Query the MinHash index to find similar (duplicate) documents.
    # สอบถามดัชนี MinHash เพื่อค้นหาเอกสารที่คล้ายกัน (ซ้ำกัน)
    pretrain_dataset_minhash_result = pretrain_dataset_minhash.map(
        lambda doc, idx: query_func(
            doc, idx, index=globals()["minhash_index"]),
        desc="Querying...",  # Status message during querying.
                             # ข้อความสถานะระหว่างการสอบถาม
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
        lambda x: len(x["__neighbors__"]) > 0
        and not np.array_equal(x["hashvalues"], empty_hashvalues),
        desc="Filtering...",  # Status message during filtering.
                              # ข้อความสถานะระหว่างการกรอง
        num_proc=global_config.num_process,
    )

    return pretrain_dataset_minhash_result


def indentify_duplicate_pretrain_dataset(pretrain_dataset_minhash, pretrain_dataset_minhash_result, deduplicate_args, global_config):
    """
    This function identifies duplicate documents in a pretraining dataset by comparing MinHash signatures.
    It processes the results from a previous MinHash comparison to extract specific duplicate details.

    ฟังก์ชันนี้มีไว้เพื่อระบุเอกสารที่ซ้ำกันในชุดข้อมูลการฝึกอบรมล่วงหน้าโดยการเปรียบเทียบลายเซ็น MinHash
    โดยจะประมวลผลผลลัพธ์จากการเปรียบเทียบ MinHash ก่อนหน้านี้เพื่อดึงรายละเอียดของข้อมูลที่ซ้ำกัน

    Parameters:
    pretrain_dataset_minhash (Dataset): A dataset containing MinHash signatures for reference documents.
                                        ชุดข้อมูลที่มีลายเซ็น MinHash สำหรับเอกสารอ้างอิง
    pretrain_dataset_minhash_result (Dataset): A dataset containing results from an initial MinHash comparison.
                                               ชุดข้อมูลที่มีผลลัพธ์จากการเปรียบเทียบ MinHash เบื้องต้น
    deduplicate_args (object/dict): Deduplication settings, including the similarity threshold.
                                    การตั้งค่าสำหรับการกำจัดข้อมูลซ้ำ รวมถึงเกณฑ์ความคล้ายคลึง
    global_config (object/dict): Global configuration settings, including the number of processes to use.
                                 การตั้งค่าทั่วไป รวมถึงจำนวน process ที่จะใช้

    Returns:
    duplicate_results (Dataset): A dataset containing details of identified duplicates, including IDs, text, and scores.
                                 ชุดข้อมูลที่มีรายละเอียดของข้อมูลที่ซ้ำกัน รวมถึง ID ข้อความ และคะแนนความคล้ายคลึง
    """

    # Map through the MinHash result dataset to identify duplicates by processing each batch.
    # วนลูปผ่านชุดข้อมูลผลลัพธ์ MinHash เพื่อระบุข้อมูลที่ซ้ำกันโดยประมวลผลแต่ละชุด
    duplicate_results = pretrain_dataset_minhash_result.map(
        lambda batch, idx: process_data(
            batch, idx, pretrain_dataset_minhash, deduplicate_args.thresold
        ),
        # Process in batches to handle large datasets efficiently.
        batched=True,
        # ประมวลผลเป็นชุดเพื่อจัดการกับชุดข้อมูลขนาดใหญ่ได้อย่างมีประสิทธิภาพ
        with_indices=True,  # Include indices for reference during processing.
                            # รวมดัชนีเพื่อใช้อ้างอิงในระหว่างการประมวลผล
        # Use multiple processes as defined in global_config.
        num_proc=global_config.num_process,
        # ใช้หลาย process ตามที่กำหนดใน global_config
        # Remove original columns to focus on duplicates.
        remove_columns=pretrain_dataset_minhash_result.column_names,
        # ลบคอลัมน์เดิมเพื่อเน้นที่ข้อมูลซ้ำ
        # Do not load from cache to ensure fresh processing.
        load_from_cache_file=False,
        # ไม่โหลดจากแคชเพื่อให้แน่ใจว่าประมวลผลใหม่
        features=Features(
            {
                # Store the ID of the duplicate document.
                "duplicate_id": Value("int32"),
                # เก็บ ID ของเอกสารที่ซ้ำกัน
                # Store the text of the duplicate document.
                "duplicate_text": Value("string"),
                # เก็บข้อความของเอกสารที่ซ้ำกัน
                # Store the source dataset of the duplicate.
                "duplicate_dataset": Value("string"),
                # เก็บชุดข้อมูลแหล่งที่มาของข้อมูลที่ซ้ำกัน
                # Store the original dataset of the document.
                "original_dataset": Value("string"),
                # เก็บชุดข้อมูลต้นฉบับของเอกสาร
                # Store the text of the original document.
                "original_text": Value("string"),
                # เก็บข้อความของเอกสารต้นฉบับ
                # Store the ID of the original document.
                "original_id": Value("string"),
                # เก็บ ID ของเอกสารต้นฉบับ
                # Store the similarity score (Jaccard index) between documents.
                "score": Value("float32"),
                # เก็บคะแนนความคล้ายคลึง (ดัชนี Jaccard) ระหว่างเอกสาร
            }
        ),
    )

    # Return the dataset containing details of detected duplicates.
    return duplicate_results
    # ส่งคืนชุดข้อมูลที่มีรายละเอียดของข้อมูลที่ซ้ำกันที่ตรวจพบ


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


def deduplicate_pretrain_dataset(pretrain_dataset, duplicate_results, pretrain_data_args, deduplicate_args, global_config):
    """
    This function removes duplicate entries from the pretraining dataset based on identified duplicate results.

    ฟังก์ชันนี้ใช้ในการลบข้อมูลซ้ำออกจากชุดข้อมูลการฝึกสอนล่วงหน้าตามผลลัพธ์ที่ระบุว่าเป็นข้อมูลซ้ำ

    Parameters:
    pretrain_dataset: The dataset that will be filtered to remove duplicates.
                      ชุดข้อมูลที่จะถูกกรองเพื่อลบข้อมูลซ้ำ
    duplicate_results: The collection of results containing information about duplicate entries.
                       คอลเลกชันของผลลัพธ์ที่มีข้อมูลเกี่ยวกับรายการข้อมูลซ้ำ
    pretrain_data_args: Arguments related to the pretraining data.
                        อาร์กิวเมนต์ที่เกี่ยวข้องกับข้อมูลการฝึกสอนล่วงหน้า
    deduplicate_args: Arguments specific to the deduplication process.
                      อาร์กิวเมนต์เฉพาะสำหรับกระบวนการลบข้อมูลซ้ำ
    global_config: General configuration parameters.
                   พารามิเตอร์การกำหนดค่าทั่วไป

    Returns:
    pretrain_dataset: The cleaned dataset with duplicates removed.
                      ชุดข้อมูลที่ถูกล้างข้อมูลแล้วโดยลบข้อมูลซ้ำออก
    """

    # Initialize a set to collect IDs of duplicates to remove.
    # สร้างชุดเพื่อรวบรวมรหัสของข้อมูลซ้ำที่จะลบ
    original_ids_to_remove = set()

    # Collect the indices of the original documents that should be removed.
    # รวบรวมดัชนีของเอกสารต้นฉบับที่ควรถูกลบออก
    for i in tqdm(
        range(0, len(duplicate_results), deduplicate_args.batch_size),
        dynamic_ncols=True,
        # Status message during index collection.
        desc="Collecting index to remove...",
        # ข้อความสถานะระหว่างการรวบรวมดัชนี
    ):
        batch = duplicate_results[i: i + deduplicate_args.batch_size]
        for idx in batch["original_id"]:
            original_ids_to_remove.add(idx)

    # Filter out the duplicates from the original pretraining dataset.
    # กรองข้อมูลซ้ำออกจากชุดข้อมูลการฝึกสอนล่วงหน้าต้นฉบับ
    pretrain_dataset[pretrain_data_args.split] = pretrain_dataset[
        pretrain_data_args.split
    ].filter(
        lambda _, idx: str(idx) not in original_ids_to_remove,
        desc="Filtering...",  # Status message during filtering.
                              # ข้อความสถานะระหว่างการกรอง
        num_proc=global_config.num_process,
        with_indices=True,
    )

    # Return the cleaned dataset.
    # ส่งคืนชุดข้อมูลที่ถูกล้างข้อมูลแล้ว
    return pretrain_dataset


def deduplicate(pretrain_data_args, deduplicate_args, global_config):
    """
    This function is designed to remove duplicate documents from a pretraining dataset by using MinHash signatures.
    It identifies and filters out duplicates based on a specified threshold, ensuring the dataset's uniqueness.

    ฟังก์ชันนี้มีไว้เพื่อลบเอกสารที่ซ้ำกันออกจากชุดข้อมูลสำหรับการฝึกสอนโดยใช้ลายเซ็น MinHash
    ฟังก์ชันนี้จะระบุและกรองข้อมูลซ้ำโดยใช้เกณฑ์ที่กำหนดเพื่อให้มั่นใจว่าชุดข้อมูลไม่มีความซ้ำซ้อน

    Parameters:
    pretrain_data_args (Namespace): Arguments related to the pretraining data, including the path name.
                                    ข้อโต้แย้งที่เกี่ยวข้องกับข้อมูลการฝึกสอนล่วงหน้า รวมถึงชื่อเส้นทาง
    deduplicate_args (Namespace): Arguments related to the deduplication process, including the MinHash path and threshold.
                                  ข้อโต้แย้งที่เกี่ยวข้องกับกระบวนการลบความซ้ำซ้อน รวมถึงเส้นทาง MinHash และเกณฑ์
    global_config (Namespace): Configuration settings such as the number of permutations and processes.
                               การตั้งค่าคอนฟิก เช่น จำนวนการเรียงสับเปลี่ยนและกระบวนการ

    Returns:
    None: The function modifies the dataset in place and saves the deduplicated version to disk.
          ไม่มี: ฟังก์ชันนี้แก้ไขชุดข้อมูลในสถานที่และบันทึกเวอร์ชันที่ลบความซ้ำซ้อนแล้วลงดิสก์
    """

    # Load the pretraining dataset and the corresponding MinHash signatures from disk.
    # โหลดชุดข้อมูลการฝึกอบรมล่วงหน้าและลายเซ็น MinHash ที่เกี่ยวข้องจากดิสก์
    pretrain_dataset, pretrain_dataset_minhash = prepare_dataset(
        pretrain_data_args, deduplicate_args)

    # Debugging print statement to verify the loaded MinHash dataset.
    # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันการโหลดชุดข้อมูล MinHash
    print(pretrain_dataset_minhash, "pretrain_dataset_minhash")

    # Query the MinHash index to find similar (duplicate) documents.
    # สอบถามดัชนี MinHash เพื่อค้นหาเอกสารที่คล้ายกัน (ซ้ำกัน)
    pretrain_dataset_minhash_result = generate_minhash_pretrain_dataset(
        pretrain_dataset_minhash, deduplicate_args, global_config)

    # Debugging print statement to verify the results of the MinHash queries.
    # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันผลลัพธ์ของการสอบถาม MinHash
    print(pretrain_dataset_minhash_result, "pretrain_dataset_minhash_result")

    # Process the query results to identify duplicates.
    # ประมวลผลผลการสอบถามเพื่อระบุข้อมูลซ้ำ
    duplicate_results = indentify_duplicate_pretrain_dataset(
        pretrain_dataset_minhash, pretrain_dataset_minhash_result, deduplicate_args, global_config)

    # Debugging print statement to verify the detected duplicates.
    # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันการตรวจหาข้อมูลซ้ำ
    print(duplicate_results, "duplicate_results")

    # Save the duplicate detection results to disk.
    # บันทึกผลการตรวจหาข้อมูลซ้ำลงดิสก์
    save_dataset_to_disk(
        duplicate_results, deduplicate_args.save_path_duplicated)

    # Filter out the duplicates from the original pretraining dataset.
    # กรองข้อมูลซ้ำออกจากชุดข้อมูลการฝึกสอนล่วงหน้าต้นฉบับ
    deduplicated_pretrain_dataset = deduplicate_pretrain_dataset(
        pretrain_dataset, duplicate_results, pretrain_data_args, deduplicate_args, global_config)

    # Debugging print statement to verify the final filtered dataset.
    # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันชุดข้อมูลที่กรองแล้ว
    print(deduplicated_pretrain_dataset, "deduplicated_pretrain_dataset")

    # Save the filtered pretraining dataset back to disk.
    # บันทึกชุดข้อมูลการฝึกสอนที่กรองแล้วกลับลงดิสก์
    # pretrain_dataset.save_to_disk(deduplicate_args.save_path)
    save_dataset_to_disk(
        deduplicated_pretrain_dataset, deduplicate_args.save_path)
