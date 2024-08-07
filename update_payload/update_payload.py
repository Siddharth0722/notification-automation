import re, json, datetime


def get_unix_time_range(timestamp):
    date_time_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timestamp_ms = int(date_time_obj.timestamp() * 1000)
    return (int(timestamp_ms))


def update_payload(filters, start_timestamp, end_timestamp):
    with open("payload_template/payload.json", "r") as f:
        payload = json.load(f)

    filters = [
        {
            "id": "b86f46e2",
            "key": {
                "key": "body",
                "dataType": "string",
                "type": "",
                "isColumn": True,
                "isJSON": False,
                "id": "body--string----true",
            },
            "op": "contains",
            "value": filters[0],
        },
        {
            "id": "b86f46e2",
            "key": {
                "key": "body",
                "dataType": "string",
                "type": "",
                "isColumn": True,
                "isJSON": False,
                "id": "body--string----true",
            },
            "op": "contains",
            "value": filters[1],
        },
        {
            "id": "3654d59b",
            "key": {
                "key": "service.name",
                "dataType": "string",
                "type": "resource",
                "isColumn": True,
                "isJSON": False,
                "id": "service.name--string--resource--true",
            },
            "op": "in",
            "value": [
                "user-notification-service",
                "user-notification-worker",
                "global-worker-uns",
            ],
        },
    ]

    payload["compositeQuery"]["builderQueries"]["A"]["filters"]["items"] = filters
    payload["start"] = get_unix_time_range(start_timestamp)
    payload["end"] = get_unix_time_range(end_timestamp)

    open("update_payload/demo_payload.json", "w").write(json.dumps(payload))
    return payload
