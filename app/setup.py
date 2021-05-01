from setuptools import setup

setup(
    name='oracles',
    version='0.1.2',
    py_modules=['oracles'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        oracles=oracles:main
    ''',
)
