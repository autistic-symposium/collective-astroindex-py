from setuptools import setup, find_packages

setup(
    name="astro",
    version='0.1',
    packages=find_packages(include=['src', \
                    'src.astro', \
                    'src.utils']),
    author="bt3gl",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['astro=src.main:run']
    },
)