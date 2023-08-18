from email import message
from botheart import *
from sendgrid.helpers.mail import Email, Content, Mail, Personalization, Substitution, Attachment

import requests
import json
import logging
import sendgrid
import random
import string
import time
from pytz import utc
from datetime import datetime
from pymongo.collection import ReturnDocument, ObjectId

sendgrid_con = None


def check_momo_refund(order_id):
    check_refund_url = config["service_url"]["payment"] + "/api/v3/internals/payment/bot/check-momo-refund"
    order = dbr.order.find_one({"_id": order_id})
    if not order:
        message = "Order not found"
    else:
        try:
            r = requests.post(
                url=check_refund_url,
                data=json.dumps({
                    "order_id": order["_id"]
                })
            )
            if r.status_code == 200 and r.text:
                message = r.json()["message"] if "message" in r.json() else "Missing field message"
            else:
                message = r.text
        except Exception as e:
            message = str(e)
    return message


def get_callback_history_by_order_id(order_id):
    history = list(dblogr.partner_callback.find({"order_id": order_id}))
    if len(history) == 0:
        mess = "Not Found"
    else:
        mess = "⭐️ Callback History:"
        for item in history:
            timeObject = datetime.fromtimestamp(item["callback_time"])
            timeStr = timeObject.strftime("%d/%m/%Y %H:%M:%S")
            del item["_id"]
            mess += "\n{} : {} - {} - {} - {} - {}".format(
                timeStr,
                item["order_id"],
                item["tracking_number"],
                item["order_status"].replace("_", "\_"),
                item["response_code"],
                item["response_text"],
            )
    # standardize mess
    mess = mess.replace("_", "\_")

    return mess


def get_callback_history_by_tracking_number(tracking_number):
    history = list(dblogr.partner_callback.find({"tracking_number": tracking_number}))
    if len(history) == 0:
        mess = "Not Found"
    else:
        mess = "⭐ Callback History:"
        for item in history:
            del item["_id"]
            timeObject = datetime.fromtimestamp(item["callback_time"])
            timeStr = timeObject.strftime("%d/%m/%Y %H:%M:%S")
            mess += "\n{} : {} - {} - {} - {} - {}".format(
                timeStr,
                item["order_id"],
                item["tracking_number"],
                item["order_status"].replace("_", "\_"),
                item["response_code"],
                item["response_text"],
            )
    # standardize mess
    mess = mess.replace("_", "\_")

    return mess


def call_partner_webhook(order_id, status):
    message = "Callback error"
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/internal/callback_partner?order_id={}&status={}".format(
            order_id, status
        )
    )
    if r.status_code == 200:
        message = f"[{order_id}] Callback success"
    else:
        message += " - [{}] Error code:{}".format(order_id, r.status_code)
    return message


def broadcast_idle(order_id):
    message = "Broadcast error"
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/internal/broadcast_idle?order_id={}".format(
            order_id
        )
    )
    if r.status_code == 200:
        message = "Broadcast success"
    else:
        message += " - Error code:{}".format(r.status_code)
    return message


def rec_stat(push_type, from_time, to_time):
    try:
        r = requests.get(
            url=config["service_url"]["api-app"] + "/v1/bot/get_rec_stat?push_type={}&from_time={}&to_time={}".format(
                push_type,
                from_time,
                to_time
            )
        )
        if r.status_code == 200:
            if len(r.json()["data"]) > 0:
                message = "RECOMMEND BY **{}** STATS:\n".format(push_type.upper())
                data = r.json()["data"]
                logging.debug(data)
                for item in data:
                    message += "- {}: {}%\n".format(item["status"].replace("_", "-"), item["percent"])
            else:
                message = "Không tìm thấy kết quả thống kê"
        else:
            message = r.text
    except Exception as e:
        message = str(e)
    return message


def repush_partner_order(partner, from_time, to_time):
    try:
        r = requests.get(
            url=config["service_url"][
                    "api-app"] + "/v1/bot/retry_partner_orders?partner={}&from_time={}&to_time={}".format(
                partner,
                from_time,
                to_time
            )
        )
        if r.status_code == 200:
            data = r.json()
            message = "FOUND: {} - REPUSH: {}".format(data["found"], data["re_pushed"])
        else:
            message = r.text
    except Exception as e:
        message = str(e)
    return message


