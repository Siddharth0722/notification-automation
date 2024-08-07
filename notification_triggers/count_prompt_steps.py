import re

def count_steps(text):
    item_pattern = re.compile(r'^\d+\.\s+.*$', re.MULTILINE)
    items = item_pattern.findall(text)
    item_count = len(items)

    return item_count