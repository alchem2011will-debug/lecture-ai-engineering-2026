"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask --temperature 0.2 "LoRAとは何ですか？"
    uv run python -m app.ask --interactive
    uv run python -m app.ask --interactive --temperature 0.2 "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールを使わない「素の」呼び出し。通常は1回だけ質問し、--interactive では会話履歴を保って続けて質問する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors, types

from app.config import MODEL, api_error_message, get_api_key

try:
    import readline  # noqa: F401
except ImportError:
    pass

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_chat(client, temperature: float | None = None):
    if temperature is None:
        return client.chats.create(model=MODEL)
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(temperature=temperature),
    )


def ask(
    question: str,
    temperature: float | None = None,
    *,
    chat=None,
) -> str:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        chat = create_chat(client, temperature)
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else "不明"
    output_tokens = usage.candidates_token_count if usage else "不明"
    print(f"[トークン] 入力: {input_tokens}, 出力: {output_tokens}")

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="生成時の temperature（省略時はモデルの既定値）",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="会話履歴を保って続けて質問する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    temperature_label = args.temperature if args.temperature is not None else "モデル既定"
    print(f"[temperature] {temperature_label}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = create_chat(client, args.temperature)
        if args.interactive:
            if args.question:
                print(f"[質問] {args.question}\n")
                print(ask(args.question, chat=chat))
            while True:
                question = input("\n[質問]（空欄で終了）: ")
                if not question.strip():
                    break
                print(ask(question, chat=chat))
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question, chat=chat))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
