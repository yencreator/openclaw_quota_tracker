---
name: OpenClaw Quota Tracker
version: 1.0.0
description: >
  Tracks API quota usage for MiniMax, Claude Code, and Gemini CLI.
  Provides daily quota status reports and alerts.
author: OpenClaw Team
tags: [quota, tracking, api-usage, monitoring, minmax, claude, gemini]
---

# OpenClaw Quota Tracker (配額管家)

## Positioning
API quota tracking system for OpenClaw's AI services. Monitors usage and provides alerts.

## 3 Differentiators
1. **Multi-Platform**: Tracks MiniMax, Claude Pro, and Gemini Pro
2. **Daily Reports**: Automatic morning quota status reports
3. **Alert System**: Notifies before quota exhaustion

## Supported Services

| Service | Type | Quota |
|---------|------|-------|
| MiniMax | API (4小時) | ~50M tokens/4hr |
| Claude Pro (阿鷹) | Subscription | 無限制 |
| Gemini Pro (小龍) | Subscription | 無限制 |

## Usage

### Quick Status
```bash
python3 quota-tracker.py
# or
python3 quota-tracker.py status
```

### Full Report
```bash
python3 quota-tracker.py report
```

### Initialize
```bash
python3 quota-tracker.py init
```

## Output Example

```
📊 配額狀態快速查看
--------------------------------------------------
🔵 MiniMax: 每4小時 50,000,000 tokens
🦅 Claude Pro: 無限制 (訂閱)
🐉 Gemini Pro: 無限制 (訂閱)
--------------------------------------------------
最後更新：2026-02-25T12:00:00
```

## Configuration

Edit `data/quota.json` to customize quotas:

```json
{
  "quotas": {
    "minimax": {
      "limit": 50000000,
      "period_hours": 4
    }
  }
}
```

## Integration with OpenClaw Cron

```yaml
# Daily quota check at 8am
name: Quota Status Morning Report
schedule: "0 8 * * *"
command: python3 quota-tracker.py report
```

## Limitations

- **MiniMax**: Requires API key for actual quota check
- **Claude/Gemini Pro**: Subscription plans, no hard limits

## Dependencies
- Python 3.8+
- json (built-in)

## Location
- Source: `openclaw_quota_tracker/`
- Data: `data/quota.json`
