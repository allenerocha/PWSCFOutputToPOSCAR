from setuptools import find_packages, setup
# Required dependencies

with open('README.md') as readme_file:
    readme = readme_file.read()

required = [
    # Please keep alphabetized
    're',
    'sys'
]

setup(
    name='PWSCFOutputToPOSCAR',
    version='3.1',
    description="Convert *.out data from QUANTUM ESPRESSO to POSCAR file.",
    long_description=readme,
    author="Allen Rocha",
    author_email='allenerocha@pm.me',
    url='https://github.com/allenerocha/PWSCFOutputToPOSCAR',
    packages={'PWSCFOutputToPOSCAR.PWSCFOutputToPOSCAR': 'PWSCFOutputToPOSCAR'},
    include_package_data=True,
    install_requires=required,
    setup_requires=[
        'setuptools_scm >= 1.7.0'
    ],
    test_suite='tests',
    tests_require='unittest'
)
