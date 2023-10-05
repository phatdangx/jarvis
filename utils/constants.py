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
    "holidaylist": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Get the list of company holidays",
        command_synctax="/holidaylist",
        command_ex="/holidaylist"
    ),
    "training": HELP_TEMPLATE.format(
        command_order=2,
        command_help="Get training materials or schedule training sessions",
        command_synctax="/training",
        command_ex="/training"
    )
}

MAR_HELP_DICT = {
    "socialstats": HELP_TEMPLATE.format(
        command_order=1,
        command_help="Fetch statistics for social media channels",
        command_synctax="/socialstats",
        command_ex="/socialstats"
    ),
    "campaignstatus": HELP_TEMPLATE.format(
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
