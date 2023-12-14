# coding=utf-8
from keboola.component import CommonInterface
import os
import sys

class Transformation:
    def __init__(self, data_dir=None):
        self.dataDir = data_dir
        self.pipFile = os.environ.get('PIP_CONFIG_FILE', '/tmp/pip.conf')

    def execute(self):
        ci = CommonInterface(data_folder_path = self.dataDir)
        cfg = ci.configuration

        parameters = cfg.parameters

        # setup PIP repositories
        with open(self.pipFile, 'w') as file:
            file.write(self.create_pip_config(cfg.parameters, cfg.image_parameters))

        # install packages
        self.install_packages(parameters.get('packages', []))

        image_parameters = cfg.image_parameters
        try:
            artifactory_url = image_parameters['artifactory_url']
            trusted_host = image_parameters['trusted_host']
            self.install_packages(packages, artifactory_url=artifactory_url, trusted_host=trusted_host, cert='/code/artifacts/cair3.cer')
        except KeyError:
            print("Could not find artifactory url, using default pypi")
            self.install_packages(packages)

        blocks = parameters.get('blocks')
        if blocks is not None:
            # Process and execute transformation scripts
            script_file = self.dataDir + 'script.py'
            file = open(script_file, 'w+')
            self.process_blocks(blocks, file)
            file.seek(os.SEEK_SET)
            self.execute_script_file(ci, file)
            file.close()

    def process_blocks(self, blocks, file):
        for block in blocks:
            print('Processing block "%s"' % (block.get('name')))
            self.process_codes(block.get('codes'), file)

    def process_codes(self, codes, file):
        for code in codes:
            print('Processing code "%s"' % (code.get('name')))
            self.process_script(code.get('script'), file)

    def process_script(self, scripts, file):
        for script in scripts:
            print('Processing script "%s"' % (self.script_excerpt(script)))
            file.write(script)
            file.write('\n')

    def execute_script_file(self, ci, file):
        import traceback

        # Configure custom pip.conf
        os.environ['PIP_CONFIG_FILE'] = self.pipFile

        # Change current working directory so that relative paths work
        os.chdir(self.dataDir)
        sys.path.append(self.dataDir)

        try:
            with file as file:
                script = file.read()
            print('Execute script "%s"' % (self.script_excerpt(script)))
            exec(script, globals())
            print('Script finished')
        except Exception as err:
            _, _, tb = sys.exc_info()
            stack_len = len(traceback.extract_tb(tb)) - 1
            print(err, file=sys.stderr)
            traceback.print_exception(*sys.exc_info(), -stack_len,
                                      file=sys.stderr, chain=True)
            raise ValueError('Script failed.')

    @staticmethod
    def script_excerpt(script):
        if len(script) > 1000:
            return script[0 : 500] + '\n...\n' + script[-500]
        else:
            return script

    @staticmethod
    def install_packages(packages):
        import subprocess
        import sys
        for package in packages:
            args = [
                os.environ['VIRTUAL_ENV'] + '/bin/python',
                '-m', 'pip', 'install',
                '--disable-pip-version-check',
                '--no-cache-dir',
                '--no-warn-script-location', # ignore error: installed in '/var/www/.local/bin' which is not on PATH.
                '--force-reinstall',
                package
            ]
            if subprocess.call(args, stderr=sys.stdout.buffer) != 0:
                raise ValueError('Failed to install package: ' + package)

    @staticmethod
    def script_excerpt(script):
        if len(script) > 1000:
            return script[0 : 500] + '\n...\n' + script[-500]
        else:
            return script

    @staticmethod
    def create_pip_config(parameters, image_parameters):
        from urllib.parse import urlparse, urlunparse

        repositories = [
            *parameters.get('pip_repositories', []),
            *image_parameters.get('pip_repositories', []),
        ]

        index_url = None
        extra_index_urls = []
        trusted_hosts = []

        for repository in repositories:
            parsed_url = urlparse(repository['url'])

            if repository.get('add_trusted_host', False):
                trusted_hosts.append(parsed_url.netloc)

            repo_credentials = repository.get('#credentials')
            if repo_credentials:
                url_with_credentials = repo_credentials + '@' + parsed_url.hostname
                if parsed_url.port:
                    url_with_credentials += ':' + str(parsed_url.port)

                parsed_url = parsed_url._replace(netloc=url_with_credentials)

            if index_url == None:
                index_url = urlunparse(parsed_url)
            else:
                extra_index_urls.append(urlunparse(parsed_url))

        pip_conf_lines = [
            '[global]'
        ]

        if index_url != None:
            pip_conf_lines.append('index-url = ' + index_url)

        if len(extra_index_urls) > 0:
            pip_conf_lines.append('extra-index-url = ' + ' '.join(extra_index_urls))

        if len(trusted_hosts) > 0:
            pip_conf_lines.append('trusted-host = ' + ' '.join(trusted_hosts))

        return "\n".join(pip_conf_lines) + "\n"
