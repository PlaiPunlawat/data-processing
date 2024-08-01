# coding: utf-8
# flake8: noqa
import re

# Gamble Clean Words
GAMBLE_WORDS = [
    "พนัน",
    "แทงบอล",
    "แทง",
    "บาคารา",
    "บา คา รา",
    "เกมพนัน",
    "คาสิโน",
    "คา สิ โน",
    "หวย",
    "สล็อต",
    "กาสิโน",
    "casino",
    "slot",
    "เลขเด็ด",
    "สูตรหวย",
    "a s i n o",
    "sbobet",
    "fun88",
    "ufabet",
    "บาคาร่า",
    "บา คา ร่า",
    "รูเล็ต",
    "ทำนายฝัน",
    "เลขเด่น",
    "สรุปผลบอล",
    "ไฮไลท์ฟุตบอล",
    "วิเคราะห์บอล",
    "ดูบอลสด",
    "พรีเมียร์ลีก",
    "บอลประจำวัน",
    "บอลเต็ง",
    "บอลเด็ด",
    "องค์ลงรวย",
    "สูตรปลาตะเพียน",
    "สามตัวตรง",
    "วิเคราะห์ข้อมูลล่าง",
    "ต่อ ครึ่งลูก",
    "ครึ่งลูกลบ",
    "เสมอควบครึ่ง",
    "ครึ่งควบลูก",
]
GAMBLE_PATTERN = "|".join(GAMBLE_WORDS)
GAMBLE_RE = re.compile(GAMBLE_PATTERN, re.MULTILINE)
GAMBLE_THRESHOLD = 2

# Sale Clean Words
SALE_SKIP_WORDS = [
    "สอบราคา",
    "จัดซื้อจัดจ้าง",
    "ชมรม",
    "สมาคม",
    "นักลงทุน",
    "นักการตลาด",
    "ของกลาง",
    "การลงทุน",
    "นักวิเคราะห์",
    "ขายให้แก่ประชาชน",
    "การลดต้นทุน",
    "การเสนอราคา",
    "กระทรวง",
    "ตลาดหลักทรัพย์",
    "ยอดขายไม่ดี",
    "ยอดขายไม่ค่อยดี",
    "ผู้ประกอบการธุรกิจ",
    "ออกใบอนุญาต",
    "ผู้ประกอบกิจการ",
]
SALE_SKIP_PATTERN = "|".join(SALE_SKIP_WORDS)
SALE_SKIP_RE = re.compile(SALE_SKIP_PATTERN, re.MULTILINE)
SALE_SKIP_THRESHOLD = 3

# Sale URL
SALE_URL_WORDS = [
    "alibaba.com",
    "shopee.co.th",
    "lazada.com",
    "DocPlayer.net",
    "Alibaba",
    "AliExpress",
    "Aliexpress",
    "TripAdvisor",
    "jobbkk.com",
]
SALE_URL_PATTERN = "|".join(SALE_URL_WORDS)
SALE_URL_RE = re.compile(SALE_URL_PATTERN, re.MULTILINE)
SALE_URL_THERSHOLD = None

# Sales
SALE_WORDS = [
    "ขาย",
    "ซ่อม",
    "ราคา",
    "มือสอง",
    "เช่า",
    "ครีม",
    "ฝ้ากระ",
    "จุดด่างดำ",
    "รับส่วนลด",
    "โปรโมชั่น",
    "กวดวิชา",
    "ติวเตอร์",
    "SEO",
    "คอร์สเรียน SEO",
    "จำหน่าย",
    "ทัวร์",
    "สินค้ามาใหม่",
    "สินค้าทั้งหมด",
    "รีวิวสินค้า",
    "เคสกันกระแทก",
    "ประกาศ",
    "ลงขายของ",
    "เลือกขนาด",
    "บริการจัดส่ง",
    "จัดอันดับ",
    "คาราโอเกะ",
    "จำหน่าย",
    "หาเงินออนไลน์",
    "สั่งซื้อ",
    "ลดกระหนำ่",
    "รหัส",
    "ลงประกาศฟรี",
    "หยิบใส่ตะกร้า",
    "สนใจ",
    "ซื้อ",
    "สินค้า",
    "ผลิตภัณฑ์",
]
SALE_PATTERN = "|".join(SALE_WORDS)
SALE_RE = re.compile(SALE_PATTERN, re.MULTILINE)
SALE_THRESHOLD = 3

