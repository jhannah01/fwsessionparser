from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '1.0'

install_requires = [
    "SQLAlchemy>=0.8.2",
    "setuptools>=0.7",
    "collective.recipe.sphinxbuilder"
]


setup(name='fwsessionparser',
    version=version,
    description="A tool to parse SSG 'get session' output",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Jon Hannah',
    author_email='jon.hannah01@gmail.com',
    url='',
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['fwsessionparser=fwsessionparser:main']
    }
)