def broadcast_stuck_orders(from_time, to_time):
    try:
        r = requests.get(
            url=config["service_url"]["api-app"] + "/v1/bot/broadcast_stuck_orders?from_time={}&to_time={}".format(
                from_time,
                to_time
            )
        )
        if r.status_code == 200:
            data = r.json()
            message = "FOUND: {} - BROADCAST: {}".format(data["found"], data["broadcast"])
        else:
            message = r.text
    except Exception as e:
        message = str(e)
    return message


def whitelist_device(imei, name, department, create_by):
    message = "Whitelist [{}] cho [{}] thất bại".format(imei, name)
    whitelist_url = "{}/api/v3/internal/user/internal-device".format(config["service_url"]["user"])
    try:
        body = {
            "device_id": imei,
            "owner": name,
            "department": department.upper(),
            "create_by": create_by
        }
        logging.debug(body)
        r = requests.post(
            url=whitelist_url,
            json=body
        )
        if r.status_code == 200:
            message = "Whitelist *{}* cho *{}* thành công.".format(imei, name)
        else:
            r.raise_for_status()
    except Exception as e:
        message = "Whitelist exception"
    return message


def send_email(subject, body, to_addresses, source="AhaMove <support@ahamove.com>", email_format="text/html"):
    global sendgrid_con
    if sendgrid_con is None:
        sendgrid_con = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    to_emails = Personalization()
    for to_address in to_addresses:
        to_emails.add_to(Email(to_address))

    mail = Mail()
    mail.from_email = Email(source)
    mail.subject = subject
    mail.add_content(Content(email_format, body))
    mail.add_personalization(to_emails)
    r = sendgrid_con.client.mail.send.post(request_body=mail.get())


def generate_secret():
    code = ''.join(random.choice(string.digits) for _ in range(4))
    return code


def get_lzd_address_by_tracking_number(tracking_number):
    message = "Data of {} can not be found".format(tracking_number)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/get_lzd_order_address?tracking_number={}".format(
            tracking_number
        )
    )
    if r.status_code == 200 and "tracking_number" in r.json():
        resp = r.json()
        message = "*Origin:* {}\n*Destination:* {}".format(resp["origin"], resp["destination"])
    return message


def update_lazada_origin_address(tracking_number, new_origin):
    message = "Update {} origin address FAILED".format(tracking_number)
    r = requests.post(
        url=config["service_url"]["api-app"] + "/v1/bot/fix_lzd_address",
        json={
            "tracking_number": tracking_number,
            "new_origin": new_origin
        }
    )
    if r.status_code == 200:
        message = "Update {} origin address SUCCESSFULLY".format(tracking_number)
    return message


def update_lazada_destination_address(tracking_number, new_destination):
    message = "Update {} destination address FAILED".format(tracking_number)
    r = requests.post(
        url=config["service_url"]["api-app"] + "/v1/bot/fix_lzd_address",
        json={
            "tracking_number": tracking_number,
            "new_destination": new_destination
        }
    )
    if r.status_code == 200:
        message = "Update {} destination address SUCCESSFULLY".format(tracking_number)
    return message


def update_lazada_origin_geocoding(tracking_number):
    message = "Update new geocoding FAILED"
    r = requests.post(
        url=config["service_url"]["api-app"] + "/v1/bot/fix_lzd_address",
        json={
            "tracking_number": tracking_number,
            "new_geocoding": True
        }
    )
    if r.status_code == 200:
        message = "Update new geocoding SUCCESSFULLY"
    else:
        message = r.text
    return message


def repush_lazada_order_by_tracking_number(tracking_number):
    message = "Repush {} FAILED".format(tracking_number)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/retry_lzd_by_tracking?tracking_number={}".format(
            tracking_number
        ),
    )
    if r.status_code == 200:
        message = "Repush {} SUCCESSFULLY".format(tracking_number)
    return message


def block_fb(fb_id):
    message = "FAILED to block {}".format(fb_id)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/block_fb?fb_id={}".format(
            fb_id
        ),
    )
    if r.status_code == 200:
        message = "BLOCKED facebook with ID = {}".format(fb_id)
    return message


