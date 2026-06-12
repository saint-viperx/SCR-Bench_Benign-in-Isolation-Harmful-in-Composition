#!/usr/bin/env python3
"""
Notion Converter - JSON to Markdown

Converts notion-exporter JSON output to structured Markdown files.

Usage:
    python converter.py <space_name> [--input <json_path>]

Example:
    python converter.py viran
    python converter.py viran --input /path/to/notion_content.json
"""

import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)


# =============================================================================
# Rich Text Conversion
# =============================================================================

def convert_rich_text(rich_text: list, users: dict = None, page_index: dict = None,
                      source_path: str = None) -> str:
    """Convert Notion rich text array to Markdown string.

    Args:
        rich_text: Notion rich text array
        users: Dict of user_id -> user info for @mentions
        page_index: Dict of page_id -> path for link resolution
        source_path: Path of source file for relative link calculation
    """
    if not rich_text:
        return ""

    result = []
    for item in rich_text:
        text = item.get("plain_text", "")
        item_type = item.get("type", "text")
        annotations = item.get("annotations", {})
        href = item.get("href")

        # Handle mentions
        if item_type == "mention":
            mention = item.get("mention", {})
            mention_type = mention.get("type")

            if mention_type == "user" and users:
                user_id = mention.get("user", {}).get("id")
                user = users.get(user_id, {})
                text = f"@{user.get('name', text)}"
            elif mention_type == "page" and page_index:
                page_id = mention.get("page", {}).get("id")
                if page_id in page_index:
                    local_path = page_index[page_id]
                    # Calculate relative path if source_path provided
                    if source_path:
                        source_dir = os.path.dirname(source_path)
                        if source_dir:
                            local_path = os.path.relpath(local_path, source_dir)
                    text = f"[{text}]({local_path})"
            elif mention_type == "date":
                # Keep plain_text for dates
                pass

        # Apply annotations (order matters for nesting)
        if annotations.get("code"):
            text = f"`{text}`"
        if annotations.get("bold"):
            text = f"**{text}**"
        if annotations.get("italic"):
            text = f"*{text}*"
        if annotations.get("strikethrough"):
            text = f"~~{text}~~"

        # Handle links with resolution
        if href and not (item_type == "mention" and "[" in text):
            if page_index:
                resolved_href, is_external = resolve_notion_link(href, page_index, source_path)
                if is_external:
                    # Mark external Notion links with arrow indicator
                    text = f"[{text} ↗]({resolved_href})"
                else:
                    text = f"[{text}]({resolved_href})"
            else:
                text = f"[{text}]({href})"

        result.append(text)

    return "".join(result)


def resolve_notion_link(href: str, page_index: dict, source_path: str = None) -> tuple:
    """Resolve a Notion URL to local path if possible.

    Args:
        href: The URL to resolve
        page_index: Dict mapping page IDs to their output paths
        source_path: The path of the source file (for relative path calculation)

    Returns:
        Tuple of (resolved_href, is_external) where is_external indicates
        the link points to a Notion page not in the export.
    """
    if not href or not page_index:
        return href, False

    # Check for Notion page URLs
    # Format: https://www.notion.so/Page-Title-abc123def456
    # Or: https://www.notion.so/workspace/abc123def456
    notion_patterns = [
        r'notion\.so/[^/]+/([a-f0-9]{32})',
        r'notion\.so/([a-f0-9]{32})',
        r'notion\.so/[^/]+-([a-f0-9]{32})',
    ]

    for pattern in notion_patterns:
        match = re.search(pattern, href)
        if match:
            # Convert to UUID format
            raw_id = match.group(1)
            page_id = f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"

            if page_id in page_index:
                target_path = page_index[page_id]

                # Calculate relative path if source_path provided
                if source_path:
                    source_dir = os.path.dirname(source_path)
                    if source_dir:
                        target_path = os.path.relpath(target_path, source_dir)

                return target_path, False
            else:
                # Notion link to page not in export - mark as external
                return href, True

    return href, False


