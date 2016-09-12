import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'waitress',
    'psycopg2',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'passlib'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    'tox'
    ]

setup(name='learning_journal',
      version='0.0',
      description='learning_journal',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = learning_journal:main
      [console_scripts]
      init_db = learning_journal.scripts.initializedb:main
      """,
      )
