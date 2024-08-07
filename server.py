# demo log id : 13343908 time: 1 day
# add service name
import os
import pymongo
from dotenv import load_dotenv
from mongodb.mongodb import store_feedback
from debugging_logs.debugging import debugging
from get_signoz_logs.check_logs import check_signoz_logs
from update_payload.update_payload import update_payload
from flask import Flask, render_template, request, jsonify, make_response
from notification_triggers.new_load_comment.new_load_comment import check_new_load_comment_logs_error

app = Flask(__name__)
load_dotenv()


def get_body_of_logs(logs):
    log_bodies = [log["data"]["body"] for log in logs["data"]["result"][0]["list"]]
    return log_bodies

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/feedbackform")
def feedbackform():
    return render_template("feedbackform.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    return store_feedback(data)


@app.route("/debugging_loads", methods=["POST"])
def debugging_logs():
    data = request.get_json()
    load_id = data["load_id"]
    message_type = data["trigger_name"]
    environment_type = data["environment_type"]
    start_timestamp = data["start_date"] +" " + data["start_time"]
    end_timestamp = data["end_date"] +" " + data["end_time"]

    print(start_timestamp)
    print(end_timestamp)

    filter = [load_id, message_type]
    payload = update_payload(filter, start_timestamp, end_timestamp)
    logs = check_signoz_logs(payload, environment_type)
    if(logs["data"]["result"][0]["list"] == None):
        return make_response({"message":"No logs found"}, 200)
    
    logs_body = get_body_of_logs(logs)

    output = check_new_load_comment_logs_error(logs_body)
    return make_response({"message":output}, 200)
    return make_response({"message":"hello"}, 200)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