# =============================================================================
# Block Conversion
# =============================================================================

def convert_block(block: dict, users: dict = None, page_index: dict = None,
                  depth: int = 0, list_counter: dict = None,
                  block_comments: dict = None, assets_map: dict = None,
                  source_path: str = None) -> str:
    """Convert a single Notion block to Markdown.

    Args:
        block: Notion block object
        users: Dict of user_id -> user info
        page_index: Dict of page_id -> path for link resolution
        depth: Current nesting depth for indentation
        list_counter: Counter for numbered lists
        block_comments: Dict of block_id -> comments
        assets_map: Dict of url -> local asset path
        source_path: Path of source file for relative link calculation
    """
    block_type = block.get("type", "unsupported")
    block_data = block.get(block_type, {})
    block_id = block.get("id", "")
    indent = "  " * depth

    # Track numbered list counters
    if list_counter is None:
        list_counter = {}

    def rt(rich_text):
        return convert_rich_text(rich_text, users, page_index, source_path)

    def get_asset_path(file_info):
        """Get local asset path if available."""
        if assets_map and file_info:
            url = file_info.get("url", "")
            local_path = file_info.get("_local_path") or assets_map.get(url)
            if local_path:
                return local_path
        return file_info.get("url", "") if file_info else ""

    # Block type handlers
    if block_type == "paragraph":
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}{text}" if text else ""

    elif block_type in ("heading_1", "heading_2", "heading_3"):
        level = int(block_type[-1])
        prefix = "#" * level
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}{prefix} {text}"

    elif block_type == "bulleted_list_item":
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}- {text}"

    elif block_type == "numbered_list_item":
        # Track list numbering per depth level
        key = f"numbered_{depth}"
        list_counter[key] = list_counter.get(key, 0) + 1
        num = list_counter[key]
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}{num}. {text}"

    elif block_type == "to_do":
        checked = "x" if block_data.get("checked") else " "
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}- [{checked}] {text}"

    elif block_type == "toggle":
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}<details>\n{indent}<summary>{text}</summary>\n"

    elif block_type == "code":
        language = block_data.get("language", "")
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}```{language}\n{text}\n{indent}```"

    elif block_type == "quote":
        text = rt(block_data.get("rich_text", []))
        # Handle multiline quotes
        lines = text.split("\n")
        result = "\n".join(f"{indent}> {line}" for line in lines)

    elif block_type == "callout":
        icon = block_data.get("icon", {})
        emoji = icon.get("emoji", "") if icon.get("type") == "emoji" else ""
        text = rt(block_data.get("rich_text", []))
        result = f"{indent}> {emoji} {text}"

    elif block_type == "divider":
        result = f"{indent}---"

    elif block_type == "image":
        file_info = block_data.get("file", {}) or block_data.get("external", {})
        path = get_asset_path(file_info)
        caption = rt(block_data.get("caption", []))
        result = f"{indent}![{caption}]({path})"

    elif block_type == "file":
        file_info = block_data.get("file", {}) or block_data.get("external", {})
        path = get_asset_path(file_info)
        caption = rt(block_data.get("caption", [])) or "Download"
        result = f"{indent}[{caption}]({path})"

    elif block_type == "video":
        file_info = block_data.get("file", {}) or block_data.get("external", {})
        path = get_asset_path(file_info)
        caption = rt(block_data.get("caption", [])) or "Video"
        result = f"{indent}[{caption}]({path})"

    elif block_type == "pdf":
        file_info = block_data.get("file", {}) or block_data.get("external", {})
        path = get_asset_path(file_info)
        caption = rt(block_data.get("caption", [])) or "PDF"
        result = f"{indent}[{caption}]({path})"

    elif block_type == "bookmark":
        url = block_data.get("url", "")
        caption = rt(block_data.get("caption", [])) or url
        result = f"{indent}[{caption}]({url})"

    elif block_type == "equation":
        expression = block_data.get("expression", "")
        result = f"{indent}$$\n{expression}\n$$"

    elif block_type == "table":
        # Tables are handled specially with table_row children
        result = ""  # Table content comes from children

    elif block_type == "table_row":
        cells = block_data.get("cells", [])
        cell_texts = [rt(cell) for cell in cells]
        result = f"{indent}| " + " | ".join(cell_texts) + " |"

    elif block_type == "child_page":
        title = block_data.get("title", "Untitled")
        page_id = block.get("id")
        if page_index and page_id in page_index:
            result = f"{indent}[{title}]({page_index[page_id]})"
        else:
            result = f"{indent}[{title}](notion://{page_id})"

    elif block_type == "child_database":
        title = block_data.get("title", "Untitled Database")
        result = f"{indent}**Database:** {title}"

    elif block_type == "column_list":
        # Column list: process each column's content and join with separator
        # Children (columns) are processed in the child handling section below
        result = ""

    elif block_type == "column":
        # Individual column: just a container, content comes from children
        result = ""

    else:
        # Unsupported block type
        result = f"{indent}<!-- Unsupported block type: {block_type} -->"

    # Add inline comments for this block
    if block_comments and block_id in block_comments:
        comments = block_comments[block_id]
        for comment in comments:
            comment_md = render_inline_comment(comment, users)
            result += f"\n{indent}{comment_md}"

    # Handle children (nested blocks)
    children = block.get("children", [])
    if children:
        # Reset numbered list counter for nested lists
        child_counter = {}
        child_results = []

        # Column list: process columns at same depth, join with HR separator
        if block_type == "column_list":
            column_contents = []
            for column in children:
                if column.get("type") == "column":
                    column_children = column.get("children", [])
                    col_child_results = []
                    col_counter = {}
                    for col_child in column_children:
                        # Process column content at current depth (no extra indent)
                        col_child_md = convert_block(col_child, users, page_index, depth,
                                                     col_counter, block_comments, assets_map,
                                                     source_path)
                        if col_child_md:
                            col_child_results.append(col_child_md)
                    if col_child_results:
                        column_contents.append("\n\n".join(col_child_results))
            if column_contents:
                # Join columns with horizontal rule separator
                result = f"\n\n{indent}---\n\n".join(column_contents)
        else:
            for child in children:
                child_md = convert_block(child, users, page_index, depth + 1, child_counter,
                                         block_comments, assets_map, source_path)
                if child_md:
                    child_results.append(child_md)

            if child_results:
                if block_type == "toggle":
                    result += "\n".join(child_results) + f"\n{indent}</details>"
                elif block_type == "table":
                    # Add table header separator after first row
                    if child_results:
                        first_row = child_results[0]
                        col_count = first_row.count("|") - 1
                        separator = f"{indent}|" + " --- |" * col_count
                        result = first_row + "\n" + separator
                        if len(child_results) > 1:
                            result += "\n" + "\n".join(child_results[1:])
                else:
                    result += "\n" + "\n".join(child_results)

    return result


