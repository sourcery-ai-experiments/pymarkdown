"""
Module to provide tests related to the MD047 rule.
"""
from test.markdown_scanner import MarkdownScanner


def test_md0047_all_samples():
    """
    Test to make sure we get the expect behavior after scanning the files in the
    test/resources/rules/md047 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["test/resources/rules/md047"]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md047/end_with_no_blank_line.md:3:41: "
        + "MD047: Files should end with a single newline character "
        + "(single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md0047_good_sample():
    """
    Test to make sure we get the expect behavior after scanning a good file from the
    test/resources/rules/md047 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["test/resources/rules/md047/end_with_blank_line.md"]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )