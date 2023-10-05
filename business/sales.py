def get_quota():
    message = """
    🎯 **Sales Quota Status**

    **Quarterly Quota:** 100,000 units
    **Units Sold So Far:** 65,432 units
    **Remaining Quota for the Quarter:** 34,568 units

    **Annual Quota:** 400,000 units
    **Units Sold Year-to-Date:** 210,567 units
    **Remaining Quota for the Year:** 189,433 units

    Stay focused and keep pushing! Remember to utilize all resources and reach out if you need support.
    """
    return message


def get_clientinfo(client_id):
    message = """
    📇 **Client Information**

    **Client Name:** Acme Corp.
    **Client ID:** {}
    **Industry:** Manufacturing
    **Key Contact:** John Doe
    **Contact Email:** john.doe@acmecorp.com
    **Contact Phone:** +1 234-567-8901
    **Last Purchase:** $25,000 on September 1, 2023
    **Total Purchases Year-to-Date:** $125,000

    For more detailed information or to update client records, please use the CRM system or contact the sales admin team.
    """.format(client_id)
    return message
