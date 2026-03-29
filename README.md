# Propertism

**NRI Property Management Platform**

Propertism Realty Advisors LLP - Professional property management services for NRI owners in Chennai.

## Project Structure

```
propertism/
├── realtor-web/          # Django application
│   ├── content/          # Content management
│   ├── properties/       # Property listings
│   ├── uilayers/         # Templates and UI
│   ├── static/           # Static files (CSS, JS, images)
│   ├── media/            # Uploaded media files
│   └── documents/        # Project documentation
├── SESSION_TRACKER.md    # Current session tracking
└── README.md            # This file
```

## Quick Links

- **Live Site**: http://propertism.in (currently showing 502 error - being fixed)
- **AWS Environment**: propertism-prod (us-west-2)
- **Repository**: https://github.com/Propertism/propertism

## Current Status

🔄 **In Progress**: Fixing 502 Bad Gateway error and static files serving

See [SESSION_TRACKER.md](SESSION_TRACKER.md) for detailed session history and current status.

## Documentation

All project documentation is located in `realtor-web/documents/`:
- Deployment guides
- DNS configuration
- Static files fix documentation
- Session logs

## Admin Access

- **URL**: http://propertism.in/admin/ (once fixed)
- **Username**: admin
- **Password**: admin123 (change after first login)

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (persistent storage)
- **Hosting**: AWS Elastic Beanstalk
- **Platform**: Python 3.11 on Amazon Linux 2023
- **Web Server**: Nginx + Gunicorn

## Brand Identity

- **Primary Color**: Navy Blue (#0F172A)
- **Accent Color**: Gold (#B89A4A)
- **Company**: Propertism Realty Advisors LLP
- **Focus**: NRI Property Management in Chennai

## Next Steps

1. Wait for AWS environment to stabilize
2. Retry deployment to fix 502 error
3. Set up SSL certificate for HTTPS
4. Upload company logo and content

---

For detailed session history and current tasks, see [SESSION_TRACKER.md](SESSION_TRACKER.md)
