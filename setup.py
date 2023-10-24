from setuptools import setup, find_packages

setup(
    name="astro1",
    version='0.1',
    packages=find_packages(include=['src', \
                    'src.intel', \
                    'src.datalake', \
                    'src.utils']),
    author="bt3gl",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['astro1=src.main:run']
    },
)