from setuptools import setup, find_packages

setup(
    name='learn-async',
    version='1.0',
    packages=find_packages(),
    install_requires=['chardet >= 2.3.0', 'cython >= 0.22', 'aiohttp >= 0.14.4', 'requests >= 2.6.0', 'XUDD >= 0.1.0'],
    url='',
    license='',
    author='Naresh Khalasi',
    author_email='khalasi@gmail.com',
    description='Learning Async concepts in Python'
)
