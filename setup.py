# Third Party
from setuptools import setup

setup(
    name='python-documentcloud2',
    version='2.0.0',
    description='A simple Python wrapper for the DocumentCloud API',
    author='Mitchell Kotler',
    author_email='mitch@muckrock.com',
    url='https://github.com/muckrock/python-documentcloud',
    license="MIT",
    packages=("documentcloud",),
    include_package_data=True,
    install_requires=(
        'future',
        'listcrunch>=1.0.1',
        'python-dateutil',
        'ratelimit',
        'requests',
        'urllib3',
    ),
    extras_require={
        'dev': [
            'black',
            'coverage',
            'isort',
            'pylint',
            'sphinx',
            'twine',
        ],
        'test': [
            'pytest',
            'pytest-mock',
            'pytest-recording',
            'vcrpy',
        ],
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    )
)
