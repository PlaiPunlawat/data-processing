# coding: utf-8
# flake8: noqa
import re

#########
# PRE-COMPILE REGEX to object for speed up processing.
#########
# -----------------------------------------------------
# Remove useless row that make overhead in regex processing

# Unusual row - line size too large
# if there are 3 large lines ( 500 characters each)
TOOLARGE_LINE_PATTERN = ".{1500}"
TOOLARGE_RE = re.compile(TOOLARGE_LINE_PATTERN, re.MULTILINE)
TOOLARGE_THRESHOLD = 2

NONECHAR_PATTERN = "๮|๞|๨|๡|๷|๻|๫|͹"
NONECHAR_RE = re.compile(NONECHAR_PATTERN, re.MULTILINE)
NONECHAR_THRESHOLD = 25

NONE_TONE_MARK_PATTERN = "ก าหนด|เป าหมาย|พ ฒนา|ค ณภาพ|ว จ ย|ค ณล กษณะ|ต างๆ|เป น |ให |บร หาร|ปร บปร ง|ใหม|อย าง|เง น"
NONE_TONE_MARK_RE = re.compile(NONE_TONE_MARK_PATTERN, re.MULTILINE)
NONE_TONE_MARK_THRESHOLD = 25

# -----------------------------------------------------


JSON_PATTERN = r"\s*\"(?:\w)*\"\s*:"
JSON_RE = re.compile(JSON_PATTERN, re.MULTILINE)
JSON_THRESHOLD = 20


GHOST_PATTERN = "เธฃเน|เธเธญ|เธเน|เธฐเธ|เธฅเธฐ|เธซเธฒ|เธญเธฒ|เธดเธ|เธตเธข|เธญเน|เธญเธ|เธดเน|เธฑเธ|เธกเน|เธฒเธ|เธชเน|เน€เธ"
GHOST_RE = re.compile(GHOST_PATTERN, re.MULTILINE)
GHOST_THRESHOLD = 4

HEX_PATTERN = "(?<![^ ])(?:[0-9A-Fa-f]{2})(?![^ ])"
HEX_RE = re.compile(HEX_PATTERN, re.MULTILINE)
HEX_THRESHOLD = 25

PAGE_PATTERN = "(?:<<[ ])?(?:ก่อนหน้า|ย้อนกลับ)[ ]{0,2}(?:\[[ ]?\d{0,6}[ ]?\]|[ ]?\d{0,6}[ ]?)*(?:ต่อไป|หน้าถัดไป|ถัดไป)?(?:[ ]?>>)?|<<(?:[ ]\d{0,6}[ ]\-[ ]\d{0,6})+[ ].{0,100}"
PAGE_RE = re.compile(PAGE_PATTERN, re.MULTILINE)
PAGE_THRESHOLD = None

EMBEDDED_SERVER_PATTERN = "<%[ ]*[^%]*%>|<%.*"
EMBEDDED_SERVER_RE = re.compile(EMBEDDED_SERVER_PATTERN, re.MULTILINE)
EMBEDDED_SERVER_THRESHOLD = None

U_PATTERN = "\uFEFF|\u00AD|[\u200A-\u200F]|\uFFFD|[\uE000-\uF8FF]|[\u202A-\u202C]|\u0092|[\u0091-\u0096]|\u2028|\u2066|\u2069|\u008d|\u0081|\u008E|<U\+[0-9A-Fa-f]{4}>"
U_RE = re.compile(U_PATTERN, re.MULTILINE)
U_THRESHOLD = None

BLOCK_PATTERN = "(?:\[[^\]]*\])|(?:«[^»]*»)|(?:<<([^>]*)>>)"
BLOCK_RE = re.compile(BLOCK_PATTERN, re.MULTILINE)
BLOCK_THRESHOLD = None

EMAIL_PATTERN = "(?:(?:([Ee]?mail|อีเมล์)[ ]{0,2}:?[ ]{0,5})?)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
EMAIL_RE = re.compile(EMAIL_PATTERN, re.MULTILINE)
EMAIL_THRESHOLD = None

