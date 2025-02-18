import pandas as pd
import pytest
from hypothesis import given, strategies as st
from pandera.errors import SchemaError
from src.domain.model import schema
from src.main import convert_date_format
import datetime  # モジュール全体をインポートする

# int64 の最大値: 2^63 - 1
INT64_MAX = 9223372036854775807

# 1行分の有効なデータを生成する Hypothesis ストラテジー
valid_row_strategy = st.fixed_dictionaries({
    "name": st.text(min_size=1),                        # 空文字は除外
    "age": st.integers(min_value=1, max_value=INT64_MAX)  # 1以上かつ int64 範囲内
})

# 複数行からなる DataFrame を生成するストラテジー（必ず1行以上）
valid_df_strategy = st.lists(valid_row_strategy, min_size=1).map(pd.DataFrame)

@given(df=valid_df_strategy)
def test_dataframe_schema(df: pd.DataFrame):
    """
    Hypothesis により生成された有効な DataFrame が、
    Pandera のスキーマに合致するかを検証するテスト。
    """
    validated_df = schema.validate(df)

    # 必須カラムの存在確認
    assert "name" in validated_df.columns, "Column 'name' is missing in the validated DataFrame"
    assert "age" in validated_df.columns, "Column 'age' is missing in the validated DataFrame"

    # 生成された値が条件に合致していることの確認
    # 全ての名前が空でないこと
    assert all(isinstance(val, str) and len(val) > 0 for val in validated_df["name"]), "Some 'name' values are empty"
    # 全ての age が1以上であること
    assert all(isinstance(val, int) and val >= 1 for val in validated_df["age"]), "Some 'age' values are less than 1"
    # 入力と検証後の DataFrame の形状が一致していることの確認
    assert validated_df.shape == df.shape, "Validated DataFrame shape does not match input shape"

def test_invalid_dataframe_missing_column():
    """
    無効な DataFrame のテスト：必須カラムの一部が欠落している場合にエラーが発生するか検証します。
    """
    # "age" カラムを欠いた DataFrame を作成
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"]
    })
    with pytest.raises(SchemaError):
        schema.validate(df)

def test_invalid_dataframe_wrong_value():
    """
    無効な DataFrame のテスト：条件に反する値（例: 空文字や0以下の数値）がある場合にエラーが発生するか検証します。
    """
    # 空文字の名前と0以下の age を持つ DataFrame
    df = pd.DataFrame({
        "name": ["", "Bob", "Charlie"],
        "age": [0, -5, 35]
    })
    with pytest.raises(SchemaError):
        schema.validate(df)

def test_valid_dataframe_dtypes():
    """
    有効な DataFrame の検証後に、各カラムのデータ型が正しいことを確認するテストです。
    """
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [30, 25, 35]
    })

    validated_df = schema.validate(df)
    # Pandas の型として、"age" は int64 になるはず
    assert validated_df["age"].dtype == "int64", f"Expected age dtype to be int64, got {validated_df['age'].dtype}"
    # "name" は object 型になるはず
    assert validated_df["name"].dtype == "object", f"Expected name dtype to be object, got {validated_df['name'].dtype}"


# 日付文字列を生成するためのストラテジー
# ここでは、年は1900～2100、月は1～12、日については簡略化のため1～28（各月必ず有効な日付となるように）を生成します。
@given(
    year=st.integers(min_value=1900, max_value=2100),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=28)
)
def test_convert_date_format_valid(year, month, day):
    from_format = "%Y-%m-%d"
    to_format = "%d/%m/%Y"

    # 日付オブジェクトを生成して、元の日付文字列を作成
    date_obj = datetime.date(year, month, day)
    original_date_str = date_obj.strftime(from_format)

    # 関数を実行して変換後の文字列を取得
    converted_date_str = convert_date_format(original_date_str, from_format, to_format)

    # 期待する出力を生成（date_obj を to_format でフォーマット）
    expected_date_str = date_obj.strftime(to_format)

    assert converted_date_str == expected_date_str, (
        f"変換結果が期待通りではありません: {converted_date_str} != {expected_date_str}"
    )

# 無効な日付文字列に対して例外が発生することを検証するテスト
def test_convert_date_format_invalid():
    from_format = "%Y-%m-%d"
    to_format = "%d/%m/%Y"

    # 存在しない日付文字列（例: 2023-02-30）を指定
    invalid_date_str = "2023-02-30"

    with pytest.raises(ValueError):
        # datetime.strptime が無効な日付の場合、ValueError を投げるのでそれを検証します。
        convert_date_format(invalid_date_str, from_format, to_format)
