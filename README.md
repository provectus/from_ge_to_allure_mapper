**Description**
Package made for mapping purpose from Great Expectations result format to Allure result format



**How to Use**
## Run from this repo
0. `pip install .`
1. Run  `python ./test/edit_test_suite.py` for getting json results
2. Run `python ./from_ge_to_allure_mapper/map_to_json.py` to generate Allure results 
## Run as package
0. `pip install from_ge_to_allure_mapper`
1. import `map_to_json.py` into your project and use `create_json_report` method
You can set root_ge_dir, allure_result_dir, allure_report_dir,test_suite directly in method params or by `config.json` 
_root_ge_dir_ - path to project great_expectations folder
_allure_result_dir_ - path to folder, when you want to save allure results
_allure_report_dir_ - path to folder, in which you save allure report
_test_suite_ - test suite name

## Run allure report
0. Install allure: https://github.com/allure-framework/allure2#download
1. Generate Allure : `allure generate -c reportsx`
2. Open allure: `allure open allure-report`
