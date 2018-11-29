from setuptools import setup


install_requires = [
    'elsa==0.1.5',
    'flask==1.0.2',
    'frozen-Flask==0.15',
    'requests==2.20.1',
    'czech-sort==0.4',
    'pyyaml==3.13',
    'python-slugify==1.2.5',
    'ics==0.4',
    'arrow==0.4.2',
    'lxml==4.2.5',
    'cssselect==1.0.3',
]
tests_require = [
    'coveralls==1.4.0',
    'flake8==3.5.0',
    'pytest==3.7.2',
    'responses==0.9.0',
    'pytest-runner==4.2',
    'pytest-cov==2.5.1',
    'pytest-flake8==1.0.2',
]


setup(
    name='pythoncz',
    packages=['pythoncz'],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
)
