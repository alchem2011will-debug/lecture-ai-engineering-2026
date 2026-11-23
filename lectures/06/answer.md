# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：`glossary_search_glossary`
- STEP 2 の [tool call]：`glossary_search_glossary({'query': '3レベル'})`
- STEP 3 の [tool call]：`fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`
- STEP 4 の [tool call]：`aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 versioning overview'})`
- 気づき・疑問：
  MCPを利用すると、自作したサーバーだけでなく、公開されているサーバーや外部で稼働しているサーバーも同じエージェントから利用できることが分かった。
  また、MCPサーバーを設定ファイルに追加するだけで、エージェントが利用できるツールを増やせることを確認した。
  接続方法には、uv、uvx、URLの3種類があることを学んだ。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装
- やったこと：
  - 基礎：
    - app/mcp_server.py に get_lecture_summary を登録し、MCPツールとして公開した。
    - また、--trace で実際にツールが呼び出されることを確認した。
  - 実装：
    - 既存の make_quiz をMCPツールとして公開した。
    - 正常な講義回と、存在しない講義回の両方で動作を確認した。
- 結果：
  - MCPツール一覧に glossary_get_lecture_summary と glossary_make_quiz が追加された。
  - 第2回を指定すると、確認問題と答えが正常に返された。
  - 第99回を指定すると、「第99回の用語が見つかりませんでした。」というメッセージが返された。
  - uv run pytest -q を実行し、21件すべてのテストが成功した。
- 気づき・疑問：
  - MCPサーバーでは、既存のPython関数を登録することで、エージェントから利用できるツールとして公開できることが分かった。
  - ツールの戻り値をモデルが受け取り、その結果をもとにユーザー向けの回答を生成する流れを理解できた。
  - 範囲外の入力に対しても、関数側で分かりやすいメッセージを返すことが重要だと分かった。
