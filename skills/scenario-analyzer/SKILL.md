---
name: scenario-analyzer
description: |
  ニュースヘッドラインを入力として18ヶ月シナリオを分析するスキル。
  scenario-analystエージェントで主分析を実行し、
  strategy-reviewerエージェントでセカンドオピニオンを取得。
  1次・2次・3次影響、推奨銘柄、レビューを含む包括的レポートを日本語で生成。
  使用例: /scenario-analyzer "Fed raises rates by 50bp"
  トリガー: ニュース分析、シナリオ分析、18ヶ月展望、中長期投資戦略
---

# Scenario Analyzer

Follow the workflow in [commands/scenario-analyzer.md](../../commands/scenario-analyzer.md).

Use the headline from `$ARGUMENTS` or prompt the user if empty.

## Rules

1. Read references under `skills/scenario-analyzer/references/` as specified in the command file.
2. Run scenario-analyst and strategy-reviewer agents per the command (second opinion required).
3. Output in **Japanese**; US-listed tickers only; 18-month horizon; scenario probabilities sum to 100%.
4. Save report to `reports/scenario_analysis_<topic>_YYYYMMDD.md`.

Do not duplicate orchestration steps here — the command file is the single source of truth.
