"""
https://github.github.com/gfm/#fenced-code-blocks
"""
import pytest

from .utils import act_and_assert


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_fenced_code_blocks_089():
    """
    Test case 089:  Simple example with backticks
    """

    # Arrange
    source_markdown = """```
<
 >
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_090():
    """
    Test case 090:  Simple example with tildes
    """

    # Arrange
    source_markdown = """~~~
<
 >
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text(2,1):\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_091():
    """
    Test case 091:  Fewer than three backticks is not enough:
    """

    # Arrange
    source_markdown = """``
foo
``"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[icode-span(1,1):foo:``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_092():
    """
    Test case 092:  (part a) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    source_markdown = """```
aaa
~~~
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa\n~~~:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_093():
    """
    Test case 093:  (part b) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    source_markdown = """~~~
aaa
```
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text(2,1):aaa\n```:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_094():
    """
    Test case 094:  (part a) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    source_markdown = """````
aaa
```
``````"""
    expected_tokens = [
        "[fcode-block(1,1):`:4::::::]",
        "[text(2,1):aaa\n```:]",
        "[end-fcode-block::6:False]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_095():
    """
    Test case 095:  (part b) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    source_markdown = """~~~~
aaa
~~~
~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4::::::]",
        "[text(2,1):aaa\n~~~:]",
        "[end-fcode-block::4:False]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096():
    """
    Test case 096:  (part a) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block:::True]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096a():
    """
    Test case 096a:  variation
    """

    # Arrange
    source_markdown = """```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1)::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096b():
    """
    Test case 096b:  variation
    """

    # Arrange
    source_markdown = """```

"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>\n</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096c():
    """
    Test case 096b:  variation
    """

    # Arrange
    source_markdown = """```


"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03\n\x03:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>

</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096d():
    """
    Test case 096b:  variation
    """

    # Arrange
    source_markdown = """```
/a
/a/a
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,2):\n\x03  \n\x03: ]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>\a
\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096e():
    """
    Test case 096b:  variation
    """

    # Arrange
    source_markdown = """```
abc
/a/a
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03  \n\x03:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>abc
  
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096f():
    """
    Test case 096b:  variation
    """

    # Arrange
    source_markdown = """```
abc

"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03\n\x03:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>abc

</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_097():
    """
    Test case 097:  (part b) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """`````

```
aaa"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n```\naaa:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>
```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098x():
    """
    Test case 098:  (part c) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """> ```
> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):aaa:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098a():
    """
    Test case 098a:  Modified 98 without a space between the block quote indicator and the string.
    """

    # Arrange
    source_markdown = """> ```
>aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):aaa:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098b():
    """
    Test case 098b:  Modified 98 with extra ">" before second line.
    """

    # Arrange
    source_markdown = """> ```
>> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):\a>\a&gt;\a aaa:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt; aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098c():
    """
    Test case 098c:  Modified 98 with less ">" before second line.
    """

    # Arrange
    source_markdown = """> ```
aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>aaa</p>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099x():
    """
    Test case 099:  A code block can have all empty lines as its content:
    """

    # Arrange
    source_markdown = """```

\a\a
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03  :]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>
\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099a():
    """
    Test case 099a:  variation
    """

    # Arrange
    source_markdown = """```

\a\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03  \n\x03:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>
\a\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099b():
    """
    Test case 099b:  variation
    """

    # Arrange
    source_markdown = """```

\a
\a\a
\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03 \n\x03  \n\x03 \n\x03:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>
\a
\a\a
\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099c():
    """
    Test case 099c:  variation
    """

    # Arrange
    source_markdown = """```
z
\a
\a\a
\a
z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03 \n\x03  \n\x03 \nz:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>z
\a
\a\a
\a
z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099d():
    """
    Test case 099c:  variation
    """

    # Arrange
    source_markdown = """```
