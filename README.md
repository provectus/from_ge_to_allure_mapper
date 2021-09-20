**Description**
Package made for mapping purpose from Great Expectations result format to Allure result format

**Install**
`pip install`

**How to Use**
import `map_to_json.py` into your project and use `create_json_report` method
You can set root_ge_dir, allure_result_dir, allure_report_dir,test_suite directly in method params or by `config.json` 
_root_ge_dir_ - path to project great_expectations folder
_allure_result_dir_ - path to folder, when you want to save allure results
_allure_report_dir_ - path to folder, in which you save allure report
_test_suite_ - test suite name