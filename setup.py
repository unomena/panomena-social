from setuptools import setup, find_packages

setup(
    name='panomena-social',
    description='Panomena Social',
    version='0.0.4',
    author='',
    license='Proprietory',
    url='http://www.unomena.com/',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    dependency_links = [
        'http://github.com/unomena/panomena-general/tarball/master#egg=panomena-general',
        'http://github.com/unomena/panomena-accounts/tarball/master#egg=panomena-accounts',
    ],
    install_requires = [
        'Django',
        'panomena-general==0.0.3',
        'panomena-accounts==0.0.5',
    ],
)
