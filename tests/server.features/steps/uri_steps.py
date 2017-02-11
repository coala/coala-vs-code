# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
from behave import given, when, then
from coala_langserver.uri import path_from_uri, dir_from_uri


@given('There is a string with "file://"')
def step_impl(context):
    context.str = 'file://Users'


@when('I pass the string with the prefix to path_from_uri')
def step_impl(context):
    context.path = path_from_uri(context.str)


@given('There is a string without "file://"')
def step_impl(context):
    context.str = '/Users'


@when('I pass the string without the prefix to path_from_uri')
def step_impl(context):
    context.path = path_from_uri(context.str)


@then('it should return a string without "file://"')
def step_impl(context):
    assert context.failed is False
    assert 'file://' not in context.path


@when('I pass the string to dir_from_uri')
def step_impl(context):
    context.path = dir_from_uri(context.str)


@then('it should return the directory of the path')
def step_impl(context):
    assert context.failed is False
    assert context.path is '/'
