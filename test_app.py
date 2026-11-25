import os
import tempfile
import unittest

from app import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.database = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        os.unlink(self.database)
        self.app = create_app({"DATABASE": self.database})
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.exists(self.database):
            os.unlink(self.database)

    def test_health_and_home(self):
        self.assertEqual(self.client.get("/health").get_json()["status"], "ok")
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_create_and_filter_animals(self):
        response = self.client.post("/api/animals", json={
            "name": "Luna",
            "species": "mace",
            "breed": "Evropiane",
            "age_months": 8,
            "gender": "femer",
            "description": "Miqësore",
            "health_status": "Shëndetplotë",
            "intake_date": "2026-11-10",
            "status": "available",
        })
        self.assertEqual(response.status_code, 201)
        found = self.client.get("/api/animals?search=luna").get_json()
        self.assertEqual(found["count"], 1)

    def test_animal_validation(self):
        response = self.client.post("/api/animals", json={"name": "Test"})
        self.assertEqual(response.status_code, 400)

    def test_adoption_flow(self):
        created = self.client.post("/api/adoptions", json={
            "animal_id": 1,
            "applicant_name": "Anila Test",
            "email": "anila@example.test",
            "phone": "+383 44 000 000",
            "message": "Dua të adoptova Belën.",
        })
        self.assertEqual(created.status_code, 201)
        application_id = created.get_json()["application"]["id"]

        approved = self.client.patch(
            f"/api/adoptions/{application_id}",
            json={"status": "approved"},
        )
        self.assertEqual(approved.status_code, 200)
        animal = self.client.get("/api/animals").get_json()["animals"][0]
        self.assertEqual(animal["status"], "adopted")

    def test_task_status_update(self):
        response = self.client.patch("/api/tasks/1", json={"status": "in_progress"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["task"]["status"], "in_progress")


if __name__ == "__main__":
    unittest.main()