def convert_blocks(blocks: list, users: dict = None, page_index: dict = None,
                   block_comments: dict = None, assets_map: dict = None,
                   source_path: str = None) -> str:
    """Convert a list of blocks to Markdown.

    Args:
        blocks: List of Notion block objects
        users: Dict of user_id -> user info
        page_index: Dict of page_id -> path for link resolution
        block_comments: Dict of block_id -> comments
        assets_map: Dict of url -> local asset path
        source_path: Path of source file for relative link calculation
    """
    results = []
    list_counter = {}
    prev_type = None

    for block in blocks:
        block_type = block.get("type")

        # Reset numbered list counter when list type changes
        if block_type != "numbered_list_item" and prev_type == "numbered_list_item":
            list_counter = {}

        md = convert_block(block, users, page_index, 0, list_counter, block_comments,
                          assets_map, source_path)
        if md:
            results.append(md)

        prev_type = block_type

    return "\n\n".join(results)


# =============================================================================
# Comments
# =============================================================================

def render_inline_comment(comment: dict, users: dict = None) -> str:
    """Render a single comment as inline Markdown."""
    author_id = comment.get("created_by", {}).get("id")
    author = users.get(author_id, {}).get("name", "Unknown") if users else "Unknown"
    created = format_timestamp(comment.get("created_time", ""))
    text = convert_rich_text(comment.get("rich_text", []), users)

    return f"> **{author}** ({created}): {text}"


