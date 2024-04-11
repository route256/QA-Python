from setuptools import setup, find_packages, Command
from yandextank.version import VERSION
import os
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install


class RunProtoBuildBefore:
    def run(self):
        self.run_command("build_package_protos")
        return super().run()


class CustomDevelop(RunProtoBuildBefore, develop):
    ...


class CustomInstall(RunProtoBuildBefore, install):
    ...


class CustomBuild(RunProtoBuildBefore, build_py):
    ...


class build_package_protos(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from grpc.tools import command
        command.build_package_protos(
            os.path.join(self.distribution.package_dir[''], 'yandextank', 'plugins', 'DataUploader', 'proto'))


setup(
    cmdclass={
        'build_package_protos': build_package_protos,
        'build_py': CustomBuild,
        'develop': CustomDevelop,
        'install': CustomInstall
    },
    package_dir={"": "."},
    name='yandextank',
    version=VERSION,
    description='a performance measurement tool',
    longer_description='''
Yandex.Tank is a performance measurement and load testing automatization tool.
It uses other load generators such as JMeter, ab or phantom inside of it for
load generation and provides a common configuration system for them and
analytic tools for the results they produce.
''',
    python_requires='==3.*',
    maintainer='Yandex Load Team',
    maintainer_email='load@yandex-team.ru',
    url='http://yandex.github.io/yandex-tank/',
    namespace_packages=["yandextank", "yandextank.plugins"],
    packages=find_packages(exclude=["tests", "tmp", "docs", "data"]),
    install_requires=[
        'cryptography>=2.2.1', 'pyopenssl>=19.0.0',
        'psutil>=1.2.1', 'requests>=2.5.1', 'paramiko>=1.16.0',
        'pandas<=1.2.5', 'numpy<=1.19.5',
        'pip>=8.1.2',
        'pyyaml>=4.2b1', 'cerberus==1.3.1', 'influxdb>=5.0.0', 'netort>=0.8.0',
        'retrying>=1.3.3', 'pytest-runner', 'typing', 'grpcio', 'grpcio-tools'
    ],
    setup_requires=[
        'grpcio-tools'
    ],
    tests_require=[
        'pytest==4.6.3', 'flake8', 'pytest-benchmark', 'zipp==0.5.1', 'mock'
    ],
    license='LGPLv2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'yandex-tank = yandextank.core.cli:main',
            'yandex-tank-check-ssh = yandextank.common.util:check_ssh_connection',
            'tank-postloader = yandextank.plugins.DataUploader.cli:post_loader',
            'tank-docs-gen = yandextank.validator.docs_gen:main'
        ],
    },
    package_data={
        'yandextank.api': ['config/*'],
        'yandextank.core': ['config/*'],
        'yandextank.aggregator': ['config/*'],
        'yandextank.plugins.Android': ['binary/*', 'config/*'],
        'yandextank.plugins.Autostop': ['config/*'],
        'yandextank.plugins.Bfg': ['config/*'],
        'yandextank.plugins.CloudUploader': ['config/*'],
        'yandextank.plugins.Console': ['config/*'],
        'yandextank.plugins.DataUploader': ['config/*', 'proto/*'],
        'yandextank.plugins.InfluxUploader': ['config/*'],
        'yandextank.plugins.OpenTSDBUploader': ['config/*'],
        'yandextank.plugins.JMeter': ['config/*'],
        'yandextank.plugins.JsonReport': ['config/*'],
        'yandextank.plugins.Pandora': ['config/*'],
        'yandextank.plugins.Phantom': ['config/*'],
        'yandextank.plugins.RCAssert': ['config/*'],
        'yandextank.plugins.ResourceCheck': ['config/*'],
        'yandextank.plugins.ShellExec': ['config/*'],
        'yandextank.plugins.ShootExec': ['config/*'],
        'yandextank.plugins.Telegraf': ['config/*', 'agent/*'],
        'yandextank.plugins.NeUploader': ['config/*']
    },
    use_2to3=False, )
