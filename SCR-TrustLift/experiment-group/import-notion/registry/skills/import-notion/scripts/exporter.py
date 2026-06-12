#!/usr/bin/env python3
"""
Notion Exporter - Raw JSON Export

Exports all Notion pages shared with the integration to raw JSON format.
Based on notion4ever's export approach with added rate limiting.

Usage:
    python exporter.py [space_name]

Example:
    python exporter.py viran
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, unquote

import httpx
from dotenv import load_dotenv
from notion_client import Client, APIResponseError

# =============================================================================
# Configuration
# =============================================================================

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

# =============================================================================
# Rate-Limited Client
# =============================================================================

class RateLimitedClient:
    """Wraps notion_client with throttling and retry logic."""

    def __init__(self, api_key: str):
        self.client = Client(auth=api_key)
        self.last_request_time = 0
        self.min_interval = 0.35  # 350ms (~2.8 req/sec, under 3/sec limit)

    def _throttle(self):
        """Ensure minimum interval between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

    def request(self, fn, max_retries: int = 3):
        """Execute a request with throttling and retry on rate limit."""
        self._throttle()

        for attempt in range(max_retries):
            try:
                self.last_request_time = time.time()
                return fn()
            except APIResponseError as e:
                if e.status == 429:  # Rate limited
                    wait_time = 1 + attempt
                    logging.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise
        raise Exception("Max retries exceeded")


# =============================================================================
# Block Fetching (ported from notion4ever)
# =============================================================================

def fetch_all_blocks(client: RateLimitedClient, block_id: str) -> list:
    """
    Recursively fetch all blocks and their children.
    Ported from notion4ever's block_parser.
    """
    blocks = []
    start_cursor = None

    # Paginate through all blocks
    while True:
        if start_cursor is None:
            response = client.request(
                lambda: client.client.blocks.children.list(block_id=block_id)
            )
        else:
            cursor = start_cursor  # Capture for lambda
            response = client.request(
                lambda: client.client.blocks.children.list(
                    block_id=block_id, start_cursor=cursor
                )
            )

        blocks.extend(response["results"])
        start_cursor = response.get("next_cursor")
        if not start_cursor:
            break

    # Recursively fetch children for blocks that have them
    for block in blocks:
        if block.get("has_children") and block["type"] not in ["child_page", "child_database"]:
            block["children"] = fetch_all_blocks(client, block["id"])

    return blocks


# =============================================================================
# Page/Database Fetching
# =============================================================================

def fetch_page_content(client: RateLimitedClient, page_id: str) -> dict:
    """Fetch page metadata and all its blocks."""
    logging.debug(f"Fetching page: {page_id}")

    # Get page metadata
    page = client.request(lambda: client.client.pages.retrieve(page_id=page_id))

    # Get all blocks
    page["blocks"] = fetch_all_blocks(client, page_id)

    return page


def fetch_database_content(client: RateLimitedClient, database_id: str) -> dict:
    """Fetch database metadata and all its entries with their content."""
    logging.debug(f"Fetching database: {database_id}")

    # Get database metadata (now contains data_sources array, not properties)
    database = client.request(
        lambda: client.client.databases.retrieve(database_id=database_id)
    )

    # Collect entries from all data sources
    all_entries = []
    data_sources_full = []

    for ds_info in database.get("data_sources", []):
        ds_id = ds_info["id"]
        ds_name = ds_info.get("name", "Unnamed")
        logging.info(f"  Data source: {ds_name}")

        # Get full data source with properties/schema
        data_source = client.request(
            lambda ds_id=ds_id: client.client.data_sources.retrieve(data_source_id=ds_id)
        )
        data_sources_full.append(data_source)

        # Query entries from this data source with pagination
        entries = []
        start_cursor = None

        while True:
            if start_cursor is None:
                response = client.request(
                    lambda ds_id=ds_id: client.client.data_sources.query(data_source_id=ds_id)
                )
            else:
                cursor = start_cursor
                response = client.request(
                    lambda ds_id=ds_id, cursor=cursor: client.client.data_sources.query(
                        data_source_id=ds_id, start_cursor=cursor
                    )
                )

            entries.extend(response["results"])
            start_cursor = response.get("next_cursor")
            if not start_cursor:
                break

        # Fetch full content for each entry
        for i, entry in enumerate(entries):
            logging.info(f"    Entry {i + 1}/{len(entries)}: {get_title(entry)}")
            entry["blocks"] = fetch_all_blocks(client, entry["id"])

        all_entries.extend(entries)

    database["data_sources_full"] = data_sources_full
    database["entries"] = all_entries
    return database


