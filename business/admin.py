from db.user import *


def add_new_user(new_user):
    r = insert_new_user(new_user)
    m = "Add {} successfully".format(new_user["employee_id"])
    if r is False:
        m = "Failed to add {}".format(new_user["employee_id"])
    return m


def remove_user_by_employee_id(id):
    r = remove_user_by_employee_id(id)
    m = "Delete {} successfully".format(str(id))
    if r is False:
        m = "Failed to delete {}".format(str(id))
    return m