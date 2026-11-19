import csv
import json
import string
from anthropic import Anthropic    
from Inconsistency import Inconsistency
from InconsistencyReport import InconsistencyReport
from Issue import Issue

SYSTEM_PROMPT = """
You are looking for inconsistencies and Issues in a list, such as a serial number or mac address for a certain make or model being different than every other row with that same make and model.
Run checks on the length and character pattern for serial number and mac address of same models.
Each line in this input starts with "Row <number>: <Row Data>", the first row is the headers. When calling out a inconsistency or issue, append the Row Number for that non-standard value, to the "line_nums" array in your output
MidAtlantic RLNKS append 0000 to their mac address, that is normal. IP's, MAC Addresses, and Serial Numbers do not need to be sequential. Outlook names have (<number>) appended to them on purpose for room capacity
Install Date, AV Completed, Provisioning and Calendar Resource are sometimes only filled in on the first row of each room
If there is an inconsistency, report the value in the minority, NOT the ones that are in the majority.
If there are no discrepancies you find, outputting an empty list is the correct response, never output informational responses using issue, that will break the automation
"""

ISSUE_REPORT_TOOL = {
    "name": "report_ip_sheet_inconsistencies",
    "description": "Submit the inconsistencies you found in an IP Sheet, call once with all issues found",
    "input_schema": InconsistencyReport.model_json_schema()
}

def main():

    sheet = load_rows("rooms_test.csv")
    client = Anthropic()
    response = client.messages.create(model="claude-haiku-5-5", max_tokens=4096,
                                      system=SYSTEM_PROMPT,
                                      tools=[ISSUE_REPORT_TOOL],
                                      tool_choice={"type": "auto"},
                                      messages=[{"role": "user",
                                                 "content": f"Review this IP sheet for inconsistencies using report_ip_sheet_inconsistencies\n<ip_sheet>\n{sheet}\n</ip_sheet>"
                                                 }]
                                               )


    report = extract_report(response)
    with open("expected.json") as f:
        expected = InconsistencyReport.model_validate(json.load(f))
        grade(to_keys(expected), to_keys(report))


# def model_tryout(model, reps):
#     response = client.messages.create(model="claude-sonnet-5-5", max_tokens=4096,
#                                     system=SYSTEM_PROMPT,
#                                     tools=[ISSUE_REPORT_TOOL],
#                                     tool_choice={"type": "auto"},
#                                     messages=[{"role": "user",
#                                                 "content": f"Review this IP sheet for inconsistencies using report_ip_sheet_inconsistencies\n<ip_sheet>\n{sheet}\n</ip_sheet>"
#                                                 }]
#                                             )


def to_keys(report):
    keys = set()
    for issue in report.inconsistencies:
        keys.add((tuple(sorted(issue.line_nums)), issue.category))
    return keys

def grade(expected, actual):
    found = expected & actual
    missed = expected - actual
    extra = actual - expected

    print("Missed: ", missed)
    print("Extra: ", extra)
    print(f"recall: {len(found)}/{len(expected)}")
    print(f"precision: {len(found)}/{len(actual)}")   
    
def extract_report(response):
    if response.stop_reason != "tool_use":
        raise RuntimeError(f"Claude didn't call the tool, stop_reason: {response.stop_reason}")
    for block in response.content:
        if block.type == "tool_use":
            return InconsistencyReport.model_validate(block.input)


def load_rows(path):
    with open(path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        rows = []
        for num, row in enumerate(reader, start=1):
            cells = []
            for cell in row:
                cells.append(cell.replace("\n"," "))
            line_delimited_row = " | ".join(cells)                            
            clean_row = f'Row {num}: {line_delimited_row}'
            rows.append(clean_row)
        return "\n".join(rows)
if __name__ == "__main__":
    main()