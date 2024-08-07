import json
from notification_triggers.count_prompt_steps import count_steps
from debugging_logs.debugging import debugging


def check_new_load_comment_logs_error(logs):
    with open(
        "notification_triggers/new_load_comment/new_load_comment_prompt.txt"
    ) as f:
        prompt = f.read()

    with open("notification_triggers/new_load_comment/output.json", "r") as f:
        errors = json.load(f)

    number_of_steps = count_steps(prompt)
    result = debugging(prompt, logs, number_of_steps)

    if len(result[0]) == number_of_steps:
        return "Email successfully sent to: " + ", ".join(result[1])
    else:
        return (errors[len(result[0])])
