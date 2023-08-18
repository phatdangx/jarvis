import db

def find_user_by_telegram_id(id):
    user = db.user.find_one({"telegram_id": str(id)})