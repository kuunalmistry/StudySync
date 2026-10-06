from flask import (
    Flask, render_template, request, redirect, url_for,
    send_from_directory, send_file, flash, jsonify, abort
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from sqlalchemy import or_, func, inspect, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import os
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from urllib.parse import quote_plus
from dotenv import load_dotenv

app = Flask(__name__)

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
load_dotenv()

# AWS S3 configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "studysync-kuunalmistry-files")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

DB_HOST = os.getenv(
    "DB_HOST",
    "studysync-mysql-kuunal.mysql.database.azure.com"
)
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "student_manager")
DB_USER = os.getenv("DB_USER", "studysyncadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_SSL_CA = os.getenv(
    "DB_SSL_CA",
    "certs/DigiCertGlobalRootG2.crt.pem"
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@"
    f"{DB_HOST}:{DB_PORT}/{quote_plus(DB_NAME)}?charset=utf8mb4"
)

ssl_options = {"check_hostname": True}

if os.path.isfile(DB_SSL_CA):
    ssl_options["ca"] = DB_SSL_CA

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": ssl_options
    }
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.secret_key = "studysync-local-secret"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "png", "jpg", "jpeg", "ipynb", "zip", "sql", "pptx"
}

SUBJECT_OPTIONS = [
    "Enterprise Grade Connected Device Application: Self-Driving Cars",
    "TYBTECH-SEM 5-Project Life Cycle Management",
    "Advanced Algorithms",
    "Emerging Technologies",
    "Computer Vision and Deep Learning",
    "Reinforcement Learning and NLP",
    "Cloud Application Development",
]


# ------------------------------------------------------------
# Models
# ------------------------------------------------------------
class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), default="Medium")
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    subtasks = relationship(
        "SubTask", backref="assignment", cascade="all, delete-orphan",
        order_by="SubTask.id"
    )


class SubTask(db.Model):
    __tablename__ = "subtasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignment_id = db.Column(
        db.Integer, ForeignKey("assignments.id"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)


class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(100))
    file_size = db.Column(db.BigInteger)
    subject = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def format_size(size):
    if size is None:
        return "0 KB"
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.0f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def file_icon(file_type):
    file_type = (file_type or "").lower()
    if file_type == "pdf":
        return "picture_as_pdf"
    if file_type in {"ipynb", "sql", "zip"}:
        return "terminal"
    if file_type in {"png", "jpg", "jpeg"}:
        return "image"
    if file_type in {"pptx"}:
        return "slideshow"
    return "description"


def file_color(file_type):
    file_type = (file_type or "").lower()
    if file_type == "pdf":
        return "coral"
    if file_type in {"ipynb", "sql", "zip"}:
        return "indigo"
    if file_type in {"png", "jpg", "jpeg"}:
        return "sky"
    if file_type == "pptx":
        return "violet"
    return "mint"


def assignment_progress(assignment):
    if not assignment.subtasks:
        return 0
    completed = sum(subtask.completed for subtask in assignment.subtasks)
    return round(completed / len(assignment.subtasks) * 100)


def due_label(assignment):
    delta = (assignment.due_date - date.today()).days
    if assignment.status == "Completed":
        return "Completed", "success"
    if delta < 0:
        return f"Overdue by {abs(delta)} day{'s' if abs(delta) != 1 else ''}", "danger"
    if delta == 0:
        return "Due today", "danger"
    if delta == 1:
        return "Due tomorrow", "warning"
    if delta <= 7:
        return f"Due in {delta} days", "info"
    return "Next week", "info"


@app.context_processor
def inject_helpers():
    return {
        "format_size": format_size,
        "file_icon": file_icon,
        "file_color": file_color,
        "assignment_progress": assignment_progress,
        "due_label": due_label,
        "today": date.today(),
        "subject_options": SUBJECT_OPTIONS,
    }


# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------
@app.route("/")
def home():
    today = date.today()
    total_assignments = Assignment.query.count()
    pending_count = Assignment.query.filter_by(status="Pending").count()
    completed_count = Assignment.query.filter_by(status="Completed").count()
    upcoming_count = Assignment.query.filter(
        Assignment.due_date >= today,
        Assignment.status != "Completed"
    ).count()

    upcoming_assignments = Assignment.query.filter(
        Assignment.due_date >= today,
        Assignment.status != "Completed"
    ).order_by(Assignment.due_date.asc()).limit(3).all()

    recent_files = UploadedFile.query.order_by(
        UploadedFile.uploaded_at.desc()
    ).limit(3).all()

    week_dates = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    week_start = datetime.combine(week_dates[0], datetime.min.time())
    weekly_assignments = Assignment.query.filter(or_(
        Assignment.created_at >= week_start,
        Assignment.completed_at >= week_start
    )).all()
    activity_by_date = {
        activity_date: {"created": 0, "completed": 0}
        for activity_date in week_dates
    }
    for assignment in weekly_assignments:
        created_date = assignment.created_at.date() if assignment.created_at else None
        if created_date in activity_by_date:
            activity_by_date[created_date]["created"] += 1
        completed_date = assignment.completed_at.date() if assignment.completed_at else None
        if completed_date in activity_by_date:
            activity_by_date[completed_date]["completed"] += 1

    weekly_activity = [
        {
            "label": activity_date.strftime("%a")[0],
            **activity_by_date[activity_date],
            "total": sum(activity_by_date[activity_date].values()),
        }
        for activity_date in week_dates
    ]
    weekly_max = max((day["total"] for day in weekly_activity), default=0)
    activity_created = sum(day["created"] for day in weekly_activity)
    activity_completed = sum(day["completed"] for day in weekly_activity)
    pace = round((completed_count / total_assignments) * 100) if total_assignments else 0

    return render_template(
        "index.html",
        total_assignments=total_assignments,
        pending_count=pending_count,
        completed_count=completed_count,
        upcoming_count=upcoming_count,
        upcoming_assignments=upcoming_assignments,
        recent_files=recent_files,
        weekly_activity=weekly_activity,
        weekly_max=weekly_max,
        activity_created=activity_created,
        activity_completed=activity_completed,
        pace=pace,
    )


# ------------------------------------------------------------
# Assignments
# ------------------------------------------------------------
@app.route("/assignments")
def assignments():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "all")
    subject_filter = request.args.get("subject", "all")

    query = Assignment.query

    if search:
        like = f"%{search}%"
        query = query.filter(or_(
            Assignment.title.ilike(like),
            Assignment.subject.ilike(like),
            Assignment.description.ilike(like)
        ))

    if status_filter == "pending":
        query = query.filter_by(status="Pending")
    elif status_filter == "completed":
        query = query.filter_by(status="Completed")

    if subject_filter != "all":
        query = query.filter_by(subject=subject_filter)

    all_assignments = query.order_by(Assignment.due_date.asc()).all()
    subjects = [row[0] for row in db.session.query(
        Assignment.subject
    ).distinct().order_by(Assignment.subject).all()]

    total = Assignment.query.count()
    pending = Assignment.query.filter_by(status="Pending").count()
    completed = Assignment.query.filter_by(status="Completed").count()
    due_this_week = Assignment.query.filter(
        Assignment.due_date >= date.today(),
        Assignment.due_date <= date.today().fromordinal(date.today().toordinal() + 7),
        Assignment.status != "Completed"
    ).count()

    return render_template(
        "assignments.html",
        assignments=all_assignments,
        subjects=subjects,
        search=search,
        status_filter=status_filter,
        subject_filter=subject_filter,
        total=total,
        pending=pending,
        completed=completed,
        due_this_week=due_this_week,
    )


@app.route("/subjects")
def subjects():
    subject_stats = []
    for subject in SUBJECT_OPTIONS:
        subject_assignments = Assignment.query.filter_by(subject=subject).all()
        subject_stats.append({
            "name": subject,
            "pending": sum(item.status != "Completed" for item in subject_assignments),
            "total": len(subject_assignments),
        })
    return render_template("subjects.html", subject_stats=subject_stats)


