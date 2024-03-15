from kbc_transformation.transformation import Transformation
import unittest

class PipConfigTest(unittest.TestCase):
    def test_no_repositories(self):
        result = Transformation.create_pip_config({}, {})

        self.assertEqual((
            "[global]\n"
        ), result)

    def test_single_repository(self):
        result = Transformation.create_pip_config({}, {
            'pip_repositories': [
                {'url': 'http://example.com'},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = http://example.com\n"
        ), result)

    def test_multiple_repositories(self):
        result = Transformation.create_pip_config({}, {
            'pip_repositories': [
                {'url': 'http://example.com'},
                {'url': 'https://keboola.com'},
                {'url': 'https://other-example.com:4043'},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = http://example.com\n"
            "extra-index-url = https://keboola.com https://other-example.com:4043\n"
        ), result)

    def test_trusted_repository(self):
        result = Transformation.create_pip_config({}, {
            'pip_repositories': [
                {'url': 'http://example.com', 'add_trusted_host': True},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = http://example.com\n"
            "trusted-host = example.com\n"
        ), result)

    def test_multiple_trusted_repositories(self):
        result = Transformation.create_pip_config({}, {
            'pip_repositories': [
                {'url': 'http://example.com', 'add_trusted_host': True},
                {'url': 'https://keboola.com:4043', 'add_trusted_host': True},
                {'url': 'https://other-example.com'},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = http://example.com\n"
            "extra-index-url = https://keboola.com:4043 https://other-example.com\n"
            "trusted-host = example.com keboola.com:4043\n"
        ), result)

    def test_repositories_with_credentials(self):
        result = Transformation.create_pip_config({}, {
            'pip_repositories': [
                {'url': 'https://example.com:8080/some/path?param=1#here', 'add_trusted_host': True, '#credentials': 'user:pass'},
                {'url': 'https://other.com:21443/some/path?param=1#here', 'add_trusted_host': True, '#credentials': 'user:pass'},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = https://user:pass@example.com:8080/some/path?param=1#here\n"
            "extra-index-url = https://user:pass@other.com:21443/some/path?param=1#here\n"
            "trusted-host = example.com:8080 other.com:21443\n"
        ), result)

    def test_repositories_in_parameters(self):
        result = Transformation.create_pip_config({
             'pip_repositories': [
                {'url': 'https://example.com:8080/simple'},
                {'url': 'https://other.com/simple'},
             ]
        }, {
            'pip_repositories': [
                {'url': 'https://other.example.com:21443/'},
            ]
        })

        self.assertEqual((
            "[global]\n"
            "index-url = https://example.com:8080/simple\n"
            "extra-index-url = https://other.com/simple https://other.example.com:21443/\n"
        ), result)
