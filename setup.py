from setuptools import setup, find_packages

setup(
    name="choices",
    version='0.1',
    packages=find_packages(include=['src', \
                    'src.analytics', \
                    'src.utils']),
    author="bt3gl",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['choices=src.main:run']
    },
)