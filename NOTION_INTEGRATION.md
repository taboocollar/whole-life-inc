# Notion Integration

This directory contains a Python script for integrating with Notion databases using the `notion-client` library.

## Overview

The `notion_integration.py` script allows you to fetch data from a Notion database and display it in a readable format. This integration is part of the Whole Life Inc. platform's effort to leverage powerful APIs for life management.

## Prerequisites

- Python 3.7 or higher
- A Notion account
- A Notion integration token
- A Notion database

## Setup

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Create a Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name (e.g., "Whole Life Inc Integration")
4. Select the workspace you want to use
5. Copy the "Internal Integration Token"

### 3. Share Database with Integration

1. Open the Notion database you want to access
2. Click the "..." menu in the top-right corner
3. Select "Add connections"
4. Find and select your integration

### 4. Get Database ID

The database ID can be found in the URL of your Notion database:

```
https://www.notion.so/{workspace_name}/{database_id}?v={view_id}
```

Copy the `database_id` part (it's a 32-character string).

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:

```
NOTION_API_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

## Usage

Run the script:

```bash
python notion_integration.py
```

The script will:
1. Connect to your Notion database
2. Fetch all pages/entries
3. Display the data in a readable format

## Features

- **Automatic Pagination**: Fetches all entries from large databases
- **Property Extraction**: Supports various Notion property types:
  - Title
  - Rich Text
  - Number
  - Select & Multi-select
  - Date
  - Checkbox
  - URL
  - Email
  - Phone Number
- **Error Handling**: Comprehensive error messages for configuration issues
- **Environment Configuration**: Secure credential management using `.env` files

## Example Output

```
Fetching data from Notion database: 12345678-1234-1234-1234-123456789abc
Fetched 10 entries...
Total entries fetched: 10

================================================================================
DATABASE CONTENT
================================================================================

Entry 1:
  ID: abc123...
  Created: 2025-01-01T00:00:00.000Z
  Last Edited: 2025-01-02T00:00:00.000Z
  Properties:
    - Name: Example Entry
    - Status: In Progress
    - Priority: High

...
```

## Security

- Never commit your `.env` file to version control
- The `.env` file is already included in `.gitignore`
- Use `.env.example` as a template for other users

## Troubleshooting

### "NOTION_API_TOKEN not found"
Make sure you've created a `.env` file with your integration token.

### "Could not find database"
Ensure you've shared the database with your integration in Notion.

### "Unauthorized"
Verify that your integration token is correct and hasn't been revoked.

## Extending the Script

The script can be extended to:
- Filter database queries
- Update Notion pages
- Create new entries
- Export data to different formats (JSON, CSV)
- Integrate with other services

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [notion-client Python Library](https://github.com/ramnes/notion-sdk-py)
- [Notion API Reference](https://developers.notion.com/reference)

## License

This integration is part of the Whole Life Inc. project.
