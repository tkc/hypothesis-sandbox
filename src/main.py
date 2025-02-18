import pandas as pd
from src.domain.model import schema
from datetime import datetime

def convert_date_format(date_str: str, from_format: str, to_format: str) -> str:
    """
    指定された from_format で表現された日付文字列を、to_format の形式に変換する関数です。
    例:
      convert_date_format("2023-08-15", "%Y-%m-%d", "%d/%m/%Y") -> "15/08/2023"
    """
    dt = datetime.strptime(date_str, from_format)
    return dt.strftime(to_format)

def main():
    # サンプルデータの DataFrame を作成
    data = {"name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35]}
    df = pd.DataFrame(data)

    # Pandera を用いて DataFrame のスキーマ検証を実施
    validated_df = schema.validate(df)
    print("Validated DataFrame:")
    print(validated_df)


if __name__ == "__main__":
    main()
