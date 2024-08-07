import os
import pymongo
from dotenv import load_dotenv
from flask import make_response

load_dotenv()

def store_feedback(feedback):
    myclient = pymongo.MongoClient(os.getenv("MONGO_URL"))
    mydb = myclient["notification_automation"]
    mycol = mydb["feedbacks"]

    try:
        mycol.insert_one(feedback)
        return make_response({"message":"Feedback submitted successfully"}, 200)
    except Exception as e:
        print(f"Failed to insert feedback into MongoDB: {e}")
        return make_response({"message":"Failed to insert feedback into MongoDB"}, 500)