URL_PATTERN = r"\b(?:(?:https?|ftp)://[^\s/$\.\?#].[^\s]*)\b|\b(?:www\.?)?(?:(?:[\w-]*)\.)*(?:com|net|org|info|biz|me|io|co|asia|xyz|th|cn|in|uk|jp|ru)\b"
URL_RE = re.compile(URL_PATTERN, re.MULTILINE)
URL_THRESHOLD = None

MENU1_PATTERN = "\|(?:[^\|\n]*\|)+.*"
MENU1_RE = re.compile(MENU1_PATTERN, re.MULTILINE)
MENU1_THRESHOLD = None

MENU2_PATTERN = "\|(?:[^\|\n]*\|)+"
MENU2_RE = re.compile(MENU2_PATTERN, re.MULTILINE)
MENU2_THRESHOLD = None

MENU3_PATTERN = "(?:(?:[^/\n]*/){4,}.*)"
MENU3_RE = re.compile(MENU3_PATTERN, re.MULTILINE)
MENU3_THRESHOLD = None

MENU4_PATTERN = "^[^\n]{0,20}[ ]{0,2}[>»\\\\].*"
MENU4_RE = re.compile(MENU4_PATTERN, re.MULTILINE)
MENU4_THRESHOLD = None

HASHTAG_PATTERN = "#\d*[ ].{0,300}|#(?:(?:[^ \n]*)[ ]?)+|Tag Archives[ ]{0,2}:.{0,300}|Posts Tagged[ ]{0,2}:.{0,300}|HASTAG[ ]{0,2}:.{0,300}|Tag[s]?[ ]{0,2}:.{0,300}|Tagged[ ].{0,300}"
HASHTAG_RE = re.compile(HASHTAG_PATTERN, re.MULTILINE)
HASHTAG_THRESHOLD = None

SIDEBAR_PATTERN = ".{0,40}(?:(?:\[|\()\d{0,9}(?:\]|\))(?:[ ]{0,2})?,?)"
SIDEBAR_RE = re.compile(SIDEBAR_PATTERN, re.MULTILINE)
SIDEBAR_THRESHOLD = None

MARKUP_PATTERN = "\{\{[^\}]*\}\}|\{\{.*"
MARKUP_RE = re.compile(MARKUP_PATTERN, re.MULTILINE)
MARKUP_THRESHOLD = None

IFRAME_PATTERN = "<iframe.*?<\/iframe>\s*|<iframe.*"
IFRAME_RE = re.compile(IFRAME_PATTERN, re.MULTILINE)
IFRAME_THRESHOLD = None

IP_PATTERN = "\((?:(?:X{1,3}|\d{1,3})\.){3}(?:X{1,3}|\d{1,3})\)|\(?IP:?[ ]?(?:(?:X{1,3}|\d{1,3})\.){3}(?:X{1,3}|\d{1,3})\)?"
IP_RE = re.compile(IP_PATTERN, re.MULTILINE)
IP_THRESHOLD = None

TEL_PATTERN = "(?:(?:[Pp]hone|[Mm]obile|มือถือ|Tel|TEL|Fax|FAX|เบอร์โทรศัพท์|เลขโทรศัพท์|เบอร์ติดต่อ|โทรศัพท์|โทรสาร[ ]{0,2}:|เบอร์โทร|โทร[ ]{0,2}:|โทร\.|โทร[ ]|ติดต่อที่[ ]{0,2}:?|ติดต่อ[ ]{0,2}:?)[ ]{0,2}):?(?:(?:[ ]{0,2})?(?:(?:\d{3}-\d{7})|(?:\d{4}-\d{6})|(?:\d{3}-\d{3}-\d{4}|(?:\d{3}-\d{3}-\d{3})|(?:\d{1}-\d{4}-\d{4})|(?:\d{2}-\d{3}-\d{4})|(?:\d{2}\s\d{3}\s\d{4})|(?:\d{2}-\d{7})|(?:\d{3}\s\d{3}\s\d{4})|(?:\d{3}\s\d{3}\s\d{3})|(?:\d{10})))[ ]{0,2},?)+|02\d{7}|0[3-7][2-9]\d{6}|0[6-9][0-9]\d{7}"
TEL_RE = re.compile(TEL_PATTERN, re.MULTILINE)
TEL_THRESHOLD = None

