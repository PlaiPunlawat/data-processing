from datasets import load_dataset, load_from_disk

import re


def load_data(dataset_arg):
    """
    ฟังก์ชันนี้มีไว้เพื่อโหลดชุดข้อมูลตามที่ระบุในอาร์กิวเมนต์
    โดยใช้วิธีการโหลดที่แตกต่างกันขึ้นอยู่กับคุณสมบัติของชุดข้อมูล

    Parameters:
    dataset_arg (Namespace): อาร์กิวเมนต์ที่ระบุคุณสมบัติของชุดข้อมูล เช่น ชื่อ, path, subset, และสถานะการใช้งานบน hub

    Returns:
    Dataset: ชุดข้อมูลที่โหลดมา
    """
    if dataset_arg.name == "LST20" or dataset_arg.name == "LST20_Test":
        # โหลดชุดข้อมูล LST20 หรือ LST20_Test
        dataset = load_dataset(
            dataset_arg.path_name, dataset_arg.subset, data_dir=dataset_arg.path
        )
    elif dataset_arg.available_on_hub:
        # โหลดชุดข้อมูลจาก hub
        dataset = load_dataset(dataset_arg.path_name, dataset_arg.subset)
    else:
        # โหลดชุดข้อมูลจาก disk
        dataset = load_from_disk(dataset_arg.path_name)
    return dataset


def preprocess_hellaswag(text):
    """
    ฟังก์ชันนี้มีไว้เพื่อทำการประมวลผลข้อความสำหรับชุดข้อมูล HellaSwag

    Parameters:
    text (str): ข้อความที่ต้องการประมวลผล

    Returns:
    str: ข้อความที่ผ่านการประมวลผลแล้ว
    """
    text = text.strip()
    # NOTE: Brackets are artifacts of the WikiHow dataset portion of HellaSwag.
    text = text.replace(" [title]", ". ")
    text = re.sub("\\[.*?\\]", "", text)
    text = text.replace("  ", " ")
    return text


def generate_query_hellaswag(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล HellaSwag

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    tuple: query ที่สร้างขึ้นจากเอกสาร
    """
    ctx = (
        doc["ctx_a_th"] + " " + ""
        if doc["ctx_b_th"] is None
        else doc["ctx_b_th"].capitalize()
    )
    return (preprocess_hellaswag(doc["activity_label_th"] + ": " + ctx),)


def generate_query_xquad(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล XQuAD

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["context"]


def generate_query_thaisum(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล ThaiSum

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["body"]


def generate_query_multirc_thai(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล MultiRC ไทย

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["paragraph_TH"]


def generate_query_copa_thai(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล COPA ไทย

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    label = doc["label"]
    answer = doc["choice1_th"] if label == 1 else doc["choice2_th"]
    return f'{doc["premise_th"]} f{answer}'


def generate_query_rte_thai(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล RTE ไทย

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["premise"] + " " + doc["hypothesis"]


def generate_query_lst20(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล LST20

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return "".join(doc["tokens"]).replace("_", " ")


def generate_query_record_thai(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล ReCoRD ไทย

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["passage_TH"]


def generate_query_ted_th_en(doc):
    """
    ฟังก์ชันนี้มีไว้เพื่อสร้าง query สำหรับชุดข้อมูล TED Talks ไทย-อังกฤษ

    Parameters:
    doc (dict): เอกสารที่ต้องการสร้าง query

    Returns:
    str: query ที่สร้างขึ้นจากเอกสาร
    """
    return doc["translation"]["th"] + " " + doc["translation"]["en"]


# แผนที่ฟังก์ชันสำหรับการสร้าง query ของชุดข้อมูลต่างๆ
MAPPER = {
    "hellaswag_thai": generate_query_hellaswag,
    "xquad": generate_query_xquad,
    "thaisum": generate_query_thaisum,
    "thaisum_test": generate_query_thaisum,
    "multirc_thai": generate_query_multirc_thai,
    "copa_thai": generate_query_copa_thai,
    "rte_thai": generate_query_rte_thai,
    "lst20": generate_query_lst20,
    "lst20_test": generate_query_lst20,
    "record_thai": generate_query_record_thai,
    "ted_talks_iwslt_th_en": generate_query_ted_th_en,
}
