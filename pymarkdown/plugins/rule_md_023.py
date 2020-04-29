"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeaderMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd023(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.setext_start_token = None
        self.any_leading_whitespace_detected = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, spaces
            plugin_name="heading-start-left, header-start-left",
            plugin_id="MD023",
            plugin_enabled_by_default=True,
            plugin_description="Headings must start at the beginning of the line",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.setext_start_token = None
        self.any_leading_whitespace_detected = False

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, (AtxHeaderMarkdownToken)):
            if token.extracted_whitespace:
                self.report_next_token_error(token)
        elif isinstance(token, (SetextHeaderMarkdownToken)):
            self.setext_start_token = token
            self.any_leading_whitespace_detected = bool(token.remaining_line)
        elif isinstance(token, (TextMarkdownToken)):
            if self.setext_start_token and not self.any_leading_whitespace_detected:
                text_to_process = token.token_text
                split_lines = text_to_process.split("\n")
                for next_line in split_lines:
                    _, ex_ws = ParserHelper.extract_whitespace(next_line, 0)
                    if ex_ws:
                        self.any_leading_whitespace_detected = True
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (MarkdownToken.token_setext_header,):
                if token.extracted_whitespace:
                    self.any_leading_whitespace_detected = True

                if self.any_leading_whitespace_detected:
                    self.report_next_token_error(self.setext_start_token)
                self.setext_start_token = None