DATE1_PATTERN = "(?:(?:การปรับปรุงปัจจุบัน|ตั้งแต่|ลงประกาศเมื่อ|อัพเดทล่าสุด|แก้ไขครั้งสุดท้าย|แก้ไขครั้งล่าสุด|เผยแพร่เมื่อ|เผยแพร่|เขียนเมื่อ|ตอบเมื่อ|เมื่อ|เขียนวันที่|วันที่|วัน)?(?:[ ]{0,2}:[ ]{0,2})?(?:จันทร์|อังคาร|พุธ|พฤหัสบดี|พฤหัสฯ?\.?|ศุกร์|เสาร์|อาทิตย์|จ\.|อ\.|พ\.|พฤ\.|ศ\.|ส\.|อา\.?)?(?:[ ]{0,2}ที่)?(?:[ ]{0,2}[\w\u0E01-\u0E5B]*[ ]{0,2}(?:,|(?:-|\u2013)))?(?:\d{1,4}[ ]{0,2}-)?[ ]{0,2}\d{0,4}(?:-|[ ]{0,2})(?:เดือน[ ]{0,2})?(?:มกราคม|กุมภาพันธ์|มีนาคม|เมษายน|พฤษภาคม|มิถุนายน|กรกฎาคม|สิงหาคม|กันยายน|ตุลาคม|พฤศจิกายน|ธันวาคม| ม\.?ค\.? | ก\.?พ\.? | มี\.?ค\.? | เม\.?ย\.? | พ\.?ค\.? | มิ\.?ย\.? | ก\.?ค\.? | ส\.?ค\.? | ก\.?ย\.? | ต\.?ค\.? | พ\.?ย\.? | ธ\.?ค\.? |January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|/)(?:-|[ ]|,]){0,2}(?:[ ]{0,2})?(?:\d{4}|\d{2})?,?(?:(?:[ ]{0,2}\d{4}|\d{2}:\d{2}:\d{2})|(?:[ ]{0,2}\d{1,2}:\d{2}(?::\d{2})?[ ]*(?:(?:(?:p|P|a|A)(?:m|M)))?)|[ ]{0,2}เวลา[ ]{0,2}\d{1,2}:\d{2}:\d{2})?(?:[ ]{0,2}น\.)?(?:[ ]{0,2}:[ ]{0,2}\d{1,2}(?:\.|:)\d{2}[ ]{0,2}น\.)?(?:[ ]{0,2}เวลา[ ]{0,2}\d{1,2}:\d{2}[ ]{0,2}[pPaA][mM][ ]{0,2}(?:PDT)?)?(?:[ ]{0,2}เวลา[ ]{0,2}\d{1,2}(?:\.|:)\d{2}[ ]{0,2}(?:น\.)?)?(?:[ ]*\d*[ ]{0,9}ผู้ชม[ ]{0,2}\d)?(?:[ ]{0,2}เวลา[ ]{0,2}:[ ]{0,2}\d{1,2}:\d{2}:\d{2}[ ](?:น\.)?)?(?:[ ]{0,2}เข้าชม[ ]{0,2}\d*[ ]{0,8}ครั้ง)?(?:[ ]{0,2}ที่[ ]{0,2}\d{1,2}:\d{2}[ ]{0,2}(?:[pPaA][mM])?)?(?:[ ]{0,2}Views:[ ]{0,2}(?:\d{0,3},?){0,3})?(?:[ ]{0,2}\(\d{1,2}:\d{2}[ ](?:น\.)?[ ]{0,2}\)(?:[ ]{0,2}ความคิดเห็น[ ]{0,2}\d)?)?(?:[ ]{0,2}-[ ]{0,2}\d{1,2}:\d{2}[ ]{0,2}(?:น\.)?)?(?:[ ]{0,2}จำนวนเข้าชม:(?:[ ]{0,2}\d{0,9},?)*)?(?:[ ]*พ\.ศ\.[ ]{0,2}\d{4}[ ]{0,2}(?:\d{1,2}:\d{2}[ ]{0,2}(?:น\.)?)?)?(?:(?:\d{0,3},?){0,3}[ ]{0,2}ครั้ง)?(?:[ ]{0,2}-\d{1,2}(?:\.|:)?\d{2}[ ]{0,2}(?:น\.)?)?(?:เวลา[ ]{0,2}\d{1,2}:\d{2}:\d{2})?(?:[ ]{0,2}(?:ถึง|จนถึง))?)(?:,[ ]{0,2})?(?:[ ]{0,2}(?:[pPaA][mM])?)?|(?:(?:[ ]{0,2}(?:\d{4}|\d{2})-\d{1,2}-(?:\d{4}|\d{1,2}))(?:[ ]{0,2},[ ]{0,2})?(?:\d{1,2}(?:\.|:)\d{2}[ ]{0,2}(?:#\d*)?(?:น\.)?)?(?:[ ]{0,2}\d{1,2}:\d{2}:\d{2})?)|(?:(?:เปิดบริการ[ ]{0,2})?(?:เวลา[ ]{0,2}\d{1,2}:\d{2}-\d{1,2}:\d{2}[ ]{0,2}(?:น\.)?))|(?:(?:Time[ ]Online[ ]:[ ]{0,2})?(?:\d{1,2}:\d{2}:\d{2})(?:[ ]{0,2}น\.)?(?:[ ]{0,2}[pPaA][mM])?)|(?:\(\d{1,2}:\d{2}[ ]{0,2}-[ ]{0,2}\d{1,2}:\d{2}(?:[ ]*น\.)?(?:[ ]{0,2}[pPaA][mM])?\))|(?:นี้[ ]{0,2}เวลา[ ]{0,2}\d{1,2}(?:\.|:)\d{2}[ ]{0,2}(?:น\.)?)|(?:\d{1,2}[ ]{0,2}(?:มกราคม|กุมภาพันธ์|มีนาคม|เมษายน|พฤษภาคม|มิถุนายน|กรกฎาคม|สิงหาคม|กันยายน|ตุลาคม|พฤศจิกายน|ธันวาคม))"
DATE1_RE = re.compile(DATE1_PATTERN, re.MULTILINE)
DATE1_THRESHOLD = None