def build_comment_map(comments: dict) -> dict:
    """Build mapping of block_id -> [comments] for inline rendering."""
    block_comments = {}  # block_id -> [comment objects]
    page_comments = {}   # page_id -> [comments without block parent]

    for page_id, page_comment_list in comments.items():
        for comment in page_comment_list:
            parent = comment.get("parent", {})
            parent_type = parent.get("type")

            if parent_type == "block_id":
                block_id = parent.get("block_id")
                if block_id not in block_comments:
                    block_comments[block_id] = []
                block_comments[block_id].append(comment)
            else:
                # Page-level comment (no specific block)
                if page_id not in page_comments:
                    page_comments[page_id] = []
                page_comments[page_id].append(comment)

    return {"blocks": block_comments, "pages": page_comments}


# =============================================================================
# Utilities
# =============================================================================

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    # Remove special characters except hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace whitespace with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug or "untitled"


def get_title(item: dict) -> str:
    """Extract title from a page or database.

    Falls back to other properties when the title property is empty:
    1. First try the type:title property (standard behavior)
    2. If empty, try properties named 'Name' or 'Entity' (common fallbacks)
    3. Then try first non-empty rich_text property
    4. Finally fall back to 'Untitled'
    """
    # Database title (rich text array at top level)
    if "title" in item and isinstance(item["title"], list):
        title = "".join(t.get("plain_text", "") for t in item["title"])
        if title.strip():
            return title

    # Page title from properties
    if "properties" in item:
        properties = item["properties"]

        # First: Try type:title property
        for prop in properties.values():
            if prop.get("type") == "title" and "title" in prop:
                title = "".join(t.get("plain_text", "") for t in prop["title"])
                if title.strip():
                    return title

        # Second: Try common fallback property names (Name, Entity)
        for fallback_name in ["Name", "Entity", "name", "entity"]:
            if fallback_name in properties:
                prop = properties[fallback_name]
                if prop.get("type") == "rich_text":
                    title = "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
                    if title.strip():
                        return title

        # Third: Try first non-empty rich_text property
        for prop_name, prop in properties.items():
            if prop.get("type") == "rich_text":
                title = "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
                if title.strip():
                    return title

    return "Untitled"


