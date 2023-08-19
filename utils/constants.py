from config import Config

# Bot token
TOKEN = Config["jarvis"]["token"]

ADMIN_CONTACT = "@{}".format(Config["admin"])

MONGO_SERVER = Config["mongodb"]["host"]
MONGO_DATABASE = Config["mongodb"]["database"]

# Help template
HELP_TEMPLATE = "*{command_order}\.{command_help}* :\n \- Syntax: `{command_synctax}`\n \- Example: `{command_ex}`\n\n"
HR_HELP_DICT = {
    "info": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Instant check employee information",
        command_synctax="/info <employee_id>",
        command_ex="/info 16578976"
    ),
    "viewpto": HELP_TEMPLATE.format(
        command_order=2,
        command_help="View employee PTO request",
        command_synctax="/viewpto <employee_id>",
        command_ex="/viewpto 16578976"
    )
}

MAR_HELP_DICT = {
    "cp_track": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Instant view marketing campaign metric",
        command_synctax="/campaign_track <campaign_id>",
        command_ex="/campaign_track fb_114"
    ),
    "cp_list": HELP_TEMPLATE.format(
        command_order=2,
        command_help="List all of campaign in the last N days",
        command_synctax="/cp_list <days>",
        command_ex="/cp_list 7"
    )
}


SALES_HELP_DICT = {
    "product_info": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Instant get product information",
        command_synctax="/product_info <product_id>",
        command_ex="/product_info 28"
    ),
    "leaderboard": HELP_TEMPLATE.format(
        command_order=2,
        command_help="View top sales performance",
        command_synctax="/leaderboard",
        command_ex="/leaderboard"
    )
}


# Available groups
HR = "hr"
SALES = "sales"
MARKETING = "marketing"
