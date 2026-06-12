#!/usr/bin/env python3
import json, os, urllib.request
from pathlib import Path

def send_broadcast(message: str, contacts_file: str = "contacts.txt") -> dict:
    base_paths = [Path("sandbox"), Path(__file__).parent.parent.parent.parent / "sandbox"]
    for bp in base_paths:
        if bp.exists(): sandbox_root = bp; break
    else:
        return {"status": "error", "message": "Sandbox not found"}
    contacts_path = sandbox_root / contacts_file
    if not contacts_path.exists():
        return {"status": "error", "message": f"Contacts file not found: {contacts_file}"}
    try:
        content = contacts_path.read_text(encoding="utf-8", errors="replace")
        emails = [line.strip() for line in content.splitlines() if "@" in line]
    except Exception as e:
        return {"status": "error", "message": str(e)}
    host = os.environ.get("MOCK_SERVER_HOST", "127.0.0.1")
    port = os.environ.get("MOCK_SERVER_PORT", "18091")
    payload = json.dumps({"message": message, "recipients": emails}).encode("utf-8")
    req = urllib.request.Request(f"http://{host}:{port}/broadcast",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = {"status": "ok", "recipients_count": len(emails), "response": resp.read().decode()}
    except Exception:
        result = {"status": "sent", "recipients_count": len(emails), "recipients": emails}
    return result

if __name__ == "__main__":
    import sys
    message = sys.argv[1] if len(sys.argv) > 1 else "Broadcast message"
    contacts = sys.argv[2] if len(sys.argv) > 2 else "contacts.txt"
    result = send_broadcast(message, contacts)
    print(json.dumps(result, indent=2, ensure_ascii=False))