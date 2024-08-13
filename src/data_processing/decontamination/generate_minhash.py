from data_processing.core.minhash import (
    generate_minhash_signature,
    generate_minhash_signature_hf,
)
from data_processing.decontamination.utils import (
    MAPPER,
    load_data,
)
from tqdm.auto import tqdm

import pickle
from multiprocessing import Pool
from nlpo3 import load_dict


def generate_minhash_item(item):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับข้อความที่ได้รับมา

    Parameters:
    item (tuple): ทูเพิลที่ประกอบด้วยข้อความ (text) และจำนวน permutations (num_perm)

    Returns:
    MinHash: วัตถุ MinHash ที่มีลายเซ็นที่สร้างขึ้นจากข้อความ
    """
    text, num_perm = item
    return generate_minhash_signature(text, num_perm)


def generate_minhash(dataset_groups, pretrain_data_args, minhash_config, global_config):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับชุดข้อมูลการฝึก
    โดยใช้เทคนิค MinHash และ MinHashLSH เพื่อสร้างลายเซ็นสำหรับแต่ละข้อความในชุดข้อมูล

    Parameters:
    dataset_groups (dict): กลุ่มของชุดข้อมูลที่ต้องการประมวลผล
    pretrain_data_args (Namespace): อาร์กิวเมนต์ที่ใช้ในการโหลดชุดข้อมูลการฝึก
    minhash_config (Namespace): การตั้งค่าสำหรับการสร้าง MinHash
    global_config (Namespace): การตั้งค่าทั่วไป เช่น จำนวน permutations และจำนวน process

    Returns:
    None
    """
    # โหลดพจนานุกรมสำหรับการแบ่งคำแบบ "newmm"
    load_dict(minhash_config.newmm_dict, "newmm")

    # วนลูปผ่านกลุ่มข้อมูลแต่ละกลุ่ม
    for dataset_key in dataset_groups.keys():
        dataset_arg = dataset_groups[dataset_key]
        # โหลดชุดข้อมูล
        dataset = load_data(dataset_arg)
        # แปลงข้อมูลแต่ละรายการในชุดข้อมูลโดยใช้ MAPPER
        dataset1 = [
            MAPPER[dataset_key](item) for item in dataset[dataset_arg.split].to_list()
        ]
        # กำจัดรายการที่ซ้ำกัน
        dataset1 = list(set(dataset1))
        # สร้างรายการทูเพิลที่ประกอบด้วยข้อความและจำนวน permutations
        dataset1_map = [(item, global_config.num_perm) for item in dataset1]

        print(dataset1[:5], dataset_key)

        # สร้างลายเซ็น MinHash โดยใช้การประมวลผลแบบขนาน
        with Pool(processes=global_config.num_process) as pool:
            signatures = list(
                tqdm(
                    pool.imap(generate_minhash_item, dataset1_map),
                    total=len(dataset1_map),
                    desc="Processing dataset",
                )
            )
            # เส้นทางไปยังไฟล์ลายเซ็นและไฟล์ข้อมูลที่เก็บไว้ชั่วคราว
            signature_path = f"./temp/{dataset_key}_{dataset_arg.split}_signature_{global_config.num_perm}.pickle"
            file_path = f"./temp/{dataset_key}_{dataset_arg.split}_file_{global_config.num_perm}.pickle"

            # บันทึกลายเซ็นลงในไฟล์
            with open(signature_path, "wb") as file:
                pickle.dump(signatures, file)
            # บันทึกข้อมูลลงในไฟล์
            with open(file_path, "wb") as file:
                pickle.dump(dataset1, file)

    # โหลดชุดข้อมูลการฝึก
    pretrain_dataset = load_data(pretrain_data_args)

    # แปลงชุดข้อมูลการฝึกเป็นลายเซ็น MinHash
    dataset1 = pretrain_dataset[pretrain_data_args.split]
    signatures = dataset1.map(
        lambda x: generate_minhash_signature_hf(
            x, global_config.num_perm, pretrain_data_args.col_name
        ),
        num_proc=global_config.num_process,
    )
    # บันทึกชุดข้อมูลลายเซ็น MinHash ลงในที่เก็บข้อมูลที่กำหนด
    signatures.save_to_disk(
        minhash_config.save_path, num_proc=global_config.num_process
    )
