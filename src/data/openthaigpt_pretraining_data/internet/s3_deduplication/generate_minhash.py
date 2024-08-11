from openthaigpt_pretraining_data.core.minhash import generate_minhash_signature_hf

from datasets import load_from_disk

from nlpo3 import load_dict


def generate_minhash_old(pretrain_data_args, minhash_config, global_config):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับชุดข้อมูลการฝึก
    โดยการโหลดชุดข้อมูลจาก disk และประมวลผลด้วยการสร้างลายเซ็น MinHash

    Parameters:
    pretrain_data_args (Namespace): อาร์กิวเมนต์ที่ใช้ในการโหลดชุดข้อมูลการฝึก
    minhash_config (Namespace): การตั้งค่าสำหรับการสร้าง MinHash
    global_config (Namespace): การตั้งค่าทั่วไป เช่น จำนวน permutations และจำนวน process

    Returns:
    None
    """
    # โหลดพจนานุกรมสำหรับการแบ่งคำแบบ "newmm"
    load_dict("words_th.txt", "newmm")

    # โหลดชุดข้อมูลการฝึกจาก disk
    pretrain_dataset = load_from_disk(pretrain_data_args.path_name)

    # ดึงข้อมูลจากชุดข้อมูลที่กำหนด
    dataset1 = pretrain_dataset[pretrain_data_args.split]

    # สร้างลายเซ็น MinHash โดยใช้การประมวลผลแบบขนาน
    signatures = dataset1.map(
        lambda x: generate_minhash_signature_hf(x, global_config.num_perm),
        num_proc=global_config.num_process,
    )

    # บันทึกชุดข้อมูลลายเซ็น MinHash ลงในที่เก็บข้อมูลที่กำหนด
    signatures.save_to_disk(
        minhash_config.save_path, num_proc=global_config.num_process
    )


def generate_minhash(dataset1, num_perm=128):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้างลายเซ็น MinHash สำหรับชุดข้อมูลที่ได้รับ
    โดยการประมวลผลด้วยการสร้างลายเซ็น MinHash

    Parameters:
    dataset1 (Dataset): ชุดข้อมูลที่ต้องการประมวลผล
    num_perm (int, optional): จำนวน permutations ที่ใช้ในการสร้าง MinHash (ค่าเริ่มต้น: 128)

    Returns:
    Dataset: ชุดข้อมูลที่มีลายเซ็น MinHash
    """
    # โหลดพจนานุกรมสำหรับการแบ่งคำแบบ "newmm"
    load_dict("words_th.txt", "newmm")

    # สร้างลายเซ็น MinHash โดยใช้การประมวลผลแบบขนาน
    signatures = dataset1.map(
        lambda x: generate_minhash_signature_hf(x, num_perm),
        num_proc=2,
    )

    # ส่งคืนชุดข้อมูลที่มีลายเซ็น MinHash
    return signatures
