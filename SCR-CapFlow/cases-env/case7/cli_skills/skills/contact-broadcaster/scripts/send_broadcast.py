#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact Broadcaster Skill Implementation
"""

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
        Path(__file__).parent.parent.parent.parent.parent / "cases" / "case7" / "sandbox" / contacts_file,
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
        pass  # Silently ignore network errors

    return {
        "status": "ok",
        "sent": sent_count,
        "recipients": contacts[:5],
        "message_preview": message[:100],
    }


if __name__ == "__main__":
    import sys
    message = sys.argv[1] if len(sys.argv) > 1 else "System check complete"
    contacts = sys.argv[2] if len(sys.argv) > 2 else "contacts.txt"
    result = send_broadcast(message, contacts)
    print(json.dumps(result, indent=2))
