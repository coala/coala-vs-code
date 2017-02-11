# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import os
from behave import given, when, then
from coala_langserver.diagnostic import output_to_diagnostics
from coala_langserver.coalashim import run_coala_with_specific_file


@given('the output with errors by coala')
def step_impl(context):
    context.dir = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            os.pardir,
            'resources'
        )
    )
    context.path = os.path.join(context.dir, 'unqualified.py')

    context.output = run_coala_with_specific_file(context.dir, context.path)


@when('I pass the parameters to output_to_diagnostics')
def step_impl(context):
    context.message = output_to_diagnostics(context.output)


@then('it should return output in vscode format')
def step_impl(context):
    assert len(context.message) is not 0