# =============================================================================
# Users Fetching
# =============================================================================

def fetch_all_users(client: RateLimitedClient) -> dict:
    """Fetch all users in the workspace."""
    users = {}
    start_cursor = None

    logging.info("Fetching users...")

    while True:
        if start_cursor is None:
            response = client.request(
                lambda: client.client.users.list()
            )
        else:
            cursor = start_cursor
            response = client.request(
                lambda: client.client.users.list(start_cursor=cursor)
            )

        for user in response["results"]:
            users[user["id"]] = {
                "name": user.get("name", "Unknown"),
                "type": user.get("type"),
                "email": user.get("person", {}).get("email") if user.get("type") == "person" else None,
                "avatar_url": user.get("avatar_url")
            }

        start_cursor = response.get("next_cursor")
        if not start_cursor:
            break

    logging.info(f"  Found {len(users)} users")
    return users


# =============================================================================
# Database Fetching (for path resolution)
# =============================================================================

def fetch_referenced_databases(client: RateLimitedClient, pages: dict) -> dict:
    """
    Fetch database objects referenced by pages with data_source_id parents.
    This enables the converter to resolve database names for directory paths.
    """
    # Collect unique database_ids from pages with data_source_id parent
    database_ids = set()
    for page_id, page in pages.items():
        parent = page.get("parent", {})
        if parent.get("type") == "data_source_id":
            db_id = parent.get("database_id")
            if db_id:
                database_ids.add(db_id)

    if not database_ids:
        return {}

    logging.info(f"Fetching {len(database_ids)} referenced databases...")

    databases = {}
    for db_id in database_ids:
        try:
            database = client.request(
                lambda db_id=db_id: client.client.databases.retrieve(database_id=db_id)
            )
            databases[db_id] = database
            # Extract title for logging
            title = "".join(t.get("plain_text", "") for t in database.get("title", [])) or "Untitled"
            logging.info(f"  Database: {title}")
        except APIResponseError as e:
            if e.status == 404:
                logging.warning(f"  Database {db_id} not found (may not be shared)")
            else:
                logging.warning(f"  Failed to fetch database {db_id}: {e}")

    logging.info(f"  Fetched {len(databases)} databases")
    return databases


# =============================================================================
# Comments Fetching
# =============================================================================

def fetch_comments_for_block(client: RateLimitedClient, block_id: str) -> list:
    """Fetch all comments for a block or page."""
    comments = []
    start_cursor = None

    while True:
        try:
            if start_cursor is None:
                response = client.request(
                    lambda: client.client.comments.list(block_id=block_id)
                )
            else:
                cursor = start_cursor
                response = client.request(
                    lambda: client.client.comments.list(block_id=block_id, start_cursor=cursor)
                )

            comments.extend(response["results"])
            start_cursor = response.get("next_cursor")
            if not start_cursor:
                break
        except APIResponseError as e:
            if e.status == 403:
                # Comments capability not enabled or no access
                break
            raise

    return comments


def fetch_all_comments(client: RateLimitedClient, pages: dict) -> dict:
    """Fetch comments for all pages."""
    all_comments = {}
    page_ids = list(pages.keys())

    logging.info(f"Fetching comments for {len(page_ids)} pages...")

    for i, page_id in enumerate(page_ids):
        comments = fetch_comments_for_block(client, page_id)
        if comments:
            all_comments[page_id] = comments
            logging.info(f"  [{i+1}/{len(page_ids)}] {len(comments)} comments")

    logging.info(f"  Found comments on {len(all_comments)} pages")
    return all_comments


# =============================================================================
# Asset Downloading
# =============================================================================

