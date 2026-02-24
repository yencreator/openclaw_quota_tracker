#!/usr/bin/env python3
"""
OpenClaw Quota Tracker - CODING PLAN VERSION
Tracks MiniMax Coding Plan prompts remaining
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "quota.json"

def load_data():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "coding_plan": {
            "total_prompts": 5000,  # Default for Pro plan
            "remaining_prompts": None,
            "last_updated": None
        }
    }

def save_data(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_prompts(remaining):
    data = load_data()
    data["coding_plan"]["remaining_prompts"] = remaining
    data["coding_plan"]["last_updated"] = datetime.now().isoformat()
    save_data(data)
    print(f"✅ 已更新：剩余 {remaining} prompts")

def generate_report():
    data = load_data()
    cp = data.get("coding_plan", {})
    
    remaining = cp.get("remaining_prompts", "未設定")
    total = cp.get("total_prompts", 5000)
    last = cp.get("last_updated", "從未")
    
    # Calculate used
    if remaining != "未設定" and remaining is not None:
        used = total - remaining
        pct = (used / total) * 100
    else:
        used = "未知"
        pct = 0
    
    report = []
    report.append("=" * 60)
    report.append("📊 OpenClaw 配額報告 (Coding Plan)")
    report.append(f"📅 查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    # MiniMax Coding Plan
    report.append("\n🔵 MiniMax Coding Plan")
    report.append("-" * 40)
    report.append(f"   方案：Pro (5000 prompts/5hr)")
    report.append(f"   配額：{total} prompts / 5小時")
    report.append(f"   -----------------------------------")
    if remaining != "未設定" and remaining is not None:
        report.append(f"   剩餘：{remaining} prompts")
        report.append(f"   已用：{used} prompts ({pct:.1f}%)")
        report.append(f"   更新：{last}")
    else:
        report.append(f"   ⚠️  尚未設定，請輸入剩餘prompts")
    
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
    report.append("💡 使用方式：")
    report.append("   1. 訪問 https://platform.minimax.io/user-center/payment/coding-plan")
    report.append("   2. 查看剩餘 prompts")
    report.append("   3. 輸入指令更新：quota-tracker.py update <數字>")
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "report":
            print(generate_report())
        elif cmd == "update":
            if len(sys.argv) > 2:
                remaining = int(sys.argv[2])
                update_prompts(remaining)
            else:
                print("用法: quota-tracker.py update <剩餘prompts>")
        else:
            print(f"未知指令：{cmd}")
    else:
        print(generate_report())

if __name__ == "__main__":
    main()
