import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='from_ge_to_allure_mapper',
    version='0.0.1.6',
    author='Bogdan Volodarskiy',
    author_email='hesherus@gmail.com',
    description='Package for mapping test report format from Great Expectations to Allure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/provectus/from_ge_to_allure_mapper',
    download_url='https://github.com/provectus/from_ge_to_allure_mapper/archive/refs/tags/v_01.6.tar.gz',
    keywords=['DATA_QA', 'GREAT_EXPECTATIONS', 'ALLURE'],
    license='MIT',
    data_files=[('../', ['from_ge_to_allure_mapper/config.json'])],
    packages=['from_ge_to_allure_mapper'],
    install_requires=(
        'great_expectations >= 0.13.37',
        'fastparquet >= 0.7.1',
        'pyarrow >= 5.0.0'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)