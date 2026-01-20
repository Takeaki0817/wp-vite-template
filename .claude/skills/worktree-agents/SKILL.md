---
name: worktree-agents
description: git worktreeを使用した並列実装オーケストレーション。「並列実装」「worktree agents」「タスク分割してブランチで実装」「仕様書を並列で実装」「複数機能を同時に開発」などのリクエスト時、または仕様書・タスクリストから複数の独立タスクを同時実装する場合に使用。
---

# Worktree Agents

git worktreeで隔離された環境を作成し、複数のサブエージェントで並列実装を行う。

## ワークフロー概要

```
1. 仕様書解析 → tasks.json生成
2. worktree作成（タスクごとにブランチ）
3. サブエージェント起動（最大3並列）
4. 進捗監視
5. マージ
6. クリーンアップ
```

## Step 1: 仕様書解析

Markdown仕様書またはタスクリストを解析してtasks.jsonを生成。

```bash
python scripts/parse_specification.py <spec.md> --output tasks.json
```

対応形式:
- チェックリスト: `- [ ] タスク名`
- 番号リスト: `1. タスク名`
- セクション: `## Task: タスク名`

出力例:
```json
{
  "tasks": [
    {"id": "task-1", "name": "認証モジュール実装", "branch_name": "auth-module"},
    {"id": "task-2", "name": "決済サービス追加", "branch_name": "payment-service"}
  ],
  "parallelism": {"max_parallelism": 2, "conflict_free": true}
}
```

## Step 2: Worktree作成

```bash
python scripts/worktree_manager.py setup tasks.json --base-branch feature/impl
```

各タスク用に隔離されたworktreeとブランチを作成。状態は`.worktree-agents/state.json`に保存。

確認:
```bash
python scripts/worktree_manager.py list
python scripts/worktree_manager.py status
```

## Step 3: サブエージェント起動

Task toolで最大3つのエージェントをバックグラウンドで起動。

各エージェントへの指示は`references/task-prompt-template.md`を参照。

```
For each task (max 3 concurrent):
  Task tool with:
    - subagent_type: "general-purpose"
    - run_in_background: true
    - prompt: [task-prompt-template.mdをベースに変数を埋める]
```

重要:
- 各エージェントは自分のworktreeパスでのみ作業
- 完了時は`.agent-done`マーカーを作成
- 失敗時は`.agent-failed`マーカーを作成

## Step 4: 進捗監視

```bash
# 現在の状態を確認
python scripts/progress_monitor.py

# 自動更新（30秒間隔）
python scripts/progress_monitor.py --watch

# JSON出力
python scripts/progress_monitor.py --json
```

表示内容:
- 各タスクのステータス（pending/in_progress/completed/failed）
- コミット数
- 未コミット変更
- 進捗率

## Step 5: マージ

### 分析

```bash
python scripts/merge_assistant.py analyze
```

コンフリクト可能性、推奨マージ順序を表示。

### 自動マージ

コンフリクトなしの場合:
```bash
python scripts/merge_assistant.py merge --strategy sequential
```

コンフリクト発生時は停止し、手動解決を案内。

### コンフリクト解決

```bash
python scripts/merge_assistant.py resolve
```

詳細は`references/merge-strategies.md`を参照。

## Step 6: クリーンアップ

```bash
python scripts/worktree_manager.py cleanup
```

オプション:
- `--force`: 未コミット変更があっても削除
- `--keep-branches`: ブランチは残す

## 設定ファイル（オプション）

プロジェクトルートに`.worktree-agents.json`:
```json
{
  "worktree_dir": ".worktree-agents",
  "branch_prefix": "wt-agent/",
  "max_concurrent": 3
}
```

## エラーハンドリング

### エージェント失敗時
1. `progress_monitor.py`で失敗を確認
2. 該当worktreeで問題を修正
3. `.agent-failed`を削除、修正後に`.agent-done`を作成
4. または`cleanup --force`で中断

### Worktree作成失敗時
```bash
python scripts/worktree_manager.py setup tasks.json --force
```

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| `parse_specification.py` | 仕様書→tasks.json変換 |
| `worktree_manager.py` | worktreeライフサイクル管理 |
| `progress_monitor.py` | 進捗監視 |
| `merge_assistant.py` | マージ分析・実行 |

## リファレンス

- `references/task-prompt-template.md` - サブエージェント用プロンプトテンプレート
- `references/merge-strategies.md` - マージ・コンフリクト解決パターン
