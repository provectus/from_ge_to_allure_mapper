import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='from_ge_to_allure_mapper',
    version='0.0.1',
    author='Bogdan Volodarskiy',
    author_email='hesherus@gmail.com',
    description='Package for mapping test report format from Great Expectations to Allure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/provectus/from_ge_to_allure_mapper',
    download_url='https://github.com/provectus/from_ge_to_allure_mapper/archive/tags/publish.tar.gz',
    keywords=['DATA_QA', 'GREAT_EXPECTATIONS', 'ALLURE'],
    license='MIT',
    packages=['from_ge_to_allure_mapper'],
    install_requires=['great_expectations'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)