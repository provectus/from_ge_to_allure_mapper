import json
import os
import sys
from datetime import datetime
import glob
import great_expectations as ge
from great_expectations.expectations.expectation import (
    ExpectationConfiguration,
)
from great_expectations.expectations.registry import (
    get_expectation_impl)

import shutil


def initialize_config():
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    root_ge_dir = data['root_folder_ge']
    allure_result_dir = data['allure_result']
    allure_report_dir = data['allure_report']
    if sys.argv[1:] is not str:
        test_suite = data['default_suite']
    else:
        test_suite = sys.argv[1:]
    return root_ge_dir, allure_result_dir, allure_report_dir, test_suite


def get_test_human_name(file):
    exp = get_expectation_impl(get_test_name(file))
    template_json = exp._prescriptive_renderer(
        configuration=ExpectationConfiguration(get_test_name(file),
                                               kwargs=get_params1(file)))[0]
    if type(template_json) is not dict:
        template_json = template_json.to_json_dict()
    template_str = template_json['string_template']['template']
    params = get_params1(file)
    result_string = template_str
    new_params = {}
    for key, value in params.items():
        if type(value) == list:
            if key == 'value_set':
                for i in value:
                    new_params["v__" + str(value.index(i))] = i
            else:
                for i in value:
                    new_params[str(key) + "_" + str(value.index(i))] = i

    if new_params:
        if 'value_set' in params.keys():
            del params['value_set']
            params.update(new_params)

        else:
            params = new_params
    for key, value in params.items():
        result_string = result_string.replace('$%s' % key, str(value))
    return result_string


def get_json(ge_root_dir, test_suite):
    file = glob.glob(
        os.path.join(os.path.abspath(ge_root_dir),
                     'great_expectations/uncommitted/validations/' + test_suite
                     + '/**/**/*.json'), recursive=False)
    with open(file[0]) as jsonfile:
        return json.load(jsonfile)


def get_test_name(file):
    return file['expectation_config']['expectation_type']


def get_suit_name(file, i):
    return file['meta']['batch_kwargs']['data_asset_name'] + "." + i['expectation_config']['kwargs'][
        'column'] if 'column' in i['expectation_config']['kwargs'] else file['meta']['batch_kwargs']['data_asset_name']


def get_jira_ticket(file):
    if 'Bug Ticket' in file['expectation_config']['meta']:

        return {
            "name": "Bug ticket",
            "url": file['expectation_config']['meta']['Bug Ticket'],
            "type": "issue"
        }
    else:
        return {}


def get_severity(file):
    return file['expectation_config']['meta']['Severity'] if 'Severity' in file['expectation_config']['meta'] else ""


def get_start_suit_time(file):
    return int(file['meta']['expectation_suite_meta']['BasicSuiteBuilderProfiler']['created_at'])


def get_stop_suit_time():
    return datetime.datetime.now().timestamp()


def parse_datetime(date_str):
    return datetime.timestamp(datetime.strptime(date_str, '%Y%m%dT%H%M%S.%fZ'))


def get_start_test_time(file):
    return parse_datetime(file['meta']['batch_markers']['ge_load_time'])


def get_stop_test_time(file):
    return parse_datetime(file['meta']['validation_time'])


def get_params(file):
    params = file['expectation_config']['kwargs']
    del params['result_format']
    result = []
    for param in params:
        result.append({"name": param, "value": str(params[param])}) if isinstance(params[param],
                                                                                  list) else result.append(
            {"name": param, "value": params[param]})
    return result


def get_params1(file):
    params = file['expectation_config']['kwargs']
    return params


def get_test_status(file):
    return "passed" if file['success'] is True else "failed"


def get_test_description(file):
    result = ""
    for f in file['result']:
        if str(f) != 'observed_value':
            result = str(f) + ": " + str(file['result'][f]) + "\n"
    return result


def get_observed_value(file):
    return "Observed value: " + str(file['result']['observed_value']) if 'observed_value' in file[
        'result'] else "Unexcpected count: " + str(file['result']['unexpected_count'])


def get_exception_message(file):
    return file['exception_info']['exception_message']


def get_exception_traceback(file):
    return file['exception_info']['exception_traceback']


def create_categories_json(allure_result):
    data = [
        {
            "name": "Ignored tests",
            "matchedStatuses": [
                "skipped"
            ]
        },
        {
            "name": "Passed tests",
            "matchedStatuses": [
                "passed"
            ]
        },
        {
            "name": "Broken tests",
            "matchedStatuses": [
                "broken"
            ]
        },
        {
            "name": "Failed tests",
            "matchedStatuses": [
                "failed"
            ]
        }
    ]

    result = json.dumps(data)
    with open(allure_result + "/categories.json", "w") as file:
        file.write(result)


def get_uuid(i, allure_report):
    fl = ""
    if os.path.exists(allure_report + '/history'):
        with open(allure_report + '/history/history.json') as jsonfile:
            fl = json.load(jsonfile)
        keys = list(fl.keys())
        keys.sort()
        return keys[i]
    else:
        return datetime.now().strftime("%S%f")


def create_suit_json(allure_result, allure_report, ge_root_dir, test_suite):
    if os.path.exists(allure_result):
        shutil.rmtree(allure_result + '/')
    os.makedirs(allure_result)
    file = get_json(ge_root_dir, test_suite)
    start_time = get_start_suit_time(file)
    stop_time = get_stop_suit_time()
    for i in file['results']:
        uuid = str(get_uuid(list(file['results']).index(i), allure_report))
        data = {
            "uuid": uuid,
            "historyId": uuid,
            "status": get_test_status(i),
            "parameters": get_params(i),
            "labels": [{
                "name": "test",
                "value": get_test_name(i)
            }, {
                "name": "suite",
                "value": get_suit_name(file, i)
            },
                {
                    "name": "severity",
                    "value": get_severity(i)
                }
            ],
            "links": [get_jira_ticket(i)],
            "name": get_test_name(i),
            "description": get_test_description(i),
            "statusDetails": {"known": False, "muted": False, "flaky": False,
                              "message": get_observed_value(i) if get_test_status(i) == 'failed' else "",
                              "trace": get_exception_traceback(i)},
            "start": start_time,
            "stop": stop_time,
            "steps": [
                {
                    "status": get_test_status(i),
                    "name": get_test_human_name(i),
                    "start": get_start_test_time(file),
                    "stop": get_stop_test_time(file)
                }]
        }

        result = json.dumps(data)

        with open(allure_result + '/' + uuid + "-result.json", "w") as fl:
            fl.write(result)


def transfer_folder(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def transfer_history(allure_result, allure_report):
    if os.path.isdir(allure_report):
        transfer_folder(allure_report + '/history', allure_result + '/history')


def create_json_report(root_ge_dir="", allure_result_dir="", allure_report_dir="", test_suite=""):
    root_ge_dir_config, allure_result_dir_config, allure_report_dir_config, test_suite_config = initialize_config()
    root_ge_dir = root_ge_dir_config if len(root_ge_dir) == 0 else root_ge_dir
    allure_result_dir = allure_result_dir_config if len(allure_result_dir) == 0 else allure_result_dir
    allure_report_dir = allure_report_dir_config if len(allure_report_dir) == 0 else allure_report_dir
    test_suite = test_suite_config if len(test_suite) == 0 else test_suite
    create_suit_json(allure_result_dir, allure_report_dir, root_ge_dir, test_suite)
    create_categories_json(allure_result_dir)
    transfer_history(allure_result_dir, allure_report_dir)


if __name__ == '__main__':
    create_json_report()
