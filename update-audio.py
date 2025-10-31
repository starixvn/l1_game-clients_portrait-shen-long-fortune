import json
import os


def update_audio_config():
    # Đường dẫn đến thư mục chứa file âm thanh
    audio_folder = "src/assets/resources/audios"
    # Đường dẫn đến file config
    config_file = "src/assets/game/audios/audio-config.json"
    # Đường dẫn đến file AudioIds.ts
    audio_ids_file = "src/assets/game/audios/AudioIds.ts"

    # Đọc file config hiện tại
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    # Lấy danh sách các file mp3 và paths
    audio_data = []
    for root, _, files in os.walk(audio_folder):
        for filename in files:
            if filename.endswith('.mp3'):
                # Lấy tên file không có đuôi .mp3
                audio_name = os.path.splitext(filename)[0]
                
                # Lấy đường dẫn tương đối từ audio_folder
                rel_path = os.path.relpath(os.path.join(root, filename), audio_folder)
                # Bỏ đuôi .mp3 và chuẩn hóa dấu /
                rel_path = os.path.splitext(rel_path)[0].replace('\\', '/')
                
                audio_data.append((audio_name, rel_path))
                
                # Nếu audio chưa có trong config
                if audio_name not in config:
                    config_entry = {
                        "bundle": "resources"
                    }
                    # Chỉ thêm path nếu khác với key
                    if rel_path != audio_name:
                        config_entry["path"] = rel_path
                    config[audio_name] = config_entry
                # Nếu audio đã có trong config nhưng chưa có path và path khác key
                elif "path" not in config[audio_name] and rel_path != audio_name:
                    config[audio_name]["path"] = rel_path

    # Lưu lại file config với định dạng đẹp
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

    # Tạo nội dung cho file AudioIds.ts chỉ với enum
    ts_content = "export enum AudioIds {\n"
    for audio_name, _ in sorted(audio_data):
        # Chuyển đổi tên file thành enum key hợp lệ (thay - thành _)
        enum_key = audio_name.replace('-', '_').upper()
        ts_content += f"    {enum_key} = '{audio_name}',\n"
    ts_content += "}\n"

    # Lưu file AudioIds.ts
    with open(audio_ids_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print("Successfully updated audio-config.json and AudioIds.ts!")

if __name__ == "__main__":
    update_audio_config()