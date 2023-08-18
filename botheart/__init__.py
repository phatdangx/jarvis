from config import get_config
from pymongo import MongoClient

import redis

config = get_config()

# Activation email template
ACTIVATION_EMAIL = "<p>Hi,</p><p>Click on the link below to activate Jarvis:</p>" \
                   "<p><a href='https://t.me/{bot_user_name}?start={secret}'>" \
                   "https://t.me/jarvis_ahm_dev_bot?start={secret}</a></p>" \
                   "<p>Your secret is: {secret}</p><p>Thanks</p>"

# Help template
HELP_TEMPLATE = "*{command_order}\.{command_help}* :\n \- Cú pháp: `{command_synctax}`\n \- Ví dụ: `{command_ex}`\n\n"
BD_HELP_DICT = {
    "bfb": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Khoá facebook cá nhân",
        command_synctax="/bfb <fb_id>",
        command_ex="/bfb 1010279895992238"
    ),
    "ufb": HELP_TEMPLATE.format(
        command_order=2,
        command_help="Mở khoá facebook cá nhân",
        command_synctax="/ufb <fb_id>",
        command_ex="/ufb 1010279895992238"
    ),
    "bp": HELP_TEMPLATE.format(
        command_order=3,
        command_help="Khoá facebook page",
        command_synctax="/bp <fb_page_id>",
        command_ex="/bp 545163675575891"
    ),
    "up": HELP_TEMPLATE.format(
        command_order=4,
        command_help="Mở khoá facebook page",
        command_synctax="/up <fb_page_id>",
        command_ex="/up 545163675575891"
    )
}

OP_HELP_DICT = {
    "ga": HELP_TEMPLATE.format(
        command_order=1,
        command_help="\[KA\] Lấy thông tin địa chỉ điểm lấy hàng và điểm giao hàng của 1 đơn LAZADA",
        command_synctax="/ga <tracking\_number>",
        command_ex="/ga AHMCR0000043486VNA"
    ),
    "uo": HELP_TEMPLATE.format(
        command_order=2,
        command_help="\[KA\] Sửa thông tin điểm LẤY HÀNG \(PICKUP\) của 1 đơn LAZADA \(Fail API do sai địa chỉ\)",
        command_synctax="/uo <tracking\_number> <new\_origin\_address, đặt giữa 2 dấu \[\]",
        command_ex="/uo AHMCR0000043486VNA [81A Nguyễn Hữu Cầu, Phường Tân Định, Quận 1, Hồ Chí Minh]"
    ),
    "ud": HELP_TEMPLATE.format(
        command_order=3,
        command_help="\[KA\] Sửa thông tin điểm GIAO HÀNG \(DROP\_OFF\) của 1 đơn LAZADA \(Fail API do sai địa chỉ\)",
        command_synctax="/ud <tracking\_number> <new\_destination\_address, đặt giữa 2 dấu \[\]",
        command_ex="/ud AHMCR0000043486VNA [439/8/27 Đường số 10, Phường 8, Quận Gò Vấp, Hồ Chí Minh]"
    ),
    "rbt": HELP_TEMPLATE.format(
        command_order=4,
        command_help="\[KA\] Tạo lại đơn LAZADA bằng tracking\_number ",
        command_synctax="/rbt <tracking\_number>",
        command_ex="/rbt AHMCR0000043486VNA"
    ),
    "aco": HELP_TEMPLATE.format(
        command_order=5,
        command_help="\[KA\] Auto complete đơn",
        command_synctax="/aco <supplier id> <danh sach order id, đặt giữa 2 dấu \[\]",
        command_ex="/aco 84944309347 [ABC,DEF]"
    ),
    "ess": HELP_TEMPLATE.format(
        command_order=6,
        command_help="\[OPS\] Gán service cho tài xế",
        command_synctax="/ess <supplier id>",
        command_ex="/ess 84944309347"
    ),
    "geo": HELP_TEMPLATE.format(
        command_order=7,
        command_help="\[KA\] Sửa lại lat long cho package LAZADA ở vùng giáp ranh giữa các tỉnh",
        command_synctax="/geo <tracking number>",
        command_ex="/geo AHMMP0000888651VNA"
    ),
    "uwo": HELP_TEMPLATE.format(
        command_order=8,
        command_help="\[Warehouse\] Update trạng thái packge warehouse",
        command_synctax="/uwo <waiting order id> <new status>",
        command_ex="/uwo LAZADA\_AHMMP0000888651VNA WAITING\_FOR\_RO"
    )
}

