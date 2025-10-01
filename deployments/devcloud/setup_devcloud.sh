#!/bin/bash
# Intel DevCloud Quick Setup Script
# Save as: setup_devcloud.sh

set -e

echo "🚀 Intel DevCloud Quick Setup for AI Agent Framework"
echo "=================================================="

# Configuration
FRAMEWORK_DIR="ai-agent-framework"
PYTHON_ENV="framework_env"
GITHUB_REPO="https://github.com/DevPrasath6/AI-Agent-Framework.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running on DevCloud
check_devcloud_environment() {
    log "Checking DevCloud environment..."

    if [[ "$HOSTNAME" == *"devcloud"* ]] || [[ "$USER" == u* ]]; then
        log "✅ Running on Intel DevCloud"
    else
        warn "This script is optimized for Intel DevCloud"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Setup workspace
setup_workspace() {
    log "Setting up workspace..."

    mkdir -p ~/workspace
    cd ~/workspace

    if [ -d "$FRAMEWORK_DIR" ]; then
        info "Framework directory exists, updating..."
        cd "$FRAMEWORK_DIR"
        git pull origin main
    else
        info "Cloning framework repository..."
        git clone "$GITHUB_REPO" "$FRAMEWORK_DIR"
        cd "$FRAMEWORK_DIR"
    fi

    log "✅ Workspace setup complete"
}

# Create Python environment
create_python_env() {
    log "Creating Python environment..."

    # Remove existing environment if it exists
    if [ -d "$PYTHON_ENV" ]; then
        warn "Removing existing environment..."
        rm -rf "$PYTHON_ENV"
    fi

    python3 -m venv "$PYTHON_ENV"
    source "$PYTHON_ENV/bin/activate"

    # Upgrade pip
    pip install --upgrade pip

    log "✅ Python environment created"
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."

    # Framework dependencies
    pip install -r requirements.txt

    # Intel-optimized packages
    info "Installing Intel-optimized packages..."
    pip install intel-extension-for-pytorch
    pip install openvino openvino-dev

    # DevCloud-specific packages
    pip install jupyter streamlit
    pip install memory-profiler

    log "✅ Dependencies installed"
}

# Configure Intel optimizations
configure_intel_optimizations() {
    log "Configuring Intel optimizations..."

    # Create optimization script
    cat > configure_intel.py << 'EOF'
import os
import subprocess

def setup_intel_env():
    """Setup Intel-optimized environment variables."""

    # OpenMP optimizations
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['MKL_NUM_THREADS'] = '4'
    os.environ['NUMBA_NUM_THREADS'] = '4'

    # Intel MKL optimizations
    os.environ['MKL_ENABLE_INSTRUCTIONS'] = 'AVX2'
    os.environ['MKL_THREADING_LAYER'] = 'GNU'

    # Memory optimizations
    os.environ['MALLOC_CONF'] = 'oversize_threshold:1,background_thread:true'

    print("✅ Intel optimizations configured")

if __name__ == "__main__":
    setup_intel_env()
EOF

    python configure_intel.py

    log "✅ Intel optimizations configured"
}

# Setup OpenVINO
setup_openvino() {
    log "Setting up OpenVINO..."

    # Source OpenVINO environment if available
    if [ -f "/opt/intel/openvino/setupvars.sh" ]; then
        source /opt/intel/openvino/setupvars.sh
        info "OpenVINO environment sourced"
    else
        warn "OpenVINO setupvars.sh not found - using pip installed version"
    fi

    # Test OpenVINO installation
    python -c "
import openvino as ov
print(f'✅ OpenVINO {ov.__version__} is available')
core = ov.Core()
print(f'Available devices: {core.available_devices}')
"

    log "✅ OpenVINO setup complete"
}

# Initialize framework
initialize_framework() {
    log "Initializing framework..."

    # Set environment variables
    export DJANGO_SETTINGS_MODULE=ai_framework.settings
    export PYTHONPATH="${PWD}:${PYTHONPATH}"

    # Database setup
    python manage.py migrate
    python manage.py collectstatic --noinput

    # Create superuser
    python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@devcloud.local', 'devcloud123')
    print("✅ Admin user created: admin/devcloud123")
else:
    print("✅ Admin user already exists")
EOF

    log "✅ Framework initialized"
}

# Test framework
test_framework() {
    log "Testing framework..."

    # Basic import test
    python -c "
import sys
sys.path.append('.')
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext
import asyncio

async def test():
    agent = SimpleAgent(name='devcloud_test_agent')
    context = ExecutionContext(agent_id=agent.id)
    result = await agent.run({'test': 'DevCloud deployment test'}, context)
    print(f'✅ Framework test successful: {result[\"status\"]}')

asyncio.run(test())
"

    # OpenVINO integration test
    python -c "
try:
    from bench.openvino_bench import OpenVINOBenchmark
    print('✅ OpenVINO integration available')
except ImportError:
    print('⚠️ OpenVINO benchmark module not found')
"

    log "✅ Framework testing complete"
}

# Create convenience scripts
create_scripts() {
    log "Creating convenience scripts..."

    # Start script
    cat > start_framework.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting AI Agent Framework on DevCloud..."

# Activate environment
source framework_env/bin/activate

# Source OpenVINO if available
if [ -f "/opt/intel/openvino/setupvars.sh" ]; then
    source /opt/intel/openvino/setupvars.sh
fi

# Set environment variables
export DJANGO_SETTINGS_MODULE=ai_framework.settings
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Start Django server
echo "Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

echo "✅ Framework started!"
echo "📊 Web interface: http://localhost:8000"
echo "🔑 Admin panel: http://localhost:8000/admin (admin/devcloud123)"
echo "📋 To stop: kill $DJANGO_PID"

# Wait for user input to stop
read -p "Press Enter to stop the framework..."
kill $DJANGO_PID
echo "✅ Framework stopped"
EOF

    # Stop script
    cat > stop_framework.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping AI Agent Framework..."
pkill -f "manage.py runserver"
pkill -f "celery worker"
echo "✅ Framework stopped"
EOF

    # Test script
    cat > test_performance.sh << 'EOF'
#!/bin/bash
echo "⚡ Running DevCloud Performance Tests..."

# Activate environment
source framework_env/bin/activate

# Source OpenVINO if available
if [ -f "/opt/intel/openvino/setupvars.sh" ]; then
    source /opt/intel/openvino/setupvars.sh
fi

# Set environment variables
export DJANGO_SETTINGS_MODULE=ai_framework.settings
export PYTHONPATH="${PWD}:${PYTHONPATH}"

echo "🧪 Running framework tests..."
python -m pytest tests/ -v --tb=short

echo "📊 Running OpenVINO benchmarks..."
python bench/openvino_bench.py --runs 10 --device CPU

echo "🤖 Testing agent performance..."
python -c "
import asyncio
import time
from src.core.agent_base import SimpleAgent
from src.core.execution_context import ExecutionContext

async def performance_test():
    agent = SimpleAgent(name='performance_test_agent')

    # Test multiple executions
    start_time = time.time()
    for i in range(10):
        context = ExecutionContext(agent_id=agent.id)
        await agent.run({'test': f'performance test {i}'}, context)

    total_time = time.time() - start_time
    print(f'✅ Performance test: 10 executions in {total_time:.2f} seconds')
    print(f'   Average: {total_time/10:.3f} seconds per execution')

asyncio.run(performance_test())
"

echo "✅ Performance tests completed"
EOF

    # Monitor script
    cat > monitor_system.sh << 'EOF'
#!/bin/bash
echo "📊 DevCloud System Monitor"
echo "=========================="

while true; do
    clear
    echo "📊 DevCloud System Monitor - $(date)"
    echo "=========================="
    echo ""
    echo "💾 Memory Usage:"
    free -h
    echo ""
    echo "🔥 CPU Usage:"
    top -bn1 | grep "Cpu(s)"
    echo ""
    echo "💾 Disk Usage:"
    df -h / | tail -1
    echo ""
    echo "🌐 Network Connections:"
    netstat -ln | grep LISTEN | head -5
    echo ""
    echo "🔄 Framework Processes:"
    ps aux | grep -E "(python|django)" | grep -v grep | head -5
    echo ""
    echo "Press Ctrl+C to exit..."
    sleep 5
done
EOF

    chmod +x *.sh

    log "✅ Convenience scripts created"
}

# Generate summary
generate_summary() {
    log "Generating deployment summary..."

    cat > DEVCLOUD_SETUP_SUMMARY.md << EOF
# 🚀 DevCloud Setup Summary

## Environment Information
- **Setup Date**: $(date)
- **Hostname**: $(hostname)
- **User**: $(whoami)
- **Python Version**: $(python3 --version)
- **Working Directory**: $(pwd)

## Installed Components
- ✅ AI Agent Framework
- ✅ Python virtual environment
- ✅ Intel-optimized packages
- ✅ OpenVINO toolkit
- ✅ Framework dependencies

## Available Scripts
- \`start_framework.sh\` - Start the framework
- \`stop_framework.sh\` - Stop the framework
- \`test_performance.sh\` - Run performance tests
- \`monitor_system.sh\` - Monitor system resources

## Access Information
- **Web Interface**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Credentials**: admin / devcloud123

## Quick Start
\`\`\`bash
# Start the framework
./start_framework.sh

# In another terminal, run tests
./test_performance.sh

# Monitor system
./monitor_system.sh
\`\`\`

## Next Steps
1. Test the framework with real workloads
2. Optimize OpenVINO models for your use case
3. Run comprehensive benchmarks
4. Deploy your custom agents

## Support
- Check logs in: \`devcloud_framework.log\`
- Run health checks: \`./debug_devcloud.sh\`
- Performance monitoring: \`./monitor_system.sh\`

## Environment Activation
\`\`\`bash
cd ~/workspace/$FRAMEWORK_DIR
source $PYTHON_ENV/bin/activate
source /opt/intel/openvino/setupvars.sh  # if available
export DJANGO_SETTINGS_MODULE=ai_framework.settings
export PYTHONPATH="\${PWD}:\${PYTHONPATH}"
\`\`\`

✅ Setup completed successfully!
EOF

    log "✅ Summary generated: DEVCLOUD_SETUP_SUMMARY.md"
}

# Main setup function
main() {
    echo ""
    log "Starting Intel DevCloud setup for AI Agent Framework..."
    echo ""

    # Run setup steps
    check_devcloud_environment
    setup_workspace
    create_python_env
    install_dependencies
    configure_intel_optimizations
    setup_openvino
    initialize_framework
    test_framework
    create_scripts
    generate_summary

    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Start framework: ./start_framework.sh"
    echo "   2. Run tests: ./test_performance.sh"
    echo "   3. Monitor system: ./monitor_system.sh"
    echo "   4. View summary: cat DEVCLOUD_SETUP_SUMMARY.md"
    echo ""
    echo "🌐 Access your framework at: http://localhost:8000"
    echo "🔑 Admin login: admin / devcloud123"
    echo ""
    echo "📚 For detailed information, see:"
    echo "   - DEVCLOUD_DEPLOYMENT_GUIDE.md"
    echo "   - DEVCLOUD_SETUP_SUMMARY.md"
    echo ""
    log "Happy coding on Intel DevCloud! 🚀"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
