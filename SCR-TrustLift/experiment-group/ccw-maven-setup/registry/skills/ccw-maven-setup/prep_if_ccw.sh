#!/bin/bash
# Prepare Maven environment for Claude Code Web (CCW)
# Does nothing if not in CCW environment

set -e

# Get script directory for accessing repo-vendored files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect CCW environment
if [ -z "$CLAUDECODE" ]; then
    echo "ℹ️  Not in Claude Code Web - no setup needed"
    exit 0
fi

echo "🔧 Claude Code Web detected - setting up Java 25..."
echo "⏱️  This setup ensures Java 25 is available for your session..."
echo "    (First run: ~60s, subsequent runs: ~10s due to caching)"

# Install SDKMAN if needed
if [ ! -d "$HOME/.sdkman" ]; then
    echo "📦 Installing SDKMAN..."
    curl -s "https://get.sdkman.io" | bash
fi

# Source SDKMAN from repo-vendored copy (version-controlled)
source "$HOME/.sdkman/bin/sdkman-init.sh" || source "$SCRIPT_DIR/sdkman-init.sh"


# Install Java 25 if needed (latest stable Temurin)
echo "🔍 Checking for Java 25..."
if ! sdk list java | grep -q "25\..*-tem.*installed"; then
    echo "☕ Installing latest stable Java 25 (Temurin)..."
    echo "   (This may take 30-60 seconds on first run)"
    # Get the latest 25.x Temurin version
    JAVA_VERSION=$(sdk list java 2>/dev/null | grep "tem" | grep "25\." | grep -v "fx\|ea" | head -1 | awk '{print $NF}')
    if [ -n "$JAVA_VERSION" ]; then
        echo "   Installing Java $JAVA_VERSION..."
        sdk install java "$JAVA_VERSION"
        echo "   ✅ Java $JAVA_VERSION installed successfully"
    else
        echo "⚠️  Could not find Java 25 Temurin, trying default..."
        sdk install java 25-tem
    fi
else
    echo "✅ Java 25 already installed"
    # Use any installed Java 25 Temurin version
    INSTALLED_VERSION=$(sdk list java 2>/dev/null | grep "25\..*-tem.*installed" | head -1 | awk '{print $NF}')
    echo "   Using Java $INSTALLED_VERSION"
    sdk use java "$INSTALLED_VERSION"
fi

# Persist Java 25 environment for the session
JAVA_HOME="$HOME/.sdkman/candidates/java/current"
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"

# If CLAUDE_ENV_FILE is available, persist for the entire session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export JAVA_HOME=\"$JAVA_HOME\"" >> "$CLAUDE_ENV_FILE"
    echo "export PATH=\"\$JAVA_HOME/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
    echo "  ✅ Java 25 environment persisted to session"
fi

echo ""
echo "✨ Java 25 setup complete!"
echo ""
echo "📊 Environment status:"
echo "   Java version:"
java -version 2>&1 | sed 's/^/   /' | head -1
echo ""
echo "⚠️  Note: Maven builds may not work in CCW due to environment limitations"
echo "   For full Maven functionality, please use local development"