TECH_HELP_DICT = {
    "cr": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Kiểm tra refund",
        command_synctax="/cr <PaymentProvider> <OrderID>",
        command_ex="/cr momo 205Z4UN5"
    ),
    "ccb": HELP_TEMPLATE.format(
        command_order=2,
        command_help="Tra cứu lịch sử callback",
        command_synctax="/ccb <Option> <OrderID hoặc TrackingNumber>. Option: 1=By OrderID, 2=By TrackingNumber",
        command_ex="/ccb 1 205Z4UN5 hoặc /ccb 2 AHMMP0000037052VNA"
    ),
    "cb": HELP_TEMPLATE.format(
        command_order=3,
        command_help="Đồng bộ trạng thái cho partner",
        command_synctax="/cb <OrderID> <\[OrderStatus\]>",
        command_ex="/cb 205Z4UN5 [ACCEPTED]"
    ),
    "bo": HELP_TEMPLATE.format(
        command_order=4,
        command_help="Broadcast đơn hàng",
        command_synctax="/bo <OrderID>",
        command_ex="/bo 205Z4UN5"
    ),
    "rcs": HELP_TEMPLATE.format(
        command_order=5,
        command_help="Thống kê recommend theo socket[fcm]",
        command_synctax="/rcs <NotiProvider> <X hours ago>",
        command_ex="/rcs socket 2"
    ),
    "rp": HELP_TEMPLATE.format(
        command_order=6,
        command_help="Repush đơn hàng của partner",
        command_synctax="/rp <Partner> <X hours ago>",
        command_ex="/rp lazada 2"
    ),
    "bso": HELP_TEMPLATE.format(
        command_order=7,
        command_help="Tìm và rebroadcast các đơn hàng chưa chuyển IDLE thành ASSIGNING",
        command_synctax="/bso <X hours ago>",
        command_ex="/bso 2"
    ),
    "wld": HELP_TEMPLATE.format(
        command_order=8,
        command_help="Whitelist device",
        command_synctax="/wld <device_imei> <owner_name> <department>",
        command_ex="/wld DE48DEDA-9F63-42D9-BB40-F20E6778E1BA Thang tech"
    ),
    "co": HELP_TEMPLATE.format(
        command_order=9,
        command_help="Cancel order",
        command_synctax="/co <order_id> <admin_id> <[comment]>",
        command_ex="/co 211773J1 84944309348 [System error]"
    ),
    "cd": HELP_TEMPLATE.format(
        command_order=10,
        command_help="Close a deal",
        command_synctax="/cd <deal_id>",
        command_ex="/cd 6290362255955541b2d12701"
    ),
    "complete": HELP_TEMPLATE.format(
        command_order=11,
        command_help="Complete order",
        command_synctax="/complete <order_id>",
        command_ex="/complete 22XMDJLK"
    ),
    "reset": HELP_TEMPLATE.format(
        command_order=12,
        command_help="Reset a child order status back to ACCEPTED",
        command_synctax="/reset <order_id>",
        command_ex="/reset 22XMDJLK"
    ),
    "city": HELP_TEMPLATE.format(
        command_order=13,
        command_help="Get city by lat long",
        command_synctax="/city <lat> <lng>",
        command_ex="/city 10.8315392 106.6773514"
    ),
    "district": HELP_TEMPLATE.format(
        command_order=14,
        command_help="Get district by lat long",
        command_synctax="/district <lat> <lng>",
        command_ex="/district 10.8315392 106.6773514"
    ),
    "trip": HELP_TEMPLATE.format(
        command_order=15,
        command_help="Plan 4H or 2H trip \- only support stg and uat",
        command_synctax="/trip <env> <service id>",
        command_ex="/trip stg SGN-SAMEDAY"
    ),
    "spa": HELP_TEMPLATE.format(
        command_order=16,
        command_help="Setup supplier/user accounts for a partner",
        command_synctax="/spa <mobile numbers> <partner id> <partner email>",
        command_ex="/spa 84867111111,84867222222 LAZODO lazodo@lazodo.com.vn"
    ),
    "rfs": HELP_TEMPLATE.format(
        command_order=17,
        command_help="Hoàn tiền cho tài xế nếu order bị cancel",
        command_synctax="/rfs <supplier numbers> <order id>",
        command_ex="/rfs 84867111111 22XMDJLK"
    )
}

