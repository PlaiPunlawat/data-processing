from data_processing.core.minhash import generate_minhash_signature_hf
from nlpo3 import load_dict

import os

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
    load_dict(os.path.join(os.path.dirname(__file__), "words_th.txt"), "newmm")

    # สร้างลายเซ็น MinHash โดยใช้การประมวลผลแบบขนาน
    signatures = dataset1.map(
        lambda x: generate_minhash_signature_hf(x, num_perm),
        num_proc=2,
    )

    # ส่งคืนชุดข้อมูลที่มีลายเซ็น MinHash
    return signatures
