def get_employee_info(employee_id):
    message = "Employee {} info...".format(employee_id)
    # Implement the real logic here. It can be query to database or requesting another RESTful API
    return message

def view_employee_pto(employee_id):
    message = "Employee {} has requested PTO. Reason: Vacation".format(employee_id)
    return message