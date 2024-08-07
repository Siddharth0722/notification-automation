import re


def extract_email():
    text = '[416b06b2887e] [EmailForwarder] Email notification sent to: registereduser6@maildrop.cc, MessageType: NEW_LOAD_COMMENT RuleId: 4027279 loadid: 13392146 companyid: trac-automation-shipper mode:  product_type: tracking response: {"status_code"=>"202", "body"=>"", "headers"=>{"server"=>["nginx"], "date"=>["Tue, 06 Aug 2024 08:33:38 GMT"], "content-length"=>["0"], "connection"=>["close"], "x-message-id"=>["-ZuPklMxTjWCde5EohhxzA"], "access-control-allow-origin"=>["https://sendgrid.api-docs.io"], "access-control-allow-methods"=>["POST"], "access-control-allow-headers"=>["Authorization, Content-Type, On-behalf-of, x-sg-elas-acl"], "access-control-max-age"=>["600"], "x-no-cors-reason"=>["https://sendgrid.com/docs/Classroom/Basics/API/cors.html"], "strict-transport-security"=>["max-age=600; includeSubDomains"]}}'

    # Regular expression to match email addresses
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    # Search for email address in the text
    email_match = re.search(email_pattern, text)

    if email_match:
        email = email_match.group()
        print(f"Extracted email: {email}")
    else:
        print("No email address found.")


extract_email()
