from data_processing.core.minhash import generate_minhash_signature_hf

from datasets import load_from_disk

from nlpo3 import load_dict

import os


def load_dictionary(minhash_config):
    # Load the newmm dictionary for word segmentation.
    # โหลดพจนานุกรม newmm สำหรับการแบ่งคำ
    load_dict(minhash_config.newmm_dict, "newmm")


def prepare_pretrain_dataset(pretrain_data_args):
    # Load the pretraining dataset from the specified path.
    # โหลดชุดข้อมูลการฝึกจากเส้นทางที่กำหนด
    pretrain_dataset = load_from_disk(pretrain_data_args.path_name)

    # Select the desired split from the dataset.
    # เลือกส่วนที่ต้องการจากชุดข้อมูล
    dataset = pretrain_dataset[pretrain_data_args.split]

    return dataset


def gen_minhash_signature_dataset(dataset, global_config):

    # Generate MinHash signatures for each document in the dataset.
    # สร้างลายเซ็น MinHash สำหรับแต่ละเอกสารในชุดข้อมูล
    signatures = dataset.map(
        lambda x: generate_minhash_signature_hf(x, global_config.num_perm),
        num_proc=global_config.num_process,
    )

    return signatures


def save_dataset_to_disk(signatures, minhash_config, global_config):
    # Save the generated signatures to the specified path on disk.
    # บันทึกลายเซ็นที่สร้างขึ้นไปยังเส้นทางที่กำหนดลงดิสก์
    signatures.save_to_disk(
        minhash_config.save_path, num_proc=global_config.num_process
    )


def generate_minhash(pretrain_data_args, minhash_config, global_config):
    """
    This function generates MinHash signatures for a pretraining dataset and saves the signatures to disk.

    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับชุดข้อมูลการฝึก และบันทึกลายเซ็นเหล่านั้นลงดิสก์

    Parameters:
    pretrain_data_args (Namespace): Arguments for loading the pretraining dataset.
                                    อาร์กิวเมนต์สำหรับโหลดชุดข้อมูลการฝึก
    minhash_config (Namespace): Configuration settings for MinHash, including the dictionary and save path.
                                การตั้งค่าสำหรับ MinHash รวมถึงพจนานุกรมและเส้นทางในการบันทึกข้อมูล
    global_config (Namespace): General settings such as the number of permutations and processes.
                               การตั้งค่าทั่วไป เช่น จำนวน permutations และจำนวนกระบวนการ

    Returns:
    None: The function does not return any value. It saves the generated MinHash signatures to disk.
          ฟังก์ชันนี้ไม่มีการคืนค่าออกมา แต่จะบันทึกลายเซ็น MinHash ที่สร้างขึ้นลงดิสก์
    """

    # Load the newmm dictionary for word segmentation.
    # โหลดพจนานุกรม newmm สำหรับการแบ่งคำ
    # load_dict(minhash_config.newmm_dict, "newmm")
    load_dictionary(minhash_config)

    # Load the pretraining dataset from the specified path.
    # โหลดชุดข้อมูลการฝึกจากเส้นทางที่กำหนด
    dataset = prepare_pretrain_dataset(pretrain_data_args)

    # Generate MinHash signatures for each document in the dataset.
    # สร้างลายเซ็น MinHash สำหรับแต่ละเอกสารในชุดข้อมูล
    signatures = gen_minhash_signature_dataset(dataset, global_config)

    # Save the generated signatures to the specified path on disk.
    # บันทึกลายเซ็นที่สร้างขึ้นไปยังเส้นทางที่กำหนดลงดิสก์
    save_dataset_to_disk(signatures, minhash_config, global_config)
