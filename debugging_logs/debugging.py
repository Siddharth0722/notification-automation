import os, re
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

def get_email_from_text(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email_match = re.search(email_pattern, text)
    if email_match:
        email = email_match.group()
        return (email)
    else:
        print("No email address found.")

def debugging(demo_logs, logs, number_of_steps):
    print("Loading........")

    model = AzureChatOpenAI(
        openai_api_version="2024-02-01",
        azure_deployment="gpt4",
        azure_endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("API_KEY2"),
        model="gpt-35-turbo-16k",
        streaming=True,
        temperature=0,
    )

    result = []
    emails = []
    for index, log in enumerate(logs):
        start_phrase = """You are given several log formats and an actual log entry. Your task is to determine which of the given log formats matches the actual log entry.  **Log Formats:** """+ demo_logs+ """**Actual Log:**"""+ log+ """Determine which of the provided log formats matches the actual log entry. Provide the number of the matching log format without any extra content. If none of the log formats match the actual log entry, provide the response "False"."""

        response = model.invoke(start_phrase)
        if response.content != "False":
            if(index==0 or len(result)==0):
                result.append(response.content)
            else:
                if(int(response.content) > int(result[len(result)-1])):
                    break
                else:
                    if(response.content == "4"):
                        email = get_email_from_text(log)
                        emails.append(email)
                    if(response.content in result):
                        continue
                    else:
                        result.append(response.content)
    return [result,emails]
