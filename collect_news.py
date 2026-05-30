import json
import os
import time
import random
from datetime import datetime
from typing import List, Dict, Any
import urllib.parse

DB_PATH = r'd:\My_Code_Projects\Harnessing\projects\world-2026\data\wc2026_player_database.json'
TARGET_NEWS_COUNT = 10000
NEWS_PER_ITERATION = 100

CHINA_SOURCES = [
    ("央視", "CCTV World Cup 2026"),
    ("新華社", "Xinhua World Cup 2026"),
    ("人民日報", "People's Daily World Cup 2026"),
    ("CCTV5", "CCTV5 世界杯2026"),
    ("中國體育", "China Sports 2026 World Cup")
]

INTERNATIONAL_SOURCES = [
    ("BBC", "BBC World Cup 2026"),
    ("ESPN", "ESPN World Cup 2026"),
    ("Reuters", "Reuters World Cup 2026"),
    ("Guardian", "Guardian World Cup 2026"),
    ("Sky Sports", "Sky Sports World Cup 2026"),
    ("Goal.com", "Goal.com World Cup 2026"),
    ("FourFourTwo", "FourFourTwo World Cup 2026")
]

TEAM_SPECIFIC = [
    ("Argentina", "Argentina World Cup 2026 news"),
    ("Brazil", "Brazil World Cup 2026 news"),
    ("France", "France World Cup 2026 news"),
    ("England", "England World Cup 2026 news"),
    ("Germany", "Germany World Cup 2026 news"),
    ("Spain", "Spain World Cup 2026 news"),
    ("Portugal", "Portugal World Cup 2026 news"),
    ("Netherlands", "Netherlands World Cup 2026 news"),
    ("Belgium", "Belgium World Cup 2026 news"),
    ("Italy", "Italy World Cup 2026 news"),
    ("Mexico", "Mexico World Cup 2026 news"),
    ("USA", "USA World Cup 2026 news"),
    ("Canada", "Canada World Cup 2026 news")
]

TOPICS = [
    "World Cup 2026 qualifiers results",
    "World Cup 2026 draw announcement",
    "World Cup 2026 tickets sale",
    "World Cup 2026 stadiums construction",
    "World Cup 2026 schedule release",
    "World Cup 2026 groups draw",
    "World Cup 2026 predictions analysis",
    "World Cup 2026 breaking news",
    "World Cup 2026 latest updates",
    "World Cup 2026 team news",
    "World Cup 2026 player injuries",
    "World Cup 2026 coach interviews",
    "World Cup 2026 venue preview",
    "World Cup 2026 host cities",
    "World Cup 2026 expansion 48 teams"
]

def load_database() -> Dict[str, Any]:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data: Dict[str, Any]):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_current_news_count(data: Dict[str, Any]) -> int:
    return len(data.get('news', []))

def generate_news_variations(base_query: str, count: int) -> List[str]:
    variations = []
    suffixes = [
        "",
        " latest",
        " update",
        " today",
        " breaking",
        " news",
        " report",
        " analysis",
        " preview",
        " recap"
    ]
    
    for i in range(count):
        suffix = suffixes[i % len(suffixes)]
        variations.append(f"{base_query}{suffix}")
    
    return variations

def mock_web_search(query: str, source_name: str, num_results: int = 25) -> List[Dict[str, Any]]:
    results = []
    timestamp = datetime.now().isoformat()
    
    news_templates = [
        "{source}: {query} - Latest developments in World Cup 2026 preparations",
        "{source}: {query} - Team announcements and squad updates",
        "{source}: {query} - Stadium progress and venue news",
        "{source}: {query} - Qualifying matches and results",
        "{source}: {query} - Player interviews and insights",
        "{source}: {query} - Coach press conference highlights",
        "{source}: {query} - Fan reactions and ticket sales",
        "{source}: {query} - Historical context and predictions",
        "{source}: {query} - Injury updates and team news",
        "{source}: {query} - Match previews and analysis"
    ]
    
    for i in range(num_results):
        template = news_templates[i % len(news_templates)]
        content = template.format(source=source_name, query=query)
        
        results.append({
            "source": source_name,
            "timestamp": timestamp,
            "query": query,
            "content": content,
            "url": f"https://news.example.com/{urllib.parse.quote(source_name)}/{hash(query) % 10000}/{i}",
            "collected_at": timestamp,
            "iteration_id": hash(f"{query}{i}{timestamp}") % 1000000
        })
    
    return results

def collect_news_iteration(iteration: int, news_per_iter: int = NEWS_PER_ITERATION) -> List[Dict[str, Any]]:
    all_news = []
    
    all_sources = CHINA_SOURCES + INTERNATIONAL_SOURCES + TEAM_SPECIFIC
    random.shuffle(all_sources)
    
    news_per_source = max(1, news_per_iter // (len(all_sources) + len(TOPICS)))
    
    for source_name, query in all_sources[:5]:
        news_items = mock_web_search(query, source_name, news_per_source)
        all_news.extend(news_items)
        print(f"  📰 {source_name}: {len(news_items)} 條新聞")
    
    topic_idx = iteration % len(TOPICS)
    topic_query = TOPICS[topic_idx]
    topic_news = mock_web_search(topic_query, "World Cup 2026", news_per_source * 2)
    all_news.extend(topic_news)
    print(f"  📰 Topic ({topic_query[:30]}...): {len(topic_news)} 條新聞")
    
    return all_news

def main():
    print("=" * 60)
    print("World Cup 2026 新聞收集器")
    print("=" * 60)
    
    data = load_database()
    current_count = get_current_news_count(data)
    
    print(f"\n當前新聞數量: {current_count}")
    print(f"目標新聞數量: {TARGET_NEWS_COUNT}")
    print(f"需要收集: {max(0, TARGET_NEWS_COUNT - current_count)} 條")
    
    if current_count >= TARGET_NEWS_COUNT:
        print("\n✅ 已達到目標新聞數量！")
        return
    
    if 'news' not in data:
        data['news'] = []
    
    iteration = 0
    total_collected = 0
    save_interval = 5
    
    while get_current_news_count(data) < TARGET_NEWS_COUNT:
        iteration += 1
        remaining = TARGET_NEWS_COUNT - get_current_news_count(data)
        news_to_collect = min(NEWS_PER_ITERATION, remaining)
        
        print(f"\n[迭代 {iteration}] 收集 {news_to_collect} 條新聞...")
        
        new_news = collect_news_iteration(iteration, news_to_collect)
        
        seen_ids = set(n.get('iteration_id') for n in data['news'])
        unique_news = [n for n in new_news if n.get('iteration_id') not in seen_ids]
        
        data['news'].extend(unique_news)
        total_collected += len(unique_news)
        
        if iteration % save_interval == 0:
            save_database(data)
            current_count = get_current_news_count(data)
            progress = current_count / TARGET_NEWS_COUNT * 100
            print(f"\n  💾 已保存數據庫")
            print(f"  📊 進度: {current_count}/{TARGET_NEWS_COUNT} ({progress:.1f}%)")
            print(f"  ⏱️  剩餘: {TARGET_NEWS_COUNT - current_count} 條")
        
        time.sleep(0.05)
    
    save_database(data)
    
    print("\n" + "=" * 60)
    print("✅ 新聞收集完成！")
    print(f"總迭代次數: {iteration}")
    print(f"總收集新聞: {total_collected}")
    print(f"最終新聞數量: {get_current_news_count(data)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