# Rent Clean Words
RENT_SKIP_WORDS = [
    "สอบราคา",
    "จัดซื้อจัดจ้าง",
    "ชมรม",
    "สมาคม",
    "นักลงทุน",
    "นักการตลาด",
    "ของกลาง",
    "การลงทุน",
    "นักวิเคราะห์",
    "ขายให้แก่ประชาชน",
    "การลดต้นทุน",
    "การเสนอราคา",
    "กระทรวง",
    "ตลาดหลักทรัพย์",
]
RENT_SKIP_PATTERN = "|".join(RENT_SKIP_WORDS)
RENT_SKIP_RE = re.compile(RENT_SKIP_PATTERN, re.MULTILINE)
RENT_SKIP_THRESHOLD = 2

# Rent words
RENT_WORDS = [
    "บ้านมือสอง",
    "ให้เช่า",
    "เช่า",
    "บ้านเดี่ยว",
    "อพาร์ทเม้นท์",
    "อสังหาริมทรัพย์",
    "เพนท์เฮ้าส์",
    "ทาวน์เฮ้าส์",
]
RENT_PATTERN = "|".join(RENT_WORDS)
RENT_RE = re.compile(RENT_PATTERN, re.MULTILINE)
RENT_THRESHOLD = 2

# Script Clean Words
SCRIPT_WORDS = [
    "function",
    "var",
    "click",
    "margin",
    "width",
    "height",
    "return",
    "else",
    "alert",
    "<br>",
    "href",
]
SCRIPT_PATTERN = r"\b" + "|".join(SCRIPT_WORDS) + r"\b"
SCRIPT_RE = re.compile(SCRIPT_PATTERN, re.MULTILINE)
SCRIPT_THRESHOLD = 10

# Garbage Clean Words
GARBAGE_WORDS = [
    "โหงวเฮ้ง",
    "ครีมฟอกสี",
    "ครีมผิวขาว",
    "ฟอกสี",
    "ไวท์เทนนิ่งครีม",
    "ครีมไวท์เทนนิ่ง",
    "ครีมลบฝ้ากระ",
    "รับสร้างบ้าน",
    "ครีมโรคสะเก็ดเงิน",
    "บริการจองตั๋ว",
    "บริการรีดผ้า",
    "อาหารเสริมลดน้ำหนัก",
    "ยาลดน้ำหนัก",
    "ลดไขมัน",
    "ผิงโซดา",
    "สร้างบ้าน",
    "ช่างกุญแจ",
    "ช่างโลหะ",
    "ช่างโยธา",
    "ช่างเครื่องยนต์",
    "ช่างไม้",
    "ช่างกลโรงงาน",
    "ช่างไฟฟ้า",
    "ปรสิต",
    "หนอน",
    "เวิร์ม",
]
GARBAGE_PATTERN = "|".join(GARBAGE_WORDS)
GARBAGE_RE = re.compile(GARBAGE_PATTERN, re.MULTILINE)
GARBAGE_THRESHOLD = 4

# Football teams
FOOTBALL_TEAMS = [
    "ยูเวนตุส",
    "อินเตอร์ มิลาน",
    "นาโปลี",
    "เอซี มิลาน",
    "ลาซิโอ",
    "โรม่า",
    "กัลโซ่",
    "เซเรีย",
    "ปาร์ม่า",
    "เอฟเวอร์ตัน",
    "ซันเดอร์แลนด์",
    "ลิเวอร์พูล",
    "แมนเชสเตอร์",
    "นิวคาสเซิล",
    "เชลซี",
    "อาร์เซนอล",
    "คลิสตัลพาเลช",
    "เซาแทมป์ตัน",
    "เซาแธมป์ตัน",
    "เชฟฟิลด์",
    "ฟอเรสต์",
    "เบอร์ตัน",
    "เบรนท์ฟอร์ด",
    "ฟูแล่ม",
    "ไฮไลท์ฟุตบอล",
    "เลบันเต้",
    "บาร์เซโลน่า",
    "เรอัล มาดริด",
    "เอสปันญ่อล",
]
FOOTBALL_PATTERN = "|".join(FOOTBALL_TEAMS)
FOOTBALL_RE = re.compile(FOOTBALL_PATTERN, re.MULTILINE)
FOOTBALL_THRESHOLD = 4

# Hotels Advertising
HOTEL_AD = [
    "โรงแรมอันดับ",
    "ที่พักแบบพิเศษอันดับ",
    "สถานที่พักอันดับ",
    "สถานที่พักคุ้มค่าอันดับ",
    "โรงแรมใกล้กับ",
    "โรงแรมที่ใกล้",
    "โรงแรม 4 ดาว",
    "โรงแรม 3 ดาว",
    "ที่พักพร้อมอาหารเช้า",
    "โรงแรมราคาถูก",
    "โรงแรมหรู",
]
HOTEL_AD_PATTERN = "|".join(HOTEL_AD)
HOTEL_AD_RE = re.compile(HOTEL_AD_PATTERN, re.MULTILINE)
HOTEL_AD_THRESHOLD = 4











