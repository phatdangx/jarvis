from config import Config

# Bot token
TOKEN = Config["jarvis"]["token"]

SUPER_ADMIN_CONTACT = "@{}".format(Config["super_admin"])

MONGO_SERVER = "mongodb://{}:{}@{}:{}".format(Config["mongodb"]["username"],
                                                Config["mongodb"]["password"],
                                                Config["mongodb"]["host"],
                                                Config["mongodb"]["port"])
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
        command_help="Fetch statistics for social media channels",
        command_synctax="/socialstats",
        command_ex="/socialstats"
    ),
    "cp_list": HELP_TEMPLATE.format(
        command_order=2,
        command_help="Get the status of current marketing campaigns",
        command_synctax="/campaignstatus",
        command_ex="/campaignstatus"
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
