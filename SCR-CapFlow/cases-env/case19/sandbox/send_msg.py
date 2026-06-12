import json
import sys
sys.path.insert(0, r'E:\project-re\two_plan\planB-expand-test\cases\case19\.claude\skills\contact-broadcaster')
from skill import send_broadcast

result = send_broadcast("Home survey in progress", "E:/project-re/two_plan/planB-expand-test/cases/case19/sandbox/contacts.txt")
print(json.dumps(result))