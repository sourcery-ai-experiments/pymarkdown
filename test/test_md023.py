"""
Module to provide tests related to the MD003 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md023_proper_indent_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md023/proper_indent_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md023/proper_indent_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_improper_indent_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md023/improper_indent_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_atx.md:0:0: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_improper_indent_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md023/improper_indent_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_setext.md:0:0: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:0:0: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:0:0: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:0:0: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
