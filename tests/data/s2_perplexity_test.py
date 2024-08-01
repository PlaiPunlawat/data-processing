from openthaigpt_pretraining_data.internet.s2_perplexity.perplexity import (
    classify_spam,
    sample_text_back,
)
from utils_test import compare_dataset


def test_classify_spam():
    assert (
        classify_spam(
            "หนังxจีนมาใหม่ TM0165 แม่เลี้ยงสาวWang Xiaoni หลับอยู่ เจอลูกเลี้ยงชวนเพื่อนมารุมเย็ดแม่เลี้ยง จับมอมยาสลบก่อนลวนลามลงมืดข่มขืนxxx สวิง 3-1 เย็ดจนแตกในซะใจ"
        )[1]
        > 40
    )
