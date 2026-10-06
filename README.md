# StudySync – Cloud-Based Student Assignment and Notes Management System

A Flask + MySQL student productivity application redesigned around the Lumina Study / StudySync UI supplied in the Stitch project.

## Included
- Dashboard with visual metrics, upcoming assignments and study momentum
- Assignment CRUD with card/list views, filters and search
- Subject-based assignment boards with in-progress and completed columns
- Optional assignment subtasks with completion-based progress
- Notes & Files repository with subject folders, upload, search, category filters, download and delete
- Dashboard assignment activity chart based on recorded creation and completion dates
- Settings page using the same visual language
- Responsive layout
- Light-mode-only interface

## Run locally
```powershell
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/`.

## Database
The existing `student_manager` MySQL database is expected. See `schema.sql` for the required tables. On local startup, the app creates missing tables and adds the nullable completion timestamp and file-subject columns when they are absent.

## AWS migration
The backend remains Flask + SQLAlchemy so the local MySQL and filesystem storage can later be migrated to:
- Elastic Beanstalk
- Amazon RDS
- Amazon S3
- IAM
