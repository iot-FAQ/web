import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(name='l_met',
      version=0.1,
      description='Meter data collection project',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services file upload metering",
      author='Fantastic Four + 1',
      author_email='roman.pavlyuk@gmail.com',
      url='http://iot.lviv.ua',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['pyramid', 'waitress', 'pyramid_chameleon' ],
      entry_points="""\
      [paste.app_factory]
      main=l_met:main
      """,
      paster_plugins=['pyramid'])
