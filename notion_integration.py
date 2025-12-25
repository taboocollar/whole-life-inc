#!/usr/bin/env python3
"""
Notion Integration Script for Whole Life Inc.

This script fetches data from a Notion database using the notion-client library.
Configure your NOTION_API_TOKEN and NOTION_DATABASE_ID in a .env file.
"""

import os
import sys
from typing import Dict, List, Any, Tuple
from notion_client import Client
from dotenv import load_dotenv


def load_configuration() -> Tuple[str, str]:
    """
    Load Notion API configuration from environment variables.
    
    Returns:
        tuple: (api_token, database_id)
    
    Raises:
        ValueError: If required environment variables are not set
    """
    load_dotenv()
    
    api_token = os.getenv("NOTION_API_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not api_token:
        raise ValueError(
            "NOTION_API_TOKEN not found. Please set it in your .env file or environment."
        )
    
    if not database_id:
        raise ValueError(
            "NOTION_DATABASE_ID not found. Please set it in your .env file or environment."
        )
    
    return api_token, database_id


def initialize_notion_client(api_token: str) -> Client:
    """
    Initialize and return a Notion client.
    
    Args:
        api_token: Notion integration API token
    
    Returns:
        Client: Initialized Notion client
    """
    return Client(auth=api_token)


def fetch_database_data(client: Client, database_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all pages from a Notion database with error handling and retry logic.
    
    Args:
        client: Initialized Notion client
        database_id: ID of the Notion database to query
    
    Returns:
        List of database pages/entries
        
    Raises:
        Exception: If unable to fetch data after retries
    """
    results = []
    has_more = True
    start_cursor = None
    max_retries = 3
    retry_delay = 2
    
    print(f"Fetching data from Notion database: {database_id}")
    
    while has_more:
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = client.databases.query(
                    database_id=database_id,
                    start_cursor=start_cursor
                )
                
                results.extend(response.get("results", []))
                has_more = response.get("has_more", False)
                start_cursor = response.get("next_cursor")
                
                print(f"Fetched {len(response.get('results', []))} entries...")
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Failed to fetch data after {max_retries} attempts: {e}", file=sys.stderr)
                    raise
                print(f"Retry {retry_count}/{max_retries} after error: {e}", file=sys.stderr)
                import time
                time.sleep(retry_delay * retry_count)  # Exponential backoff
    
    print(f"Total entries fetched: {len(results)}")
    return results


def extract_page_properties(page: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and simplify properties from a Notion page.
    
    Args:
        page: A single page object from Notion API
    
    Returns:
        Dictionary with simplified page properties
    """
    extracted = {
        "id": page.get("id"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
        "properties": {}
    }
    
    properties = page.get("properties", {})
    
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get("type")
        
        if prop_type == "title":
            title_content = prop_data.get("title", [])
            extracted["properties"][prop_name] = (
                title_content[0].get("plain_text", "") if title_content else ""
            )
        elif prop_type == "rich_text":
            rich_text_content = prop_data.get("rich_text", [])
            extracted["properties"][prop_name] = (
                rich_text_content[0].get("plain_text", "") if rich_text_content else ""
            )
        elif prop_type == "number":
            extracted["properties"][prop_name] = prop_data.get("number")
        elif prop_type == "select":
            select_data = prop_data.get("select")
            extracted["properties"][prop_name] = (
                select_data.get("name") if select_data else None
            )
        elif prop_type == "multi_select":
            multi_select_data = prop_data.get("multi_select", [])
            extracted["properties"][prop_name] = [
                item.get("name") for item in multi_select_data
            ]
        elif prop_type == "date":
            date_data = prop_data.get("date")
            extracted["properties"][prop_name] = (
                date_data.get("start") if date_data else None
            )
        elif prop_type == "checkbox":
            extracted["properties"][prop_name] = prop_data.get("checkbox")
        elif prop_type == "url":
            extracted["properties"][prop_name] = prop_data.get("url")
        elif prop_type == "email":
            extracted["properties"][prop_name] = prop_data.get("email")
        elif prop_type == "phone_number":
            extracted["properties"][prop_name] = prop_data.get("phone_number")
        else:
            # For other types, store the raw data
            extracted["properties"][prop_name] = prop_data
    
    return extracted


def display_database_data(pages: List[Dict[str, Any]]) -> None:
    """
    Display the fetched database data in a readable format.
    
    Args:
        pages: List of pages from the Notion database
    """
    print("\n" + "="*80)
    print("DATABASE CONTENT")
    print("="*80 + "\n")
    
    for i, page in enumerate(pages, 1):
        extracted = extract_page_properties(page)
        
        print(f"Entry {i}:")
        print(f"  ID: {extracted['id']}")
        print(f"  Created: {extracted['created_time']}")
        print(f"  Last Edited: {extracted['last_edited_time']}")
        print(f"  Properties:")
        
        for prop_name, prop_value in extracted["properties"].items():
            print(f"    - {prop_name}: {prop_value}")
        
        print()


def main() -> int:
    """
    Main function to execute the Notion data fetching script.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        # Load configuration
        api_token, database_id = load_configuration()
        
        # Initialize Notion client
        notion = initialize_notion_client(api_token)
        
        # Fetch database data
        pages = fetch_database_data(notion, database_id)
        
        if not pages:
            print("\nNo entries found in the database.")
            return 0
        
        # Display the data
        display_database_data(pages)
        
        print(f"\nSuccessfully fetched and displayed {len(pages)} entries.")
        return 0
        
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        print("\nPlease ensure you have a .env file with the required variables:", file=sys.stderr)
        print("  - NOTION_API_TOKEN", file=sys.stderr)
        print("  - NOTION_DATABASE_ID", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
