import datetime
from hypothesis import given, settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition, invariant

# -------------------------------------------
# 1. 境界値テスト（Boundary Value Testing）
# -------------------------------------------
# 例: 整数の境界値（最小値、最大値付近）のテスト

@given(x=st.integers(min_value=-10, max_value=10))
def test_integer_boundaries(x):
    # ここでは、整数 x が -10～10 の範囲内にあることを確認するテスト例
    assert -10 <= x <= 10

# -------------------------------------------
# 2. エッジケーステスト（Edge Case Testing）
# -------------------------------------------
# 例: 極端に長い文字列や特殊文字を含む文字列のテスト

@given(s=st.text(min_size=1000, max_size=2000))
def test_long_string(s):
    # 長さが1000以上2000以下の文字列を生成し、長さが条件通りかを確認
    assert 1000 <= len(s) <= 2000

@given(s=st.text(alphabet=st.characters(blacklist_categories=["Cs"]), min_size=0))
def test_special_characters(s):
    # 制御文字などが除外された文字を利用して文字列を生成し、文字列が正常に処理できるか確認
    # ここでは単に型のチェックを実施
    assert isinstance(s, str)

# -------------------------------------------
# 3. ランダム入力テスト（Random Input Testing）
# -------------------------------------------
# 例: ランダムな整数と文字列の組み合わせをテスト

@given(x=st.integers(), s=st.text())
def test_random_input(x, s):
    # ここでは、x が整数で s が文字列であることを確認
    assert isinstance(x, int)
    assert isinstance(s, str)

# -------------------------------------------
# 4. 組み合わせテスト（Combinatorial Testing）
# -------------------------------------------
# 例: 2つのパラメータの組み合わせで、ある計算結果が一定条件を満たすか

@given(a=st.integers(min_value=0, max_value=100),
       b=st.integers(min_value=0, max_value=100))
def test_sum_combinations(a, b):
    # 例えば、a と b の和が 0～200 の範囲に収まることを検証
    s = a + b
    assert 0 <= s <= 200

# -------------------------------------------
# 5. カスタム生成（Composite Strategy）
# -------------------------------------------
# 例: 複雑な辞書データを生成する
from hypothesis.strategies import composite

@composite
def person_strategy(draw):
    # 名前は1文字以上、年齢は0～120の範囲とする
    name = draw(st.text(min_size=1))
    age = draw(st.integers(min_value=0, max_value=120))
    # 日付は誕生日として、1900年から今日までの範囲で生成
    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date.today()
    # 日付の差分（天数）を生成して、誕生日とする
    days_between = (end_date - start_date).days
    random_days = draw(st.integers(min_value=0, max_value=days_between))
    birthday = start_date + datetime.timedelta(days=random_days)
    return {"name": name, "age": age, "birthday": birthday.isoformat()}

@given(person=person_strategy())
def test_person_data(person):
    # person データが辞書形式で、名前、年齢、誕生日があることを検証
    assert "name" in person and len(person["name"]) > 0
    assert "age" in person and 0 <= person["age"] <= 120
    # birthday は ISO 8601 形式の日付文字列であることを簡単に検証
    assert isinstance(person["birthday"], str)
    # さらに、datetimeに変換できるか確認
    dt = datetime.datetime.fromisoformat(person["birthday"])
    assert isinstance(dt, datetime.datetime)

# -------------------------------------------
# 6. 状態を持つテスト（Stateful Testing）
# -------------------------------------------
# 例: 簡単なスタック（LIFO）の実装に対する状態遷移テスト

class StackStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.stack = []

    @rule(item=st.integers())
    def push(self, item):
        self.stack.append(item)

    @precondition(lambda self: len(self.stack) > 0)
    @rule()
    def pop(self):
        popped = self.stack.pop()
        # popした値は、最後にpushした値と一致するはず（LIFO）
        assert popped == self.stack[-1] if self.stack else popped

    @invariant()
    def invariant_stack_not_negative(self):
        # スタックの長さは常に0以上
        assert len(self.stack) >= 0
