*** Settings ***
| Documentation | Tests for the testcase rule 'TooManyTestSteps'
| Resource      | tests/acceptance/SharedKeywords.robot
| #
| Test Teardown
| ... | # provide some debugging information if things go bad
| ... | Run keyword if | "${TEST STATUS}" == "FAIL"
| ... | log | ${result.stdout}\n${result.stderr}

*** Test Cases ***
| Testcase WITHOUT too many test steps
| | [Documentation]
| | ... | Verify that a testcase without too many test steps triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestSteps
| | ... | ${SUITE SOURCE} | use this file as input
| |
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | No operation
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

| Testcase WITH too many test steps
| | [Documentation]
| | ... | Verify that a testcase with too many test steps triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestSteps
| | ... | test_data/acceptance/rules/TooManyTestSteps.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings

| Testcase WITHOUT too many test steps after configuration
| | [Documentation]
| | ... | Verify that a testcase with too many test steps triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestSteps
| | ... | --configure  | TooManyTestSteps:20
| | ... | test_data/acceptance/rules/TooManyTestSteps.robot
| |
| | rflint return code should be | 0
| | rflint should report 0 errors
| | rflint should report 0 warnings

| Testcase WITH too many test steps after configuration
| | [Documentation]
| | ... | Verify that a testcase with too many test steps triggers the rule.
| |
| | [Setup] | Run rf-lint with the following options:
| | ... | --no-filename
| | ... | --ignore | all
| | ... | --error  | TooManyTestSteps
| | ... | --configure  | TooManyTestSteps:1
| | ... | test_data/acceptance/rules/TooManyTestSteps.robot
| |
| | rflint return code should be | 1
| | rflint should report 1 errors
| | rflint should report 0 warnings
