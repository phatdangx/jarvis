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


# Available groups
HR = "hr"
SALES = "sales"
MARKETING = "marketing"
