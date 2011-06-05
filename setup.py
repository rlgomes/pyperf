from distutils.core import setup

setup (
    name='PyPerf',
    version='0.1.0',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    py_modules = ['src/pyperf','src/tableprinter'],
    url='',
    license='Apache 2.0 License',
    description='',
    long_description=open('README').read(),
)