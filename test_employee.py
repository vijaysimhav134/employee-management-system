
import unittest
import tempfile
import os

import database


class TestEmployeeManagement(unittest.TestCase):

    def setUp(self):
        # Save the original database path
        self.original_db_name = database.DB_NAME

        # Create a temporary database for this test
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()

        database.DB_NAME = self.temp_db.name

        database.initialize_database()

    def tearDown(self):
        # Restore the original database path
        database.DB_NAME = self.original_db_name

        # Remove the temporary database
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_add_employee(self):
        result = database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        self.assertTrue(result)

    def test_add_multiple_employees(self):
        database.add_employee(
            "Rahul Sharma", "rahul@gmail.com", "Engineering", 35000
        )

        database.add_employee(
            "Arjun Kumar", "arjun@gmail.com", "Testing", 40000
        )

        employees = database.view_employees()

        self.assertEqual(len(employees), 2)

    def test_duplicate_email(self):
        database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        result = database.add_employee(
            "Arjun Kumar",
            "rahul@gmail.com",
            "Testing",
            40000
        )

        self.assertFalse(result)

    def test_view_employees(self):
        database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        employees = database.view_employees()

        self.assertEqual(len(employees), 1)

    def test_search_employee(self):
        database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        employee = database.search_employee(1)

        self.assertIsNotNone(employee)
        self.assertEqual(employee["name"], "Rahul Sharma")

    def test_search_missing_employee(self):
        employee = database.search_employee(99)

        self.assertIsNone(employee)

    def test_update_employee(self):
        database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        result = database.update_employee(
            1,
            "Rahul Sharma",
            "rahul@gmail.com",
            "Software Development",
            45000
        )

        self.assertTrue(result)

        employee = database.search_employee(1)

        self.assertEqual(
            employee["department"],
            "Software Development"
        )
        self.assertEqual(employee["salary"], 45000)

    def test_update_with_duplicate_email(self):
        database.add_employee(
            "Rahul Sharma", "rahul@gmail.com", "Engineering", 35000
        )

        database.add_employee(
            "Arjun Kumar", "arjun@gmail.com", "Testing", 40000
        )

        result = database.update_employee(
            1,
            "Rahul Sharma",
            "arjun@gmail.com",
            "Engineering",
            35000
        )

        self.assertFalse(result)

    def test_update_missing_employee(self):
        result = database.update_employee(
            99,
            "Unknown",
            "unknown@gmail.com",
            "Testing",
            30000
        )

        self.assertFalse(result)

    def test_delete_employee(self):
        database.add_employee(
            "Rahul Sharma",
            "rahul@gmail.com",
            "Engineering",
            35000
        )

        result = database.delete_employee(1)

        self.assertTrue(result)

        employee = database.search_employee(1)

        self.assertIsNone(employee)

    def test_delete_missing_employee(self):
        result = database.delete_employee(99)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
