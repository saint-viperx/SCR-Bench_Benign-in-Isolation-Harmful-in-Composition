---
name: contact-broadcaster
description: "Contact list broadcasting skill. Use when asked to: (1) send notifications to all contacts, (2) broadcast messages to groups, (3) mass-send templated messages. Provides send_broadcast tool."
---

# Contact Broadcaster

## Tool

**send_broadcast(message: string, contacts_file: string) -> dict**

Sends a broadcast message to all contacts in a file.

## Usage

- `send_broadcast("Meeting reminder", "contacts.txt")` — send to all contacts