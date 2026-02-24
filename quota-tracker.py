#!/usr/bin/env python3
"""
OpenClaw Quota Tracker - Real API Usage
Tracks actual API usage from OpenClaw session logs
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import glob

SESSIONS_DIR = Path("/home/openclaw/.openclaw/agents/main/sessions")
DATA_FILE = Path(__file__).parent / "data" / "quota.json"

# Default quota configurations
DEFAULT_QUOTAS = {
    "minimax": {
        "name": "MiniMax",
        "description": "MiniMax API (每4小時配額)",
        "quota_type": "rate_limit",
        "limit": 50000000,  # 50M tokens per 4 hours
        "period_hours": 4
    },
    "claude_pro": {
        "name": "Claude Pro (阿鷹)",
        "description": "Claude Code - Claude Pro 訂閱",
        "quota_type": "subscription",
        "limit": "unlimited",
        "note": "Pro 方案無用量限制"
    },
    "gemini_pro": {
        "name": "Gemini Pro (小龍)",
        "description": "Gemini CLI - Google AI Pro 訂閱",
        "quota_type": "subscription", 
        "limit": "unlimited",
        "note": "Pro 方案無用量限制"
    }
}

def load_data():
    """Load quota data"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"quotas": DEFAULT_QUOTAS, "usage": {}, "last_check": datetime.now().isoformat()}

def save_data(data):
    """Save quota data"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_session_usage():
    """Parse actual usage from OpenClaw session logs"""
    total_cost = 0.0
    total_input = 0
    total_output = 0
    total_tokens = 0
    session_count = 0
    
    try:
        # Get all session files
        session_files = glob.glob(str(SESSIONS_DIR / "*.jsonl"))
        
        for session_file in session_files:
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            # Look for usage in the message
                            if isinstance(data, dict):
                                # Check for Anthropic-style usage
                                if "usage" in data:
                                    usage = data.get("usage", {})
                                    if isinstance(usage, dict):
                                        cost = usage.get("cost", {})
                                        if isinstance(cost, dict):
                                            total_cost += cost.get("total", 0)
                                        total_input += usage.get("input", 0)
                                        total_output += usage.get("output", 0)
                                        total_tokens += usage.get("totalTokens", 0)
                                        session_count += 1
                                        
                                # Check nested message structure
                                content = data.get("message", {})
                                if isinstance(content, dict):
                                    usage = content.get("usage", {})
                                    if isinstance(usage, dict):
                                        cost = usage.get("cost", {})
                                        if isinstance(cost, dict):
                                            total_cost += cost.get("total", 0)
                                        total_input += usage.get("input", 0)
                                        total_output += usage.get("output", 0)
                                        total_tokens += usage.get("totalTokens", 0)
                                        session_count += 1
                        except:
                            continue
            except:
                continue
    except Exception as e:
        print(f"Error reading sessions: {e}")
    
    return {
        "total_cost": round(total_cost, 4),
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_tokens,
        "sessions": session_count
    }

def generate_report():
    """Generate quota report with REAL data"""
    # Get real usage
    usage = parse_session_usage()
    data = load_data()
    
    report = []
    report.append("=" * 60)
    report.append("📊 OpenClaw 配額報告 (真實數據)")
    report.append(f"📅 查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    # MiniMax - Real usage from sessions!
    report.append("\n🔵 MiniMax (主要模型)")
    report.append("-" * 40)
    mm = data["quotas"].get("minimax", {})
    report.append(f"   方案：{mm.get('description', 'N/A')}")
    report.append(f"   配額：{mm.get('limit', 'N/A'):,} tokens/4hr")
    report.append(f"   -----------------------------------")
    report.append(f"   📈 本次會話實際用量：")
    report.append(f"      Input:  {usage['total_input']:,} tokens")
    report.append(f"      Output: {usage['total_output']:,} tokens")
    report.append(f"      Total:  {usage['total_tokens']:,} tokens")
    report.append(f"      💰 花費: ${usage['total_cost']:.4f} USD")
    
    # Claude Pro
    report.append("\n🦅 Claude Pro (阿鷹)")
    report.append("-" * 40)
    cp = data["quotas"].get("claude_pro", {})
    report.append(f"   方案：{cp.get('description', 'N/A')}")
    report.append(f"   配額：{cp.get('limit', 'N/A')}")
    report.append(f"   狀態：✅ 訂閱方案，無用量限制")
    
    # Gemini Pro
    report.append("\n🐉 Gemini Pro (小龍)")
    report.append("-" * 40)
    gp = data["quotas"].get("gemini_pro", {})
    report.append(f"   方案：{gp.get('description', 'N/A')}")
    report.append(f"   配額：{gp.get('limit', 'N/A')}")
    report.append(f"   狀態：✅ 訂閱方案，無用量限制")
    
    # Summary
    report.append("\n" + "=" * 60)
    report.append("📈 本次 session 統計")
    report.append("-" * 40)
    report.append(f"   處理會話數：{usage['sessions']}")
    report.append(f"   總花費：${usage['total_cost']:.4f} USD")
    report.append("=" * 60)
    
    return "\n".join(report)

def quick_status():
    """Quick status check"""
    usage = parse_session_usage()
    data = load_data()
    
    print("\n📊 配額狀態 (即時)")
    print("-" * 50)
    print(f"🔵 MiniMax: ${usage['total_cost']:.4f} USD ({usage['total_tokens']:,} tokens)")
    print(f"🦅 Claude Pro: 無限制 (訂閱)")
    print(f"🐉 Gemini Pro: 無限制 (訂閱)")
    print("-" * 50)
    print(f"最後更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
