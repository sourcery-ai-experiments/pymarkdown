"""
Module to provide processing for the list blocks.
"""

import logging
import string

from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.markdown_token import (
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import OrderedListStackToken, UnorderedListStackToken

LOGGER = logging.getLogger(__name__)


class ListBlockProcessor:
    """
    Class to provide processing for the list blocks.
    """

    __ulist_start_characters = "-+*"
    __olist_start_characters = ".)"

    @staticmethod
    # pylint: disable=too-many-arguments
    def is_ulist_start(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an un-numbered list.
        """
        LOGGER.debug("is_ulist_start>>pre>>")
        is_start = False
        after_all_whitespace_index = -1
        if adj_ws is None:
            adj_ws = extracted_whitespace

        if (
            (
                ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
                or skip_whitespace_check
            )
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, ListBlockProcessor.__ulist_start_characters
            )
            and (
                ParserHelper.is_character_at_index_whitespace(
                    line_to_parse, start_index + 1
                )
                or ((start_index + 1) == len(line_to_parse))
            )
        ):

            LOGGER.debug("is_ulist_start>>mid>>")
            after_all_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, start_index + 1
            )
            LOGGER.debug(
                "after_all_whitespace_index>>%s>>len>>%s",
                str(after_all_whitespace_index),
                str(len(line_to_parse)),
            )

            is_break, _ = LeafBlockProcessor.is_thematic_break(
                line_to_parse, start_index, extracted_whitespace
            )
            if not is_break and not (
                parser_state.token_stack[-1].is_paragraph
                and not parser_state.token_stack[-2].is_list
                and (after_all_whitespace_index == len(line_to_parse))
            ):
                is_start = True

        LOGGER.debug("is_ulist_start>>result>>%s", str(is_start))
        return is_start, after_all_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_olist_start(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an numbered or ordered list.
        """
        is_start = False
        end_whitespace_index = -1
        index = None
        my_count = None
        if adj_ws is None:
            adj_ws = extracted_whitespace
        if (
            ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, string.digits
        ):
            index = start_index
            while ParserHelper.is_character_at_index_one_of(
                line_to_parse, index, string.digits
            ):
                index += 1
            my_count = index - start_index
            olist_index_number = line_to_parse[start_index:index]
            LOGGER.debug("olist?%s<<count>>%s<<", olist_index_number, str(my_count))
            LOGGER.debug("olist>>%s", str(line_to_parse[index]))
            LOGGER.debug(
                "index+1>>%s>>len>>%s", str(index + 1), str(len(line_to_parse))
            )

            end_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, index + 1
            )
            LOGGER.debug(
                "end_whitespace_index>>%s>>len>>%s>>%s",
                str(end_whitespace_index),
                str(len(line_to_parse)),
                olist_index_number,
            )

            if (
                my_count <= 9
                and ParserHelper.is_character_at_index_one_of(
                    line_to_parse, index, ListBlockProcessor.__olist_start_characters
                )
                and not (
                    parser_state.token_stack[-1].is_paragraph
                    and not parser_state.token_stack[-2].is_list
                    and (
                        (end_whitespace_index == len(line_to_parse))
                        or olist_index_number != "1"
                    )
                )
                and (
                    ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index + 1
                    )
                    or ((index + 1) == len(line_to_parse))
                )
            ):
                is_start = True

        LOGGER.debug("is_olist_start>>result>>%s", str(is_start))
        return is_start, index, my_count, end_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def handle_ulist_block(
        parser_state,
        did_process,
        was_container_start,
        no_para_start_if_empty,
        position_marker,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        removed_chars_at_start,
        current_container_blocks,
    ):
        """
        Handle the processing of a ulist block.
        """
        end_of_ulist_start_index = -1
        container_level_tokens = []
        if not did_process:
            started_ulist, end_of_ulist_start_index = ListBlockProcessor.is_ulist_start(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                adj_ws=adj_ws,
            )
            if started_ulist:
                LOGGER.debug("clt>>ulist-start")
                removed_chars_at_start = 0

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = ListBlockProcessor.__pre_list(
                    parser_state,
                    position_marker.text_to_parse,
                    position_marker.index_number,
                    extracted_whitespace,
                    0,
                    stack_bq_count,
                    this_bq_count,
                )

                LOGGER.debug(
                    "total=%s;ws-before=%s;ws_after=%s;start_index=%s",
                    str(indent_level),
                    str(ws_before_marker),
                    str(ws_after_marker),
                    str(position_marker.index_number),
                )
                new_stack = UnorderedListStackToken(
                    indent_level,
                    position_marker.text_to_parse[position_marker.index_number],
                    ws_before_marker,
                    ws_after_marker,
                    position_marker.index_number,
                )
                new_token = UnorderedListStartMarkdownToken(
                    position_marker.text_to_parse[position_marker.index_number],
                    indent_level,
                    extracted_whitespace,
                    position_marker,
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    position_marker.text_to_parse,
                ) = ListBlockProcessor.__post_list(
                    parser_state,
                    new_stack,
                    new_token,
                    position_marker.text_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                    position_marker,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True

        return (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
            no_para_start_if_empty,
            position_marker.text_to_parse,
            container_level_tokens,
            removed_chars_at_start,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def handle_olist_block(
        parser_state,
        did_process,
        was_container_start,
        no_para_start_if_empty,
        position_marker,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        removed_chars_at_start,
        current_container_blocks,
    ):
        """
        Handle the processing of a olist block.
        """
        end_of_olist_start_index = -1
        container_level_tokens = []
        if not did_process:
            (
                started_olist,
                index,
                my_count,
                end_of_olist_start_index,
            ) = ListBlockProcessor.is_olist_start(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                adj_ws=adj_ws,
            )
            if started_olist:
                assert not container_level_tokens
                LOGGER.debug("clt>>olist-start")
                removed_chars_at_start = 0

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = ListBlockProcessor.__pre_list(
                    parser_state,
                    position_marker.text_to_parse,
                    index,
                    extracted_whitespace,
                    my_count,
                    stack_bq_count,
                    this_bq_count,
                )

                LOGGER.debug(
                    "total=%s;ws-before=%s;ws_after=%s;start_index=%s",
                    str(indent_level),
                    str(ws_before_marker),
                    str(ws_after_marker),
                    str(position_marker.index_number),
                )

                new_stack = OrderedListStackToken(
                    indent_level,
                    position_marker.text_to_parse[
                        position_marker.index_number : index + 1
                    ],
                    ws_before_marker,
                    ws_after_marker,
                    position_marker.index_number,
                )
                new_token = OrderedListStartMarkdownToken(
                    position_marker.text_to_parse[index],
                    position_marker.text_to_parse[position_marker.index_number : index],
                    indent_level,
                    extracted_whitespace,
                    position_marker,
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    position_marker.text_to_parse,
                ) = ListBlockProcessor.__post_list(
                    parser_state,
                    new_stack,
                    new_token,
                    position_marker.text_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                    position_marker,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True
        return (
            did_process,
            was_container_start,
            end_of_olist_start_index,
            no_para_start_if_empty,
            position_marker.text_to_parse,
            container_level_tokens,
            removed_chars_at_start,
        )
        # pylint: enable=too-many-arguments

    @staticmethod
    def list_in_process(
        parser_state, line_to_parse, start_index, extracted_whitespace, ind,
    ):
        """
        Handle the processing of a line where there is a list in process.
        """
        container_level_tokens = []

        LOGGER.debug("!!!!!FOUND>>%s", str(parser_state.token_stack[ind]))
        LOGGER.debug("!!!!!FOUND>>%s", str(parser_state.token_stack[ind].extra_data))
        requested_list_indent = parser_state.token_stack[ind].indent_level
        before_ws_length = parser_state.token_stack[ind].ws_before_marker
        LOGGER.debug(
            "!!!!!requested_list_indent>>%s,before_ws=%s",
            str(requested_list_indent),
            str(before_ws_length),
        )

        leading_space_length = ParserHelper.calculate_length(extracted_whitespace)

        started_ulist, _ = ListBlockProcessor.is_ulist_start(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        started_olist, _, _, _ = ListBlockProcessor.is_olist_start(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )

        allow_list_continue = True
        if leading_space_length >= 4 and (started_ulist or started_olist):
            allow_list_continue = not parser_state.token_document[-1].is_blank_line

        LOGGER.debug(
            "leading_space_length>>%s>>requested_list_indent>>%s>>is_in_paragraph>>%s",
            str(leading_space_length),
            str(requested_list_indent),
            str(parser_state.token_stack[-1].is_paragraph),
        )
        if leading_space_length >= requested_list_indent and allow_list_continue:
            line_to_parse = ListBlockProcessor.__adjust_line_for_list_in_process(
                line_to_parse, start_index, leading_space_length, requested_list_indent,
            )
        else:
            requested_list_indent = requested_list_indent - before_ws_length
            LOGGER.debug(
                "leading_space_length>>%s>>adj requested_list_indent>>%s>>%s<<",
                str(leading_space_length),
                str(requested_list_indent),
                str(parser_state.token_stack[-1].is_paragraph),
            )
            if (
                parser_state.token_stack[-1].is_paragraph
                and leading_space_length >= requested_list_indent
                and allow_list_continue
            ):
                line_to_parse = ListBlockProcessor.__adjust_line_for_list_in_process(
                    line_to_parse,
                    start_index,
                    requested_list_indent,
                    requested_list_indent,
                )
            else:
                container_level_tokens = ListBlockProcessor.__check_for_list_closures(
                    parser_state, line_to_parse, start_index, extracted_whitespace, ind,
                )
                if parser_state.token_stack[-1].is_list:
                    requested_list_indent = parser_state.token_stack[-1].indent_level
                    LOGGER.warning(">>line_to_parse>>%s>>", line_to_parse)
                    LOGGER.warning(">>start_index>>%s", str(start_index))
                    LOGGER.warning(
                        ">>requested_list_indent>>%s", str(requested_list_indent)
                    )
                    LOGGER.warning(">>before_ws_length>>%s", str(before_ws_length))
                    line_to_parse = ListBlockProcessor.__adjust_line_for_list_in_process(
                        line_to_parse,
                        start_index,
                        requested_list_indent,
                        before_ws_length,
                    )

        return container_level_tokens, line_to_parse

    # pylint: disable=too-many-arguments
    @staticmethod
    def __pre_list(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        marker_width,
        stack_bq_count,
        this_bq_count,
    ):
        """
        Handle the processing of the first part of the list.
        """

        (
            after_marker_ws_index,
            after_marker_whitespace,
        ) = ParserHelper.extract_whitespace(line_to_parse, start_index + 1)
        ws_after_marker = ParserHelper.calculate_length(
            after_marker_whitespace, start_index=start_index + 1
        )
        ws_before_marker = ParserHelper.calculate_length(extracted_whitespace)

        LOGGER.debug(
            "--ws_before_marker>>%s>>marker_width>>%s",
            str(ws_before_marker),
            str(marker_width),
        )
        LOGGER.debug("--%s--%s", str(start_index), str(start_index + 1))
        # assert "\t" not in after_marker_whitespace

        (
            container_level_tokens,
            stack_bq_count,
        ) = ListBlockProcessor.__handle_list_nesting(
            parser_state, stack_bq_count, this_bq_count
        )
        LOGGER.debug(
            ">>>>>XX>>%s>>%s<<", str(after_marker_ws_index), str(len(line_to_parse))
        )
        if after_marker_ws_index == len(line_to_parse):
            LOGGER.debug("BOOOOOOOM")
            indent_level = 2 + marker_width
            remaining_whitespace = 0
            ws_after_marker = 1
        else:
            indent_level = ws_before_marker + 1 + ws_after_marker + marker_width
            remaining_whitespace = 0
            LOGGER.debug(
                "ws_after_marker>>%s<<indent_level<<%s<<rem<<%s<<",
                str(ws_after_marker),
                str(indent_level),
                str(remaining_whitespace),
            )
            if ws_after_marker > 4:
                indent_level = indent_level - ws_after_marker + 1
                remaining_whitespace = ws_after_marker - 1
                ws_after_marker = 1
        LOGGER.debug(
            "ws_after_marker>>%s<<indent_level<<%s<<rem<<%s<<",
            str(ws_after_marker),
            str(indent_level),
            str(remaining_whitespace),
        )
        return (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
            after_marker_ws_index,
            ws_before_marker,
            container_level_tokens,
            stack_bq_count,
        )
        # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_list_nesting(parser_state, stack_bq_count, this_bq_count):
        """
        Resolve any nesting issues with block quotes.
        """
        LOGGER.debug(
            ">>stack_bq_count>>%s>>this_bq_count>>%s",
            str(stack_bq_count),
            str(this_bq_count),
        )
        container_level_tokens = []
        while this_bq_count < stack_bq_count:

            assert not container_level_tokens
            inf = len(parser_state.token_stack) - 1
            while not parser_state.token_stack[inf].is_block_quote:
                inf -= 1

            container_level_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=inf,
                include_block_quotes=True,
                include_lists=True,
            )
            LOGGER.debug("container_level_tokens>>%s", str(container_level_tokens))
            stack_bq_count -= 1
        return container_level_tokens, stack_bq_count

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __post_list(
        parser_state,
        new_stack,
        new_token,
        line_to_parse,
        remaining_whitespace,
        after_marker_ws_index,
        indent_level,
        current_container_blocks,
        position_marker,
    ):
        """
        Handle the processing of the last part of the list.
        """

        LOGGER.debug("new_stack>>%s", str(new_stack))

        emit_item = True
        emit_li = True
        did_find, last_list_index = LeafBlockProcessor.check_for_list_in_process(
            parser_state
        )
        if did_find:
            (
                container_level_tokens,
                emit_li,
            ) = ListBlockProcessor.__close_required_lists_after_start(
                parser_state, last_list_index, new_stack, current_container_blocks,
            )
            emit_item = False
        else:
            LOGGER.debug(
                "NOT list-in-process>>%s",
                str(parser_state.token_stack[last_list_index]),
            )
            container_level_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state
            )
        LOGGER.debug("container_level_tokens>>%s", str(container_level_tokens))

        LOGGER.debug("__post_list>>before>>%s", str(container_level_tokens))
        if emit_item or not emit_li:
            LOGGER.debug("__post_list>>adding>>%s", str(new_token))
            parser_state.token_stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            LOGGER.debug("__post_list>>new list item>>")
            assert emit_li
            LOGGER.debug("instead of-->%s", str(new_token))
            container_level_tokens.append(
                NewListItemMarkdownToken(
                    indent_level, position_marker, new_token.extracted_whitespace
                )
            )
        LOGGER.debug(
            "__post_list>>rem>>%s>>after_in>>%s",
            str(remaining_whitespace),
            str(after_marker_ws_index),
        )
        line_to_parse = (
            "".rjust(remaining_whitespace, " ") + line_to_parse[after_marker_ws_index:]
        )
        LOGGER.debug("__post_list>>after>>%s", str(container_level_tokens))

        return True, container_level_tokens, line_to_parse
        # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    def __close_required_lists_after_start(
        parser_state, last_list_index, new_stack, current_container_blocks,
    ):
        """
        After a list start, check to see if any others need closing.
        """
        LOGGER.debug(
            "list-in-process>>%s", str(parser_state.token_stack[last_list_index])
        )
        container_level_tokens, _, _ = parser_state.close_open_blocks_fn(
            parser_state, until_this_index=last_list_index + 1
        )
        LOGGER.debug("old-stack>>%s<<", str(container_level_tokens))

        repeat_check = True
        while repeat_check:
            LOGGER.debug("start")
            repeat_check = False
            (
                do_not_emit,
                emit_li,
                extra_tokens,
                last_list_index,
            ) = ListBlockProcessor.__are_list_starts_equal(
                parser_state, last_list_index, new_stack, current_container_blocks,
            )
            LOGGER.debug("extra_tokens>>%s", str(extra_tokens))
            container_level_tokens.extend(extra_tokens)
            if do_not_emit:
                LOGGER.debug("post_list>>don't emit")
                (
                    did_find,
                    last_list_index,
                ) = LeafBlockProcessor.check_for_list_in_process(parser_state)
                LOGGER.debug(
                    "did_find>>%s--last_list_index--%s",
                    str(did_find),
                    str(last_list_index),
                )
                assert did_find
                LOGGER.debug(
                    "ARE-EQUAL>>stack>>%s>>new>>%s",
                    str(parser_state.token_stack[last_list_index]),
                    str(new_stack),
                )
                if (
                    parser_state.token_stack[last_list_index].type_name
                    == new_stack.type_name
                    or new_stack.start_index
                    > parser_state.token_stack[last_list_index].start_index
                ):
                    pass
                else:
                    repeat_check = True
            else:
                LOGGER.debug("post_list>>close open blocks and emit")
                close_tokens, _, _ = parser_state.close_open_blocks_fn(
                    parser_state, until_this_index=last_list_index, include_lists=True
                )
                assert close_tokens
                container_level_tokens.extend(close_tokens)

                (
                    did_find,
                    last_list_index,
                ) = LeafBlockProcessor.check_for_list_in_process(parser_state)
                LOGGER.debug(
                    "did_find>>%s--last_list_index--%s",
                    str(did_find),
                    str(last_list_index),
                )
                if did_find:
                    LOGGER.debug(
                        "ARE-EQUAL>>stack>>%s>>new>>%s",
                        str(parser_state.token_stack[last_list_index]),
                        str(new_stack),
                    )
                    if (
                        new_stack.indent_level
                        <= parser_state.token_stack[last_list_index].indent_level
                    ):
                        repeat_check = True
        return container_level_tokens, emit_li

    @staticmethod
    def __are_list_starts_equal(
        parser_state, last_list_index, new_stack, current_container_blocks,
    ):
        """
        Check to see if the list starts are equal, and hence a continuation of
        the current list.
        """

        balancing_tokens = []

        LOGGER.debug(
            "ARE-EQUAL>>stack>>%s>>new>>%s",
            str(parser_state.token_stack[last_list_index]),
            str(new_stack),
        )
        if parser_state.token_stack[last_list_index] == new_stack:
            balancing_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_list_index,
                include_block_quotes=True,
            )
            return True, True, balancing_tokens, last_list_index

        document_token_index = len(parser_state.token_document) - 1
        while document_token_index >= 0 and not (
            parser_state.token_document[document_token_index].is_any_list_token
        ):
            document_token_index -= 1
        assert document_token_index >= 0

        LOGGER.debug(
            "ARE-EQUAL>>Last_List_token=%s",
            str(parser_state.token_document[document_token_index]),
        )
        old_start_index = parser_state.token_document[document_token_index].indent_level

        old_last_marker_character = parser_state.token_stack[
            last_list_index
        ].list_character[-1]
        current_start_index = new_stack.ws_before_marker
        LOGGER.debug(
            "old>>%s>>%s",
            str(parser_state.token_stack[last_list_index].extra_data),
            old_last_marker_character,
        )
        LOGGER.debug(
            "new>>%s>>%s", str(new_stack.extra_data), new_stack.list_character[-1]
        )
        if (
            parser_state.token_stack[last_list_index].type_name == new_stack.type_name
            and old_last_marker_character == new_stack.list_character[-1]
        ):
            do_not_emit, emit_li = ListBlockProcessor.__process_eligible_list_start(
                parser_state,
                balancing_tokens,
                current_start_index,
                old_start_index,
                current_container_blocks,
            )
            return do_not_emit, emit_li, balancing_tokens, last_list_index

        LOGGER.debug("SUBLIST WITH DIFFERENT")
        LOGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        LOGGER.debug(
            "are_list_starts_equal>>current_start_index>>%s>>old_start_index>>%s",
            str(current_start_index),
            str(old_start_index),
        )
        if current_start_index >= old_start_index:
            LOGGER.debug("are_list_starts_equal>>True")
            return True, False, balancing_tokens, last_list_index

        LOGGER.debug("are_list_starts_equal>>False")
        LOGGER.debug(">>%s", str(parser_state.token_stack))
        return False, False, balancing_tokens, last_list_index

    @staticmethod
    def __process_eligible_list_start(
        parser_state,
        balancing_tokens,
        current_start_index,
        old_start_index,
        current_container_blocks,
    ):
        LOGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        LOGGER.debug(
            "are_list_starts_equal>>current_start_index>>%s>>old_start_index>>%s",
            str(current_start_index),
            str(old_start_index),
        )
        if current_start_index < old_start_index:

            LOGGER.debug("current_container_blocks>>%s", str(current_container_blocks))
            if len(current_container_blocks) > 1:
                LOGGER.debug(
                    "current_container_blocks-->%s", str(parser_state.token_stack)
                )
                last_stack_depth = parser_state.token_stack[-1].ws_before_marker
                while current_start_index < last_stack_depth:
                    last_stack_index = parser_state.token_stack.index(
                        parser_state.token_stack[-1]
                    )
                    close_tokens, _, _ = parser_state.close_open_blocks_fn(
                        parser_state,
                        until_this_index=last_stack_index,
                        include_lists=True,
                    )
                    assert close_tokens
                    balancing_tokens.extend(close_tokens)
                    LOGGER.debug("close_tokens>>%s", str(close_tokens))
                    last_stack_depth = parser_state.token_stack[-1].ws_before_marker

            return True, True

        LOGGER.debug("are_list_starts_equal>>True")
        return True, False

    @staticmethod
    def __adjust_line_for_list_in_process(
        line_to_parse, start_index, leading_space_length, requested_list_indent
    ):
        """
        Alter the current line to better represent the current level of lists.
        """
        LOGGER.debug("enough ws to continue")
        remaining_indent = leading_space_length - requested_list_indent
        line_to_parse = "".rjust(remaining_indent, " ") + line_to_parse[start_index:]
        return line_to_parse

    @staticmethod
    def __check_for_list_closures(
        parser_state, line_to_parse, start_index, extracted_whitespace, ind,
    ):
        """
        Check to see if the list in progress and the level of lists shown require
        the closing of some of the sublists.
        """
        container_level_tokens = []
        LOGGER.debug("ws(naa)>>line_to_parse>>%s<<", line_to_parse)
        LOGGER.debug("ws(naa)>>stack>>%s", str(parser_state.token_stack))
        LOGGER.debug("ws(naa)>>tokens>>%s", str(parser_state.token_document))

        is_theme_break, _ = LeafBlockProcessor.is_thematic_break(
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        LOGGER.debug("ws(naa)>>is_theme_break>>%s", str(is_theme_break))

        if not parser_state.token_stack[-1].is_paragraph or is_theme_break:
            LOGGER.debug("ws (normal and adjusted) not enough to continue")

            container_level_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=ind, include_lists=True
            )
        else:
            LOGGER.debug("ws (normal and adjusted) continue")
        return container_level_tokens