# Available GROUPS
TECH = "TECH"
BD = "BD"
OP = "OP"
KA = "KA"

# Bot Admin contact
ADMIN_CONTACT = "@steven_dang"

# Jarvis TOKEN
TOKEN = config["jarvis"]["token"]

# Redis
redis_key_pattern = "jarvis:{}"
redis_connection_pool = redis.ConnectionPool(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["db"],
    password=config["redis"]["password"]
)
redis_client = redis.Redis(connection_pool=redis_connection_pool)


# DB connection init
MONGODB_SERVER = config["mongo"]["primary"]
MONGODB_SERVER_READONLY = config["mongo"]["secondary"]
MONGODB_LOG_SERVER = config["mongolog"]["primary"]
MONGODB_LOG_SERVER_READONLY = config["mongolog"]["secondary"]

client = MongoClient(MONGODB_SERVER, serverSelectionTimeoutMS=1000, connectTimeoutMS=10000)
clientr = MongoClient(MONGODB_SERVER_READONLY, serverSelectionTimeoutMS=1000, connectTimeoutMS=10000)

db = client.ahamove
dbr = clientr.ahamove

if config["env"] == "prod":
    log_client = MongoClient(MONGODB_LOG_SERVER, serverSelectionTimeoutMS=1000, connectTimeoutMS=10000)
    log_clientr = MongoClient(MONGODB_LOG_SERVER_READONLY, serverSelectionTimeoutMS=1000, connectTimeoutMS=10000)
    dblog = log_client.ahamovelog
    dblogr = log_clientr.ahamovelog
else:
    dblog = client.ahamovelog
    dblogr = clientr.ahamovelog

KA_SUPPLIER_IDS = [
    "84944309347",  # Phat
    "84354410865",
    "84766972846",
    "84786897613",
    "84774487690",
    "84796469484",
    "84354804065",
    "84363722677",
    "84354914465",
    "84353173865",
    "84797617994",
    "84702806189",
    "84706960184",
    "84702885484",
    "84702805584",
    "84706964190",
    "84906806122",
    "84906982293",
    "84906894214",
    "84906774513",
    "84906709213",
    "84909229174",
    "84909294510",
    "84909298744",
    "84909548961",
    "84931138442",
    "84909258840",
    "84909304812",
    "84909384025",
    "84909268834",
    "84909923473",
    "84568427052",
    "84568427049",
    "84568427050",
    "84568427047",
    "84568427048",
    "84568427043",
    "84568427044",
    "84568427041",
    "84568427042",
    "84568427034",
    "84563202656",
    "84563202736",
    "84563202846",
    "84563202415",
    "84563202823",
    "84924738869",
    "84924228898",
    "84924229045",
    "84924228766",
    "84924229019",
    "84586631868"
]

# order transaction type
WITHDRAWAL = "WITHDRAWAL"
ORDER_COMMISSION = "ORDER_COMMISSION"
ORDER_RECEIVABLE = "ORDER_RECEIVABLE"
ORDER_PAYMENT = "ORDER_PAYMENT"
ORDER_CANCEL = "ORDER_CANCEL"

# status
PENDING = "PENDING"

# payment method
MOMO = "MOMO"