def unblock_fb(fb_id):
    message = "FAILED to unblock {}".format(fb_id)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/unblock_fb?fb_id={}".format(
            fb_id
        ),
    )
    if r.status_code == 200:
        message = "UNBLOCKED facebook with ID = {}".format(fb_id)
    return message


def block_fb_page(page_id):
    message = "FAILED to block page {}".format(page_id)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/block_fb_page?page_id={}".format(
            page_id
        ),
    )
    if r.status_code == 200:
        message = "BLOCKED facebook page with ID = {}".format(page_id)
    return message


def unblock_fb_page(page_id):
    message = "FAILED to unblock page {}".format(page_id)
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/unblock_fb_page?page_id={}".format(
            page_id
        ),
    )
    if r.status_code == 200:
        message = "UNBLOCKED facebook page with ID = {}".format(page_id)
    return message


def auto_complete_orders(supplier_id, order_ids):
    message = "FAILED to complete order"
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/bot/auto_complete_order?supplier_id={}&order_ids={}".format(
            supplier_id,
            order_ids
        ),
        headers={
            "Authorization": "Bearer 2a3ed4a50e40ac863e73ed6df939818f205f2b1acea5b8613979e0a0f06b9f37"
        }
    )
    if r.status_code == 200:
        message = "SUCCESSFULLY complete these order. Check the order status again after 1 hours"
    return message


def cancel_order(admin_id, order_id, cancel_comment):
    message = "FAILED to cancel order"
    admin_token = db.supplier_token.find_one({"supplier_id": admin_id, "role": {"$in": ["moderator", "admin"]}})
    if not admin_token:
        message = "Admin token not found"
    if cancel_comment == "":
        message = "Cancel comment can not be empty"
    r = requests.get(
        url=config["service_url"]["api-app"] + "/v1/order/cancel?token={}&order_id={}&comment={}".format(
            admin_token["token"],
            order_id,
            cancel_comment
        )
    )
    if r.status_code == 200:
        message = "CANCEL SUCCESSFULLY"
    return message


def close_deal(deal_id):
    if deal_id != "":
        r = requests.put(
            url="{}/api/v3/internal/order/mart/group/close-deal/{}".format(config["service_url"]["order"], deal_id)
        )
        if r.status_code == 200:
            message = "close deal successfully"
        else:
            message = "error: {}".format(r.text)
    else:
        message = "invalid deal id"
    return message


def complete_order(order_id):
    m = "💔"
    try:
        if order_id != "":
            order = db.order.find_one({"_id": order_id})
            if order["status"] in ["COMPLETED", "CANCELLED"]:
                return "order status not valid"
            if "supplier_id" not in order or not order["supplier_id"]:
                return "supplier id is missing"
            supplier_token = db.supplier_token.find_one({"supplier_id": order["supplier_id"]})
            if supplier_token:
                # pickup first
                is_picked_up = False
                if order["status"] == "ACCEPTED":
                    r = requests.get(
                        url="{}/v1/order/pickup?order_id={}&token={}".format(
                            config["service_url"]["api-app"],
                            order_id,
                            supplier_token["token"]))
                    if r.status_code != 200:
                        return "error when picking up package"
                    is_picked_up = True
                if order["status"] == "IN PROCESS" or is_picked_up:
                    # complete every stop point first
                    for i in range(1, len(order["path"])):
                        if "status" not in order["path"][i]:
                            r = requests.get(
                                url="{}/v1/order/complete?order_id={}&token={}".format(
                                    config["service_url"]["api-app"],
                                    "{}-{}".format(order_id, str(i)),
                                    supplier_token["token"]
                                )
                            )
                            if r.status_code != 200:
                                return "error when completing {}-{}".format(order_id, str(i))
                    # complete whole order
                    r = requests.get(
                            url="{}/v1/order/complete?order_id={}&token={}".format(
                                config["service_url"]["api-app"],
                                order_id,
                                supplier_token["token"]))
                    if r.status_code == 200:
                        m = "complete {} successfully".format(order_id)
                    else:
                        m = "fail to complete {}: {}".format(order_id, r.text)
            else:
                m = "supplier token not found"
        else:
            m = "invalid order id"
    except Exception as e:
        m = "😂 - {}".format(str(e))
    return m


