"""
更新 wc2026_player_database.json 添加 is_xfactor 字段
rating >= 85 的球員標記為 X-Factor
"""

import json
import os
from datetime import datetime


def update_xfactor_field(data_path: str) -> dict:
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    xfactor_count = 0
    total_players = 0
    
    for team_name, team_data in data.get("teams", {}).items():
        if "players" not in team_data:
            continue
        
        for player in team_data["players"]:
            total_players += 1
            rating = player.get("rating", 0)
            player["is_xfactor"] = rating >= 85
            
            if rating >= 85:
                xfactor_count += 1
    
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    if "xfactor_players" not in data:
        data["xfactor_players"] = []
    
    existing_names = {p.get("name") for p in data["xfactor_players"]}
    
    for team_name, team_data in data.get("teams", {}).items():
        if "players" not in team_data:
            continue
        
        for player in team_data["players"]:
            if player.get("is_xfactor") and player.get("name") not in existing_names:
                data["xfactor_players"].append({
                    "name": player.get("name"),
                    "team": team_name,
                    "rating": player.get("rating"),
                    "position": player.get("position"),
                    "identified_at": datetime.now().isoformat()
                })
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {
        "total_players": total_players,
        "xfactor_count": xfactor_count,
        "xfactor_ratio": xfactor_count / total_players if total_players > 0 else 0
    }


if __name__ == "__main__":
    data_path = "data/wc2026_player_database.json"
    
    result = update_xfactor_field(data_path)
    
    print(f"✅ 更新完成")
    print(f"總球員數：{result['total_players']}")
    print(f"X-Factor 球員數：{result['xfactor_count']}")
    print(f"X-Factor 比例：{result['xfactor_ratio']*100:.2f}%")
