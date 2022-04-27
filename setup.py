import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prettier",
    description='Properly pprint of nested objects',
    author_email='yytrofimov@gmail.com',
    url='https://github.com/yytrofimov/Prettier',
    version="0.0.7",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license_files=('LICENSE.txt',),
    py_modules=["prettier"],
    package_dir={'': 'src/'},
)
