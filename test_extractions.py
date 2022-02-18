import os

import unittest

from extractions import (
    extract_backend_dependency_install,
    extract_frontend_build_output,
    extract_eslint_output,
    extract_django_unittests_output,
)


BASE_DIR = os.getcwd()


class ExtractionMethodsTests(unittest.TestCase):
    def setUp(self):
        dep_output_file_path = os.path.join(
            BASE_DIR, ".configs", "dependency_output.txt"
        )
        self.dep_text_output = ""
        with open(dep_output_file_path, "r") as file:
            self.dep_text_output += file.read()

        output_file_path = os.path.join(BASE_DIR, ".configs", "output.txt")
        self.text_output = ""
        with open(output_file_path, "r") as file:
            self.text_output += file.read()

    def test_extract_backend_dependency_install_new_install(self):
        output = extract_backend_dependency_install(self.dep_text_output.split("\n"))
        self.assertTrue(output[0].startswith("Collecting stone-grading@"))
        self.assertTrue(output[-1].startswith("Successfully installed"))
        self.assertEqual(len(output), 80)

    def test_extract_backend_dependency_install_no_new_install(self):
        output = extract_backend_dependency_install(self.text_output.split("\n"))
        self.assertTrue(output[0].startswith("Collecting stone-grading@"))
        self.assertTrue(output[-1].startswith("Requirement already satisfied: "))
        self.assertEqual(len(output), 75)

    def test_extract_frontend_build_output(self):
        output = extract_frontend_build_output(self.text_output.split("\n"))
        self.assertTrue(output[0].startswith("> gradia@0.1.0 build"))
        self.assertTrue(output[-1].startswith("  bit.ly/CRA-deploy"))
        self.assertEqual(len(output), 69)

    def test_extract_django_unittests_output(self):
        output = extract_django_unittests_output(self.text_output.split("\n"))
        self.assertTrue(
            output[0].startswith("============================= test session")
        )
        self.assertTrue(output[-1].startswith("============= 18 failed, 176 passed,"))
        self.assertEqual(len(output), 606)

    # def test_extract_eslint_output(self):
    #     output = extract_eslint_output(self.text_output.split("\n"))
