"""
Module to provide processing for the block quotes.
"""
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.markdown_token import BlockQuoteMarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    IndentedCodeBlockStackToken,
    ParagraphStackToken,
)


class BlockQuoteProcessor:
    """
    Class to provide processing for the block quotes.
    """

    __block_quote_character = ">"

    @staticmethod
    def is_block_quote_start(
        line_to_parse, start_index, extracted_whitespace, adj_ws=None
    ):
        """
        Determine if we have the start of a block quote section.
        """

        if adj_ws is None:
            adj_ws = extracted_whitespace

        if ParserHelper.is_length_less_than_or_equal_to(
            adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteProcessor.__block_quote_character
        ):
            return True
        return False

    @staticmethod
    def __count_block_quote_starts(
        line_to_parse, start_index, stack_bq_count, is_top_of_stack_fenced_code_block
    ):
        """
        Having detected a block quote character (">") on a line, continue to consume
        and count while the block quote pattern is there.
        """

        this_bq_count = 0
        adjusted_line = line_to_parse
        if stack_bq_count == 0 and is_top_of_stack_fenced_code_block:
            start_index -= 1
        else:
            this_bq_count += 1
            start_index += 1

            print(
                "stack_bq_count--"
                + str(stack_bq_count)
                + "--is_top_of_stack_fenced_code_block--"
                + str(is_top_of_stack_fenced_code_block)
            )

            while True:
                if ParserHelper.is_character_at_index_whitespace(
                    adjusted_line, start_index
                ):
                    if adjusted_line[start_index] == "\t":
                        adjusted_tab_length = ParserHelper.calculate_length(
                            "\t", start_index=start_index
                        )
                        print("--" + adjusted_line.replace("\t", "\\t") + "--")
                        adjusted_line = (
                            adjusted_line[0:start_index]
                            + "".rjust(adjusted_tab_length)
                            + adjusted_line[start_index + 1 :]
                        )
                        print("--" + adjusted_line.replace("\t", "\\t") + "--")
                    start_index += 1

                if is_top_of_stack_fenced_code_block and (
                    this_bq_count >= stack_bq_count
                ):
                    break

                if start_index == len(
                    adjusted_line
                ) or ParserHelper.is_character_at_index_not(
                    adjusted_line,
                    start_index,
                    BlockQuoteProcessor.__block_quote_character,
                ):
                    break
                this_bq_count += 1
                start_index += 1

            print(
                "__count_block_quote_starts--"
                + str(start_index)
                + "--"
                + adjusted_line.replace("\t", "\\t")
                + "--"
            )
        return this_bq_count, start_index, adjusted_line

    @staticmethod
    def count_of_block_quotes_on_stack(token_stack):
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        stack_bq_count = 0
        for next_item_on_stack in token_stack:
            if next_item_on_stack.is_block_quote:
                stack_bq_count += 1

        return stack_bq_count

    @staticmethod
    def __ensure_stack_at_level(
        token_stack,
        this_bq_count,
        stack_bq_count,
        extracted_whitespace,
        close_open_blocks_fn,
    ):
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """

        container_level_tokens = []
        if this_bq_count > stack_bq_count:
            container_level_tokens, _, _ = close_open_blocks_fn(
                only_these_blocks=[ParagraphStackToken, IndentedCodeBlockStackToken],
            )
            while this_bq_count > stack_bq_count:
                token_stack.append(BlockQuoteStackToken())
                stack_bq_count += 1
                container_level_tokens.append(
                    BlockQuoteMarkdownToken(extracted_whitespace)
                )
        return container_level_tokens, stack_bq_count

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_block_quote_section(
        token_stack,
        line_to_parse,
        start_index,
        stack_bq_count,
        extracted_whitespace,
        close_open_blocks_fn,
        handle_blank_line_fn,
    ):
        """
        Handle the processing of a section clearly identified as having block quotes.
        """

        print(
            "IN>__handle_block_quote_section---"
            + line_to_parse.replace("\t", "\\t")
            + "<<<"
        )
        print("stack_bq_count--" + str(stack_bq_count))
        print("token_stack[-1]--" + str(token_stack[-1]))

        leaf_tokens = []
        container_level_tokens = []
        removed_chars_at_start = 0

        print(
            "__handle_block_quote_section---"
            + str(start_index)
            + "--"
            + line_to_parse.replace("\t", "\\t")
            + "--"
        )
        (
            this_bq_count,
            start_index,
            line_to_parse,
        ) = BlockQuoteProcessor.__count_block_quote_starts(
            line_to_parse,
            start_index,
            stack_bq_count,
            token_stack[-1].is_fenced_code_block,
        )
        print(
            "__handle_block_quote_section---this_bq_count--"
            + str(this_bq_count)
            + "--"
            + str(start_index)
            + "--"
            + line_to_parse.replace("\t", "\\t")
            + "--"
        )

        if not token_stack[-1].is_fenced_code_block:
            print("handle_block_quote_section>>not fenced")
            (
                container_level_tokens,
                stack_bq_count,
            ) = BlockQuoteProcessor.__ensure_stack_at_level(
                token_stack,
                this_bq_count,
                stack_bq_count,
                extracted_whitespace,
                close_open_blocks_fn,
            )

            line_to_parse = line_to_parse[start_index:]
            removed_chars_at_start = start_index

            if not line_to_parse.strip():
                (leaf_tokens, lines_to_requeue, _,) = handle_blank_line_fn(
                    line_to_parse, from_main_transform=False
                )
                # TODO will need to deal with force_ignore_first_as_lrd
                assert not lines_to_requeue
        else:
            print("handle_block_quote_section>>fenced")
            line_to_parse = line_to_parse[start_index:]

        print(
            "OUT>__handle_block_quote_section---"
            + line_to_parse.replace("\t", "\\t")
            + "<<<"
        )

        return (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            stack_bq_count,
            this_bq_count,
            removed_chars_at_start,
        )
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def check_for_lazy_handling(
        token_stack,
        this_bq_count,
        stack_bq_count,
        line_to_parse,
        extracted_whitespace,
        close_open_blocks_fn,
    ):
        """
        Check if there is any processing to be handled during the handling of
        lazy continuation lines in block quotes.
        """

        print("__check_for_lazy_handling")
        container_level_tokens = []
        if this_bq_count == 0 and stack_bq_count > 0:
            print("haven't processed")
            print(
                "this_bq_count>"
                + str(this_bq_count)
                + ">>stack_bq_count>>"
                + str(stack_bq_count)
                + "<<"
            )

            is_fenced_start, _, _, _ = LeafBlockProcessor.is_fenced_code_block(
                line_to_parse, 0, extracted_whitespace, skip_whitespace_check=True
            )
            print("fenced_start?" + str(is_fenced_start))

            if token_stack[-1].is_code_block or is_fenced_start:
                print("__check_for_lazy_handling>>code block")
                assert not container_level_tokens
                container_level_tokens, _, _ = close_open_blocks_fn(
                    only_these_blocks=[BlockQuoteStackToken, type(token_stack[-1])],
                    include_block_quotes=True,
                )
            else:
                print("__check_for_lazy_handling>>not code block")
                print("__check_for_lazy_handling>>" + str(token_stack))

        return container_level_tokens
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    @staticmethod
    def handle_block_quote_block(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        adj_ws,
        this_bq_count,
        stack_bq_count,
        close_open_blocks_fn,
        handle_blank_line_fn,
    ):
        """
        Handle the processing of a blockquote block.
        """

        did_process = False
        was_container_start = False
        end_of_bquote_start_index = -1
        leaf_tokens = []
        container_level_tokens = []
        removed_chars_at_start = 0

        if BlockQuoteProcessor.is_block_quote_start(
            line_to_parse, start_index, extracted_whitespace, adj_ws=adj_ws
        ):
            print("clt>>block-start")
            (
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                stack_bq_count,
                alt_this_bq_count,
                removed_chars_at_start,
            ) = BlockQuoteProcessor.__handle_block_quote_section(
                token_stack,
                line_to_parse,
                start_index,
                stack_bq_count,
                extracted_whitespace,
                close_open_blocks_fn,
                handle_blank_line_fn,
            )

            # TODO for nesting, may need to augment with this_bq_count already set.
            if this_bq_count == 0:
                this_bq_count = alt_this_bq_count
            else:
                print(
                    ">>>>>>>>>>>>>>>"
                    + str(this_bq_count)
                    + ">>>"
                    + str(alt_this_bq_count)
                )
                this_bq_count = alt_this_bq_count

            did_process = True
            was_container_start = True
            end_of_bquote_start_index = start_index

        return (
            did_process,
            was_container_start,
            end_of_bquote_start_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
        )

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals