# Hypothesis Data Generation Examples

## 目次

- [基本データ型](#basic-data-types)
  - [整数](#integers)
  - [浮動小数点数](#floats)
  - [テキスト](#text)
    - [前後にスペースを含む文字列](#前後にスペースを含む文字列)
    - [前後に改行コードを含む文字列](#前後に改行コードを含む文字列)
    - [特殊文字を含む文字列（日本語を含む）](#特殊文字を含む文字列日本語を含む)
    - [数値と文字列が混じった文字列](#数値と文字列が混じった文字列)
    - [電話番号 (ハイフンあり/なし)](#電話番号-ハイフンありなし)
  - [真偽値](#booleans)
  - [リスト](#lists)
  - [タプル](#tuples)
  - [辞書](#dictionaries)
  - [日付](#dates)
  - [日時](#datetimes)
  - [時刻](#times)
  - [時間差](#timedeltas)
  - [Enum](#enums)
  - [セット](#sets)
  - [UUID](#uuids)
  - [バイナリ](#binary)
  - [メールアドレス](#emails)
- [ストラテジーの組み合わせ](#combining-strategies)
  - [値のフィルタリング](#filtering-values)
  - [値のマッピング](#mapping-values)
  - [フラットマッピングストラテジー](#flatmapping-strategies)
  - [OneOf ストラテジー](#oneof-strategies)
- [カスタムストラテジー](#custom-strategies)
  - [`st.builds()` の使用](#using-stbuilds)
- [高度なストラテジー](#advanced-strategies)
  - [再帰的なストラテジー](#recursive-strategies)
  - [データ依存ストラテジー](#data-dependent-strategies)
  - [状態を持つストラテジー](#stateful-strategies)
- [ベストプラクティス](#best-practices)
- [和暦の日付](#japanese-calendar-dates-wareki)
- [DataFrame のテスト](#dataframe-testing)
- [結論](#conclusion)

---

# Hypothesis Data Generation Examples

This document provides examples of how to generate different types of data using Hypothesis, a property-based testing library for Python.

## Basic Data Types

### Integers

The `integers()` strategy generates integer values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers())
def test_integer_example(value):
    print(f"Generated integer: {value}")
    assert isinstance(value, int)
```

**Example Generated Values:**

```
Generated integer: 0
Generated integer: 10
Generated integer: -5
Generated integer: 1000
Generated integer: -200
```

### Floats

The `floats()` strategy generates floating-point values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.floats())
def test_float_example(value):
    print(f"Generated float: {value}")
    assert isinstance(value, float)
```

**Example Generated Values:**

```
Generated float: 0.0
Generated float: 3.14
Generated float: -2.71
Generated float: 1.0e6
Generated float: -5.0e-3
```

### Text

`text()`ストラテジーは、文字列値を生成します。

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text())
def test_text_example(value):
    print(f"Generated text: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text: ""
Generated text: "hello"
Generated text: "world"
Generated text: "Hypothesis"
Generated text: "データ生成"
```

#### 前後にスペースを含む文字列

`text()`ストラテジーは、デフォルトでは前後にスペースを含まない文字列を生成しますが、`whitespace`引数を調整することで、前後にスペースを含む文字列を生成できます。

#### 前後に改行コードを含む文字列

`text()`ストラテジーは、デフォルトでは前後に改行コードを含まない文字列を生成しますが、`whitespace`引数を調整することで、前後に改行コードを含む文字列を生成できます。

#### 特殊文字を含む文字列（日本語を含む）

`text()`ストラテジーは、デフォルトでは制御文字や非 ASCII 文字などの特殊文字を生成しませんが、`characters()`ストラテジーと組み合わせることで、特殊文字を含む文字列を生成できます。
日本語の特殊文字（句読点、記号など）も同様に生成可能です。

#### 数値と文字列が混じった文字列

数値と文字列が混じった文字列を生成するには、`st.text()`ストラテジーの`alphabet`引数に、`st.ascii_letters`と`st.digits()`を`st.one_of()`で組み合わせます。

#### 数値と文字列と空欄と特殊文字が混じった文字列

数値、文字列、空欄、特殊文字が混じった文字列を生成するには、`st.text()`ストラテジーの`alphabet`引数に、`st.ascii_letters`、`st.digits()`、`st.characters()`、そして空白文字を含むストラテジーを`st.one_of()`で組み合わせます。

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.one_of(st.ascii_letters, st.digits(), st.characters(), st.whitespace())))
def test_text_with_numbers_whitespace_special_chars_example(value):
    print(f"Generated text with numbers, whitespace and special chars: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text with numbers, whitespace and special chars: "abc 123 def !@#$%"
Generated text with numbers, whitespace and special chars: "12345\\t67890\\n"
Generated text with numbers, whitespace and special chars: "abcdefg\\u3000特殊文字"
Generated text with numbers, whitespace and special chars: "混合999文字 888列 777 ☆★"
```

#### 電話番号 (ハイフンあり/なし)

電話番号をハイフンあり/なしで生成する例を以下に示します。

**ハイフンなしの電話番号:**

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(min_size=10, max_size=11, alphabet=st.digits()))
def test_phone_number_no_hyphen_example(value):
    print(f"Generated phone number (no hyphen): {value}")
    assert isinstance(value, str)
    assert value.isdigit()
    assert 10 <= len(value) <= 11
```

**生成例:**

```
Generated phone number (no hyphen): 09012345678
Generated phone number (no hyphen): 0312345678
```

**ハイフンありの電話番号:**

```python
from hypothesis import given
import hypothesis.strategies as st

def format_phone_number(digits):
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    else:  # len(digits) == 11
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

@given(st.text(min_size=10, max_size=11, alphabet=st.digits()).map(format_phone_number))
def test_phone_number_with_hyphen_example(value):
    print(f"Generated phone number (with hyphen): {value}")
    assert isinstance(value, str)
    parts = value.split('-')
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
```

**生成例:**

```
Generated phone number (with hyphen): 090-1234-5678
Generated phone number (with hyphen): 03-123-4567
```

#### 文字列の任意の箇所にスペースを含む文字列

`text()`ストラテジーは`whitespace`引数に`st.characters()`を渡すことで、文字列の任意の場所に空白文字（スペース、タブ、改行など）を含む文字列を生成できます。

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.characters() | st.whitespace()))
def test_text_with_arbitrary_whitespace_example(value):
    print(f"Generated text with arbitrary whitespace: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text with arbitrary whitespace: "hello world"
Generated text with arbitrary whitespace: "  hello  world  "
Generated text with arbitrary whitespace: "hello\\tworld\\n"
Generated text with arbitrary whitespace: "  \\t\\n  "
```

**生成例:**

```
Generated phone number (no hyphen): 09012345678
Generated phone number (no hyphen): 0312345678
```

**ハイフンありの電話番号:**

```python
from hypothesis import given
import hypothesis.strategies as st

def format_phone_number(digits):
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    else: # len(digits) == 11
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

@given(st.text(min_size=10, max_size=11, alphabet=st.digits()).map(format_phone_number))
def test_phone_number_with_hyphen_example(value):
    print(f"Generated phone number (with hyphen): {value}")
    assert isinstance(value, str)
    parts = value.split('-')
    assert len(parts) in [3]
    assert all(part.isdigit() for part in parts)
```

**生成例:**

```
Generated phone number (with hyphen): 090-1234-5678
Generated phone number (with hyphen): 03-123-4567
```

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.one_of(st.ascii_letters, st.digits(), st.characters(), st.whitespace())))
def test_text_with_numbers_whitespace_special_chars_example(value):
    print(f"Generated text with numbers, whitespace and special chars: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text with numbers, whitespace and special chars: "abc 123 def !@#$%"
Generated text with numbers, whitespace and special chars: "12345\\t67890\\n"
Generated text with numbers, whitespace and special chars: "abcdefg\\u3000特殊文字"
Generated text with numbers, whitespace and special chars: "混合999文字 888列 777 ☆★"
```

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.one_of(st.ascii_letters, st.digits())))
def test_text_with_numbers_example(value):
    print(f"Generated text with numbers: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text with numbers: "abc123def456"
Generated text with numbers: "1234567890"
Generated text with numbers: "abcdefg"
Generated text with numbers: "混合999文字888列777"
```

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.characters()))
def test_text_with_special_chars_example(value):
    print(f"Generated text with special characters: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
**生成例:**

```

Generated text with special characters: "\\u0001\\u0002\\u0003 こんにちは\\u0004\\u0005\\u0006"
Generated text with special characters: "記号#$%&'()\\u3000\\\*+,-./:;<=>?@[]^\_`{|}~"
Generated text with special characters: "特殊文字が含まれています\\u2020\\u2021"
Generated text with special characters: "日本語の特殊文字、句読点。？！"
Generated text with special characters: "色々な記号と日本語の組み合わせ：☆★※◎ 〒"

````

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(alphabet=st.characters()))
def test_text_with_special_chars_example(value):
    print(f"Generated text with special characters: {value}")
    assert isinstance(value, str)
````

**生成例:**

```
Generated text with newline: "\\nhello world\\n"
Generated text with newline: "\\n\\tHypothesis\\n"
Generated text with newline: "\\nデータ生成\\n"
```

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text(whitespace=st.characters()))
def test_text_with_whitespace_example(value):
    print(f"Generated text with whitespace: {value}")
    assert isinstance(value, str)
```

**生成例:**

```
Generated text with whitespace: "  hello world  "
Generated text with whitespace: "\\t  Hypothesis  \\n"
Generated text with whitespace: " データ生成 "
```

**Example Generated Values:**

```
Generated text: ""
Generated text: "hello"
Generated text: "world"
Generated text: "Hypothesis"
Generated text: "データ生成"
```

### Booleans

The `booleans()` strategy generates boolean values (True or False).

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.booleans())
def test_boolean_example(value):
    print(f"Generated boolean: {value}")
    assert isinstance(value, bool)
```

**Example Generated Values:**

```
Generated boolean: True
Generated boolean: False
Generated boolean: True
```

### Lists

The `lists()` strategy generates lists of values. You can specify the strategy for the elements of the list.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_list_example(value):
    print(f"Generated list: {value}")
    assert isinstance(value, list)
    if value:
        assert isinstance(value[0], int)
```

**Example Generated Values:**

```
Generated list: []
Generated list: [1, 2, 3]
Generated list: [-10, 0, 5]
Generated list: [100]
```

### Tuples

The `tuples()` strategy generates tuples of values. You can specify the strategies for each element of the tuple.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.tuples(st.integers(), st.text()))
def test_tuple_example(value):
    print(f"Generated tuple: {value}")
    assert isinstance(value, tuple)
    assert isinstance(value[0], int)
    assert isinstance(value[1], str)
```

**Example Generated Values:**

```
Generated tuple: (0, "")
Generated tuple: (10, "hello")
Generated tuple: (-5, "world")
Generated tuple: (-5, "データ")
```

### Dictionaries

The `dictionaries()` strategy generates dictionaries. You need to specify strategies for keys and values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_dictionary_example(value):
    print(f"Generated dictionary: {value}")
    assert isinstance(value, dict)
    if value:
        assert isinstance(list(value.keys())[0], str)
        assert isinstance(list(value.values())[0], int)
```

**Example Generated Values:**

```
Generated dictionary: {}
Generated dictionary: {"a": 1, "b": 2}
Generated dictionary: {"key": -5, "another_key": 100}
```

### Dates

The `dates()` strategy generates date objects.

```python
from hypothesis import given
import hypothesis.strategies as st
import datetime

@given(st.dates())
def test_date_example(value):
    print(f"Generated date: {value}")
    assert isinstance(value, datetime.date)
```

**Example Generated Values:**

```
Generated date: 1970-01-01
Generated date: 2023-10-27
Generated date: 2000-05-15
```

### Datetimes

The `datetimes()` strategy generates datetime objects.

```python
from hypothesis import given
import hypothesis.strategies as st
import datetime

@given(st.datetimes())
def test_datetime_example(value):
    print(f"Generated datetime: {value}")
    assert isinstance(value, datetime.datetime)
```

**Example Generated Values:**

```
Generated datetime: 1970-01-01 00:00:00
Generated datetime: 2023-10-27 10:30:00
Generated datetime: 2000-05-15 18:45:30
```

### Times

The `times()` strategy generates time objects.

```python
from hypothesis import given
import hypothesis.strategies as st
import datetime

@given(st.times())
def test_time_example(value):
    print(f"Generated time: {value}")
    assert isinstance(value, datetime.time)
```

**Example Generated Values:**

```
Generated time: 00:00:00
Generated time: 10:30:00
Generated time: 18:45:30
```

### Timedeltas

The `timedeltas()` strategy generates timedelta objects, representing durations.

```python
from hypothesis import given
import hypothesis.strategies as st
import datetime

@given(st.timedeltas())
def test_timedelta_example(value):
    print(f"Generated timedelta: {value}")
    assert isinstance(value, datetime.timedelta)
```

**Example Generated Values:**

```
Generated timedelta: 0:00:00
Generated timedelta: 1 day, 0:00:00
Generated timedelta: -1 day, 0:00:00
```

### Enums

The `enums()` strategy generates values from a Python `enum.Enum`.

```python
from hypothesis import given
import hypothesis.strategies as st
import enum

class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

@given(st.enums(Color))
def test_enum_example(value):
    print(f"Generated enum value: {value}")
    assert isinstance(value, Color)
```

**Example Generated Values:**

```
Generated enum value: Color.RED
Generated enum value: Color.GREEN
Generated enum value: Color.BLUE
```

### Sets

The `sets()` strategy generates sets of unique values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.sets(st.integers()))
def test_set_example(value):
    print(f"Generated set: {value}")
    assert isinstance(value, set)
    for item in value:
        assert isinstance(item, int)
```

**Example Generated Values:**

```
Generated set: set()
Generated set: {1, 2, 3}
Generated set: {-1, 0, 1}
Generated set: {1, 2, 3}
Generated set: {-1, 0, 1}
```

### UUIDs

The `uuids()` strategy generates UUID objects.

```python
from hypothesis import given
import hypothesis.strategies as st
import uuid

@given(st.uuids())
def test_uuid_example(value):
    print(f"Generated UUID: {value}")
    assert isinstance(value, uuid.UUID)
```

**Example Generated Values:**

```
Generated UUID: 123e4567-e89b-12d3-a456-426614174000
Generated UUID: 00000000-0000-0000-0000-000000000000
Generated UUID: ffffffff-ffff-ffff-ffff-ffffffffffff
```

### Binary

The `binary()` strategy generates bytes objects.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.binary())
def test_binary_example(value):
    print(f"Generated binary: {value}")
    assert isinstance(value, bytes)
```

**Example Generated Values:**

```
Generated binary: b''
Generated binary: b'\\x00\\x01\\x02\\x03'
Generated binary: b'Hello, world!'
```

### Emails

The `emails()` strategy generates email address strings.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.emails())
def test_email_example(value):
    print(f"Generated email: {value}")
    assert isinstance(value, str)
    assert "@" in value
    assert "." in value.split("@")[1]
```

**Example Generated Values:**

```
Generated email: user@example.com
Generated email: test.user@subdomain.example.net
Generated email: long-email-address@very.long.domain.example.co.uk
```

## Combining Strategies

### Filtering Values

You can use `filter()` to generate values that satisfy a specific condition.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text().filter(lambda s: s.startswith("F")))
def test_filtered_text_example(value):
    print(f"Generated filtered text: {value}")
    assert value.startswith("F")
```

**Example Generated Values:**

```
Generated filtered text: "F"
Generated filtered text: "Foo"
Generated filtered text: "FBar"
Generated filtered text: "Fuzz"
```

### Mapping Values

You can use `map()` to transform generated values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers().map(lambda x: x * 2))
def test_mapped_integer_example(value):
    print(f"Generated mapped integer: {value}")
    assert value % 2 == 0
```

**Example Generated Values:**

```
Generated mapped integer: 0
Generated mapped integer: 20
Generated mapped integer: -10
Generated mapped integer: 2000
```

### Flatmapping Strategies

You can use `flatmap()` to create strategies that depend on generated values.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(min_value=1, max_value=10).flatmap(lambda n: st.lists(st.integers(), min_size=n, max_size=n)))
def test_flatmap_example(value):
    print(f"Generated flatmapped list: {value}")
    assert isinstance(value, list)
    assert len(value) >= 1
    assert len(value) <= 10
```

**Example Generated Values:**

```
Generated flatmapped list: [1, 2, 3] # list of size 3
Generated flatmapped list: [10, 20] # list of size 2
Generated flatmapped list: [5] # list of size 1
```

### OneOf Strategies

You can use `one_of()` to choose values from multiple strategies.

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.one_of(st.integers(), st.text()))
def test_one_of_example(value):
    print(f"Generated one_of value: {value}")
    assert isinstance(value, (int, str))
```

**Example Generated Values:**

```
Generated one_of value: 10
Generated one_of value: "hello"
Generated one_of value: -5
Generated one_of value: "world"
```

## Custom Strategies

You can define your own strategies using `st.builds()` or by creating a class that inherits from `hypothesis.strategies.SearchStrategy`.

## サンプル数とユニーク性

Hypothesis は、デフォルトで 100 個のテストサンプルを生成します。このサンプル数は、`@given`デコレータの`settings`引数を使用して調整できます。

### サンプル数の調整

`hypothesis.settings(max_examples=N)`を使用すると、生成するサンプル数を`N`に設定できます。

```python
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.integers(), settings=settings(max_examples=50))
def test_integer_example_with_sample_size(value):
    print(f"Generated integer: {value}")
    assert isinstance(value, int)
```

上記の例では、`max_examples=50`と設定しているため、テストは 50 個のサンプルで実行されます。

### ユニーク性について

Hypothesis は、可能な限り多様で偏りのないサンプルを生成しようとしますが、生成される値が常にユニークであるとは限りません。特に、ストラテジーが生成できる値の範囲が限られている場合や、複雑な制約条件がある場合は、重複するサンプルが生成される可能性が高まります。

もし、ユニークなサンプルを生成する必要がある場合は、以下のストラテジーや手法を検討してください。

- **`st.sets()`**: `sets()`ストラテジーは、常にユニークな要素を持つセットを生成します。
- **`st.sampled_from()`**: `sampled_from()`ストラテジーは、与えられたリストやシーケンスからユニークな要素をサンプリングします。
- **`st.filter()`**: `filter()`関数を使用して、生成されたサンプルが既存のサンプルと重複しないようにフィルタリングすることも可能ですが、効率は低い場合があります。

基本的には、Hypothesis はテストの網羅性を高めるために多様なサンプルを生成することに重点を置いており、完全なユニーク性を保証するものではないことに注意してください。ユニーク性が重要な場合は、上記の手法を適切に利用する必要があります。

### Using `st.builds()`

`st.builds()` allows you to create a strategy from a function and other strategies for its arguments.

```python
from hypothesis import given
import hypothesis.strategies as st

def create_person(name: str, age: int):
    return {"name": name, "age": age}

@given(st.builds(create_person, name=st.text(), age=st.integers(min_value=0, max_value=120)))
def test_builds_example(value):
    print(f"Generated person: {value}")
    assert isinstance(value, dict)
    assert isinstance(value["name"], str)
    assert isinstance(value["age"], int)
    assert 0 <= value["age"] <= 120
```

**Example Generated Values:**

```
Generated person: {'name': 'Alice', 'age': 30}
Generated person: {'name': 'Bob', 'age': 25}
Generated person: {'name': 'Eve', 'age': 40}
```

More details on creating custom strategies by inheriting from `SearchStrategy` will be added in future updates.

## 高度なストラテジー

Hypothesis には、組み込みのストラテジーに加えて、より高度なデータ生成を可能にするための機能がいくつか用意されています。

### 再帰的なストラテジー

`recursive()`ストラテジーを使用すると、自己参照的な構造を持つデータ (例: 木構造、リスト構造) を生成できます。

### データ依存ストラテジー

`flatmap()`ストラテジーを使用すると、以前に生成されたデータに基づいて、次のデータを生成できます。

### 状態を持つストラテジー

`stateful()`ストラテジーを使用すると、状態を保持しながらデータを生成し、より複雑なデータ生成パターンを実現できます。

## ベストプラクティス

Hypothesis を効果的に活用するためのベストプラクティスを以下に示します。

- タスクに適したストラテジーを選択する
- 複数のストラテジーを組み合わせて複雑なデータを生成する
- 可読性が高く、保守しやすいコード例を書く
- テストの実行時間とサンプル数のバランスを考慮する

## Japanese Calendar Dates (Wareki)

You can generate dates in the Japanese calendar (Wareki) by using an external library like `japanese-calendar`. First, you need to install it:

```bash
pip install japanese-calendar
```

Then, you can use the following code to generate Wareki dates:

```python
from hypothesis import given
import hypothesis.strategies as st
import datetime
from japanese_calendar import JapaneseDate

@given(st.dates())
def test_wareki_date_example(value):
    wareki_date = JapaneseDate(value)
    print(f"Generated Wareki date: {wareki_date}")
    assert isinstance(wareki_date, JapaneseDate)
```

**Example Generated Values:**

```
Generated Wareki date: JapaneseDate(1970, 1, 1, era='明治', era_year=103, zodiac='戌', long_era='明治', long_zodiac='戌年')
Generated Wareki date: JapaneseDate(2023, 10, 27, era='令和', era_year=5, zodiac='卯', long_era='令和', long_zodiac='卯年')
Generated Wareki date: JapaneseDate(2000, 5, 15, era='平成', era_year=12, zodiac='辰', long_era='平成', long_zodiac='辰年')
```

**Note:** You need to install the `japanese-calendar` library to run this example.

This document provides a comprehensive overview of data generation with Hypothesis. For more advanced features and strategies, please refer to the official Hypothesis documentation.

## DataFrame のテスト

Hypothesis を使用して pandas DataFrame をテストするためのサンプルコードを以下に示します。
Hypothesis には DataFrame 専用の組み込みストラテジーは存在しないため、既存のストラテジーを組み合わせて DataFrame を生成する必要があります。

```python
import pandas as pd
from hypothesis import given
import hypothesis.strategies as st

# 各列のデータ型に応じたストラテジーを定義
column_strategies = {
    'id': st.integers(),
    'name': st.text(),
    'age': st.integers(min_value=0, max_value=120),
    'city': st.sampled_from(['Tokyo', 'New York', 'London', 'Paris'])
}

# DataFrame を生成するストラテジー
# st.fixed_dictionaries() を使用して、各列に異なるストラテジーを適用
# st.lists() を使用して、複数の行を生成
dataframes = st.lists(
    st.fixed_dictionaries(column_strategies)
).map(pd.DataFrame)

@given(dataframes)
def test_dataframe_example(df):
    print(f"Generated DataFrame:\n{df}")
    assert isinstance(df, pd.DataFrame)
    # DataFrame に対するテストロジックをここに記述
    # 例:
    assert len(df.columns) == len(column_strategies)
    for col_name, strategy in column_strategies.items():
        assert col_name in df.columns
        # 各列のデータ型が期待通りかチェック
        # (ここでは、各ストラテジーが生成する型をチェック)
        #   assert all(isinstance(x, strategy.example()) for x in df[col_name])

```

この例では、`st.fixed_dictionaries()` を使用して、各列に異なるストラテジーを適用した辞書を生成し、それを `st.lists()` でリスト化することで、複数の行を持つ DataFrame を生成しています。
`map(pd.DataFrame)` を使用して、生成されたリストを pandas DataFrame に変換しています。

## 結論

Hypothesis は、Python のための強力なプロパティベースのテストライブラリであり、様々な種類のデータを生成するための豊富な機能を提供します。このドキュメントでは、基本的なデータ型から複雑なデータ構造まで、Hypothesis を使用して生成できるデータの例を幅広く紹介しました。

ここで紹介した例は、Hypothesis の機能のほんの一部です。より高度な機能や詳細については、公式ドキュメントを参照してください。

Hypothesis を活用することで、テストの品質と信頼性を向上させ、より堅牢なソフトウェア開発を実現できるでしょう。
