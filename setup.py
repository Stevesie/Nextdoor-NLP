#!/usr/bin/env python

from setuptools import setup

def set_up():
    setup(
        name='nextdoor_nlp',
        description='Analyze Nextdoor textual data via the Stevesie API',
        author='Steve Spagnola',
        author_email='steve@stevesie.com',
        install_requires=[
            'requests>=2.5.1',
            'nltk>=3.2.5'
        ])

if __name__ == '__main__':
    set_up()
