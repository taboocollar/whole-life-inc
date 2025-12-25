#!/bin/bash
# Artifact 3: Upgrade Script for Deploying New AI Tools
# 
# This script deploys advanced automation tools including CrewAI, LangGraph, 
# LangChain, and other AI frameworks with comprehensive error handling,
# rollback capabilities, and dependency validation.

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LOG_FILE="${LOG_FILE:-/tmp/ai_tools_upgrade_$(date +%Y%m%d_%H%M%S).log}"
BACKUP_DIR="${BACKUP_DIR:-/tmp/ai_tools_backup_$(date +%Y%m%d_%H%M%S)}"
PYTHON_CMD="${PYTHON_CMD:-python3}"
PIP_CMD="${PIP_CMD:-pip3}"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Error handler
error_handler() {
    local line_num=$1
    log_error "Script failed at line $line_num"
    log_error "Initiating rollback procedure..."
    rollback_installation
    exit 1
}

trap 'error_handler $LINENO' ERR

# Rollback function
rollback_installation() {
    log_warning "Rolling back installation..."
    
    if [ -d "$BACKUP_DIR" ]; then
        log_info "Restoring from backup: $BACKUP_DIR"
        
        # Restore requirements.txt if backup exists
        if [ -f "$BACKUP_DIR/requirements.txt" ]; then
            cp "$BACKUP_DIR/requirements.txt" requirements.txt
            log_info "Restored requirements.txt"
        fi
        
        # Reinstall previous packages
        if [ -f "$BACKUP_DIR/installed_packages.txt" ]; then
            log_info "Restoring previous package versions..."
            $PIP_CMD install -r "$BACKUP_DIR/installed_packages.txt" --force-reinstall
            log_success "Previous packages restored"
        fi
    else
        log_warning "No backup directory found, cannot rollback"
    fi
}

