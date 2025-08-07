# =============================================================================
# File 13: setup.py (Optional - per installazione)
# =============================================================================

#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Leggi README per long description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Leggi requirements
def read_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='streamblur-pro',
    version='4.0.0',
    author='StreamBlur Pro Team',
    author_email='info@streamblurpro.com',
    description='AI-powered virtual camera with real-time background blur',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/streamblur-pro/streamblur-pro',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Video',
        'Topic :: Communications :: Video Conferencing',
    ],
    python_requires='>=3.9',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'streamblur-pro=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'streamblur_pro': ['assets/*', 'config/*'],
    },
)
