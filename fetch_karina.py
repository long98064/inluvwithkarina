import instaloader
import json
import os

def get_karina_posts():
    L = instaloader.Instaloader()
    # Lấy profile công khai của Karina
    profile = instaloader.Profile.from_username(L.context, "katarinabluu")
    
    posts_data = []
    
    # Lấy 3 bài viết mới nhất
    for count, post in enumerate(profile.get_posts()):
        if count >= 3: break 
        
        # Tạo mã nhúng đơn giản (chỉ cần link bài viết, script của Insta sẽ lo phần còn lại)
        posts_data.append({
            "url": f"https://www.instagram.com/p/{post.shortcode}/",
            "shortcode": post.shortcode,
            "timestamp": post.date_utc.isoformat()
        })
    
    # Lưu vào file JSON
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"profiles": [{"username": "katarinabluu", "posts": posts_data}]}, f, indent=4)

if __name__ == "__main__":
    get_karina_posts()