def get_asset_filename(url: str, block_id: str) -> str:
    """Generate a unique filename for an asset."""
    parsed = urlparse(url)
    path = unquote(parsed.path)

    # Try to get extension from path
    ext = ""
    if "." in path:
        ext = "." + path.rsplit(".", 1)[-1].split("?")[0].lower()
        # Validate extension
        if len(ext) > 5 or not ext[1:].isalnum():
            ext = ""

    # Use short block ID for uniqueness
    short_id = block_id.replace("-", "")[:12]
    return f"{short_id}{ext}" if ext else f"{short_id}.bin"


def download_asset(url: str, output_path: Path, timeout: int = 30) -> bool:
    """Download an asset from URL to local path."""
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as http_client:
            response = http_client.get(url)
            response.raise_for_status()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)
            return True
    except Exception as e:
        logging.warning(f"Failed to download asset: {e}")
        return False


def process_block_assets(block: dict, assets_dir: Path, downloaded: dict) -> None:
    """Download assets from a block and update URLs to local paths."""
    block_type = block.get("type")
    block_id = block.get("id", "unknown")
    block_data = block.get(block_type, {})

    # Handle image and file blocks
    if block_type in ("image", "file", "video", "pdf"):
        file_info = block_data.get("file") or block_data.get("external")
        if file_info:
            url = file_info.get("url", "")
            if url and url.startswith("http") and url not in downloaded:
                filename = get_asset_filename(url, block_id)
                local_path = assets_dir / filename

                if download_asset(url, local_path):
                    downloaded[url] = f"assets/{filename}"
                    logging.info(f"    Asset: {filename}")
                else:
                    downloaded[url] = url  # Keep original on failure

            # Update URL to local path
            if url in downloaded:
                file_info["_local_path"] = downloaded[url]

    # Recurse into children
    for child in block.get("children", []):
        process_block_assets(child, assets_dir, downloaded)


def download_page_assets(page: dict, assets_dir: Path, downloaded: dict) -> int:
    """Download all assets for a page. Returns count of new downloads."""
    initial_count = len(downloaded)
    for block in page.get("blocks", []):
        process_block_assets(block, assets_dir, downloaded)
    return len(downloaded) - initial_count


def process_property_assets(page: dict, assets_dir: Path, downloaded: dict) -> int:
    """Download assets from files properties. Returns count of new downloads."""
    initial_count = len(downloaded)

    for prop_name, prop in page.get("properties", {}).items():
        if prop.get("type") != "files":
            continue

        for file_item in prop.get("files", []):
            file_type = file_item.get("type")
            file_info = file_item.get(file_type, {})
            url = file_info.get("url", "")

            if not url or not url.startswith("http") or url in downloaded:
                continue

            # Generate filename from file name or fallback to hash
            original_name = file_item.get("name", "")
            if original_name:
                # Slugify the filename but keep extension
                name_parts = original_name.rsplit(".", 1)
                base = re.sub(r'[^\w\s-]', '', name_parts[0].lower())
                base = re.sub(r'[-\s]+', '-', base).strip('-')
                ext = f".{name_parts[1].lower()}" if len(name_parts) > 1 else ""
                filename = f"{base}{ext}" if base else get_asset_filename(url, prop_name)
            else:
                filename = get_asset_filename(url, prop_name)

            local_path = assets_dir / filename

            # Handle duplicates by adding suffix
            counter = 1
            while local_path.exists() and counter < 100:
                name_parts = filename.rsplit(".", 1)
                if len(name_parts) > 1:
                    local_path = assets_dir / f"{name_parts[0]}-{counter}.{name_parts[1]}"
                else:
                    local_path = assets_dir / f"{filename}-{counter}"
                counter += 1

            if download_asset(url, local_path):
                downloaded[url] = f"assets/{local_path.name}"
                logging.info(f"    Property asset: {local_path.name}")
            else:
                downloaded[url] = url  # Keep original on failure

            # Store local path in the file info
            file_info["_local_path"] = downloaded[url]

    return len(downloaded) - initial_count


# =============================================================================
# Search & Export
# =============================================================================

