# Heroku Deployment Guide

## Prerequisites
- Heroku CLI installed
- Git repository initialized
- Heroku account

## Deployment Steps

### 1. Create Heroku App
```bash
heroku create your-app-name
```

### 2. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 3. Add Redis (Optional, for caching)
```bash
heroku addons:create heroku-redis:mini
```

### 4. Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set LOG_LEVEL=INFO
```

### 5. Deploy
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

### 6. Initialize Database
```bash
heroku run python -c "from src.database import DatabaseManager; DatabaseManager().init_database()"
```

### 7. Open Application
```bash
heroku open
```

## Environment Variables

Set these in Heroku dashboard or via CLI:

- `SECRET_KEY`: Your secret key for sessions
- `FLASK_ENV`: Set to "production"
- `DATABASE_URL`: Automatically set by Heroku PostgreSQL
- `LOG_LEVEL`: Set to "INFO" or "WARNING"

## Monitoring

### View Logs
```bash
heroku logs --tail
```

### Check Dyno Status
```bash
heroku ps
```

### Database Console
```bash
heroku pg:psql
```

## Scaling

### Scale Web Dynos
```bash
heroku ps:scale web=2
```

### Upgrade Database
```bash
heroku addons:upgrade heroku-postgresql:basic
```

## Custom Domain (Optional)

### Add Domain
```bash
heroku domains:add www.yourdomain.com
```

### SSL Certificate
```bash
heroku certs:auto:enable
```