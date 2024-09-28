import unittest
from datetime import datetime
from app import count_completed_trainings,completed_trainings_in_fiscal_year,find_expiring_or_expired_trainings
import os

class TestTrainingApp(unittest.TestCase):

    def setUp(self):
        # Mock data to use in the tests
        self.data = [
            {
                "name": "John Doe",
                "completions": [
                    {"name": "Electrical Safety for Labs", "timestamp": "08/31/2022", "expires": None},
                    {"name": "X-Ray Safety", "timestamp": "09/01/2023", "expires": None},
                    {"name": "Laboratory Safety Training", "timestamp": "07/05/2023", "expires": None}
                ]
            },
            {
                "name": "Jane Doe",
                "completions": [
                    {"name": "X-Ray Safety", "timestamp": "06/01/2023", "expires": "06/01/2024"},
                    {"name": "Laboratory Safety Training", "timestamp": "05/05/2022", "expires": None}
                ]
            },
            {
                "name": "Jim Beam",
                "completions": [
                    {"name": "Electrical Safety for Labs", "timestamp": "05/02/2022", "expires": None},
                    {"name": "X-Ray Safety", "timestamp": "11/02/2022", "expires": "11/02/2023"}
                ]
            }
        ]

    def test_if_app_exists_in_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'app.py')
        # print(file_path)
        self.assertTrue(os.path.isfile(file_path), "app.py does not exist in the current directory")
    
    def test_if_training_exists_in_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'training.txt')
        # print(file_path)
        self.assertTrue(os.path.isfile(file_path), "Training.py does not exist in the current directory")

    def test_count_completed_trainings(self):
        result = count_completed_trainings(self.data)
        expected = {
            "Electrical Safety for Labs": 2,
            "X-Ray Safety": 3,
            "Laboratory Safety Training": 2
        }
        self.assertEqual(result, expected)

    def test_completed_trainings_in_fiscal_year(self):
        trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
        fiscal_year = 2024
        result = completed_trainings_in_fiscal_year(self.data, trainings, fiscal_year)
        expected = {
            "X-Ray Safety": ["John Doe"],
            "Laboratory Safety Training": ["John Doe"]
        }
        self.assertEqual(result, expected)

    def test_find_expiring_or_expired_trainings(self):
        check_date = "10/10/2023"
        result = find_expiring_or_expired_trainings(self.data, check_date)
        expected = {
            "Jim Beam": [
                {"expires": "11/02/2023","status": "expires soon","training": "X-Ray Safety"}
            ]
        }
        # print("this is result->",result)
        self.assertEqual(result, expected)

    def test_find_expired_trainings(self):
        check_date = "12/01/2023"
        result = find_expiring_or_expired_trainings(self.data, check_date)
        expected = {
            "Jim Beam": [
                {"training": "X-Ray Safety", "expires": "11/02/2023", "status": "expired"}
            ]
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
