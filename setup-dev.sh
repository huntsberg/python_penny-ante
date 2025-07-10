#!/bin/bash
# Development setup script for penny-ante
# This script sets up the development environment using pipx for global tools

set -e

echo "🎯 Setting up penny-ante development environment..."

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo "📦 Installing pipx..."
    pip install pipx
    pipx ensurepath
    echo "✅ pipx installed. You may need to restart your shell."
fi

# Install global development tools with pipx
echo "🔧 Installing global development tools..."
pipx install poethepoet
pipx install black
pipx install build

# Install project in development mode
echo "📚 Installing penny-ante in development mode..."
poe install-dev

# Show project info
echo "ℹ️  Project information:"
poe info

echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  poe --help          # Show all available tasks"
echo "  poe test            # Run tests"
echo "  poe demo            # Demo the roulette wheel"
echo "  poe pre-commit      # Run pre-commit checks"
echo ""
echo "Happy coding! 🎰" 