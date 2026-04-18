#!/bin/bash

# Vercel Deployment Script for Name Classifier API v2
# This script helps deploy the Django app to Vercel with PostgreSQL

echo "🚀 Deploying Name Classifier API v2 to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install it with: npm install -g vercel"
    exit 1
fi

# Check if logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel. Run: vercel login"
    exit 1
fi

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Check your Vercel dashboard for the deployment URL"
echo "⚙️  Don't forget to set environment variables in Vercel dashboard:"
echo "   - DATABASE_URL (your PostgreSQL connection string)"
echo "   - SECRET_KEY (your Django secret key)"
echo "   - DEBUG = False"