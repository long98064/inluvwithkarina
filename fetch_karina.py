import instaloader
import json
import os
import time
import random

def fetch_instagram_data():
    L = instaloader.Instaloader()
    # Bạn có thể thêm username/password nếu muốn tránh bị chặn (tùy chọn)
    # L.login("user", "pass") 

    idols = [
        {"name": "Karina", "username": "katarinabluu"},
        {"name": "Winter", "username": "imwinter"}
    ]

    # 1. Đọc dữ liệu hiện tại để không làm mất ảnh Pinterest đã có
    data = {"profiles": []}
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except Exception as e:
            print(f"⚠️ Không đọc được data.json cũ, sẽ tạo mới. Lỗi: {e}")

    # 2. Quét dữ liệu từng Idol
    for idol_info in idols:
        print(f"--- Đang lấy bài Instagram cho: {idol_info['name']} ---")
        
        # Tìm profile cũ trong data.json để lấy lại ảnh Pinterest
        existing_profile = next((p for p in data['profiles'] if p['username'] == idol_info['username']), None)
        pin_posts = []
        if existing_profile:
            # Lọc ra những bài là Pinterest để giữ lại
            pin_posts = [p for p in existing_profile.get('posts', []) if p.get('type') == 'pinterest']

        new_insta_posts = []
        try:
            profile = instaloader.Profile.from_username(L.context, idol_info['username'])
            for count, post in enumerate(profile.get_posts()):
                if count >= 3: break
                new_insta_posts.append({
                    "type": "instagram",
                    "url": f"https://www.instagram.com/p/{post.shortcode}/"
                })
            print(f"✅ Đã lấy được 3 bài Instagram mới cho {idol_info['name']}")
        except Exception as e:
            print(f"❌ Lỗi quét Instagram: {e}. Sẽ giữ lại bài Instagram cũ nếu có.")
            if existing_profile:
                new_insta_posts = [p for p in existing_profile.get('posts', []) if p.get('type') == 'instagram']

        # Cập nhật hoặc thêm mới profile
        if existing_profile:
            existing_profile['posts'] = new_insta_posts + pin_posts
        else:
            data['profiles'].append({
                "name": idol_info['name'],
                "username": idol_info['username'],
                "posts": new_insta_posts + pin_posts
            })
        
        # Nghỉ để tránh bị quét
        time.sleep(random.uniform(10, 15))

    # 3. Lưu lại
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("🏁 Xong! Kiểm tra data.json để thấy kết quả.")

if __name__ == "__main__":
    fetch_instagram_data()