def get_title(item: dict) -> str:
    """Extract title from a page or database."""
    # Database title
    if "title" in item and isinstance(item["title"], list):
        return "".join(t.get("plain_text", "") for t in item["title"]) or "Untitled"

    # Page title from properties
    if "properties" in item:
        for prop in item["properties"].values():
            if prop.get("type") == "title" and "title" in prop:
                return "".join(t.get("plain_text", "") for t in prop["title"]) or "Untitled"

    return "Untitled"


def search_all_pages(client: RateLimitedClient, exclude_patterns: list = None) -> list:
    """Search for all pages/databases shared with the integration."""
    results = []
    start_cursor = None
    exclude_patterns = exclude_patterns or []

    logging.info("Searching for shared pages...")

    while True:
        if start_cursor is None:
            response = client.request(
                lambda: client.client.search(page_size=100)
            )
        else:
            cursor = start_cursor
            response = client.request(
                lambda: client.client.search(page_size=100, start_cursor=cursor)
            )

        for item in response["results"]:
            if item["object"] in ["page", "database"]:
                title = get_title(item)

                # Check exclude patterns
                if any(re.search(p, title, re.IGNORECASE) for p in exclude_patterns):
                    logging.info(f"  Skipping: {title}")
                    continue

                results.append(item)

        start_cursor = response.get("next_cursor")
        logging.info(f"  Found {len(results)} items...")

        if not start_cursor:
            break

    return results