DATE2_PATTERN = "[พค]\.?ศ\.?[ ]{0,2}\d{4}|\d{4}[ ]{0,2}เวลา[ ]{0,2}\d{2}:?\.?\d{2}(?:[ ][Pp][Mm])|[พค]\.?ศ\."
DATE2_RE = re.compile(DATE2_PATTERN, re.MULTILINE)
DATE2_THRESHOLD = None

HTML_PATTERN = (
    "<br>?|&nbsp|{\s*document\..*|SELECT.*FROM.*WHERE.*|<a\s*href=.*|<img\s*src=.*"
)
HTML_RE = re.compile(HTML_PATTERN, re.MULTILINE)
HTML_THRESHOLD = None

REFINE1_PATTERN = "^[ ]?ตอนที่[ ]*\d{0,3}(?:[-–]?\d{0,3})?[ ]{0,2}.{0,100}|^สั่ง.{0,50}บาท|^[ ]?เลขจดแจ้ง[ ]{0,2}.{0,13}|^.{0,100}\.jpg[ ]{0,2}\(.{0,50}|^.{0,20}รายการ|^[ ]?สนใจ[ ]{0,2}.{0,15}โทร[ ]{0,2}.{0,12}|^[ ]?ผู้แสดงความคิดเห็น.{0,60}|^\(.{0,40}[ ]{0,2}\d{0,5}[ ]{0,2}.{0,10}\).{0,200}|^[ ]?ผู้เข้าชมทั้งหมด.{0,30}|^[ ]?ฉบับที่[ ]{0,2}\d{0,7}[^-–]{0,30}-?–?[ ]|^[ ]?โพสต์ที่แชร์โดย.{0,200}|^[ ]?Copyright.{0,200}|กำลังแสดงหน้าที.{0,200}|[ ]{0,2}รีวิว.{0,100}|^[ ]?ข้อที่ \d{0,4}|^เข้าชม/ผู้ติดตาม.{0,13}"
REFINE1_RE = re.compile(REFINE1_PATTERN, re.MULTILINE)
REFINE1_THRESHOLD = None

