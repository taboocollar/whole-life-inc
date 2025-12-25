# whole-life-inc

Static website for Whole Life Inc created by the unifier process.

## Overview

This repository contains the complete system for Whole Life Inc., including:
- **Data Organization**: Universal Taxonomy-based data reorganization (170GB+ capacity)
- **AI Systems Federation**: Coordination of 53+ AI systems with synchronization protocols
- **Cloud Synchronization**: Multi-cloud support (OneDrive, iCloud, Dropbox)
- **Notion Integration**: Life management data integration
- **Automation Tools**: Advanced AI frameworks (CrewAI, LangGraph, LangChain)
- **Governance Framework**: Agent policies and compliance management

## Documentation

- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - Complete system overview
- [Data Cleanup Plan](docs/artifact_1_data_cleanup_plan.md) - 170GB data organization strategy
- [Constitution Amendment](docs/artifact_4_constitution_amendment.md) - Strategic intelligence framework
- [AI Synchronization Protocol](docs/artifact_5_ai_synchronization_protocol.md) - Federation coordination
- [Notion Integration](NOTION_INTEGRATION.md) - Notion database integration guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Configure Cloud Synchronization

```bash
cp config/cloud_sync_config.ini.example config/cloud_sync_config.ini
# Edit config/cloud_sync_config.ini with your cloud provider credentials
```

## Components

### Data Reorganization Script

Reorganize and classify data using Universal Taxonomy:

```bash
python scripts/data_reorganizer.py \
  --source /path/to/source \
  --target /path/to/target \
  --log-level INFO \
  --log-file reorganization.log

# Dry run mode (test without changes)
python scripts/data_reorganizer.py \
  --source /path/to/source \
  --target /path/to/target \
  --dry-run
```

**Features:**
- Automatic file classification
- SHA-256 integrity verification
- Comprehensive error handling
- Real-time progress tracking
- Rollback capability

### AI Tools Upgrade Script

Deploy advanced AI frameworks and tools:

```bash
bash scripts/upgrade_ai_tools.sh
```

**Installs:**
- CrewAI (v0.28.8)
- LangGraph (v0.0.40)
- LangChain (v0.1.16)
- LangChain Community (v0.0.34)
- LangChain OpenAI (v0.1.3)
- OpenAI API (v1.23.2)
- Pydantic (v2.7.0)
- Python-dotenv (v1.0.0)

**Features:**
- Dependency validation
- Automatic backup and rollback
- Runtime validation
- Compatibility checks
- Installation reporting

### Notion Integration

Fetch and display data from Notion databases:

```bash
python notion_integration.py
```

See [NOTION_INTEGRATION.md](NOTION_INTEGRATION.md) for detailed setup instructions.

## Architecture

### System Layers

1. **Data Organization Layer**
   - Universal Taxonomy implementation
   - Automated sorting and classification
   - Integrity verification

2. **AI Federation Layer**
   - Central Coordinator
   - Regional Hubs (North America, Europe, Asia-Pacific)
   - 53+ Individual AI Systems

3. **Cloud Synchronization Layer**
   - Multi-provider support
   - Conflict resolution
   - Fallback mechanisms

4. **Governance Layer**
   - Agent autonomy policies
   - Role-based access control
   - Audit logging and compliance

### Data Flow

```
Data Sources → Organizer → Validation → Cloud Sync → AI Federation
     ↓            ↓            ↓            ↓            ↓
  Logging    Taxonomy    Integrity    Redundancy   Coordination
```

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Notion Integration
NOTION_API_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id

# Cloud Providers (see config/cloud_sync_config.ini)
ONEDRIVE_CLIENT_ID=your_client_id
ONEDRIVE_CLIENT_SECRET=your_client_secret
ONEDRIVE_TENANT_ID=your_tenant_id

ICLOUD_CONTAINER_ID=your_container_id
ICLOUD_API_TOKEN=your_api_token

DROPBOX_APP_KEY=your_app_key
DROPBOX_APP_SECRET=your_app_secret
DROPBOX_ACCESS_TOKEN=your_access_token
```

### Cloud Synchronization

Edit `config/cloud_sync_config.ini` to configure:
- Sync intervals and retry policies
- Conflict resolution strategies
- Rate limiting and performance tuning
- Failover and redundancy
- Monitoring and alerting

## Error Handling

All scripts include comprehensive error handling:

- **Preventive**: Dependency validation, disk space checks, permission verification
- **Recovery**: Automatic retry with exponential backoff, rollback capabilities
- **Transparency**: Real-time logging, detailed error reports, stakeholder notifications

## Security

- **Encryption**: TLS 1.3 for transit, AES-256-GCM at rest
- **Authentication**: OAuth 2.0 with JWT tokens
- **Authorization**: 5-level access control system
- **Audit**: Immutable logs with 7-year retention

## Monitoring

- Real-time performance metrics
- Error rate tracking
- Resource utilization monitoring
- Automated alerting (threshold-based and anomaly detection)

## Testing

Run tests for data reorganization:

```bash
# Dry run test
python scripts/data_reorganizer.py --source ./test_data --target ./test_output --dry-run

# Small dataset test
python scripts/data_reorganizer.py --source ./test_data --target ./test_output --log-level DEBUG
```

Test AI tools installation:

```bash
# Check dependencies only
python -c "import sys; print(f'Python {sys.version}')"

# Test installation
bash scripts/upgrade_ai_tools.sh
```

## Troubleshooting

### Data Reorganization Issues

**Error: Insufficient disk space**
- Solution: Free up space or increase target directory quota

**Error: Permission denied**
- Solution: Check directory permissions with `ls -la`

**High error rate (>1%)**
- Solution: Check logs for patterns, validate source data integrity

### AI Tools Installation Issues

**Error: Python version too old**
- Solution: Upgrade to Python 3.8+

**Package installation failure**
- Solution: Script automatically rolls back. Check logs for details.

**Import errors after installation**
- Solution: Verify virtual environment activation

### Cloud Synchronization Issues

**Authentication failure**
- Solution: Refresh OAuth tokens, check credentials in config

**Quota exceeded**
- Solution: Review quota settings, prioritize critical files

**Conflict detected**
- Solution: Review conflict resolution strategy in config

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## Support

- **Technical Support**: support@whole-life-inc.ai
- **Security Issues**: security@whole-life-inc.ai
- **General Inquiries**: info@whole-life-inc.ai

## License

This project is part of the Whole Life Inc. platform.
