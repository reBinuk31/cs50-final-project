from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db_connection
from datetime import date
from urllib.parse import urlparse

app = Flask(__name__)
app.config["SECRET_KEY"] = "jobtrack-dev-secret-change-this"

def valid_job_url(value):
    if not value:
        return True

    parsed = urlparse(value)

    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
        and "." in parsed.netloc
        and " " not in value
    )

def valid_date(value):
    try:
        date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False

@app.route("/")
def index():
    connection = get_db_connection()

    applications = connection.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        applications=applications
    )

@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    conn = get_db_connection()

    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,),
    ).fetchone()

    if application is None:
        conn.close()
        flash("Application not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        date_applied = request.form.get("date_applied", "").strip()
        job_url = request.form.get("job_url", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company or not job_title or not date_applied:
            flash("Company, job title, and date applied are required.", "error")

        elif not valid_date(date_applied):
            flash("Please enter a valid application date.", "error")

        elif not valid_job_url(job_url):
            flash("Enter a valid job URL beginning with http:// or https://.", "error")

        else:
            conn.execute(
                """
                UPDATE applications
                SET company = ?,
                    job_title = ?,
                    date_applied = ?,
                    job_url = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    company,
                    job_title,
                    date_applied,
                    job_url,
                    notes,
                    application_id,
                ),
            )

            conn.commit()
            conn.close()

            flash("Application updated successfully!", "success")
            return redirect(
                url_for("details", application_id=application_id)
            )

        # Reload the form with the user's submitted values after validation fails.
        application = dict(application)
        application.update({
            "company": company,
            "job_title": job_title,
            "date_applied": date_applied,
            "job_url": job_url,
            "notes": notes,
        })

    conn.close()
    return render_template("edit.html", application=application)

@app.route("/details/<int:application_id>")
def details(application_id):
    conn = get_db_connection()

    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,)
    ).fetchone()

    conn.close()

    if application is None:
        return "Application not found", 404

    return render_template("details.html", application=application)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        date_applied = request.form.get("date_applied", "").strip()
        job_url = request.form.get("job_url", "").strip()
        notes = request.form.get("notes", "").strip()

        # Keep submitted values if validation fails.
        form_data = {
            "company": company,
            "job_title": job_title,
            "date_applied": date_applied,
            "job_url": job_url,
            "notes": notes,
        }

        if not company or not job_title or not date_applied:
            flash(
                "Company, job title, and date applied are required.",
                "error",
            )
            return render_template("add.html", form_data=form_data)

        if not valid_date(date_applied):
            flash("Please enter a valid application date.", "error")
            return render_template("add.html", form_data=form_data)

        if not valid_job_url(job_url):
            flash(
                "Enter a valid job URL beginning with http:// or https://.",
                "error",
            )
            return render_template("add.html", form_data=form_data)

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO applications
                (company, job_title, date_applied, job_url, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company, job_title, date_applied, job_url, notes),
        )

        connection.commit()
        connection.close()

        flash("Application added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html", form_data={})

@app.route("/update_status", methods=["POST"])
def update_status():
    application_id = request.form.get("application_id", "").strip()
    status = request.form.get("status", "").strip()

    allowed_statuses = ["Applied", "Interview", "Offer", "Rejected"]

    if not application_id.isdigit() or status not in allowed_statuses:
        flash("Invalid application ID or status.", "error")
        return redirect(url_for("index"))

    connection = get_db_connection()

    application = connection.execute(
        "SELECT id FROM applications WHERE id = ?",
        (application_id,),
    ).fetchone()

    if application is None:
        connection.close()
        flash("Application not found.", "error")
        return redirect(url_for("index"))

    connection.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, application_id),
    )
    connection.commit()
    connection.close()

    flash("Application status updated successfully!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    connection = get_db_connection()

    application = connection.execute(
        "SELECT id FROM applications WHERE id = ?",
        (application_id,),
    ).fetchone()

    if application is None:
        connection.close()
        flash("Application not found. Nothing was deleted.", "error")
        return redirect(url_for("index"))

    connection.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,),
    )
    connection.commit()
    connection.close()

    flash("Application deleted successfully!", "success")
    return redirect(url_for("index"))