def reset_sameday_order_to_accepted(order_id):
    if order_id != "":
        order = db.order.find_one({"_id": order_id})
        if "parent_id" not in order or not order["parent_id"]:
            m = "can not reset order without parent"
        if "status" in order and order["status"] in ["CANCELLED"]:
            m = "invalid order status"
        parent_order = db.order.find_one({"_id": order["parent_id"]})
        child_order_pickup_index = 0
        child_order_drop_off_index = 0
        for i in range(0, len(order["path"])):
            if "order_id" in order["path"][i] and order["path"][i]["order_id"] == order_id and \
                    "action_type" in order["path"][i] and order["path"][i]["action_type"] == "PICK UP":
                child_order_pickup_index = i
            if "order_id" in order["path"][i] and order["path"][i]["order_id"] == order_id and \
                    "action_type" in order["path"][i] and order["path"][i]["action_type"] == "DROP OFF":
                child_order_drop_off_index = i
        # reset status
        child_res = db.order.update_one(
            {"_id": order_id},
            {
                "$set": {
                    "status": "ACCEPTED"
                },
                "$unset": {
                    "path.1.status": ""
                }
            }
        )
        parent_res = db.order.update_one(
            {"_id": parent_order["_id"]},
            {
                "$unset": {
                    "path.{}.status".format(child_order_pickup_index): "",
                    "path.{}.status".format(child_order_drop_off_index): ""
                }
            }
        )
        if child_res.matched_count != 0 and parent_res.matched_count != 0:
            m = "reset status for {}".format(order_id)
        else:
            m = "reset failed!"
    else:
        m = "invalid order id"
    return m


def get_city_by_lat_lng(lat, lng):
    city = db.city.find_one(
        {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    }
                }
            }
        }
    )
    if city:
        m = "{}".format(city["_id"])
    else:
        m = "city not found"
    return m


def get_district_by_lat_lng(lat, lng):
    city = db.city.find_one(
        {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    }
                }
            }
        }
    )
    if not city:
        m = "city not found"
    else:
        district = dblog.geomap.find_one({
            "city_id": city["_id"],
            "engtype_2": {
                "$in": [
                    "Urban District",
                    "District",
                    "Township",
                    ""
                ]
            },
            "type_3": {"$eq": None},
            "geometry": {
                "$geoIntersects": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    }
                }
            }
        })
        if district:
            m = "{} ({})".format(district["hasc_2"], district["name_2"])
        else:
            m = "district not found"
    return m


def plan_trip_2h_4h(env, service_id):
    if service_id != "" and env != "" and env in ["stg", "uat"]:
        url = config["service_url"]["plan-trip-stg"]
        if env == "uat":
            url = config["service_url"]["plan-trip-uat"]
        r = requests.post(
            url=url,
            data=json.dumps({
                "service_ids": service_id
            })
        )
        if r.status_code == 200:
            response = r.json()
            if "logUrl" in response and response["logUrl"]:
                m = "<a href='{}'> 📊 Cloud Watch </a>".format(response["logUrl"])
            else:
                m = "No Log URL"
        else:
            m = "fail to plan trip"

    else:
        m = "invalid parameters"
    return m


def stat_order_today():
    now = datetime.now()
    today_start_time = time.mktime(utc.localize(datetime(now.year, now.month, now.day, 0, 0, 0)).utctimetuple())
    current_time = time.time()
    query = {
        "city_id": {"$exists": True},
        "create_time": {
            "$gte": today_start_time,
            "$lt": current_time
        }
    }
    order_count = dbr.order.find(query).count()
    order_today_count = dbr.order_today.find(query).count()
    m = "order_count = {}\norder_today_count= {}".format(order_count, order_today_count)
    return m


def enable_supplier_service(supplier_id):
    supplier = dbr.supplier.find_one({"_id": supplier_id})
    if not supplier:
        m = "supplier not found"
        return m
    if "services" not in supplier or len(supplier["services"]) == 0:
        m = "tài xế chưa được gán service"
    elif "enabled_services" in supplier and len(supplier["enabled_services"]) > 0:
        m = "tài xế đã enable service"
    else:
        first_service_id = supplier["services"][0]
        db.supplier.update_one({"_id": supplier_id}, {"$set": {"enabled_services": [first_service_id]}})
        m = "gán service {} cho tài xế thành công".format(first_service_id)

    return m