z
\a
z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03 \nz:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>z
\a
z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099e():
    """
    Test case 099e:  variation
    """

    # Arrange
    source_markdown = """```
\a
\a\a
\a
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,2):\n\x03  \n\x03 : ]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>\a
\a\a
\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099f():
    """
    Test case 099f:  variation
    """

    # Arrange
    source_markdown = """```

\a
\a\aabc
\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03 \n  abc\n\x03 \n\x03:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>
\a
\a\aabc
\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099g():
    """
    Test case 099c:  variation
    """

    # Arrange
    source_markdown = """```
z

\a
\a\a
\a

z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03\n\x03 \n\x03  \n\x03 \n\x03\nz:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>z

\a
\a\a
\a

z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099h():
    """
    Test case 099h:  variation
    """

    # Arrange
    source_markdown = """`````

```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n```\naaa:]",
        "[end-fcode-block::5:False]",
    ]
    expected_gfm = """<pre><code>
```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099i():
    """
    Test case 099h:  variation
    """

    # Arrange
    source_markdown = """`````


```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\n```\naaa:]",
        "[end-fcode-block::5:False]",
    ]
    expected_gfm = """<pre><code>

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099j():
    """
    Test case 099h:  variation
    """

    # Arrange
    source_markdown = """`````


bbb

ccc

```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\nbbb\n\x03\nccc\n\x03\n```\naaa:]",
        "[end-fcode-block::5:False]",
    ]
    expected_gfm = """<pre><code>

bbb

ccc

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099ja():
    """
    Test case 099h:  variation
    """

    # Arrange
    source_markdown = """`````


bbb

ccc

```
aaa
`````
"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\nbbb\n\x03\nccc\n\x03\n```\naaa:]",
        "[end-fcode-block::5:False]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<pre><code>

bbb

ccc

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099k():
    """
    Test case 099f:  variation
    """

    # Arrange
    source_markdown = """```



\a
\a\aabc
\a



```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03\n\x03\n\x03 \n  abc\n\x03 \n\x03\n\x03\n\x03:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>


\a
\a\aabc
\a



</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099l():
    """
    Test case 099c:  variation
    """

    # Arrange
    source_markdown = """```
z



\a
\a\a
\a



z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03\n\x03\n\x03\n\x03 \n\x03  \n\x03 \n\x03\n\x03\n\x03\nz:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>z



\a
\a\a
\a



z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_100():
    """
    Test case 100:  A code block can be empty:
    """

    # Arrange
    source_markdown = """```
```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block::3:False]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_101():
    """
    Test case 101:  (part a)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    source_markdown = """ ```
 aaa
aaa
```"""
    expected_tokens = [
        "[fcode-block(1,2):`:3::::: :]",
        "[text(2,2):aaa\naaa:\a \a\x03\a]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_102():
    """
    Test case 102:  (part b)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    source_markdown = """  ```
aaa
  aaa
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:::::  :]",
        "[text(2,1):aaa\n\a  \a\x03\aaaa\naaa:]",
        "[end-fcode-block:  :3:False]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_103():
    """
    Test case 103:  (part c)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    source_markdown = """   ```
   aaa
    aaa
  aaa
   ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text(2,4):aaa\n\a   \a\x03\a aaa\n\a  \a\x03\aaaa:\a   \a\x03\a]",
        "[end-fcode-block:   :3:False]",
    ]
    expected_gfm = """<pre><code>aaa
 aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_104():
    """
    Test case 104:  Four spaces indentation produces an indented code block:
    """

    # Arrange
    source_markdown = """    ```
    aaa
    ```"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):```\naaa\n```:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>```
aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_105():
    """
    Test case 105:  (part a) Closing fences may be indented by 0-3 spaces, and their indentation need not match that of the opening fence:
    """

    # Arrange
    source_markdown = """```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa:]",
        "[end-fcode-block:  :3:False]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_106():
    """
    Test case 106:  (part b) Closing fences may be indented by 0-3 spaces, and their indentation need not match that of the opening fence:
    """

    # Arrange
    source_markdown = """   ```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text(2,1):aaa:]",
        "[end-fcode-block:  :3:False]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_107():
    """
    Test case 107:  This is not a closing fence, because it is indented 4 spaces:
    """

    # Arrange
    source_markdown = """```