@app.route("/subjects/<path:subject>")
def subject_detail(subject):
    if subject not in SUBJECT_OPTIONS:
        abort(404)
    subject_assignments = Assignment.query.filter_by(subject=subject).order_by(
        Assignment.due_date.asc()
    ).all()
    return render_template(
        "subject_assignments.html",
        subject=subject,
        in_progress=[item for item in subject_assignments if item.status != "Completed"],
        completed=[item for item in subject_assignments if item.status == "Completed"],
    )


@app.route("/add-assignment", methods=["POST"])
def add_assignment():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "")
    priority = request.form.get("priority", "Medium")
    subtask_titles = [title.strip() for title in request.form.getlist("subtasks") if title.strip()]

    if not title or subject not in SUBJECT_OPTIONS or not due_date:
        flash("Please fill in all required assignment fields.", "error")
        return redirect(request.referrer or url_for("home"))

    new_assignment = Assignment(
        title=title,
        subject=subject,
        description=description,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        priority=priority,
        status="Pending"
    )
    new_assignment.subtasks = [SubTask(title=title) for title in subtask_titles]
    db.session.add(new_assignment)
    db.session.commit()
    flash("Assignment added successfully.", "success")
    return redirect(request.referrer or url_for("home"))


@app.route("/add-subtask/<int:assignment_id>", methods=["POST"])
def add_subtask(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    title = request.form.get("title", "").strip()
    if title:
        db.session.add(SubTask(assignment_id=assignment.id, title=title))
        db.session.commit()
        flash("Subtask added.", "success")
    return redirect(url_for("edit_assignment", assignment_id=assignment.id))


@app.route("/toggle-subtask/<int:subtask_id>", methods=["POST"])
def toggle_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    subtask.completed = not subtask.completed
    db.session.commit()
    return redirect(request.referrer or url_for("edit_assignment", assignment_id=subtask.assignment_id))


@app.route("/delete-subtask/<int:subtask_id>", methods=["POST"])
def delete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    assignment_id = subtask.assignment_id
    db.session.delete(subtask)
    db.session.commit()
    return redirect(url_for("edit_assignment", assignment_id=assignment_id))


@app.route("/complete-assignment/<int:assignment_id>", methods=["POST"])
def complete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    assignment.status = "Completed"
    if assignment.completed_at is None:
        assignment.completed_at = datetime.utcnow()
    db.session.commit()
    flash("Assignment marked as completed.", "success")
    return redirect(request.referrer or url_for("assignments"))


@app.route("/delete-assignment/<int:assignment_id>", methods=["POST"])
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    flash("Assignment deleted.", "success")
    return redirect(request.referrer or url_for("assignments"))


@app.route("/edit-assignment/<int:assignment_id>", methods=["GET", "POST"])
def edit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    if request.method == "POST":
        assignment.title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        if subject not in SUBJECT_OPTIONS:
            flash("Please choose a subject from the list.", "error")
            return redirect(url_for("edit_assignment", assignment_id=assignment.id))
        assignment.subject = subject
        assignment.description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date")
        assignment.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        assignment.priority = request.form.get("priority", "Medium")
        new_status = request.form.get("status", "Pending")
        if new_status != assignment.status:
            assignment.completed_at = datetime.utcnow() if new_status == "Completed" else None
        assignment.status = new_status
        db.session.commit()
        flash("Assignment updated successfully.", "success")
        return redirect(url_for("assignments"))

    return render_template("edit_assignment.html", assignment=assignment)


# ------------------------------------------------------------
# Files / Notes
# ------------------------------------------------------------
@app.route("/files")
def files():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    subject_filter = request.args.get("subject", "all")
    if subject_filter not in SUBJECT_OPTIONS:
        subject_filter = "all"

    query = UploadedFile.query

    if search:
        query = query.filter(UploadedFile.filename.ilike(f"%{search}%"))

    if category != "all":
        if category == "notes":
            query = query.filter(UploadedFile.file_type.in_(["pdf", "doc", "docx"]))
        elif category == "labs":
            query = query.filter(UploadedFile.file_type.in_(["ipynb", "sql", "zip"]))
        elif category == "slides":
            query = query.filter(UploadedFile.file_type == "pptx")

    if subject_filter != "all":
        query = query.filter_by(subject=subject_filter)

    uploaded_files = query.order_by(UploadedFile.uploaded_at.desc()).all()
    total_files = UploadedFile.query.count()
    total_bytes = db.session.query(
        func.coalesce(func.sum(UploadedFile.file_size), 0)
    ).scalar() or 0

    return render_template(
        "files.html",
        files=uploaded_files,
        total_files=total_files,
        total_bytes=total_bytes,
        search=search,
        category=category,
        subjects=SUBJECT_OPTIONS,
        subject_filter=subject_filter,
        course_file_counts={
            subject: UploadedFile.query.filter_by(subject=subject).count()
            for subject in SUBJECT_OPTIONS
        },
    )


@app.route("/upload-file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for("files"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("files"))

    if not allowed_file(file.filename):
        flash("File type not allowed.", "error")
        return redirect(url_for("files"))

    original_filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    stored_filename = f"{timestamp}_{original_filename}"
    s3_key = f"files/{stored_filename}"

    # Determine size without writing the file to the local uploads folder.
    file.stream.seek(0, os.SEEK_END)
    file_size = file.stream.tell()
    file.stream.seek(0)

    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.mimetype or "application/octet-stream"
            },
        )
    except ClientError:
        app.logger.exception("S3 upload failed")
        flash("File upload to cloud storage failed.", "error")
        return redirect(url_for("files"))

    extension = original_filename.rsplit(".", 1)[1].lower()
    subject = request.form.get("subject", "").strip()
    new_file = UploadedFile(
        filename=original_filename,
        stored_filename=s3_key,
        file_type=extension,
        file_size=file_size,
        subject=subject if subject in SUBJECT_OPTIONS else None,
    )

    try:
        db.session.add(new_file)
        db.session.commit()
    except Exception:
        # Keep S3 and MySQL consistent if the database write fails.
        db.session.rollback()
        try:
            s3.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        except ClientError:
            app.logger.exception("Failed to roll back S3 object after DB error")
        raise

    flash("File uploaded successfully.", "success")
    return redirect(
        url_for("files", subject=subject)
        if subject in SUBJECT_OPTIONS else url_for("files")
    )


