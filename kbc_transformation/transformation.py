# coding=utf-8
from keboola import docker
import os
import sys

class Transformation:
    def __init__(self, data_dir=None):
        self.dataDir = data_dir

    def execute(self):
        cfg = docker.Config(self.dataDir)
        parameters = cfg.get_parameters()

        # install packages
        packages = parameters.get('packages')
        if packages is None:
            packages = []

        self.install_packages(packages)

        # prepare tagged files
        tags = parameters.get('tags')
        if tags is None:
            tags = []
        self.prepare_tagged_files(cfg, tags)

        blocks = parameters.get('blocks')
        if blocks is not None:
            # Process and execute transformation scripts
            script_file = cfg.get_data_dir() + 'script.py'
            file = open(script_file, 'w+')
            self.process_blocks(blocks, file)
            file.seek(os.SEEK_SET)
            self.execute_script_file(cfg, file)
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

    def execute_script_file(self, cfg, file):
        import traceback

        # Change current working directory so that relative paths work
        os.chdir(cfg.get_data_dir())
        sys.path.append(cfg.get_data_dir())

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
    def prepare_tagged_files(cfg, tags):
        """
        When supplied a list of tags, select input files with the given tags and prepare the
        most recent file of those into a /user/ folder
        Args:
            cfg: keboola.docker.Config object
            tags: List of tag names.
        """
        from datetime import datetime, timezone
        from shutil import copyfile

        if not os.path.exists(os.path.join(cfg.get_data_dir(), 'in', 'user')):
            os.makedirs(os.path.join(cfg.get_data_dir(), 'in', 'user'))

        for tag in tags:
            last_time = datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc)
            last_manifest = ''
            for file in cfg.get_input_files():
                manifest = cfg.get_file_manifest(file)
                if tag in manifest['tags']:
                    file_time = datetime.strptime(manifest['created'],
                                                  '%Y-%m-%dT%H:%M:%S%z')
                    if file_time > last_time:
                        last_time = file_time
                        last_manifest = file
            if last_manifest == '':
                raise ValueError("No files were found for tag: " + tag)
            else:
                copyfile(last_manifest,
                         os.path.join(cfg.get_data_dir(), 'in', 'user', tag))
                copyfile(last_manifest + '.manifest',
                         os.path.join(cfg.get_data_dir(), 'in', 'user',
                                      tag + '.manifest'))
