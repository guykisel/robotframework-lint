from setuptools import setup

execfile('rflint/version.py')

setup(
    name             = 'robotframework-lint',
    version          = __version__,
    author           = 'Bryan Oakley',
    author_email     = 'bryan.oakley@gmail.com',
    url              = 'https://github.com/boakley/robotframework-lint/',
    keywords         = 'robotframework',
    license          = 'Apache License 2.0',
    description      = 'Static analysis tool for robotframework plain text files',
    long_description = open('README.md').read(),
    zip_safe         = False,
    include_package_data = True,
    install_requires = ['robotframework'],
    classifiers      = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
        ],
    packages         =[
        'rflint',
        'rflint.rules',
        'rflint.parser',
        ],
    scripts          =[], 
    entry_points={
        'console_scripts': [
            "rflint = rflint.__main__:main"
        ]
    }
)
