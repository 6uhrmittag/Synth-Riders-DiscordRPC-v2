# API documentation[¶](https://srt.readthedocs.io/en/latest/api.html#module-srt "Permalink to this headline")

A tiny library for parsing, modifying, and composing SRT files.

_exception_ `srt.``SRTParseError`(_expected\_start_, _actual\_start_, _unmatched\_content_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.SRTParseError "Permalink to this definition")

Raised when part of an SRT block could not be parsed.

Parameters

- **expected\_start** ([_int_](https://docs.python.org/3.8/library/functions.html#int "(in Python v3.8)")) – The expected contiguous start index

- **actual\_start** ([_int_](https://docs.python.org/3.8/library/functions.html#int "(in Python v3.8)")) – The actual non-contiguous start index

- **unmatched\_content** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – The content between the expected start index and the actual start index

_class_ `srt.``Subtitle`(_index_, _start_, _end_, _content_, _proprietary\=''_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "Permalink to this definition")

The metadata relating to a single subtitle. Subtitles are sorted by start time by default. If no index was provided, index 0 will be used on writing an SRT block.

Parameters

- **index** ([_int_](https://docs.python.org/3.8/library/functions.html#int "(in Python v3.8)") _or_ [_None_](https://docs.python.org/3.8/library/constants.html#None "(in Python v3.8)")) – The SRT index for this subtitle

- **start** ([`datetime.timedelta`](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)")) – The time that the subtitle should start being shown

- **end** ([`datetime.timedelta`](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)")) – The time that the subtitle should stop being shown

- **proprietary** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – Proprietary metadata for this subtitle

- **content** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – The subtitle content. Should not contain OS-specific line separators, only \\n. This is taken care of already if you use [
  `srt.parse()`](https://srt.readthedocs.io/en/latest/api.html#srt.parse "srt.parse") to generate Subtitle objects.

`to_srt`(_strict\=True_, _eol\='\\n'_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle.to_srt "Permalink to this definition")

Convert the current [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") to an SRT block.

Parameters

- **strict** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – If disabled, will allow blank lines in the content of the SRT block, which is a violation of the SRT standard and may cause your media player to explode

- **eol** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – The end of line string to use (default “\\n”)

Returns

The metadata of the current [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") object as an SRT formatted subtitle block

Return type

[str](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")

_exception_ `srt.``TimestampParseError`[¶](https://srt.readthedocs.io/en/latest/api.html#srt.TimestampParseError "Permalink to this definition")

Raised when an SRT timestamp could not be parsed.

`srt.``compose`(_subtitles_, _reindex\=True_, _start\_index\=1_, _strict\=True_, _eol\=None_, _in\_place\=False_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.compose "Permalink to this definition")

Convert an iterator of [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects to a string of joined SRT blocks.

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">timedelta</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">start</span> <span class="o">=</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">seconds</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">end</span> <span class="o">=</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">seconds</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">subs</span> <span class="o">=</span> <span class="p">[</span>
<span class="gp">... </span>    <span class="n">Subtitle</span><span class="p">(</span><span class="n">index</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="n">start</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">end</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="s1">'x'</span><span class="p">),</span>
<span class="gp">... </span>    <span class="n">Subtitle</span><span class="p">(</span><span class="n">index</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="n">start</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">end</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="s1">'y'</span><span class="p">),</span>
<span class="gp">... </span><span class="p">]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">compose</span><span class="p">(</span><span class="n">subs</span><span class="p">)</span>  
<span class="go">'1\n00:00:01,000 --&gt; 00:00:02,000\nx\n\n2\n00:00:01,000 --&gt; ...'</span>
```

Parameters

- **subtitles** ([iterator](https://docs.python.org/3.8/glossary.html#term-iterator "(in Python v3.8)") of [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects) – The subtitles to convert to SRT blocks

- **reindex** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – Whether to reindex subtitles based on start time

- **start\_index** ([_int_](https://docs.python.org/3.8/library/functions.html#int "(in Python v3.8)")) – If reindexing, the index to start reindexing from

- **strict** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – Whether to enable strict mode, see [`Subtitle.to_srt()`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle.to_srt "srt.Subtitle.to_srt") for more information

- **eol** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – The end of line string to use (default “\\n”)

- **in\_place** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – Whether to reindex subs in-place for performance (version <=1.0.0 behaviour)

Returns

A single SRT formatted string, with each input [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") represented as an SRT block

Return type

[str](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")

`srt.``make_legal_content`(_content_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.make_legal_content "Permalink to this definition")

Remove illegal content from a content block. Illegal content includes:

- Blank lines

- Starting or ending with a blank line

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">make_legal_content</span><span class="p">(</span><span class="s1">'</span><span class="se">\n</span><span class="s1">foo</span><span class="se">\n\n</span><span class="s1">bar</span><span class="se">\n</span><span class="s1">'</span><span class="p">)</span>
<span class="go">'foo\nbar'</span>
```

Parameters

**content** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – The content to make legal

Returns

The legalised content

Return type

srt

`srt.``parse`(_srt_, _ignore\_errors\=False_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.parse "Permalink to this definition")

Convert an SRT formatted string (in Python 2, a `unicode` object) to a [generator](https://docs.python.org/3.8/glossary.html#term-generator "(in Python v3.8)") of Subtitle objects.

This function works around bugs present in many SRT files, most notably that it is designed to not bork when presented with a blank line as part of a subtitle’s content.

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">subs</span> <span class="o">=</span> <span class="n">parse</span><span class="p">(</span><span class="s2">"""</span><span class="se">\</span>
<span class="gp">... </span><span class="s2">422</span>
<span class="gp">... </span><span class="s2">00:31:39,931 --&gt; 00:31:41,931</span>
<span class="gp">... </span><span class="s2">Using mainly spoons,</span>
<span class="gp">...</span>
<span class="gp">... </span><span class="s2">423</span>
<span class="gp">... </span><span class="s2">00:31:41,933 --&gt; 00:31:43,435</span>
<span class="gp">... </span><span class="s2">we dig a tunnel under the city and release it into the wild.</span>
<span class="gp">...</span>
<span class="gp">... </span><span class="s2">"""</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="nb">list</span><span class="p">(</span><span class="n">subs</span><span class="p">)</span>  
<span class="go">[Subtitle(...index=422...), Subtitle(...index=423...)]</span>
```

Parameters

- **srt** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)") _or_ _a file-like object_) – Subtitles in SRT format

- **ignore\_errors** – If True, garbled SRT data will be ignored, and we’ll continue trying to parse the rest of the file, instead of raising [`SRTParseError`](https://srt.readthedocs.io/en/latest/api.html#srt.SRTParseError "srt.SRTParseError") and stopping execution.

Returns

The subtitles contained in the SRT file as [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects

Return type

[generator](https://docs.python.org/3.8/glossary.html#term-generator "(in Python v3.8)") of [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects

Raises

[**SRTParseError**](https://srt.readthedocs.io/en/latest/api.html#srt.SRTParseError "srt.SRTParseError") – If the matches are not contiguous and `ignore_errors` is False.

`srt.``sort_and_reindex`(_subtitles_, _start\_index\=1_, _in\_place\=False_, _skip\=True_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.sort_and_reindex "Permalink to this definition")

Reorder subtitles to be sorted by start time order, and rewrite the indexes to be in that same order. This ensures that the SRT file will play in an expected fashion after, for example, times were changed in some subtitles and they may need to be resorted.

If skip=True, subtitles will also be skipped if they are considered not to be useful. Currently, the conditions to be considered “not useful” are as follows:

- Content is empty, or only whitespace

- The start time is negative

- The start time is equal to or later than the end time

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">timedelta</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">one</span> <span class="o">=</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">seconds</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">two</span> <span class="o">=</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">seconds</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">three</span> <span class="o">=</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">seconds</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">subs</span> <span class="o">=</span> <span class="p">[</span>
<span class="gp">... </span>    <span class="n">Subtitle</span><span class="p">(</span><span class="n">index</span><span class="o">=</span><span class="mi">999</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="n">one</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">two</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="s1">'1'</span><span class="p">),</span>
<span class="gp">... </span>    <span class="n">Subtitle</span><span class="p">(</span><span class="n">index</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="n">two</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="n">three</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="s1">'2'</span><span class="p">),</span>
<span class="gp">... </span><span class="p">]</span>
<span class="gp">&gt;&gt;&gt; </span><span class="nb">list</span><span class="p">(</span><span class="n">sort_and_reindex</span><span class="p">(</span><span class="n">subs</span><span class="p">))</span>  
<span class="go">[Subtitle(...index=1...), Subtitle(...index=2...)]</span>
```

Parameters

- **subtitles** – [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects in any order

- **start\_index** ([_int_](https://docs.python.org/3.8/library/functions.html#int "(in Python v3.8)")) – The index to start from

- **in\_place** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – Whether to modify subs in-place for performance (version <=1.0.0 behaviour)

- **skip** ([_bool_](https://docs.python.org/3.8/library/functions.html#bool "(in Python v3.8)")) – Whether to skip subtitles considered not useful (see above for rules)

Returns

The sorted subtitles

Return type

[generator](https://docs.python.org/3.8/glossary.html#term-generator "(in Python v3.8)") of [`Subtitle`](https://srt.readthedocs.io/en/latest/api.html#srt.Subtitle "srt.Subtitle") objects

`srt.``srt_timestamp_to_timedelta`(_timestamp_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.srt_timestamp_to_timedelta "Permalink to this definition")

Convert an SRT timestamp to a [`timedelta`](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)").

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">srt_timestamp_to_timedelta</span><span class="p">(</span><span class="s1">'01:23:04,000'</span><span class="p">)</span>
<span class="go">datetime.timedelta(seconds=4984)</span>
```

Parameters

**timestamp** ([_str_](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")) – A timestamp in SRT format

Returns

The timestamp as a [`timedelta`](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)")

Return type

[datetime.timedelta](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)")

Raises

[**TimestampParseError**](https://srt.readthedocs.io/en/latest/api.html#srt.TimestampParseError "srt.TimestampParseError") – If the timestamp is not parseable

`srt.``timedelta_to_srt_timestamp`(_timedelta\_timestamp_)[¶](https://srt.readthedocs.io/en/latest/api.html#srt.timedelta_to_srt_timestamp "Permalink to this definition")

Convert a [`timedelta`](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)") to an SRT timestamp.

```
<span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">datetime</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">delta</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">timedelta</span><span class="p">(</span><span class="n">hours</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">minutes</span><span class="o">=</span><span class="mi">23</span><span class="p">,</span> <span class="n">seconds</span><span class="o">=</span><span class="mi">4</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">timedelta_to_srt_timestamp</span><span class="p">(</span><span class="n">delta</span><span class="p">)</span>
<span class="go">'01:23:04,000'</span>
```

Parameters

**timedelta\_timestamp** ([_datetime.timedelta_](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta "(in Python v3.8)")) – A datetime to convert to an SRT timestamp

Returns

The timestamp in SRT format

Return type

[str](https://docs.python.org/3.8/library/stdtypes.html#str "(in Python v3.8)")