aaa
    ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa\n    ```:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>aaa
    ```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_108():
    """
    Test case 108:  (part a) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    source_markdown = """``` ```
aaa"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1): :```::]",
        """[text(1,8):
aaa::\n]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code> </code>
aaa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_109():
    """
    Test case 109:  (part b) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    source_markdown = """~~~~~~
aaa
~~~ ~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:6::::::]",
        "[text(2,1):aaa\n~~~ ~~:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>aaa
~~~ ~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_110():
    """
    Test case 110:  Fenced code blocks can interrupt paragraphs, and can be followed directly by paragraphs, without a blank line between:
    """

    # Arrange
    source_markdown = """foo
```
bar
```
baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):bar:]",
        "[end-fcode-block::3:False]",
        "[para(5,1):]",
        "[text(5,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo</p>
<pre><code>bar
</code></pre>
<p>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_111():
    """
    Test case 111:  Other blocks can also occur before and after fenced code blocks without an intervening blank line:
    """

    # Arrange
    source_markdown = """foo
---
~~~
bar
~~~
# baz"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):foo:]",
        "[end-setext::]",
        "[fcode-block(3,1):~:3::::::]",
        "[text(4,1):bar:]",
        "[end-fcode-block::3:False]",
        "[atx(6,1):1:0:]",
        "[text(6,3):baz: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>foo</h2>
<pre><code>bar
</code></pre>
<h1>baz</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_112():
    """
    Test case 112:  (part a) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """```ruby
def foo(x)
  return 3
end
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:ruby:::::]",
        "[text(2,1):def foo(x)\n  return 3\nend:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_113():
    """
    Test case 113:  (part b) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """~~~~    ruby startline=3 $%@#$
def foo(x)
  return 3
end
~~~~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4:ruby:: startline=3 $%@#$:::    ]",
        "[text(2,1):def foo(x)\n  return 3\nend:]",
        "[end-fcode-block::7:False]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_114():
    """
    Test case 114:  (part c) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """````;
````"""
    expected_tokens = ["[fcode-block(1,1):`:4:;:::::]", "[end-fcode-block::4:False]"]
    expected_gfm = """<pre><code class="language-;"></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_115():
    """
    Test case 115:  Info strings for backtick code blocks cannot contain backticks:
    """

    # Arrange
    source_markdown = """``` aa ```
foo"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):aa:```: : ]",
        """[text(1,11):
foo::\n]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>aa</code>
foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_116():
    """
    Test case 116:  Info strings for tilde code blocks can contain backticks and tildes:
    """

    # Arrange
    source_markdown = """~~~ aa ``` ~~~
foo
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3:aa:: ``` ~~~::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-aa">foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_117():
    """
    Test case 117:  Closing code fences cannot have info strings:
    """

    # Arrange
    source_markdown = """```
``` aaa
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):``` aaa:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>``` aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_01x():
    """
    Test case extra 01:  start a "list block" within a fenced code block
    """

    # Arrange
    source_markdown = """```
- some text
some other text
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):- some text\nsome other text:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>- some text
some other text
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_01a():
    """
    Test case extra 01:  start a "list block" within a fenced code block
    """

    # Arrange
    source_markdown = """```
- [foo]:
/url
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):- [foo]:\n/url:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>- [foo]:
/url
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_02x():
    """
    Test case extra 02:  variation of 1 where list already opened
    """

    # Arrange
    source_markdown = """- ```
- some text
some other text
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code></code></pre>
</li>
<li>some text
some other text</li>
</ul>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_fenced_code_blocks_extra_02a():
    """
    Test case extra 02:  variation of 1 where list already opened
    """

    # Arrange
    source_markdown = """- ```
- [foo]:
/url
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[link-ref-def(2,3):True::foo::\n:/url:::::]",
        "[end-ulist:::True]",
        "[fcode-block(4,1):`:3::::::]",
        "[BLANK(5,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code></code></pre>