def format_timestamp(iso_str: str) -> str:
    """Format ISO timestamp for display."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso_str


# =============================================================================
# Page Processing
# =============================================================================

def build_page_hierarchy(pages: dict) -> dict:
    """Build parent->children mapping for nested directory structure."""
    children = {}  # parent_id -> [child_ids]
    roots = []     # pages with no parent page

    for page_id, page in pages.items():
        parent = page.get("parent", {})
        parent_type = parent.get("type")

        if parent_type == "page_id":
            parent_id = parent.get("page_id")
            if parent_id not in children:
                children[parent_id] = []
            children[parent_id].append(page_id)
        elif parent_type in ("workspace", "block_id"):
            roots.append(page_id)
        # data_source_id (database entries) handled separately

    return {"children": children, "roots": roots}


def get_page_path(page_id: str, pages: dict, hierarchy: dict,
                  databases: dict = None, cache: dict = None) -> str:
    """Recursively build nested path for a page following Notion hierarchy.

    Args:
        page_id: The page ID to get path for
        pages: Dict of page_id -> page object
        hierarchy: Page hierarchy from build_page_hierarchy()
        databases: Dict of database_id -> database object (from _databases)
        cache: Path cache for performance
    """
    if cache is None:
        cache = {}
    if databases is None:
        databases = {}
    if page_id in cache:
        return cache[page_id]

    page = pages.get(page_id)
    if not page:
        return f"unknown/{page_id}.md"

    title = get_title(page)
    slug = slugify(title)
    parent = page.get("parent", {})
    parent_type = parent.get("type")

    if parent_type == "page_id":
        # Nested under a page - recursively get parent path
        parent_id = parent.get("page_id")
        parent_path = get_page_path(parent_id, pages, hierarchy, databases, cache)
        parent_dir = "/".join(parent_path.split("/")[:-1])
        path = f"{parent_dir}/{slug}/{page_id}.md"

    elif parent_type == "data_source_id":
        # Database entry - find the database's parent and nest there
        db_id = parent.get("database_id")

        # Get database info to find its parent
        db_info = databases.get(db_id) or pages.get(db_id)
        if db_info:
            db_parent = db_info.get("parent", {})
            db_parent_type = db_parent.get("type")
            db_title = get_title(db_info)
            db_slug = slugify(db_title)

            if db_parent_type == "page_id":
                # Database is under a page - nest entry there
                db_parent_id = db_parent.get("page_id")
                db_parent_path = get_page_path(db_parent_id, pages, hierarchy, databases, cache)
                db_parent_dir = "/".join(db_parent_path.split("/")[:-1])
                path = f"{db_parent_dir}/{db_slug}/{slug}/{page_id}.md"
            else:
                # Database is at root level
                path = f"{db_slug}/{slug}/{page_id}.md"
        else:
            # Fallback: database not found
            path = f"unknown/{slug}/{page_id}.md"

    else:
        # Root-level page (workspace or block_id parent)
        path = f"{slug}/{page_id}.md"

    cache[page_id] = path
    return path


def build_page_index(data: dict) -> dict:
    """Build index mapping page IDs to their output paths with nested hierarchy."""
    pages = data.get("pages", {})
    databases = data.get("_databases", {})  # Referenced databases for path resolution
    hierarchy = build_page_hierarchy(pages)
    cache = {}

    index = {}
    for page_id in pages:
        index[page_id] = get_page_path(page_id, pages, hierarchy, databases, cache)

    return index


def extract_property_value(prop: dict) -> str:
    """Extract a simple value from a Notion property."""
    prop_type = prop.get("type")

    if prop_type == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    elif prop_type == "number":
        val = prop.get("number")
        return str(val) if val is not None else ""
    elif prop_type == "select":
        select = prop.get("select")
        return select.get("name", "") if select else ""
    elif prop_type == "multi_select":
        items = prop.get("multi_select", [])
        return ", ".join(item.get("name", "") for item in items)
    elif prop_type == "date":
        date = prop.get("date")
        if date:
            return date.get("start", "")
        return ""
    elif prop_type == "checkbox":
        return "true" if prop.get("checkbox") else "false"
    elif prop_type == "url":
        return prop.get("url", "") or ""
    elif prop_type == "email":
        return prop.get("email", "") or ""
    elif prop_type == "phone_number":
        return prop.get("phone_number", "") or ""
    elif prop_type == "status":
        status = prop.get("status")
        return status.get("name", "") if status else ""
    elif prop_type == "files":
        files = prop.get("files", [])
        links = []
        for file_item in files:
            name = file_item.get("name", "File")
            file_type = file_item.get("type")
            file_info = file_item.get(file_type, {})
            # Use local path if available, otherwise original URL
            url = file_info.get("_local_path") or file_info.get("url", "")
            # Convert assets/ to _assets/ for output directory
            if url and url.startswith("assets/"):
                url = "_" + url
            if url:
                links.append(f"[{name}]({url})")
        return ", ".join(links)

    return ""


def generate_frontmatter(page: dict, users: dict = None) -> str:
    """Generate YAML frontmatter for a page."""
    lines = ["---"]

    lines.append(f"notion_id: {page.get('id', '')}")

    # Add Notion URL
    notion_url = page.get("url", "")
    if notion_url:
        lines.append(f"notion_url: {notion_url}")

    title = get_title(page)
    # Escape quotes in title
    title_escaped = title.replace('"', '\\"')
    lines.append(f'title: "{title_escaped}"')
    lines.append(f"created: {format_timestamp(page.get('created_time', ''))}")
    lines.append(f"last_edited: {format_timestamp(page.get('last_edited_time', ''))}")

    # Add created_by if available
    created_by = page.get("created_by", {})
    if created_by and users:
        user = users.get(created_by.get("id"), {})
        if user.get("name"):
            name_escaped = user['name'].replace('"', '\\"')
            lines.append(f'author: "{name_escaped}"')

    # Add properties for database entries (excluding title)
    properties = page.get("properties", {})
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get("type")
        if prop_type == "title":
            continue  # Already handled

        value = extract_property_value(prop_data)
        if value:
            # Sanitize for YAML
            safe_name = prop_name.lower().replace(" ", "_").replace("-", "_")
            safe_name = re.sub(r'[^\w]', '', safe_name)
            if isinstance(value, str) and ("\n" in value or ":" in value or '"' in value):
                value = value.replace('"', '\\"')
                value = f'"{value}"'
            lines.append(f"{safe_name}: {value}")

    lines.append("---")
    return "\n".join(lines)


def convert_page(page: dict, users: dict = None, page_index: dict = None,
                 comments: dict = None, assets_map: dict = None,
                 source_path: str = None) -> str:
    """Convert a single page to Markdown with inline comments.

    Args:
        page: Notion page object
        users: Dict of user_id -> user info
        page_index: Dict of page_id -> path for link resolution
        comments: Dict of page_id -> comments
        assets_map: Dict of url -> local asset path
        source_path: Path of output file for relative link calculation
    """
    parts = []

    # Build comment map for this page
    comment_map = build_comment_map(comments) if comments else {"blocks": {}, "pages": {}}
    block_comments = comment_map["blocks"]
    page_level_comments = comment_map["pages"].get(page.get("id"), [])

    # Frontmatter
    parts.append(generate_frontmatter(page, users))
    parts.append("")

    # Title
    title = get_title(page)
    parts.append(f"# {title}")
    parts.append("")

    # Content with inline comments
    blocks = page.get("blocks", [])
    if blocks:
        content = convert_blocks(blocks, users, page_index, block_comments, assets_map,
                                source_path)
        parts.append(content)

    # Page-level comments (not attached to specific blocks) go at bottom
    if page_level_comments:
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append("## Page Comments")
        parts.append("")
        for comment in page_level_comments:
            parts.append(render_inline_comment(comment, users))

    return "\n".join(parts)


# =============================================================================
# Main Conversion
# =============================================================================

def load_config(config_path: Path) -> dict:
    """Load config from JSON file."""
    with open(config_path, "r") as f:
        return json.load(f)


def resolve_path(path_str: str) -> Path:
    """Resolve ~ in paths."""
    return Path(path_str).expanduser().resolve()


def find_latest_export(raw_export_path: Path) -> Path:
    """Find the most recent export directory."""
    exports = sorted(raw_export_path.glob("*"), reverse=True)
    for export_dir in exports:
        # Try new name first, fall back to old
        for filename in ["export.json", "notion_content.json"]:
            json_file = export_dir / filename
            if json_file.exists():
                return json_file
    raise FileNotFoundError(f"No exports found in {raw_export_path}")


def copy_assets(source_assets_dir: Path, output_assets_dir: Path) -> int:
    """Copy assets from export to output _assets directory."""
    if not source_assets_dir.exists():
        return 0

    count = 0
    output_assets_dir.mkdir(parents=True, exist_ok=True)

    for asset_file in source_assets_dir.iterdir():
        if asset_file.is_file():
            dest = output_assets_dir / asset_file.name
            # Handle duplicates - skip if already exists
            if dest.exists():
                continue
            shutil.copy2(asset_file, dest)
            count += 1

    return count


def convert_workspace(data: dict, output_dir: Path, source_assets_dir: Path = None) -> dict:
    """Convert all pages to Markdown files."""
    users = data.get("_users", {})
    comments = data.get("_comments", {})
    assets_map = data.get("_assets", {})
    pages = data.get("pages", {})

    # Build page index for link resolution
    page_index = build_page_index(data)

    # Save index file
    index_file = output_dir / "_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(page_index, f, indent=2)
    logging.info(f"Saved index: {index_file}")

    # Save users file
    users_file = output_dir / "_users.json"
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    logging.info(f"Saved users: {users_file}")

    # Copy assets to _assets location (not assets/)
    output_assets_dir = output_dir / "_assets"
    asset_count = 0
    if source_assets_dir:
        asset_count = copy_assets(source_assets_dir, output_assets_dir)
        if asset_count:
            logging.info(f"Copied {asset_count} assets to {output_assets_dir}")

    # Convert each page
    stats = {"pages": 0, "databases": 0, "entries": 0, "errors": 0, "assets": asset_count}

    for page_id, page in pages.items():
        try:
            obj_type = page.get("object")
            title = get_title(page)

            # Get output path from index
            rel_path = page_index.get(page_id)
            if not rel_path:
                continue

            output_file = output_dir / rel_path
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert and write (pass rel_path for relative link calculation)
            markdown = convert_page(page, users, page_index, comments, assets_map, rel_path)
            output_file.write_text(markdown, encoding="utf-8")

            # Update stats
            if obj_type == "database":
                stats["databases"] += 1
                logging.info(f"Database: {title}")

                # Also write schema for databases
                schema_file = output_file.parent / "_schema.json"
                schema = {
                    "id": page_id,
                    "title": title,
                    "data_sources": page.get("data_sources_full", [])
                }
                with open(schema_file, "w", encoding="utf-8") as f:
                    json.dump(schema, f, indent=2)
            else:
                parent = page.get("parent", {})
                if parent.get("type") == "data_source_id":
                    stats["entries"] += 1
                else:
                    stats["pages"] += 1

        except Exception as e:
            logging.error(f"Failed to convert {page_id}: {e}")
            stats["errors"] += 1

    return stats


def main():
    config_path = Path.home() / ".claude" / "notion-exporter.config.json"
    config = load_config(config_path) if config_path.exists() else {}

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python converter.py <space_name> [--input <json_path>]")
        print()
        if config.get("spaces"):
            print("Available spaces:")
            for name in sorted(config["spaces"].keys()):
                print(f"  - {name}")
        sys.exit(1)

    space_name = sys.argv[1]

    # Check for explicit input path
    input_path = None
    if "--input" in sys.argv:
        idx = sys.argv.index("--input")
        if idx + 1 < len(sys.argv):
            input_path = Path(sys.argv[idx + 1])

    space_config = config.get("spaces", {}).get(space_name)
    if not space_config:
        logging.error(f"Unknown space: {space_name}")
        sys.exit(1)

    target_path = resolve_path(space_config["targetPath"])

    # Find input JSON
    if input_path:
        json_file = input_path
        source_assets_dir = input_path.parent / "assets"
    else:
        raw_export_path = target_path / space_config["rawExportPath"]
        json_file = find_latest_export(raw_export_path)
        source_assets_dir = json_file.parent / "assets"

    logging.info(f"Input: {json_file}")

    # Load export data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    logging.info(f"Loaded {data.get('page_count', 0)} pages, {data.get('database_count', 0)} databases")
    logging.info(f"  Users: {data.get('user_count', 0)}, Comments: {data.get('comment_count', 0)}, Assets: {data.get('asset_count', 0)}")

    # Output directory
    output_dir = target_path / "data" / "notion"
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Output: {output_dir}")

    # Convert
    stats = convert_workspace(data, output_dir, source_assets_dir)

    print()
    print(f"Done! Converted {stats['pages']} pages, {stats['databases']} databases, {stats['entries']} entries")
    print(f"  Assets: {stats['assets']}")
    if stats["errors"]:
        print(f"Errors: {stats['errors']}")


if __name__ == "__main__":
    main()
