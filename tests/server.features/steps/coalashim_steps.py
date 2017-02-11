# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import os
import json
from behave import given, when, then
from coala_langserver.coalashim import run_coala_with_specific_file


@given('the current directory and path of qualified.py')
def step_impl(context):
    context.dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            os.pardir,
            os.pardir
        )
    )
    context.path = os.path.join(context.dir, 'tests', 'resources', 'qualified.py')


@when('I pass the qualified.py to run_coala_with_specific_file')
def step_impl(context):
    context.output = run_coala_with_specific_file(context.dir, context.path)


@then('it should return output in json format')
def step_impl(context):
    assert context.failed is False


@then('with no error in the output')
def step_impl(context):
    assert context.output is None


@given('the current directory and path of unqualified.py')
def step_impl(context):
    context.dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            os.pardir,
            os.pardir
        )
    )
    context.path = os.path.join(context.dir, 'tests', 'resources', 'unqualified.py')


@when('I pass the unqualified.py to run_coala_with_specific_file')
def step_impl(context):
    context.output = run_coala_with_specific_file(context.dir, context.path)


@then('with autopep8 errors in the output')
def step_impl(context):
    assert json.loads(context.output)['results']['autopep8'] is not None
