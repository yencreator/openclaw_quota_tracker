#!/usr/bin/env python3
"""
OpenClaw Quota Tracker
Tracks API quota usage for MiniMax, Claude Code, and Gemini CLI
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "quota.json"

# Default quota configurations
DEFAULT_QUOTAS = {
    "minimax": {
        "name": "MiniMax",
        "description": "MiniMax API (4小時配額)",
        "quota_type": "rate_limit",
        "limit": 50000000,  # 50M tokens per 4 hours (example)
        "period_hours": 4,
        "reset_at": None
    },
    "claude_pro": {
        "name": "Claude Pro (阿鷹)",
        "description": "Claude Code - Claude Pro 訂閱",
        "quota_type": "subscription",
        "limit": "unlimited",
        "period_hours": None,
        "note": "Pro 方案無用量限制，但可用次數追蹤"
    },
    "gemini_pro": {
        "name": "Gemini Pro (小龍)",
        "description": "Gemini CLI - Google AI Pro 訂閱",
        "quota_type": "subscription", 
        "limit": "unlimited",
        "period_hours": None,
        "note": "Pro 方案無用量限制"
    }
}

def load_data():
    """Load quota data"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "quotas": DEFAULT_QUOTAS,
        "usage": {},
        "last_check": datetime.now().isoformat()
    }

def save_data(data):
    """Save quota data"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_minimax_quota():
    """Check MiniMax quota (simulated - requires API call)"""
    # Note: MiniMax API would need actual API call to get real quota
    # This is a placeholder that can be enhanced
    return {
        "status": "unknown",
        "used": 0,
        "limit": DEFAULT_QUOTAS["minimax"]["limit"],
        "note": "需要 MiniMax API Key 才能查詢實際用量"
    }

def get_session_usage():
    """Get usage from OpenClaw sessions"""
    sessions_file = Path("/home/openclaw/.openclaw/agents/main/sessions/sessions.json")
    if sessions_file.exists():
        with open(sessions_file, "r") as f:
            sessions = json.load(f)
        return sessions
    return {}

def generate_report():
    """Generate quota report"""
    data = load_data()
    usage = get_session_usage()
    
    report = []
    report.append("=" * 60)
    report.append("📊 OpenClaw 配額報告")
    report.append(f"📅 查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    # MiniMax
    report.append("\n🔵 MiniMax (每4小時配額)")
    report.append("-" * 40)
    mm_quota = data["quotas"].get("minimax", {})
    report.append(f"   方案：{mm_quota.get('description', 'N/A')}")
    report.append(f"   配額：{mm_quota.get('limit', 'N/A')} tokens/4hr")
    report.append(f"   狀態：⚠️ 需設定 API Key 才能查詢實際用量")
    
    # Claude Pro
    report.append("\n🦅 Claude Pro (阿鷹)")
    report.append("-" * 40)
    cp_quota = data["quotas"].get("claude_pro", {})
    report.append(f"   方案：{cp_quota.get('description', 'N/A')}")
    report.append(f"   配額：{cp_quota.get('limit', 'N/A')}")
    report.append(f"   狀態：✅ 訂閱方案，無用量限制")
    
    # Gemini Pro
    report.append("\n🐉 Gemini Pro (小龍)")
    report.append("-" * 40)
    gp_quota = data["quotas"].get("gemini_pro", {})
    report.append(f"   方案：{gp_quota.get('description', 'N/A')}")
    report.append(f"   配額：{gp_quota.get('limit', 'N/A')}")
    report.append(f"   狀態：✅ 訂閱方案，無用量限制")
    
    # Session stats
    report.append("\n📈 本次會話統計")
    report.append("-" * 40)
    if usage:
        total_tokens = sum(s.get("tokens", 0) for s in usage.values() if isinstance(s, dict))
        report.append(f"   活躍會話數：{len(usage)}")
        report.append(f"   總 Token：{total_tokens:,}")
    else:
        report.append("   無法讀取會話資料")
    
    report.append("\n" + "=" * 60)
    report.append("💡 說明：")
    report.append("   - MiniMax：需要 API Key 才能查詢實際用量")
    report.append("   - Claude/Gemini Pro：訂閱方案，原則上無限制")
    report.append("   - 本系統追蹤會話Token使用量作為參考")
    report.append("=" * 60)
    
    return "\n".join(report)

def quick_status():
    """Quick status check"""
    data = load_data()
    
    print("\n📊 配額狀態快速查看")
    print("-" * 50)
    print(f"🔵 MiniMax: 每4小時 {data['quotas']['minimax']['limit']:,} tokens")
    print(f"🦅 Claude Pro: 無限制 (訂閱)")
    print(f"🐉 Gemini Pro: 無限制 (訂閱)")
    print("-" * 50)
    print(f"最後更新：{data.get('last_check', 'N/A')}")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "report":
            print(generate_report())
        elif cmd == "status":
            quick_status()
        elif cmd == "init":
            data = load_data()
            print("✅ 配額資料已初始化")
            quick_status()
        else:
            print(f"未知指令：{cmd}")
    else:
        quick_status()

if __name__ == "__main__":
    main()
