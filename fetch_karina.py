import instaloader
import json
import time
import random

def fetch_data():
    L = instaloader.Instaloader()
    # Danh sách các idol bạn muốn theo dõi
    idols = [
        {"name": "Karina", "username": "katarinabluu"},
        {"name": "Winter", "username": "imwinter"}
    ]
    
    final_data = {"profiles": []}

    for idol in idols:
        print(f"Đang lấy dữ liệu của {idol['name']}...")
        try:
            profile = instaloader.Profile.from_username(L.context, idol['username'])
            posts_data = []
            
            for count, post in enumerate(profile.get_posts()):
                if count >= 3: break 
                posts_data.append({
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "shortcode": post.shortcode,
                    "timestamp": post.date_utc.isoformat()
                })
            
            final_data["profiles"].append({
                "name": idol['name'],
                "username": idol['username'],
                "posts": posts_data
            })
            
            # Nghỉ ngơi một chút để tránh bị Instagram chặn (rất quan trọng khi quét nhiều người)
            time.sleep(random.uniform(5, 10))
            
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu {idol['name']}: {e}")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
