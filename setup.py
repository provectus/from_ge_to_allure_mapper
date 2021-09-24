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
    license='MIT',
    packages=['from_ge_to_allure_mapper'],
    install_requires=['great_expectations'],
)