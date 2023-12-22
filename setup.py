from setuptools import setup

setup(
    name='dbseeker',
    version='0.7a0',
    install_requires=['mysql-connector-python', 'tabulate'],
    url='https://github.com/dueclic/dbseeker',
    license='MIT',
    author='dueclic',
    author_email='info@dueclic.com',
    description='A little but functional script that lets you search on every'
                ' database of a MySQL server for an input string.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
