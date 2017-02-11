# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
from behave import given, when, then
from coala_langserver.log import log


@given('There is a string')
def step_impl(context):
    context.str = 'file://Users'


@when('I pass the string to log')
def step_impl(context):
    log(context.str)


@then('it should return normally')
def step_impl(context):
    assert context.failed is False
