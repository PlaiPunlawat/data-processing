from datasets import Dataset, DatasetDict
from hydra import compose, initialize
import unittest
from data_processing.deduplication.deduplicate import (
    deduplicate,
    generate_minhash_pretrain_dataset,
    indentify_duplicate_pretrain_dataset,
    deduplicate_pretrain_dataset
)

from data_processing.deduplication.generate_minhash import (
    generate_minhash,
    load_dictionary,
    gen_minhash_signature_dataset,


)

import pandas as pd
from datasets import Dataset
import hydra

# Data for the dataset
train_data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "url": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "title": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "source": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "text": [
        "สวัสดีจ๊ะ! วันนี้ขายส้มโอนะคะ ส้มโอสดป้ายแดง อร่อยมากค่า ดูมั่งมี้ทั้งภาพและวิดีโอลามกห้ามพลาดเด็ดขาดจร้า",
        "สวัสดีจ๊ะ! วันนี้ขายส้มโอนะคะ ส้มโอสดป้ายแดง อร่อยมากค่า ดูมั่งมี้ทั้งภาพและวิดีโอลามกห้ามพลาดเด็ดขาดจร้า",
        "ในสวนผลไม้แห่งนี้ มีต้นไม้นานาพันธุ์ที่ออกผลสุกงอมในทุกฤดูกาล เราสามารถเก็บเกี่ยวผลไม้สดใหม่จากธรรมชาติได้ตลอดทั้งปี ไม่ว่าจะเป็นส้ม กล้วย ชมพู่ มะม่วง หรือทุเรียนอร่อยนัว เราจะได้ลิ้มรสความหวานกรุ่นและรสชาติดั้งเดิมที่แสนจะน่าปลื้ม",
        "ในสวนผลไม้แห่งนี้ มีต้นไม้นานาพันธุ์ที่ออกผลสุกงอมในทุกฤดูกาล เราสามารถเก็บเกี่ยวผลไม้สดใหม่จากธรรมชาติได้ตลอดทั้งปี ไม่ว่าจะเป็นส้ม กล้วย ชมพู่ มะม่วง หรือทุเรียนอร่อยนัว เราจะได้ลิ้มรสความหวานกรุ่นและรสชาติดั้งเดิมที่แสนจะน่าปลื้ม",
        "ในสวนผลไม้แห่งนี้ มีต้นไม้นานาพันธุ์ที่ออกผลสุกงอมในทุกฤดูกาล เราสามารถเก็บเกี่ยวผลไม้สดใหม่จากธรรมชาติได้ตลอดทั้งปี ไม่ว่าจะเป็นส้ม กล้วย ชมพู่ มะม่วง หรือทุเรียนอร่อยนัว เราจะได้ลิ้มรสความหวานกรุ่นและรสชาติดั้งเดิมที่แสนจะน่าปลื้ม",
        "ในสวนผลไม้แห่งนี้ มีต้นไม้นานาพันธุ์ที่ออกผลสุกงอมในทุกฤดูกาล เราสามารถเก็บเกี่ยวผลไม้สดใหม่จากธรรมชาติได้ตลอดทั้งปี ไม่ว่าจะเป็นส้ม กล้วย ชมพู่ มะม่วง หรือทุเรียนอร่อยนัว เราจะได้ลิ้มรสความหวานกรุ่นและรสชาติดั้งเดิมที่แสนจะน่าปลื้ม",
        "สาวๆสายแก้มมุ้งมิ้ง เตรียมพร้อมสำหรับเทศกาลผิวกระจ่างใสที่กำลังจะมาถึงนี้! โปรเด็ดสุดคุ้มจากร้าน Glowlicious Skincare แนะนำผลิตภัณฑ์ทำความสะอาดผิวหน้าขั้นเทพ ล้างสิ่งสกปรกและซิลิโคนได้อย่างหมดจด เนื้อแนบเนียนนุ่มลื่น ปราศจากน้ำมันส่วนเกิน มีวิตามินเอสูง เหมาะสำหรับผิวมันและผิวผสม ราคาเพียง 499 บาท จากปกติ 799 บาท เพื่อนๆสนใจสอบถามรายละเอียดเพิ่มเติมได้ที่ ไลน์ glowliciousskin หรือดูจากแคตตาล็อกที่แนบมา",
        "สาวๆสายแก้มมุ้งมิ้ง เตรียมพร้อมสำหรับเทศกาลผิวกระจ่างใสที่กำลังจะมาถึงนี้! โปรเด็ดสุดคุ้มจากร้าน Glowlicious Skincare แนะนำผลิตภัณฑ์ทำความสะอาดผิวหน้าขั้นเทพ ล้างสิ่งสกปรกและซิลิโคนได้อย่างหมดจด เนื้อแนบเนียนนุ่มลื่น ปราศจากน้ำมันส่วนเกิน มีวิตามินเอสูง เหมาะสำหรับผิวมันและผิวผสม ราคาเพียง 499 บาท จากปกติ 799 บาท เพื่อนๆสนใจสอบถามรายละเอียดเพิ่มเติมได้ที่ ไลน์ glowliciousskin หรือดูจากแคตตาล็อกที่แนบมา",
        "หนังสือเล่มนี้ได้พรรณนาเรื่องราวชีวิตของนักเดินทางผู้กล้าหาญที่ได้ผจญภัยข้ามพรมแดนไปยังดินแดนห่างไกล เขาได้สัมผัสกับวัฒนธรรมและประเพณีที่แตกต่าง ได้เห็นธรรมชาติที่งดงามและสมบูรณ์แบบ รวมถึงได้พบกับความท้าทายและอุปสรรคนานัปการ แต่ด้วยความมุ่งมั่นและพลังใจที่เข้มแข็ง เขาสามารถฟันฝ่าอุปสรรคเหล่านั้นไปได้",
        "ในยามเช้าที่สดใส พร้อมแสงอรุณอันงดงามของดวงอาทิตย์ ฉันรู้สึกได้ถึงพลังสดชื่นและความหวังใหม่ที่จะเติมเต็มวันนี้ด้วยความสำเร็จและความสุขที่ยั่งยืน ช่างเป็นภาพที่สวยงามและทรงพลังจริงๆ ที่ได้ต้อนรับวันใหม่อันน่าตื่นเต้นนี้",
        "ขายนมผึ้งป่าดิบจากเมืองลำปางแท้ 100% ไม่มีผสมน้ำตาลหรือสารปนเปื้อนแม้แต่น้อย สดใหม่จากรังผึ้งดอยสูง อร่อยถึงรสถึงกลิ่น บำรุงร่างกายสุขภาพดีเยี่ยม สนใจสั่งซื้อติดต่อคุณชายเฉลิมชัย หรือทางไลน์ iD: chaleamchaihoney ราคาพิเศษ 690 บาท กระปุก",

    ]}

