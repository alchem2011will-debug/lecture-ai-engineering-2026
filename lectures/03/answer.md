# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：素のLLMは講座固有の情報を正確に説明できなかった一方、エージェントは用語集を参照して正しい定義を回答できた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - search_glossary({'query': 'QLoRA'})
  - search_glossary({'query': 'LoRA'})
  - make_quiz({'lecture': 2})
- 1つの質問での LLM 呼び出し回数（`requests`）：
  - LoRAとQLoRAの質問：2回
  - 第2回の確認問題：2回
- 追加したツールと、docstring に書いた説明：
  - ツール名：make_quiz
  - 指定した回の講義内容から確認問題を1問作る。
  - ユーザーが講義内容についてクイズや確認問題を求めたときに使う。
  - lectureに対象の講義回を指定する。

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
  - 基礎：
    - `make_quiz` のdocstringを変更し、どのような質問で使うツールなのかを具体的に説明した。
  - 実装：
    - `save_learning_log` ツールを実装した。
    - `requires_approval=True` を設定し、保存前にユーザーの承認を求めるようにした。
  - 発展：
    - Google ADKを使って glossary_agent を作成した。
    - Pydantic AI版の INSTRUCTIONS と、search_glossary、get_lecture_summary、make_quiz の3つのツールを再利用した。
    - ADKの Agent にモデル名、エージェント名、指示文、ツールを設定した。
- 結果：
  - 基礎：
    - `--trace` で `make_quiz({'lecture': 2})` が呼び出されることを確認した。
    - LLMのリクエスト回数は2回、ツール呼び出し回数は1回だった。
    - 変更前後でツールの選択結果に変化はなかった。
  - 実装：
    - `n` を入力すると保存が拒否された。
    - `y` を入力すると learning_log/ にMarkdownファイルが保存された。
  - 発展：
    - `PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent` でエージェントを起動できた。
    - 「AIE2026の宿題にある3レベルとは何か」という質問に対して、用語集を参照した正しい回答が得られた。
- 気づき・疑問：
  - 基礎：
    - docstringはLLMがツールを選択する際の判断材料になる。
    - 説明を変更しても、必ずツールの選択結果が変わるわけではない。
  - 実装：
    - AIにファイル保存などの操作を任せる場合、人間の承認を挟むことで意図しない操作を防げる。
  - 発展：
    - Pydantic AIでは `agent.tool_plain()` でツールを登録するが、Google ADKでは `Agent` の `tools` 引数に関数を渡すという違いがあった。
    - 同じ指示文とツールを再利用することで、異なるフレームワークでも同様のエージェントを構築できることが分かった。
