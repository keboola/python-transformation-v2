from kbc_transformation.transformation import Transformation
import unittest
import os
import shutil
import csv

class TransformationTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Container is in the production runned with "www-data" user,
        # so we want to test it in the same way.
        # Code directory is not writtable for "www-data" user, so we use /tmp dir.
        tests_dir = '/code/tests'
        tmp_dir = '/tmp/tests'
        if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)
        shutil.copytree(tests_dir, tmp_dir)
        self.data_dir = tmp_dir

    def test_long_script_text(self):
        data_dir = self.data_dir + '/longScript/'
        result_file = os.path.abspath(data_dir + '/out/tables/sample.csv')
        app = Transformation(data_dir)
        app.execute()

        self.assertTrue(os.path.isfile(result_file))
        with open(result_file, 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.assertEqual(int(row['biggerFunky']),
                                 (int(row['funkyNumber']) ** 3))


    def test_emptyConfig(self):
        data_dir = self.data_dir + '/emptyConfig/'
        app = Transformation(data_dir)
        app.execute()

    def test_transformData(self):
        data_dir = self.data_dir + '/transformData/'
        result_file = os.path.abspath(data_dir + '/out/tables/sample.csv')
        app = Transformation(data_dir)
        app.execute()

        self.assertTrue(os.path.isfile(result_file))
        with open(result_file, 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.assertEqual(int(row['biggerFunky']),
                                 (int(row['funkyNumber']) ** 3))

    def test_package(self):
        data_dir = self.data_dir + '/package/'
        result_file = os.path.abspath(data_dir + '/out/files/out.txt')
        app = Transformation(data_dir)
        app.execute()
        with open(result_file, 'rt') as file:
            # Cup of coffee, result of the "art" package
            self.assertEqual('c[_]', file.read().strip())

    def test_tagged_files(self,):
        data_dir = self.data_dir + '/taggedFiles/'
        # generate absolute path before the application is run, because it
        # may alter current working directory
        result_dir = os.path.abspath(data_dir)

        app = Transformation(data_dir)
        app.execute()

        self.assertTrue(os.path.isfile(result_dir + '/in/user/pokus'))
        self.assertTrue(os.path.isfile(result_dir + '/in/user/model'))
        self.assertTrue(os.path.isfile(result_dir + '/out/tables/sample.csv'))
        with open(result_dir + '/out/tables/sample.csv', 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.assertEqual(int(row['x']), 5)

    def test_package_error(self):
        data_dir = self.data_dir + '/failedInstallPackages/'
        app = Transformation(data_dir)
        with self.assertRaisesRegex(ValueError, "Failed to install package: "
                                                "some-non-existent-package"):
            app.execute()

    def test_script_syntax_error(self):
        data_dir = self.data_dir + '/scriptSyntaxError/'
        app = Transformation(data_dir)
        with self.assertRaisesRegex(ValueError, "Script failed."):
            app.execute()

    def test_current_working_dir(self, ):
        data_dir = self.data_dir + '/currentWorkingDirectory/'
        # generate absolute path before the application is run, because it
        # may alter current working directory
        result_dir = os.path.abspath(data_dir)

        app = Transformation(data_dir)
        app.execute()

        self.assertTrue(os.path.isfile(result_dir + '/hello.txt'))
        with open(result_dir + '/hello.txt', 'rt') as sample:
            self.assertEqual('I was imported\n', sample.read())

    def test_pip_repositories(self):
        data_dir = self.data_dir + '/pipRepositories/'
        result_file = os.path.abspath(data_dir + '/out/files/out.txt')
        app = Transformation(data_dir)
        app.execute()
        with open(result_file, 'rt') as file:
            # Cup of coffee, result of the "art" package
            self.assertEqual('c[_]', file.read().strip())

    def test_pip_repositories_error(self):
        data_dir = self.data_dir + '/pipRepositoriesError/'
        result_file = os.path.abspath(data_dir + '/out/files/out.txt')
        app = Transformation(data_dir)

        with self.assertRaisesRegex(ValueError, "Failed to install package: matrix"):
            app.execute()