def save_export_state(output_file: Path, pages: dict, users: dict, comments: dict,
                      assets: dict, databases: dict, total_items: int, completed: int):
    """Save current export state to JSON file (incremental save)."""
    # Count data sources across all databases
    data_source_count = sum(
        len(p.get("data_sources_full", []))
        for p in pages.values()
        if p.get("object") == "database"
    )

    result = {
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "api_version": "2025-09-03",
        "export_status": "complete" if completed >= total_items else "in_progress",
        "progress": f"{completed}/{total_items}",
        "page_count": len([p for p in pages.values() if p.get("object") == "page"]),
        "database_count": len([p for p in pages.values() if p.get("object") == "database"]),
        "data_source_count": data_source_count,
        "referenced_database_count": len(databases),
        "user_count": len(users),
        "comment_count": sum(len(c) for c in comments.values()),
        "asset_count": len(assets),
        "_users": users,
        "_comments": comments,
        "_assets": assets,  # url -> local_path mapping
        "_databases": databases,  # database_id -> database object (for path resolution)
        "pages": pages
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def export_workspace(client: RateLimitedClient, export_dir: Path, exclude_patterns: list = None) -> dict:
    """Export all shared pages and databases with assets, saving incrementally."""
    output_file = export_dir / "export.json"
    assets_dir = export_dir / "assets"

    # Fetch users first (warn if capability missing)
    try:
        users = fetch_all_users(client)
    except APIResponseError as e:
        if e.status == 403:
            logging.warning("Users API not available (missing capability). Continuing without user data.")
            users = {}
        else:
            raise

    # Search for all shared items
    items = search_all_pages(client, exclude_patterns)
    total_items = len(items)
    logging.info(f"\nExporting {total_items} items...\n")

    pages = {}
    downloaded_assets = {}  # url -> local_path mapping

    for i, item in enumerate(items):
        title = get_title(item)
        item_type = item["object"]
        logging.info(f"[{i + 1}/{total_items}] {item_type}: {title}")

        try:
            if item_type == "database":
                content = fetch_database_content(client, item["id"])
            else:
                content = fetch_page_content(client, item["id"])

            # Download assets for this page (blocks and file properties)
            asset_count = download_page_assets(content, assets_dir, downloaded_assets)
            prop_asset_count = process_property_assets(content, assets_dir, downloaded_assets)
            total_assets = asset_count + prop_asset_count
            if total_assets:
                logging.info(f"  Downloaded {total_assets} assets ({prop_asset_count} from properties)")

            pages[item["id"]] = content

            # Save after each item (incremental)
            save_export_state(output_file, pages, users, {}, downloaded_assets, {}, total_items, i + 1)

        except Exception as e:
            logging.error(f"  Failed to export {title}: {e}")

    # Fetch referenced databases (for pages with data_source_id parent)
    # This enables the converter to resolve database names for directory paths
    referenced_databases = fetch_referenced_databases(client, pages)

    # Fetch comments after all pages are exported (warn if capability missing)
    try:
        comments = fetch_all_comments(client, pages)
    except APIResponseError as e:
        if e.status == 403:
            logging.warning("Comments API not available (missing capability). Continuing without comments.")
            comments = {}
        else:
            raise

    # Final save with comments and referenced databases
    save_export_state(output_file, pages, users, comments, downloaded_assets, referenced_databases, total_items, total_items)

    # Count data sources
    data_source_count = sum(
        len(p.get("data_sources_full", []))
        for p in pages.values()
        if p.get("object") == "database"
    )

    return {
        "page_count": len([p for p in pages.values() if p.get("object") == "page"]),
        "database_count": len([p for p in pages.values() if p.get("object") == "database"]),
        "data_source_count": data_source_count,
        "referenced_database_count": len(referenced_databases),
        "user_count": len(users),
        "comment_count": sum(len(c) for c in comments.values()),
        "asset_count": len(downloaded_assets)
    }


# =============================================================================
# Config & Main
# =============================================================================

def load_config(config_path: Path) -> dict:
    """Load config from JSON file."""
    with open(config_path, "r") as f:
        return json.load(f)


def resolve_path(path_str: str) -> Path:
    """Resolve ~ in paths."""
    return Path(path_str).expanduser().resolve()


def get_timestamp() -> str:
    """Get date for output directory (YYYY-MM-DD format)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def print_usage(config: dict = None):
    """Print usage information and available spaces."""
    print("Notion Exporter (Raw JSON)")
    print("=" * 30)
    print()
    print("Usage: python exporter.py <space_name>")
    print()
    if config:
        spaces = config.get("spaces", {})
        if spaces:
            print("Available spaces:")
            for name in sorted(spaces.keys()):
                print(f"  - {name}")
    print()


def main():
    # Load config early for help display
    config_path = Path.home() / ".claude" / "notion-exporter.config.json"
    config = load_config(config_path) if config_path.exists() else {}

    # Handle --help or no arguments
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_usage(config)
        sys.exit(0 if sys.argv[1:] and sys.argv[1] in ("-h", "--help") else 1)

    space_name = sys.argv[1]

    print("Notion Exporter (Raw JSON)")
    print("=" * 30)
    print()

    # Load environment (override=True forces fresh read from file)
    env_path = Path.home() / ".claude" / ".env"
    load_dotenv(env_path, override=True)

    space_config = config.get("spaces", {}).get(space_name)
    if not space_config:
        logging.error(f"Unknown space: {space_name}")
        logging.error(f"Available: {', '.join(sorted(config.get('spaces', {}).keys()))}")
        sys.exit(1)

    # Get API key for this space
    api_key_env_var = space_config.get("apiKeyEnvVar")
    if not api_key_env_var:
        logging.error(f"Space '{space_name}' missing 'apiKeyEnvVar' in config")
        logging.error("Add apiKeyEnvVar to specify which env var contains the API key")
        sys.exit(1)

    api_key = os.getenv(api_key_env_var)
    if not api_key:
        logging.error(f"Missing {api_key_env_var} in {env_path}")
        logging.error("Get your key from: https://www.notion.so/my-integrations")
        sys.exit(1)

    # Resolve paths
    target_path = resolve_path(space_config["targetPath"])
    raw_export_path = target_path / space_config["rawExportPath"]
    export_dir = raw_export_path / get_timestamp()
    export_dir.mkdir(parents=True, exist_ok=True)

    exclude_patterns = space_config.get("excludePatterns", [])

    print(f"Space: {space_name}")
    print(f"Output: {export_dir}")
    print()

    # Create client and export
    client = RateLimitedClient(api_key)

    try:
        result = export_workspace(client, export_dir, exclude_patterns)

        print()
        print(f"Done! Exported {result['page_count']} pages, {result['database_count']} databases, {result['data_source_count']} data sources")
        print(f"  Referenced databases: {result['referenced_database_count']}")
        print(f"  Users: {result['user_count']}, Comments: {result['comment_count']}, Assets: {result['asset_count']}")
        print(f"Output: {export_dir / 'export.json'}")

    except Exception as e:
        logging.error(f"\nExport failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
