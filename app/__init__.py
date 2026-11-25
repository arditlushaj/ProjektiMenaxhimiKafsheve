import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, current_app, g, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "qendra.db"


def get_db() -> sqlite3.Connection:
    if "database" not in g:
        database = current_app.config.get("DATABASE", str(DATABASE))
        g.database = sqlite3.connect(database)
        g.database.row_factory = sqlite3.Row
    return g.database


def init_db() -> None:
    with get_db() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                age_months INTEGER,
                gender TEXT NOT NULL,
                description TEXT,
                health_status TEXT,
                status TEXT NOT NULL DEFAULT 'available',
                intake_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS adoption_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER NOT NULL,
                applicant_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                message TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS care_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'to_do',
                due_date TEXT,
                FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
            );
            """
        )

        if db.execute("SELECT COUNT(*) FROM animals").fetchone()[0] == 0:
            db.executemany(
                """
                INSERT INTO animals
                (name, species, breed, age_months, gender, description, health_status, status, intake_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("Bela", "qen", "Sterqok", 12, "femer", "Shume e qete dhe miqesore", "E vaksinuar", "available", "2026-10-01"),
                    ("Miu", "mace", "Evropiane", 6, "mashkull", "Lojtare dhe e paster", "Shendetplotë", "in_care", "2026-10-05"),
                    ("Rex", "qen", "Labrador", 24, "mashkull", "Qen besnik dhe energjik", "Nen vezhgim mjekesor", "available", "2026-10-10"),
                ],
            )

        if db.execute("SELECT COUNT(*) FROM care_tasks").fetchone()[0] == 0:
            db.execute(
                "INSERT INTO care_tasks (animal_id, title, description, status, due_date) VALUES (?, ?, ?, ?, ?)",
                (1, "Ushqyerja e Belës", "Ushqim i planshur në mengjes", "to_do", "2026-10-15"),
            )


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = test_config["DATABASE"] if test_config and "DATABASE" in test_config else str(DATABASE)

    with app.app_context():
        init_db()
        database = g.pop("database", None)
        if database is not None:
            database.close()

    @app.teardown_appcontext
    def close_db(_error):
        database = g.pop("database", None)
        if database is not None:
            database.close()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/animals")
    def list_animals():
        search = request.args.get("search", "").strip().lower()
        status = request.args.get("status", "").strip()
        with get_db() as db:
            query = "SELECT * FROM animals WHERE 1=1"
            parameters = []
            if search:
                query += " AND (LOWER(name) LIKE ? OR LOWER(species) LIKE ?)"
                parameters.extend([f"%{search}%", f"%{search}%"])
            if status:
                query += " AND status = ?"
                parameters.append(status)
            query += " ORDER BY id"
            animals = [dict(row) for row in db.execute(query, parameters).fetchall()]
        return jsonify({"animals": animals, "count": len(animals)})

    @app.post("/api/animals")
    def create_animal():
        data = request.get_json(silent=True) or {}
        required = ("name", "species", "gender", "intake_date")
        missing = [field for field in required if not str(data.get(field, "")).strip()]
        if missing:
            return jsonify({"error": "Fushat e detyrueshme mungojnë.", "fields": missing}), 400
        if data["gender"] not in ("mashkull", "femer"):
            return jsonify({"error": "Gjinia nuk është e vlefshme."}), 400
        try:
            intake_date = date.fromisoformat(str(data["intake_date"]))
        except ValueError:
            return jsonify({"error": "Data e pranimit nuk është e vlefshme."}), 400

        with get_db() as db:
            cursor = db.execute(
                """
                INSERT INTO animals
                (name, species, breed, age_months, gender, description, health_status, status, intake_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["name"].strip(),
                    data["species"].strip(),
                    data.get("breed", "").strip(),
                    data.get("age_months") or None,
                    data["gender"],
                    data.get("description", "").strip(),
                    data.get("health_status", "").strip(),
                    data.get("status", "available"),
                    intake_date.isoformat(),
                ),
            )
            animal = dict(db.execute("SELECT * FROM animals WHERE id = ?", (cursor.lastrowid,)).fetchone())
        return jsonify({"animal": animal}), 201

    @app.post("/api/adoptions")
    def create_adoption():
        data = request.get_json(silent=True) or {}
        required = ("animal_id", "applicant_name", "email")
        missing = [field for field in required if not str(data.get(field, "")).strip()]
        if missing:
            return jsonify({"error": "Fushat e detyrueshme mungojnë.", "fields": missing}), 400
        if "@" not in data["email"]:
            return jsonify({"error": "Email-i nuk është i vlefshëm."}), 400

        with get_db() as db:
            animal = db.execute("SELECT id, status FROM animals WHERE id = ?", (data["animal_id"],)).fetchone()
            if not animal:
                return jsonify({"error": "Kafsha nuk u gjet."}), 404
            if animal["status"] != "available":
                return jsonify({"error": "Kjo kafshë nuk është aktualisht në dispozicion."}), 409
            cursor = db.execute(
                """
                INSERT INTO adoption_applications
                (animal_id, applicant_name, email, phone, message, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
                """,
                (
                    animal["id"],
                    data["applicant_name"].strip(),
                    data["email"].strip().lower(),
                    data.get("phone", "").strip(),
                    data.get("message", "").strip(),
                ),
            )
            application = dict(
                db.execute("SELECT * FROM adoption_applications WHERE id = ?", (cursor.lastrowid,)).fetchone()
            )
        return jsonify({"application": application}), 201

    @app.get("/api/adoptions")
    def list_adoptions():
        with get_db() as db:
            rows = db.execute(
                """
                SELECT adoption_applications.*, animals.name AS animal_name
                FROM adoption_applications
                JOIN animals ON animals.id = adoption_applications.animal_id
                ORDER BY adoption_applications.id DESC
                """
            ).fetchall()
        return jsonify({"applications": [dict(row) for row in rows], "count": len(rows)})

    @app.patch("/api/adoptions/<int:application_id>")
    def update_adoption(application_id):
        data = request.get_json(silent=True) or {}
        status = data.get("status")
        if status not in ("pending", "approved", "rejected"):
            return jsonify({"error": "Statusi i aplikimit nuk është i vlefshëm."}), 400
        with get_db() as db:
            application = db.execute(
                "SELECT * FROM adoption_applications WHERE id = ?", (application_id,)
            ).fetchone()
            if not application:
                return jsonify({"error": "Aplikimi nuk u gjet."}), 404
            db.execute(
                "UPDATE adoption_applications SET status = ? WHERE id = ?", (status, application_id)
            )
            if status == "approved":
                db.execute(
                    "UPDATE animals SET status = 'adopted' WHERE id = ?", (application["animal_id"],)
                )
            updated = dict(
                db.execute(
                    "SELECT * FROM adoption_applications WHERE id = ?", (application_id,)
                ).fetchone()
            )
        return jsonify({"application": updated})

    @app.get("/api/tasks")
    def list_tasks():
        with get_db() as db:
            rows = db.execute(
                """
                SELECT care_tasks.*, animals.name AS animal_name
                FROM care_tasks LEFT JOIN animals ON animals.id = care_tasks.animal_id
                ORDER BY care_tasks.id
                """
            ).fetchall()
        return jsonify({"tasks": [dict(row) for row in rows], "count": len(rows)})

    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id):
        data = request.get_json(silent=True) or {}
        status = data.get("status")
        if status not in ("to_do", "in_progress", "done"):
            return jsonify({"error": "Statusi i detyrës nuk është i vlefshëm."}), 400
        with get_db() as db:
            task = db.execute("SELECT id FROM care_tasks WHERE id = ?", (task_id,)).fetchone()
            if not task:
                return jsonify({"error": "Detyra nuk u gjet."}), 404
            db.execute("UPDATE care_tasks SET status = ? WHERE id = ?", (status, task_id))
            updated = dict(db.execute("SELECT * FROM care_tasks WHERE id = ?", (task_id,)).fetchone())
        return jsonify({"task": updated})

    return app