REFINE2_PATTERN = "Submitted[ ]by.{0,100}|^เขียนโดย.{0,100}|^Poste?d?[ ]{0,2}(?:by|on){0,2}.{0,100}|^เมื่อวาน[ ]{0,2}\d.{0,100}|^อาทิตย์นี้[ ]{0,2}\d.{0,100}|^อาทิตย์ที่แล้ว[ ]{0,2}\d.{0,100}|^เดือนนี้[ ]{0,2}\d.{0,100}|^เดือนที่แล้ว[ ]{0,2}\d.{0,100}|^รวมผู้เยี่ยมชม[ ]{0,2}\d.{0,100}|^จำนวนผู้ชมโดยประมาณ[ ]{0,2}\d.{0,100}|^รหัสสินค้า[ ]{0,2}\d.{0,100}|^บาร์โค้ด[ ]{0,2}\d.{0,100}|^[ ]โดย[ ]{0,2}.{0,100}|^เข้าชม[ ]{0,2}\d.{0,100}|^โหวต[ ]{0,2}\d.{0,100}|^มุมมอง[ ]{0,2}\d.{0,100}"
REFINE2_RE = re.compile(REFINE2_PATTERN, re.MULTILINE)
REFINE2_THRESHOLD = None

REFINE3_PATTERN = "^[^@\n]{0,30}@\d{0,10}.{0,30}|.{0,100}[-]$|\d*[ ]*x[ ]\d*[^ ][ ]?|^ดูหนัง[ ]?(?:ออนไลน์)?[ ].{0,60}|^คุ้มค่าที่สุดอันดับ[ ]{0,2}\d{0,2}.{0,80}|^เปิด[^\d\n]+.{0,10}"
REFINE3_RE = re.compile(REFINE3_PATTERN, re.MULTILINE)
REFINE3_THRESHOLD = None

REFINE4_PATTERN = "^[^\n]{0,50}คลิก\)|[Ff]acebook[ ]{0,2}(?:\d{0,3},?\d{0,3})[ ]{0,2}เข้าชม|^[ ]{0,2}[^ ]{0,20}[ ]{0,2}\d{0,9}[ ]{0,2}ความเห็น|\[url=.{0,100}|^ผู้ชม[ ]{0,2}(?:\d{0,3},?)+|\([ ]?\)"
REFINE4_RE = re.compile(REFINE4_PATTERN, re.MULTILINE)
REFINE4_THRESHOLD = None

REFINE5_PATTERN = "^[^\d]{0,30}\d{0,10}[ ]{0,2}views.{0,100}|^Prev.{0,100}Next|^สินค้าติดต่อที่.{0,100}|^อ่านต่อคลิก.{0,100}|^สินค้าโปรโมชั่น.{0,200}|^US[ ]?\$\d{0,3},?\d{0,3}.?\d{0,3}.{0,50}"
REFINE5_RE = re.compile(REFINE5_PATTERN, re.MULTILINE)
REFINE5_THRESHOLD = None

REFINE6_PATTERN = "^เจ้าหน้าที่ฝ่ายขาย:\n.{0,80}|^(?:\*+[ ]{0,2}[^\*\n]{0,50}[ ]{0,2}\*+)[ ]{0,2}[\+]?(?:(?:\d{0,3},?)+)?|[\*\+]{2,5}|^(?:[^:\n]{0,30}:).{0,200}"
REFINE6_RE = re.compile(REFINE6_PATTERN, re.MULTILINE)
REFINE6_THRESHOLD = None

