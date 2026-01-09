import instaloader
import json
import time
import random

def fetch_data():
    L = instaloader.Instaloader()
    # Danh sách
    idols = [
        {"name": "Karina", "username": "katarinabluu"},
        {"name": "Winter", "username": "imwinter"}
    ]
    
    final_data = {"profiles": []}

    for idol in idols:
        print(f"--- Đang quét: {idol['name']} ---")
        try:
            profile = instaloader.Profile.from_username(L.context, idol['username'])
            posts_data = []
            for count, post in enumerate(profile.get_posts()):
                if count >= 3: break 
                posts_data.append({
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "shortcode": post.shortcode
                })
            
            final_data["profiles"].append({
                "name": idol['name'],
                "username": idol['username'],
                "posts": posts_data
            })
            print(f"Thành công lấy {len(posts_data)} bài của {idol['name']}")
            time.sleep(random.uniform(10, 20)) # Nghỉ để tránh bị chặn
            
        except Exception as e:
            print(f"Lỗi tại {idol['name']}: {e}")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
