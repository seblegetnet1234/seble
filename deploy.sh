#!/bin/bash

# Deployment script for Amharic Medical IR System

set -e

echo "🚀 Starting deployment..."

# Check if environment is specified
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh [development|production|docker]"
    exit 1
fi

ENVIRONMENT=$1

case $ENVIRONMENT in
    "development")
        echo "📦 Setting up development environment..."
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            python -m venv venv
        fi
        
        # Activate virtual environment
        source venv/bin/activate || source venv/Scripts/activate
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Copy environment file
        if [ ! -f ".env" ]; then
            cp .env.example .env
            echo "⚠️  Please update .env file with your configuration"
        fi
        
        # Initialize database
        python -c "from src.database import DatabaseManager; DatabaseManager().init_database()"
        
        echo "✅ Development environment ready!"
        echo "Run: python wsgi.py"
        ;;
        
    "production")
        echo "🏭 Setting up production environment..."
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Set production environment
        export FLASK_ENV=production
        export FLASK_DEBUG=False
        
        # Initialize database
        python -c "from src.database import DatabaseManager; DatabaseManager().init_database()"
        
        # Start with gunicorn
        echo "✅ Starting production server..."
        gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 120 wsgi:app
        ;;
        
    "docker")
        echo "🐳 Setting up Docker environment..."
        
        # Build and start containers
        docker-compose down
        docker-compose build
        docker-compose up -d
        
        # Wait for services to start
        echo "⏳ Waiting for services to start..."
        sleep 10
        
        # Check if services are running
        docker-compose ps
        
        echo "✅ Docker environment ready!"
        echo "Access the application at: http://localhost"
        ;;
        
    *)
        echo "❌ Invalid environment: $ENVIRONMENT"
        echo "Usage: ./deploy.sh [development|production|docker]"
        exit 1
        ;;
esac

echo "🎉 Deployment completed successfully!"