test_data = {
    "text": ["I am doing fine, thank you.", "I don't like this at all."],
    "label": [0, 0]
}

# Create Dataset objects
train_dataset = Dataset.from_dict(train_data)
test_dataset = Dataset.from_dict(test_data)

# Combine into a DatasetDict
dataset_dict = DatasetDict({
    "train": train_dataset,
    "test": test_dataset
})


class TestGenerateMinhash(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialize Hydra and load configuration for the tests.
        """
        # Initialize Hydra and specify the path to the config directory
        initialize(config_path="config",
                   job_name="test_app", version_base="1.1")
        # Compose the configuration from the config file
        cls.cfg = compose(config_name="deduplication")

    def test_deduplicate(self):
        # Load dic
        load_dictionary(self.cfg.minhash)

        # Prepare dataset
        print(dataset_dict, "dataset_dict")
        for t in dataset_dict["train"]["text"]:
            print(t)
        dataset = dataset_dict["train"]
        print(dataset)

        # gen minhash signature
        pretrain_dataset = dataset_dict.copy()
        pretrain_dataset_minhash = gen_minhash_signature_dataset(
            dataset, self.cfg.global_config)

        # gen minhash pretrain dataset
        pretrain_dataset_minhash_result = generate_minhash_pretrain_dataset(
            pretrain_dataset_minhash, self.cfg.deduplication, self.cfg.global_config)

        # Debugging print statement to verify the results of the MinHash queries.
        # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันผลลัพธ์ของการสอบถาม MinHash
        print(pretrain_dataset_minhash_result,
              "pretrain_dataset_minhash_result")

        # Process the query results to identify duplicates.
        # ประมวลผลผลการสอบถามเพื่อระบุข้อมูลซ้ำ
        duplicate_results = indentify_duplicate_pretrain_dataset(
            pretrain_dataset_minhash, pretrain_dataset_minhash_result, self.cfg.deduplication, self.cfg.global_config)

        # Debugging print statement to verify the detected duplicates.
        # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันการตรวจหาข้อมูลซ้ำ
        print(duplicate_results, "duplicate_results")


        # Deduplicate pretrain dataset
        pretrain_dataset = deduplicate_pretrain_dataset(
            pretrain_dataset, duplicate_results, self.cfg.train_dataset, self.cfg.deduplication, self.cfg.global_config)

        # Debugging print statement to verify the final filtered dataset.
        # คำสั่งพิมพ์เพื่อการดีบักเพื่อยืนยันชุดข้อมูลที่กรองแล้ว
        print(pretrain_dataset, "pretrain_dataset")

        for t in pretrain_dataset["train"]["text"]:
            print(t)

        self.assertGreater(len(dataset_dict["train"]), len(pretrain_dataset["train"]))


if __name__ == "__main__":
    unittest.main()
