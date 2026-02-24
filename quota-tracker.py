#!/usr/bin/env python3
"""
OpenClaw Quota Tracker - Real API Usage
Tracks actual API usage from OpenClaw session logs
Only counts TODAY's usage!
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import glob

SESSIONS_DIR = Path("/home/openclaw/.openclaw/agents/main/sessions")
DATA_FILE = Path(__file__).parent / "data" / "quota.json"

# MiniMax pricing (from their website)
# Input: $15 / 1M tokens, Output: $60 / 1M tokens
MINIMAX_PRICING = {
    "input_per_million": 15.0,
    "output_per_million": 60.0
}

def load_data():
    """Load quota data"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"quotas": {}, "usage": {}, "last_check": datetime.now().isoformat()}

def parse_today_usage():
    """Parse ONLY today's usage from OpenClaw session logs"""
    today = datetime.now().strftime("%Y-%m-%d")
    today_date = datetime.now().date()
    
    total_input = 0
    total_output = 0
    total_tokens = 0
    session_count = 0
    
    try:
        session_files = glob.glob(str(SESSIONS_DIR / "*.jsonl"))
        
        for session_file in session_files:
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            
                            # Check timestamp - check BOTH UTC and local date
                            timestamp = data.get("timestamp", "")
                            if not timestamp:
                                continue
                            try:
                                # Parse as UTC
                                ts_dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                ts_date_utc = ts_dt.date()
                                ts_date_local = (ts_dt + timedelta(hours=8)).date()
                                
                                # Accept either UTC today OR local today
                                if ts_date_utc != today_date and ts_date_local != today_date:
                                    continue
                            except:
                                continue
                            
                            # Look for usage
                            usage = None
                            
                            if "usage" in data and isinstance(data["usage"], dict):
                                usage = data["usage"]
                            elif "message" in data and isinstance(data["message"], dict):
                                if "usage" in data["message"]:
                                    usage = data["message"]["usage"]
                            
                            if usage:
                                total_input += usage.get("input", 0)
                                total_output += usage.get("output", 0)
                                total_tokens += usage.get("totalTokens", 0)
                                session_count += 1
                                
                        except:
                            continue
            except:
                continue
    except Exception as e:
        print(f"Error: {e}")
    
    # Calculate cost with correct MiniMax pricing
    input_cost = (total_input / 1_000_000) * MINIMAX_PRICING["input_per_million"]
    output_cost = (total_output / 1_000_000) * MINIMAX_PRICING["output_per_million"]
    total_cost = input_cost + output_cost
    
    return {
        "total_cost": round(total_cost, 4),
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_tokens,
        "sessions": session_count
    }

def generate_report():
    """Generate quota report with TODAY's data only"""
    usage = parse_today_usage()
    
    report = []
    report.append("=" * 60)
    report.append("📊 OpenClaw 配額報告 (今日)")
    report.append(f"📅 查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    # MiniMax - Today's usage
    report.append("\n🔵 MiniMax (今日用量)")
    report.append("-" * 40)
    report.append(f"   配額：50,000,000 tokens / 4hr")
    report.append(f"   -----------------------------------")
    report.append(f"   📈 今日用量：")
    report.append(f"      Input:  {usage['total_input']:,} tokens")
    report.append(f"      Output: {usage['total_output']:,} tokens")
    report.append(f"      Total:  {usage['total_tokens']:,} tokens")
    report.append(f"      💰 花費: ${usage['total_cost']:.4f} USD")
    
    # Claude Pro
    report.append("\n🦅 Claude Pro (阿鷹)")
    report.append("-" * 40)
    report.append(f"   方案：Claude Pro 訂閱")
    report.append(f"   狀態：✅ 無用量限制")
    
    # Gemini Pro
    report.append("\n🐉 Gemini Pro (小龍)")
    report.append("-" * 40)
    report.append(f"   方案：Google AI Pro 訂閱")
    report.append(f"   狀態：✅ 無用量限制")
    
    report.append("\n" + "=" * 60)
    report.append(f"💡 計價方式：MiniMax 官網定價")
    report.append(f"   Input: $15 / 1M tokens")
    report.append(f"   Output: $60 / 1M tokens")
    report.append("=" * 60)
    
    return "\n".join(report)

def quick_status():
    """Quick status check"""
    usage = parse_today_usage()
    
    print("\n📊 今日配額 (即時)")
    print("-" * 50)
    print(f"🔵 MiniMax 今日: ${usage['total_cost']:.4f} ({usage['total_tokens']:,} tokens)")
    print(f"🦅 Claude Pro: 無限制")
    print(f"🐉 Gemini Pro: 無限制")
    print("-" * 50)

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "report":
            print(generate_report())
        elif cmd == "status":
            quick_status()
        else:
            print(f"未知指令：{cmd}")
    else:
        quick_status()

if __name__ == "__main__":
    main()
