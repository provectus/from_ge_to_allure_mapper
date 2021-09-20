#!/usr/bin/env python
# coding: utf-8

# # Edit Your Expectation Suite
# Use this notebook to recreate and modify your expectation suite:
#
# **Expectation Suite Name**: `test_suite`
#
# We'd love it if you **reach out to us on** the [**Great Expectations Slack Channel**](https://greatexpectations.io/slack)

# In[ ]:
from great_expectations import DataContext
from datetime import datetime
import great_expectations as ge
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def validate_data():
    context = DataContext(os.path.join(BASE_DIR, 'great_expectations'))
    print(BASE_DIR)
    print(context)

    # Feel free to change the name of your suite here. Renaming this will not
    # remove the other one.
    expectation_suite_name = "test_suite"
    suite = context.get_expectation_suite(expectation_suite_name)
    suite.expectations = []

    batch_kwargs = {'data_asset_name': 'titanic_pivot', 'datasource': 'PandasDatasource',
                    'path': os.path.join(BASE_DIR, 'data/titanic_pivot.parquet')}
    batch = context.get_batch(batch_kwargs, suite)
    batch.head()

    # ## Create & Edit Expectations
    #
    # Add expectations by calling specific expectation methods on the `batch` object. They all begin with `.expect_` which makes autocompleting easy using tab.
    #
    # You can see all the available expectations in the **[expectation glossary](https://docs.greatexpectations.io/en/latest/reference/glossary_of_expectations.html?utm_source=notebook&utm_medium=create_expectations)**.

    # ### Table Expectation(s)

    # In[ ]:

    batch.expect_table_row_count_to_be_between(max_value=975, min_value=798, meta={
                                               "Jira Ticket": "https://github.com/allure-framework/allure-docs/issues/21", "Severity": "trivial"})

    # In[ ]:

    batch.expect_table_column_count_to_equal(value=8)

    # In[ ]:

    batch.expect_table_columns_to_match_ordered_list(column_list=[
                                                     'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'Siblings/Spouses Aboard', 'Parents/Children Aboard', 'Fare'])

    # ### Column Expectation(s)

    # #### `Survived`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Survived')

    # In[ ]:

    batch.expect_column_distinct_values_to_be_in_set(
        column='Survived', value_set=[0, 1])

    # #### `Age`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Age')

    # In[ ]:

    batch.expect_column_min_to_be_between(
        column='Age', max_value=4.0, min_value=1.0)

    # In[ ]:

    batch.expect_column_max_to_be_between(
        column='Age', max_value=81.0, min_value=79.0)

    # In[ ]:

    batch.expect_column_mean_to_be_between(
        column='Age', max_value=30.471443066516347, min_value=28.471443066516347)

    # In[ ]:

    batch.expect_column_median_to_be_between(
        column='Age', max_value=29.0, min_value=27.0)

    # #### `Name`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Name')

    # In[ ]:

    batch.expect_column_value_lengths_to_be_between(column='Name', min_value=1)

    # #### `Pclass`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Pclass')

    # In[ ]:

    batch.expect_column_distinct_values_to_be_in_set(
        column='Pclass', value_set=['male', 'female'])

    # #### `Sex`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Sex')

    # #### `Siblings/Spouses Aboard`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Siblings/Spouses Aboard')

    # In[ ]:

    batch.expect_column_distinct_values_to_be_in_set(
        column='Siblings/Spouses Aboard', value_set=[0, 1, 2, 3, 4])

    # In[ ]:

    batch.expect_column_most_common_value_to_be_in_set(
        column='Siblings/Spouses Aboard', value_set=[0])

    # #### `Parents/Children Aboard`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Parents/Children Aboard')

    # In[ ]:

    batch.expect_column_distinct_values_to_be_in_set(
        column='Parents/Children Aboard', value_set=[0, 1, 2, 3, 4])

    # In[ ]:

    batch.expect_column_most_common_value_to_be_in_set(
        column='Parents/Children Aboard', value_set=[0])

    # #### `Fare`

    # In[ ]:

    batch.expect_column_values_to_not_be_null(column='Fare')

    # In[ ]:

    batch.expect_column_min_to_be_between(
        column='Fare', max_value=8.0, min_value=7.0)

    # In[ ]:

    batch.expect_column_max_to_be_between(
        column='Fare', max_value=200.0, min_value=150)

    # In[ ]:

    batch.save_expectation_suite(discard_failed_expectations=False)

    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch])

    validation_result_identifier = results.list_validation_result_identifiers()[
        0]

    context.build_data_docs()

    # context.open_data_docs(validation_result_identifier)


if __name__ == '__main__':
    validate_data()