</li>
<li></li>
</ul>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_03x():
    """
    Test case extra 03:  variation of 1 where list already opened but no new list item

    NOTE: Small change to output to remove newline at pre/code at end.
    """

    # Arrange
    source_markdown = """- ```
  some text
some other text
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):some text:]",
        "[end-fcode-block:::True]",
        "[end-ulist:::True]",
        "[para(3,1):]",
        "[text(3,1):some other text:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>some text
</code></pre>
</li>
</ul>
<p>some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_fenced_code_blocks_extra_03a():
    """
    Test case extra 03:  variation of 1 where list already opened but no new list item
    """

    # Arrange
    source_markdown = """- ```
  [foo]:
/url
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[link-ref-def(2,3):True::foo::\n:/url:::::]",
        "[text(4,1):</script>:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
        "[html-block(4,1)]",
        "[text(4,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>[foo]:
</code></pre>
</li>
</ul>
<p>/url</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_04x():
    """
    Test case extra 04:  start a "block quote" within a fenced code block
    """

    # Arrange
    source_markdown = """```
> some text
some other text
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a>\a&gt;\a some text\nsome other text:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>&gt; some text
some other text
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_04a():
    """
    Test case extra 04:  start a "block quote" within a fenced code block
    """

    # Arrange
    source_markdown = """```
> [foo]:
/url
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a>\a&gt;\a [foo]:\n/url:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>&gt; [foo]:
/url
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_05x():
    """
    Test case extra 05:  variation of 4 where list already opened
    """

    # Arrange
    source_markdown = """> ```
> some text
some other text
```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):some text:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,1):]",
        "[text(3,1):some other text:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>some text
</code></pre>
</blockquote>
<p>some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_05a():
    """
    Test case extra 05:  variation of 4 where list already opened

    NOTE: Small change to output to remove newline at pre/code at end.
    """

    # Arrange
    source_markdown = """> ```
> [foo]:
/url
```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):[foo]::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,1):]",
        "[text(3,1):/url:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>[foo]:
</code></pre>
</blockquote>
<p>/url</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_06xx():
    """
    Test case extra 05:  variation of 4 where block already opened but
                         no block character
    """

    # Arrange
    source_markdown = """> ```
  some text
some other text
```
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,3):  \n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>some text
some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_06xa():
    """
    Test case extra 05:  variation of 4 where block already opened but
                         no block character
    """

    # Arrange
    source_markdown = """> ```
  some text
some other text
```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,3):  \n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>some text
some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_fenced_code_blocks_extra_06a():
    """
    Test case extra 05:  variation of 4 where block already opened but
                         no block character
    """

    # Arrange
    source_markdown = """> ```
  [foo]:
/url
```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[link-ref-def(2,3):True:  :foo::\n:/url:::::]",
        "[fcode-block(4,1):`:3::::::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_07():
    """
    Test case extra 07:  mixed block quotes and list blocks
    """

    # Arrange
    source_markdown = """```
* a
  > b
  >
* c
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):* a\n  \a>\a&gt;\a b\n  \a>\a&gt;\a\n* c:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>* a
  &gt; b
  &gt;
* c
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08x():
    """
    Test case extra 08:  tests
    """

    # Arrange
    source_markdown = """```
abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03\ndef:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>abc

def
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08a():
    """
    Test case extra 08:  tests
    """

    # Arrange
    source_markdown = """```

abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\nabc\n\x03\ndef:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>
abc

def
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08b():
    """
    Test case extra 08:  tests
    """

    # Arrange
    source_markdown = """```
abc
```

abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::3:False]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):abc:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):def:]",
        "[end-para:::False]",
        "[fcode-block(8,1):`:3::::::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code>abc
</code></pre>
<p>abc</p>
<p>def</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08c():
    """
    Test case extra 08:  tests
    """

    # Arrange
    source_markdown = """```
\a\a
abc

def
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,3):\nabc\n\x03\ndef:  ]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>\a\a
abc

def
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
