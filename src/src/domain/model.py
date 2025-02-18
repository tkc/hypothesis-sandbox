import pandera as pa
from pandera import Column, DataFrameSchema

# DataFrameSchema を用いて、対象の DataFrame のスキーマを定義します。
# このスキーマでは、"name" カラムと "age" カラムの条件を指定しています。
schema = DataFrameSchema(
    {
        # "name" カラムは文字列型 (str) である必要があります。
        # また、各要素に対してチェックを行い、文字列の長さが0より大きい（空文字ではない）ことを検証します。
        # "nullable=False" で、NULL 値を許容しないことを指定しています。
        "name": Column(
            str,
            checks=pa.Check(lambda s: len(s) > 0, element_wise=True),
            nullable=False,
        ),
        # "age" カラムは整数型 (int) である必要があります。
        # チェック関数により、各要素が 0 より大きい（つまり正の整数）であることを検証します。
        # "nullable=False" により、このカラムに NULL 値が存在しないことを保証します。
        "age": Column(
            int,
            checks=pa.Check(lambda x: x > 0),
            nullable=False,
        ),
    }
)