REFINE7_PATTERN = "\(?อ่าน[ ]{0,2}\d{0,3},?\d{0,3}[ ]{0,2}(?:ครั้ง[ ]{0,2})?\)?|โพสต์[ ].{0,100}|Read[ ]{0,2}\d{0,9}[ ]{0,2}times|[^ \n]{0,20}[ ]{0,2}pantip|^Previous (?:Post|article).{0,150}|^Next (?:Post|article).{0,150}|^ตอบกลับ[ ]{0,2}.{0,200}"
REFINE7_RE = re.compile(REFINE7_PATTERN, re.MULTILINE)
REFINE7_THRESHOLD = None

REFINE8_PATTERN = "^[ ]?(?:[Pp]ostby|[Pp]osted[ ](?:by|on)).*|^[ ]?เข้าชม/ผู้ติดตาม.*|^[ ]?จำนวนผู้ชมโดยประมาณ[ :]?.*|^[ ]?ลงประกาศฟรี[ ].*|^\|[ ]|^[ ]?จาก[ ].*|^[ ]?By.*|^[ ]{0,2}?โดย[ ]{0,2}?.*"
REFINE8_RE = re.compile(REFINE8_PATTERN, re.MULTILINE)
REFINE8_THRESHOLD = None

REFINE9_PATTERN = "^[^\n\.]{0,60}\.{3}$|^[^\n]{0,30}ฉบับที่[ ].*|^Home[ ]/[ ].{100}|^[^\n\|]{0,60}\|.{0,60}"
REFINE9_RE = re.compile(REFINE9_PATTERN, re.MULTILINE)
REFINE9_THRESHOLD = None

REFINE10_PATTERN = "^[ ]?(?:\)|↑|►|←|«)[ ]?|^[-_]+"
REFINE10_RE = re.compile(REFINE10_PATTERN, re.MULTILINE)
REFINE10_THRESHOLD = None

REFINE11_PATTERN = "^สถิติ(?:วันนี้|สัปดาห์นี้|เมื่อวาน(?:นี้)?|เดือนนี้)[ ]{0,2}.{0,50}|Online[ ]สถิติ.{0,50}"
REFINE11_RE = re.compile(REFINE11_PATTERN, re.MULTILINE)
REFINE11_THRESHOLD = None

REFINE12_PATTERN = (
    "^[^\n\(]{0,80}\(รายละเอียด\)[ ]\(แจ้งลิงก์เสีย\)|^ด[\. ][ชญ][\. ].*|\.{5,}"
)
REFINE12_RE = re.compile(REFINE12_PATTERN, re.MULTILINE)
REFINE12_THRESHOLD = None

REFINE13_PATTERN = "^[ ]?(?:เรื่องย่อ[ ].{0,100}|คุ้มค่าที่สุดอันดับ.{0,100}|คุ้[ ]่าที่สุดอันดับ.{0,100}|\(?ลงโฆษณาฟรี[ ].{0,200}|\(free[ ]online[ ].{0,100}|\(คลิกเพื่อดูต้นฉบับ\)[ ].{0,100}|แก้ไขครั้งสุดท้ายโดย[ ].{0,100})|^[^\d\n]{0,30}[ ]\d{0,3},?\d{0,3}[ ]ครั้ง.{0,50}"
REFINE13_RE = re.compile(REFINE13_PATTERN, re.MULTILINE)
REFINE13_THRESHOLD = None

REFINE14_PATTERN = "^(?:[฿$]?\d{0,9}\.?,?\d{0,9}-?–?:?/?(?:[ ]{0,2}x[ ]{0,2}\d{0,8})?(?:\\bกม\\b\.?)?(?:\\bน\\b\.)?(?:ล้าน|แสน|หมื่น|พัน|ร้อย|สิบ|บาท|[ ])?){0,5}"
REFINE14_RE = re.compile(REFINE14_PATTERN, re.MULTILINE)
REFINE14_THRESHOLD = None