def setup_partner_accounts(mobile_numbers, partner_id, partner_email):
    data = {
        "partner_mobiles": mobile_numbers,
        "partner_id": partner_id,
        "partner_email": partner_email,
    }

    r = requests.post(
        url=config["service_url"]["api-host"] + "/api/v3/internal/partner-portal/testing-accounts",
        json=data,
    )
    if r.status_code != 200:
        return "Tạo tài khoản thất bại, liên hệ @khangvu4122"

    return "Tạo tài khoản thành công"


def add_supplier_transaction(supplier, currency, amount, type, order_id=None, ref_id=None, note="",
                             transaction_id=None, payment_provider_log_id=None, status=None):
    transaction = {
        "supplier_id": supplier["_id"],
        "currency": currency,
        "amount": amount,
        "main_account": supplier["main_account"][currency] if currency in supplier["main_account"] else 0,
        "bonus_account": supplier["bonus_account"][currency] if currency in supplier["bonus_account"] else 0,
        "type": type,
        "time": time.time()
    }
    if transaction_id:
        transaction["_id"] = ObjectId(transaction_id)
    if order_id:
        transaction["order_id"] = order_id
    if ref_id:
        transaction["ref_id"] = ref_id
    if note:
        transaction["note"] = note
    if status:
        transaction["status"] = status
    if payment_provider_log_id:
        transaction["payment_provider_log_id"] = payment_provider_log_id
    if "deposit_account" in supplier:
        transaction["deposit_account"] = supplier["deposit_account"][currency] \
            if currency in supplier["deposit_account"] else 0

    # Admin can recall from main_account with type is WITHDRAWAL, so we need to check this condition before add source
    if type is WITHDRAWAL and status is PENDING:
        transaction["source"] = MOMO.lower()

    result = db.supplier_transaction.insert_one(transaction)

    if "_id" not in transaction:
        transaction["_id"] = result.inserted_id
    return transaction


def refund_supplier(supplier_id, order_id):
    try:
        order = db.order.find_one({"_id": order_id})
        currency = order["currency"]
        supplier_transactions = list(db.supplier_transaction.find({
            "supplier_id": supplier_id,
            "time": {
                "$gt": order["create_time"]
            },
            "type": {
                "$in": [ORDER_COMMISSION, ORDER_RECEIVABLE, ORDER_PAYMENT, ORDER_CANCEL]
            },
            "order_id": order_id
        }))
        if len(supplier_transactions) == 0:
            return "ERROR: {} - {} - transaction not found".format(order_id, supplier_id)

        sum_amount = 0
        cancel_trans_count = 0
        for trans in supplier_transactions:
            sum_amount += trans["amount"]
            if trans["type"] == ORDER_CANCEL:
                cancel_trans_count += 1
        if cancel_trans_count > 1:
            return "ERROR: {} - {} - more than 1 cancel transaction".format(order_id, supplier_id)
        if sum_amount == 0:
            return "ERROR: {} - {} - refunded".format(order_id, supplier_id)
        # sum_amount > 0 mean AHM need to collect money from supplier when order cancel
        refund_amount = -sum_amount
        updates = {"main_account.VND": refund_amount}
        supplier = db.supplier.find_one_and_update(
            {"_id": supplier_id},
            {"$inc": updates},
            return_document=ReturnDocument.AFTER
        )
        if supplier:
            add_supplier_transaction(supplier, currency, refund_amount, ORDER_CANCEL, order["_id"])
        return "SUCCESS: refunded for {} - {}".format(supplier_id, order_id)
    except Exception as e:
        return "ERROR: {}".format(str(e))


def update_waiting_order_record(wid, new_status):
    r = dblog.waiting_order.update_one(
        {
            "_id": wid
        },
        {
            "$set": {
                "status": new_status,
                "updated_by_bot": True
            }
        }
    )
    if r.matched_count != 0:
        return "Success"
    else:
        return "Failed"

