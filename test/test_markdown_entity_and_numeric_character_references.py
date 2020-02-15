"""
https://github.github.com/gfm/#entity-and-numeric-character-references
"""
import io
import os
import sys

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_character_references_321():
    """
    Test case 321:  Entity references consist of & + any of the valid HTML5 entity names + ;. The document https://html.spec.whatwg.org/multipage/entities.json is used as an authoritative source for the valid entity references and their corresponding code points.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&nbsp; &amp; &copy; &AElig; &Dcaron;
&frac34; &HilbertSpace; &DifferentialD;
&ClockwiseContourIntegral; &ngE;"""
    expected_tokens = [
        "[para:]",
        "[text:\u00A0 &amp; © Æ Ď\n¾ ℋ ⅆ\n∲ ≧̸:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_322():
    """
    Test case 322:  Decimal numeric character references consist of &# + a string of 1–7 arabic digits + ;. A numeric character reference is parsed as the corresponding Unicode character. Invalid Unicode code points will be replaced by the REPLACEMENT CHARACTER (U+FFFD). For security reasons, the code point U+0000 will also be replaced by U+FFFD.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&#35; &#1234; &#992; &#0;"""
    expected_tokens = [
        "[para:]",
        "[text:# Ӓ Ϡ �:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_323():
    """
    Test case 323:  Hexadecimal numeric character references consist of &# + either X or x + a string of 1-6 hexadecimal digits + ;. They too are parsed as the corresponding Unicode character (this time specified with a hexadecimal numeral instead of decimal).
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&#X22; &#XD06; &#xcab;"""
    expected_tokens = [
        "[para:]",
        "[text:&quot; ആ ಫ:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_324():
    """
    Test case 324:  Here are some nonentities:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&nbsp &x; &#; &#x;
&#87654321;
&#abcdef0;
&ThisIsNotDefined; &hi?;"""
    expected_tokens = [
        "[para:]",
        "[text:&amp;nbsp &amp;x; &amp;#; &amp;#x;\n&amp;#87654321;\n&amp;#abcdef0;\n&amp;ThisIsNotDefined; &amp;hi?;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_324a():
    """
    Test case 324a:  Extension of 324
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&"""
    expected_tokens = [
        "[para:]",
        "[text:&amp;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_325():
    """
    Test case 325:  Although HTML5 does accept some entity references without a trailing semicolon (such as &copy), these are not recognized here, because it makes the grammar too ambiguous:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&copy"""
    expected_tokens = [
        "[para:]",
        "[text:&amp;copy:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_326():
    """
    Test case 326:  Strings that are not on the list of HTML5 named entities are not recognized as entity references either:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&MadeUpEntity;"""
    expected_tokens = [
        "[para:]",
        "[text:&amp;MadeUpEntity;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_327():
    """
    Test case 327:  (part 1) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = '<a href="&ouml;&ouml;.html">'
    expected_tokens = [
        "[html-block]",
        '[text:<a href="&ouml;&ouml;.html">:]',
        "[end-html-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_328():
    """
    Test case 328:  (part 2) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = '[foo](/f&ouml;&ouml; "f&ouml;&ouml;")'
    expected_tokens = [
        "[para:]",
        "[text:[foo](/föö &quot;föö&quot;):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will break with link definitions
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_329():
    """
    Test case 329:  (part 3) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]

[foo]: /f&ouml;&ouml; "f&ouml;&ouml;"""
    expected_tokens = [
        "[para:]",
        "[text:[foo]:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:[foo]: /föö &quot;föö:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will break with link definitions
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_330():
    """
    Test case 330:  (part 4) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``` f&ouml;&ouml;
foo
```
"""
    expected_tokens = [
        "[fcode-block:`:3:föö::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
        "[BLANK:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_331():
    """
    Test case 331:  (part 1) Entity and numeric character references are treated as literal text in code spans and code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`f&ouml;&ouml;`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:f&amp;ouml;&amp;ouml;]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_332():
    """
    Test case 332:  (part 2) Entity and numeric character references are treated as literal text in code spans and code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    f&ouml;f&ouml;"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:f&amp;ouml;f&amp;ouml;:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_333():
    """
    Test case 333:  (part 1) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&#42;foo&#42;
*foo*"""
    expected_tokens = [
        "[para:]",
        "[text:*foo*\n*foo*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO emphasis
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_334():
    """
    Test case 334:  (part 2) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&#42; foo

* foo"""
    expected_tokens = [
        "[para:]",
        "[text:* foo:]",
        "[end-para]",
        "[BLANK:]",
        "[ulist:*::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_335():
    """
    Test case 335:  (part 3) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo&#10;&#10;bar"""
    expected_tokens = [
        "[para:]",
        "[text:foo\n\nbar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_336():
    """
    Test case 336:  (part 4) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """&#9;foo"""
    expected_tokens = [
        "[para:]",
        "[text:\tfoo:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_character_references_337():
    """
    Test case 337:  (part 5) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[a](url &quot;tit&quot;)"""
    expected_tokens = [
        "[para:]",
        "[text:[a](url &quot;tit&quot;):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_missing_entities_json_file():
    """
    Test the entities.json not being present in the specified directory.
    """

    tokenizer = TokenizedMarkdown()
    tokenizer.resource_path = "resourcesx"
    std_output = io.StringIO()
    try:
        old_out = sys.stdout
        sys.stdout = std_output

        tokenizer.transform("")
        assert False, "Should have exited prior to this."
    except SystemExit as this_exception:
        assert this_exception.code == 1
    finally:
        sys.stdout = old_out

    assert std_output.getvalue().startswith(
        "Named character entity map file 'resourcesx\\entities.json' was not loaded ([Errno 2] No such file or directory: '"
    )


def test_bad_entities_json_file():
    """
    Test the entities.json not being a valid json file in the specified directory.
    """

    tokenizer = TokenizedMarkdown()
    tokenizer.resource_path = os.path.join(os.path.split(__file__)[0], "resources")
    entities_json_file = os.path.join(tokenizer.resource_path, "entities.json")
    std_output = io.StringIO()
    try:
        old_out = sys.stdout
        sys.stdout = std_output

        tokenizer.transform("")
        assert False, "Should have exited prior to this."
    except SystemExit as this_exception:
        assert this_exception.code == 1
    finally:
        sys.stdout = old_out

    assert (
        std_output.getvalue()
        == "Named character entity map file '"
        + entities_json_file
        + "' is not a valid JSON file (Expecting value: line 1 column 1 (char 0)).\n"
    )


# TODO
#
# & and various forms at end of line
#
# 327 special parsing for html blocks?
# <a href="&ouml;&ouml;.html" x="&ouml;">
# <x-me foo="&ouml;">

# <script>
# &ouml; bar="&ouml;" bbb