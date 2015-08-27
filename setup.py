
"""
A setuptools based setup module.
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
 Always prefer setuptools over distutils
"""

from setuptools import setup, find_packages

setup(
    name='city_search_app',
    version='0.0.1',
    description='A uwsgi city search api',
    url='https://github.com/haldous2/city-search-app',
    author='Eric Westman',
    author_email='haldous2@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='uwsgi ajax autocomplete',
    packages=find_packages(exclude=['docs','extras',]),
    #install_requires=['mysql-python'],
    # pip install -e .['dev','test]
    extras_require={
        'dev': ['mock>=1.3.0','nose>=1.3.7','webtest>=2.0.18'],
        'test': ['mock>=1.3.0','nose>=1.3.7','webtest>=2.0.18'],
    },
)