# Dependency validation
check_dependencies() {
    log_info "Checking system dependencies..."
    
    # Check Python version
    local python_version=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    local major=$(echo $python_version | cut -d. -f1)
    local minor=$(echo $python_version | cut -d. -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
        log_error "Python 3.8 or higher required, found $python_version"
        exit 1
    fi
    log_success "Python version $python_version is compatible"
    
    # Check pip
    if ! command -v $PIP_CMD &> /dev/null; then
        log_error "pip not found, please install pip"
        exit 1
    fi
    log_success "pip is available"
    
    # Check git (optional but recommended)
    if ! command -v git &> /dev/null; then
        log_warning "git not found, some features may be limited"
    else
        log_success "git is available"
    fi
    
    # Check disk space (require at least 2GB free)
    local available_space=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    if [ "$available_space" -lt 2 ]; then
        log_error "Insufficient disk space: ${available_space}GB available, 2GB required"
        exit 1
    fi
    log_success "Sufficient disk space available: ${available_space}GB"
}

# Backup current environment
backup_environment() {
    log_info "Creating backup of current environment..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup requirements.txt if it exists
    if [ -f "requirements.txt" ]; then
        cp requirements.txt "$BACKUP_DIR/requirements.txt"
        log_info "Backed up requirements.txt"
    fi
    
    # Save currently installed packages
    $PIP_CMD freeze > "$BACKUP_DIR/installed_packages.txt"
    log_info "Backed up installed packages list"
    
    log_success "Backup created at: $BACKUP_DIR"
}

# Check if package is already installed
is_package_installed() {
    local package=$1
    $PIP_CMD show "$package" &> /dev/null
}

# Get installed package version
get_package_version() {
    local package=$1
    $PIP_CMD show "$package" 2>/dev/null | grep "Version:" | awk '{print $2}'
}

# Install or upgrade a package
install_package() {
    local package=$1
    local version=${2:-}
    
    local package_spec="$package"
    if [ -n "$version" ]; then
        package_spec="${package}==${version}"
    fi
    
    if is_package_installed "$package"; then
        local current_version=$(get_package_version "$package")
        if [ -n "$version" ] && [ "$current_version" == "$version" ]; then
            log_info "Package $package==$version already installed, skipping"
            return 0
        fi
        log_info "Upgrading $package from $current_version..."
    else
        log_info "Installing $package_spec..."
    fi
    
    if $PIP_CMD install "$package_spec" >> "$LOG_FILE" 2>&1; then
        log_success "Successfully installed/upgraded $package_spec"
        return 0
    else
        log_error "Failed to install $package_spec"
        return 1
    fi
}

# Runtime validation
validate_installation() {
    local package=$1
    
    log_info "Validating $package installation..."
    
    # Try to import the package in Python
    if $PYTHON_CMD -c "import ${package//-/_}" 2>> "$LOG_FILE"; then
        log_success "$package validation successful"
        return 0
    else
        log_error "$package validation failed - import error"
        return 1
    fi
}

# Main installation function
install_ai_tools() {
    log_info "Starting AI tools installation..."
    log_info "Log file: $LOG_FILE"
    
    # Define packages to install
    # Format: "package_name|version|validate_name"
    declare -a packages=(
        "crewai|0.28.8|crewai"
        "langgraph|0.0.40|langgraph"
        "langchain|0.1.16|langchain"
        "langchain-community|0.0.34|langchain_community"
        "langchain-openai|0.1.3|langchain_openai"
        "openai|1.23.2|openai"
        "pydantic|2.7.0|pydantic"
        "python-dotenv|1.0.0|dotenv"
    )
    
    local failed_packages=()
    
    for package_info in "${packages[@]}"; do
        IFS='|' read -r package version validate_name <<< "$package_info"
        
        if ! install_package "$package" "$version"; then
            failed_packages+=("$package")
            continue
        fi
        
        # Runtime validation
        if ! validate_installation "$validate_name"; then
            failed_packages+=("$package")
        fi
    done
    
    # Check if any packages failed
    if [ ${#failed_packages[@]} -gt 0 ]; then
        log_error "Failed to install the following packages:"
        for pkg in "${failed_packages[@]}"; do
            log_error "  - $pkg"
        done
        return 1
    fi
    
    log_success "All AI tools installed successfully"
    return 0
}

# Update requirements.txt
update_requirements() {
    log_info "Updating requirements.txt..."
    
    # Generate new requirements file
    $PIP_CMD freeze > requirements.txt.new
    
    # Backup old requirements
    if [ -f "requirements.txt" ]; then
        mv requirements.txt requirements.txt.old
    fi
    
    mv requirements.txt.new requirements.txt
    log_success "requirements.txt updated"
}

# Compatibility check
check_compatibility() {
    log_info "Running compatibility checks..."
    
    # Check for known conflicts
    local numpy_version=$(get_package_version "numpy" || echo "not_installed")
    if [ "$numpy_version" != "not_installed" ]; then
        local major=$(echo $numpy_version | cut -d. -f1)
        if [ "$major" -ge 2 ]; then
            log_warning "NumPy 2.x detected, some packages may have compatibility issues"
        fi
    fi
    
    # Check VS Code compatibility (if .vscode exists)
    if [ -d ".vscode" ]; then
        log_info "VS Code configuration detected"
        if [ -f ".vscode/settings.json" ]; then
            log_success "VS Code settings found, ensure Python extension is up to date"
        fi
    fi
    
    log_success "Compatibility checks complete"
}

# Generate post-installation report
generate_report() {
    log_info "Generating installation report..."
    
    local report_file="ai_tools_installation_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "=================================="
        echo "AI Tools Installation Report"
        echo "=================================="
        echo "Date: $(date)"
        echo "Python Version: $($PYTHON_CMD --version)"
        echo "Pip Version: $($PIP_CMD --version)"
        echo ""
        echo "Installed Packages:"
        echo "----------------------------------"
        $PIP_CMD list | grep -E "crewai|langgraph|langchain|openai|pydantic"
        echo ""
        echo "Backup Location: $BACKUP_DIR"
        echo "Log File: $LOG_FILE"
        echo ""
        echo "Installation Status: SUCCESS"
    } > "$report_file"
    
    log_success "Installation report saved to: $report_file"
}

# Main execution
main() {
    echo "=================================="
    echo "AI Tools Upgrade Script"
    echo "=================================="
    echo ""
    
    # Step 1: Check dependencies
    check_dependencies
    
    # Step 2: Backup current environment
    backup_environment
    
    # Step 3: Install AI tools
    if ! install_ai_tools; then
        log_error "Installation failed"
        rollback_installation
        exit 1
    fi
    
    # Step 4: Update requirements.txt
    update_requirements
    
    # Step 5: Compatibility checks
    check_compatibility
    
    # Step 6: Generate report
    generate_report
    
    echo ""
    log_success "=================================="
    log_success "AI Tools Installation Complete!"
    log_success "=================================="
    echo ""
    log_info "Next steps:"
    log_info "1. Review the installation report"
    log_info "2. Test your AI workflows"
    log_info "3. Update your documentation"
    echo ""
    log_info "Backup is available at: $BACKUP_DIR"
    log_info "If you encounter issues, run: bash $(basename $0) --rollback"
}

# Parse command line arguments
if [ "${1:-}" == "--rollback" ]; then
    log_warning "Manual rollback requested"
    rollback_installation
    exit 0
elif [ "${1:-}" == "--help" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --rollback    Rollback to previous installation"
    echo "  --help        Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  LOG_FILE      Path to log file (default: /tmp/ai_tools_upgrade_*.log)"
    echo "  BACKUP_DIR    Path to backup directory (default: /tmp/ai_tools_backup_*)"
    echo "  PYTHON_CMD    Python command (default: python3)"
    echo "  PIP_CMD       Pip command (default: pip3)"
    exit 0
fi

# Run main function
main