@app.route("/download-file/<int:file_id>")
def download_file(file_id):
    uploaded_file = UploadedFile.query.get_or_404(file_id)

    try:
        s3_object = s3.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=uploaded_file.stored_filename,
        )
        file_data = BytesIO(s3_object["Body"].read())
    except ClientError:
        app.logger.exception("S3 download failed")
        flash("Unable to download the file from cloud storage.", "error")
        return redirect(url_for("files"))

    return send_file(
        file_data,
        as_attachment=True,
        download_name=uploaded_file.filename,
        mimetype=s3_object.get("ContentType") or "application/octet-stream",
    )


@app.route("/delete-file/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    uploaded_file = UploadedFile.query.get_or_404(file_id)

    try:
        s3.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=uploaded_file.stored_filename,
        )
    except ClientError:
        app.logger.exception("S3 delete failed")
        flash("Unable to delete the file from cloud storage.", "error")
        return redirect(url_for("files"))

    db.session.delete(uploaded_file)
    db.session.commit()
    flash("File deleted successfully.", "success")
    return redirect(url_for("files"))


# ------------------------------------------------------------
# Settings
# ------------------------------------------------------------
@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.errorhandler(413)
def file_too_large(_error):
    flash("File is too large. Maximum size is 10 MB.", "error")
    return redirect(url_for("files"))


def initialize_database():
    db.create_all()
    assignment_columns = {
        column["name"] for column in inspect(db.engine).get_columns("assignments")
    }
    if "completed_at" not in assignment_columns:
        db.session.execute(text(
            "ALTER TABLE assignments ADD COLUMN completed_at DATETIME NULL"
        ))

    uploaded_file_columns = {
        column["name"] for column in inspect(db.engine).get_columns("uploaded_files")
    }
    if "subject" not in uploaded_file_columns:
        db.session.execute(text(
            "ALTER TABLE uploaded_files ADD COLUMN subject VARCHAR(100) NULL"
        ))
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        initialize_database()
    app.run(debug=True)
