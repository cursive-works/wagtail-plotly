import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Package dependencies
install_requires = [
    "plotly>=4.14.3",
    "wagtail>=2.13",
    "wagtail-json-widget>=0.0.1",
]

setup(
    name='wagtail_plotly',
    version=__import__('wagtail_plotly').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Plotly for Wagtail CMS',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/cursive-works/wagtail-plotly',
    author='Martin Swarbrick',
    author_email='martin.swarbrick@cursive.works',
    keywords=['WAGTAIL', 'PLOTLY', 'STREAMFIELD', 'WAGTAIL_PLOTLY', 'WAGTAIL CMS'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
    ],
    install_requires=install_requires,
)
