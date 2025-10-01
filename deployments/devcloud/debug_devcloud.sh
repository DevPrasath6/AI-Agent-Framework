#!/bin/bash
# Intel DevCloud Debug and Health Check Script
# Save as: debug_devcloud.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging functions
log() { echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"; }
warn() { echo -e "${YELLOW}[WARNING] $1${NC}"; }
error() { echo -e "${RED}[ERROR] $1${NC}"; }
info() { echo -e "${BLUE}[INFO] $1${NC}"; }
debug() { echo -e "${CYAN}[DEBUG] $1${NC}"; }
section() { echo -e "${PURPLE}$1${NC}"; }

# Configuration
FRAMEWORK_DIR="."
PYTHON_ENV="framework_env"
LOG_FILE="devcloud_debug.log"

# Start logging
exec > >(tee -a "$LOG_FILE")
exec 2>&1

echo "🔍 Intel DevCloud Debug & Health Check"
echo "======================================"
echo "Timestamp: $(date)"
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo ""

# System Information
check_system_info() {
    section "🖥️  System Information"
    echo "───────────────────────"

    info "OS Information:"
    cat /etc/os-release 2>/dev/null || echo "OS info not available"
    echo ""

    info "CPU Information:"
    lscpu | grep -E "(Architecture|CPU\(s\)|Model name|CPU MHz)" 2>/dev/null || echo "CPU info not available"
    echo ""

    info "Memory Information:"
    free -h
    echo ""

    info "Disk Usage:"
    df -h / 2>/dev/null
    echo ""

    info "Current Directory:"
    pwd
    ls -la | head -10
    echo ""
}

# DevCloud Environment Check
check_devcloud_env() {
    section "☁️  DevCloud Environment"
    echo "────────────────────────"

    if [[ "$HOSTNAME" == *"devcloud"* ]] || [[ "$USER" == u* ]]; then
        log "✅ Running on Intel DevCloud"
    else
        warn "Not detected as DevCloud environment"
    fi

    info "Environment variables:"
    env | grep -E "(DEVCLOUD|INTEL|ONEAPI|MKL|OPENVINO)" || echo "No Intel environment variables found"
    echo ""

    info "Intel tools in PATH:"
    which icc 2>/dev/null && echo "✅ Intel C++ Compiler found" || echo "❌ Intel C++ Compiler not found"
    which icpc 2>/dev/null && echo "✅ Intel C++ Compiler found" || echo "❌ Intel C++ Compiler not found"
    which python3 && echo "✅ Python3 found" || echo "❌ Python3 not found"
    echo ""
}

# Python Environment Check
check_python_env() {
    section "🐍 Python Environment"
    echo "─────────────────────"

    info "Python version:"
    python3 --version
    echo ""

    info "Virtual environment:"
    if [ -d "$PYTHON_ENV" ]; then
        log "✅ Virtual environment exists: $PYTHON_ENV"

        info "Activating virtual environment..."
        source "$PYTHON_ENV/bin/activate"

        info "Python in venv:"
        which python
        python --version
        echo ""

        info "Pip version:"
        pip --version
        echo ""

        info "Installed packages:"
        pip list | head -20
        echo "... (showing first 20 packages)"
        echo ""

    else
        error "❌ Virtual environment not found: $PYTHON_ENV"
        warn "Run setup_devcloud.sh to create the environment"
    fi
}

# Framework Structure Check
check_framework_structure() {
    section "📁 Framework Structure"
    echo "─────────────────────"

    info "Framework directory contents:"
    ls -la
    echo ""

    info "Checking key directories:"
    for dir in "src" "django_app" "tests" "docs" "deployments"; do
        if [ -d "$dir" ]; then
            log "✅ $dir/ directory exists"
        else
            error "❌ $dir/ directory missing"
        fi
    done
    echo ""

    info "Checking key files:"
    for file in "manage.py" "requirements.txt" "README.md" "pyproject.toml"; do
        if [ -f "$file" ]; then
            log "✅ $file exists"
        else
            error "❌ $file missing"
        fi
    done
    echo ""
}

# Dependencies Check
check_dependencies() {
    section "📦 Dependencies Check"
    echo "─────────────────────"

    if [ -f "$PYTHON_ENV/bin/activate" ]; then
        source "$PYTHON_ENV/bin/activate"

        info "Checking core dependencies:"

        # Django
        python -c "import django; print(f'✅ Django {django.get_version()}')" 2>/dev/null || error "❌ Django import failed"

        # OpenVINO
        python -c "import openvino as ov; print(f'✅ OpenVINO {ov.__version__}')" 2>/dev/null || error "❌ OpenVINO import failed"

        # Intel Extension for PyTorch
        python -c "import intel_extension_for_pytorch as ipex; print(f'✅ Intel Extension for PyTorch {ipex.__version__}')" 2>/dev/null || warn "⚠️ Intel Extension for PyTorch not available"

        # Other key packages
        python -c "import numpy; print(f'✅ NumPy {numpy.__version__}')" 2>/dev/null || error "❌ NumPy import failed"
        python -c "import pandas; print(f'✅ Pandas {pandas.__version__}')" 2>/dev/null || error "❌ Pandas import failed"
        python -c "import celery; print(f'✅ Celery {celery.__version__}')" 2>/dev/null || error "❌ Celery import failed"

        echo ""
    else
        error "Virtual environment not activated"
    fi
}

# OpenVINO Check
check_openvino() {
    section "🧠 OpenVINO Check"
    echo "─────────────────"

    if [ -f "$PYTHON_ENV/bin/activate" ]; then
        source "$PYTHON_ENV/bin/activate"

        info "OpenVINO environment:"
        if [ -f "/opt/intel/openvino/setupvars.sh" ]; then
            log "✅ OpenVINO setupvars.sh found"
            source /opt/intel/openvino/setupvars.sh
        else
            warn "⚠️ OpenVINO setupvars.sh not found, using pip version"
        fi
        echo ""

        info "Testing OpenVINO functionality:"
        python << 'EOF'
try:
    import openvino as ov
    print(f"✅ OpenVINO version: {ov.__version__}")

    core = ov.Core()
    devices = core.available_devices
    print(f"✅ Available devices: {devices}")

    if 'CPU' in devices:
        print("✅ CPU device available")
    if 'GPU' in devices:
        print("✅ GPU device available")

    # Test basic functionality
    model = ov.Model([ov.opset8.parameter([1, 3, 224, 224], ov.Type.f32)], "test_model")
    compiled = core.compile_model(model, "CPU")
    print("✅ Basic OpenVINO functionality working")

except Exception as e:
    print(f"❌ OpenVINO test failed: {e}")
EOF
        echo ""
    fi
}

# Framework Import Check
check_framework_imports() {
    section "🔧 Framework Imports"
    echo "────────────────────"

    if [ -f "$PYTHON_ENV/bin/activate" ]; then
        source "$PYTHON_ENV/bin/activate"

        # Set environment variables
        export DJANGO_SETTINGS_MODULE=ai_framework.settings
        export PYTHONPATH="${PWD}:${PYTHONPATH}"

        info "Testing framework imports:"
        python << 'EOF'
import sys
sys.path.append('.')

try:
    from src.core.agent_base import SimpleAgent
    print("✅ SimpleAgent import successful")
except Exception as e:
    print(f"❌ SimpleAgent import failed: {e}")

try:
    from src.core.execution_context import ExecutionContext
    print("✅ ExecutionContext import successful")
except Exception as e:
    print(f"❌ ExecutionContext import failed: {e}")

try:
    from src.orchestrator.workflow_engine import WorkflowEngine
    print("✅ WorkflowEngine import successful")
except Exception as e:
    print(f"❌ WorkflowEngine import failed: {e}")

try:
    import django
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
EOF
        echo ""
    fi
}

# Network and Services Check
check_network_services() {
    section "🌐 Network & Services"
    echo "──────────────────────"

    info "Active network connections:"
    netstat -ln 2>/dev/null | grep -E "(8000|8080|5432|6379|9092)" | head -10 || echo "No relevant services found"
    echo ""

    info "Running Python processes:"
    ps aux | grep python | grep -v grep | head -5 || echo "No Python processes found"
    echo ""

    info "Port availability check:"
    for port in 8000 8080 5432 6379; do
        if netstat -ln 2>/dev/null | grep -q ":$port "; then
            warn "⚠️ Port $port is already in use"
        else
            log "✅ Port $port is available"
        fi
    done
    echo ""
}

# Performance Check
check_performance() {
    section "⚡ Performance Check"
    echo "────────────────────"

    if [ -f "$PYTHON_ENV/bin/activate" ]; then
        source "$PYTHON_ENV/bin/activate"

        # Set environment variables
        export DJANGO_SETTINGS_MODULE=ai_framework.settings
        export PYTHONPATH="${PWD}:${PYTHONPATH}"

        info "Running performance test:"
        python << 'EOF'
import time
import asyncio
import sys
sys.path.append('.')

async def performance_test():
    try:
        from src.core.agent_base import SimpleAgent
        from src.core.execution_context import ExecutionContext

        agent = SimpleAgent(name='debug_test_agent')

        # Measure execution time
        start_time = time.time()
        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run({'test': 'debug performance test'}, context)
        execution_time = time.time() - start_time

        print(f"✅ Agent execution time: {execution_time:.3f} seconds")
        print(f"✅ Agent result status: {result.get('status', 'unknown')}")

    except Exception as e:
        print(f"❌ Performance test failed: {e}")

asyncio.run(performance_test())
EOF
        echo ""
    fi
}

# Log Analysis
analyze_logs() {
    section "📋 Log Analysis"
    echo "──────────────"

    info "Recent log files:"
    find . -name "*.log" -mtime -1 2>/dev/null | head -10 || echo "No recent log files found"
    echo ""

    if [ -f "django_app/debug.log" ]; then
        info "Recent Django errors:"
        tail -20 django_app/debug.log | grep -i error || echo "No recent errors"
        echo ""
    fi

    info "Disk usage by log files:"
    find . -name "*.log" -exec du -h {} \; 2>/dev/null | sort -hr | head -10 || echo "No log files found"
    echo ""
}

# Database Check
check_database() {
    section "🗄️  Database Check"
    echo "──────────────────"

    if [ -f "$PYTHON_ENV/bin/activate" ]; then
        source "$PYTHON_ENV/bin/activate"

        export DJANGO_SETTINGS_MODULE=ai_framework.settings
        export PYTHONPATH="${PWD}:${PYTHONPATH}"

        info "Database file check:"
        if [ -f "django_app/db.sqlite3" ]; then
            log "✅ SQLite database exists"
            ls -lh django_app/db.sqlite3
        else
            warn "⚠️ SQLite database not found"
        fi
        echo ""

        info "Testing database connection:"
        python << 'EOF'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_framework.settings')
django.setup()

try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ Database connection successful")

    # Check migrations
    from django.core.management import execute_from_command_line
    import sys
    from io import StringIO

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
        output = mystdout.getvalue()
        if '[X]' in output:
            print("✅ Database migrations applied")
        else:
            print("⚠️ Some migrations may be pending")
    except:
        print("⚠️ Could not check migrations")
    finally:
        sys.stdout = old_stdout

except Exception as e:
    print(f"❌ Database connection failed: {e}")
EOF
        echo ""
    fi
}

# Generate Health Report
generate_health_report() {
    section "📊 Health Report Summary"
    echo "─────────────────────────"

    echo "🔍 Debug completed at: $(date)"
    echo ""
    echo "📋 Quick Status:"

    # Environment
    if [[ "$HOSTNAME" == *"devcloud"* ]] || [[ "$USER" == u* ]]; then
        echo "   ✅ DevCloud environment detected"
    else
        echo "   ⚠️ DevCloud environment not detected"
    fi

    # Virtual environment
    if [ -d "$PYTHON_ENV" ]; then
        echo "   ✅ Python virtual environment exists"
    else
        echo "   ❌ Python virtual environment missing"
    fi

    # Framework files
    if [ -f "manage.py" ] && [ -f "requirements.txt" ]; then
        echo "   ✅ Framework files present"
    else
        echo "   ❌ Framework files missing"
    fi

    # Database
    if [ -f "django_app/db.sqlite3" ]; then
        echo "   ✅ Database file exists"
    else
        echo "   ⚠️ Database file not found"
    fi

    echo ""
    echo "📝 Debug log saved to: $LOG_FILE"
    echo "🔧 For detailed analysis, review the full output above"
    echo ""
    echo "🚀 To start the framework:"
    echo "   ./start_framework.sh"
    echo ""
    echo "🧪 To run tests:"
    echo "   ./test_performance.sh"
    echo ""
}

# Main debug function
main() {
    check_system_info
    check_devcloud_env
    check_python_env
    check_framework_structure
    check_dependencies
    check_openvino
    check_framework_imports
    check_network_services
    check_performance
    analyze_logs
    check_database
    generate_health_report
}

# Run main function
main "$@"
