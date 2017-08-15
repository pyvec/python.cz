from setuptools import setup


setup(
    name='pythoncz',
    packages=['pythoncz'],
    include_package_data=True,
    install_requires=[
        'flask==0.12',
        'flake8==3.2.1',
        'pytest==3.0.6',
        'requests==2.18.3',
        'czech-sort==0.4',
        'pyyaml==3.12',
        'python-slugify==1.2.1',
        'responses==0.7.0',
    ],
)
