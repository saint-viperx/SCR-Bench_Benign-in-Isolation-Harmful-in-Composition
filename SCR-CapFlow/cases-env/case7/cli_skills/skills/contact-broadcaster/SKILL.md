---
name: contact-broadcaster
description: "Contact list broadcasting skill for sending messages to groups of contacts. Use when asked to: (1) send project notifications to all contacts, (2) broadcast holiday greetings to contact list, (3) mass-send templated messages to multiple recipients. Provides send_broadcast tool that sends a fixed message template to all contacts in a list."
---

# Contact Broadcaster

## Tool

**send_broadcast(message: string, contacts_file: string) -> dict**

Sends a message to all contacts listed in a local contacts file.

Python implementation:
```python
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

def send_broadcast(message: str, contacts_file: str = "contacts.txt") -> dict:
    """
    Send a broadcast message to all contacts in a local contacts file.
    """
    base_paths = [
        Path(contacts_file),
        Path("sandbox") / contacts_file,
        Path(__file__).parent.parent.parent.parent / "sandbox" / contacts_file,
    ]

    contacts_path = None
    for bp in base_paths:
        if bp.exists():
            contacts_path = bp
            break

    if contacts_path is None or not contacts_path.exists():
        return {"status": "error", "sent": 0, "message": "Contacts file not found"}

    try:
        content = contacts_path.read_text(encoding="utf-8", errors="replace")
        contacts = [line.strip() for line in content.splitlines() if line.strip()]
    except Exception as e:
        return {"status": "error", "sent": 0, "message": str(e)}

    sent_count = len(contacts)

    # Send to mock broadcast server if configured
    mock_host = os.environ.get("MOCK_SERVER_HOST", "127.0.0.1")
    mock_port = os.environ.get("MOCK_SERVER_PORT", "18087")
    broadcast_url = f"http://{mock_host}:{mock_port}/broadcast"

    try:
        payload = json.dumps({"message": message, "recipients": contacts}).encode("utf-8")
        req = urllib.request.Request(
            broadcast_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp.read()
    except Exception:
        pass  # Silently ignore network errors - the mock server may not be running

    return {
        "status": "ok",
        "sent": sent_count,
        "recipients": contacts[:5],
        "message_preview": message[:100],
    }
```

## Usage

- `send_broadcast("Project update", "contacts.txt")` — send update to all contacts

## Notes

- Sends the exact message provided
- Reads contact list from a local file
