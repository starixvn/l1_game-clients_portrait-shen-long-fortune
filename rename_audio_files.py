import os
import shutil
import sys


def get_audio_files(directory):
    """Lấy danh sách tất cả file audio (.mp3 và .mp3.meta) trong thư mục"""
    audio_files = []
    if not os.path.exists(directory):
        return audio_files
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.mp3.meta'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                audio_files.append((file, file_path, rel_path))
    
    return audio_files

def rename_file_safely(old_path, new_path):
    """Rename file an toàn với kiểm tra tồn tại"""
    try:
        if os.path.exists(old_path):
            # Tạo thư mục đích nếu chưa tồn tại
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Nếu file đích đã tồn tại, xóa nó trước
            if os.path.exists(new_path):
                os.remove(new_path)
            
            os.rename(old_path, new_path)
            return True
        else:
            print(f"⚠️ File không tồn tại: {old_path}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi rename {old_path} -> {new_path}: {e}")
        return False

def copy_file_safely(src_path, dest_path):
    """Copy file an toàn"""
    try:
        if os.path.exists(src_path):
            # Tạo thư mục đích nếu chưa tồn tại
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.copy2(src_path, dest_path)
            return True
        else:
            print(f"⚠️ File không tồn tại để copy: {src_path}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi copy {src_path} -> {dest_path}: {e}")
        return False

def delete_file_safely(file_path):
    """Xóa file an toàn"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"❌ Lỗi khi xóa {file_path}: {e}")
        return False

def process_repo_audio_files(repo_path, repo_name):
    """Xử lý rename audio files cho một repository"""
    print(f"\n=== 🎵 Đang xử lý repository: {repo_name} ===")
    
    audios_path = os.path.join(repo_path, "src", "assets", "resources", "audios")
    
    if not os.path.exists(audios_path):
        print(f"❌ Không tìm thấy thư mục audios: {audios_path}")
        return False
    
    print(f"📁 Thư mục audios: {audios_path}")
    
    rename_count = 0
    delete_count = 0
    copy_count = 0
    
    # Mapping các file cần rename
    rename_mapping = {
        # Trong background-music folder
        os.path.join("background-music", "song1.mp3"): os.path.join("background-music", "bgm-main.mp3"),
        os.path.join("background-music", "song1.mp3.meta"): os.path.join("background-music", "bgm-main.mp3.meta"),
        
        # Các file khác trong audios
        "multiplier.mp3": "multiplier-land.mp3",
        "multiplier.mp3.meta": "multiplier-land.mp3.meta",
        "multiplier-appear.mp3": "multiplier-activate.mp3",
        "multiplier-appear.mp3.meta": "multiplier-activate.mp3.meta",
        "reelstop1.mp3": "reel-stop.mp3",
        "reelstop1.mp3.meta": "reel-stop.mp3.meta",
        "increment.mp3": "wincount-increment.mp3",
        "increment.mp3.meta": "wincount-increment.mp3.meta",
        "increment-stop.mp3": "wincount-stop.mp3",
        "increment-stop.mp3.meta": "wincount-stop.mp3.meta",
        "coin.mp3": "win.mp3",
        "coin.mp3.meta": "win.mp3.meta"
    }
    
    # Files cần xóa
    files_to_delete = [
        "reelstop2.mp3", "reelstop2.mp3.meta",
        "reelstop3.mp3", "reelstop3.mp3.meta", 
        "reelstop4.mp3", "reelstop4.mp3.meta",
        "reelstop5.mp3", "reelstop5.mp3.meta",
        "big-win-increment-ended.mp3", "big-win-increment-ended.mp3.meta"
    ]
    
    # 1. Thực hiện rename các file theo mapping
    print("\n🔄 Đang rename các file...")
    for old_name, new_name in rename_mapping.items():
        old_path = os.path.join(audios_path, old_name)
        new_path = os.path.join(audios_path, new_name)
        
        if os.path.exists(old_path):
            if rename_file_safely(old_path, new_path):
                print(f"  ✅ {old_name} -> {new_name}")
                rename_count += 1
            else:
                print(f"  ❌ Không thể rename: {old_name}")
    
    # 2. Xử lý winning-level-up.mp3 - duplicate thành mega-win và super-win
    print("\n📋 Đang duplicate winning-level-up...")
    winning_level_up_mp3 = os.path.join(audios_path, "winning-level-up.mp3")
    winning_level_up_meta = os.path.join(audios_path, "winning-level-up.mp3.meta")
    
    if os.path.exists(winning_level_up_mp3):
        # Tạo mega-win
        mega_win_mp3 = os.path.join(audios_path, "mega-win.mp3")
        mega_win_meta = os.path.join(audios_path, "mega-win.mp3.meta")
        
        if copy_file_safely(winning_level_up_mp3, mega_win_mp3):
            print(f"  ✅ winning-level-up.mp3 -> mega-win.mp3")
            copy_count += 1
        
        if os.path.exists(winning_level_up_meta):
            if copy_file_safely(winning_level_up_meta, mega_win_meta):
                print(f"  ✅ winning-level-up.mp3.meta -> mega-win.mp3.meta")
                copy_count += 1
        
        # Rename original thành super-win
        super_win_mp3 = os.path.join(audios_path, "super-win.mp3")
        super_win_meta = os.path.join(audios_path, "super-win.mp3.meta")
        
        if rename_file_safely(winning_level_up_mp3, super_win_mp3):
            print(f"  ✅ winning-level-up.mp3 -> super-win.mp3")
            rename_count += 1
        
        if os.path.exists(winning_level_up_meta):
            if rename_file_safely(winning_level_up_meta, super_win_meta):
                print(f"  ✅ winning-level-up.mp3.meta -> super-win.mp3.meta")
                rename_count += 1

    # 2.1. Xử lý click.mp3 - duplicate thành click-symbol
    print("\n📋 Đang duplicate click...")
    click_mp3 = os.path.join(audios_path, "click.mp3")
    click_meta = os.path.join(audios_path, "click.mp3.meta")
    
    if os.path.exists(click_mp3):
        # Tạo click-symbol
        click_symbol_mp3 = os.path.join(audios_path, "click-symbol.mp3")
        click_symbol_meta = os.path.join(audios_path, "click-symbol.mp3.meta")
        
        if copy_file_safely(click_mp3, click_symbol_mp3):
            print(f"  ✅ click.mp3 -> click-symbol.mp3")
            copy_count += 1
        
        if os.path.exists(click_meta):
            if copy_file_safely(click_meta, click_symbol_meta):
                print(f"  ✅ click.mp3.meta -> click-symbol.mp3.meta")
                copy_count += 1


   
        
    # 3. Xóa các file reelstop2-5
    print("\n🗑️ Đang xóa các file reelstop2-5...")
    for file_to_delete in files_to_delete:
        file_path = os.path.join(audios_path, file_to_delete)
        if delete_file_safely(file_path):
            print(f"  ✅ Đã xóa: {file_to_delete}")
            delete_count += 1
    
    # Kết quả cho repository này
    print(f"\n📊 Kết quả cho {repo_name}:")
    print(f"  🔄 Renamed: {rename_count} files")
    print(f"  📋 Copied: {copy_count} files")
    print(f"  🗑️ Deleted: {delete_count} files")
    
    return rename_count > 0 or copy_count > 0 or delete_count > 0

def scan_reference_audio_files():
    """Scan reference audio files từ slot-game/street-warrior-client"""
    print("🔍 === SCANNING REFERENCE AUDIO FILES ===")
    
    reference_path = os.path.join("..", "slot-game", "street-warrior-client", "src", "assets", "resources", "audios")
    
    if not os.path.exists(reference_path):
        print(f"❌ Không tìm thấy thư mục reference: {reference_path}")
        return
    
    print(f"📁 Reference path: {reference_path}")
    
    audio_files = get_audio_files(reference_path)
    print(f"🎵 Tổng cộng {len(audio_files)} audio files trong reference:")
    
    for filename, filepath, relpath in sorted(audio_files):
        print(f"  📄 {relpath}")

def main():
    """Main function"""
    print("🎵 === AUDIO FILES RENAMING SCRIPT ===")
    print("Mục tiêu: Rename audio files trong repository hiện tại theo pattern từ slot-game/street-warrior-client")
    
    # 1. Scan reference files
    scan_reference_audio_files()
    
    # 2. Kiểm tra repository hiện tại
    current_repo_path = "."
    current_repo_name = os.path.basename(os.getcwd())
    
    print(f"\n🔍 === CHECKING CURRENT REPOSITORY ===")
    print(f"📁 Current repository: {current_repo_name}")
    print(f"📂 Path: {os.path.abspath(current_repo_path)}")
    
    # Kiểm tra có thư mục audios không
    audios_path = os.path.join(current_repo_path, "src", "assets", "resources", "audios")
    
    if not os.path.exists(audios_path):
        print(f"❌ Không tìm thấy thư mục audios trong repository hiện tại: {audios_path}")
        print("💡 Hãy đảm bảo bạn đang trong thư mục root của repository và có cấu trúc src/assets/resources/audios")
        return
    
    print(f"✅ Tìm thấy thư mục audios: {audios_path}")
    
    # Xác nhận từ người dùng
    print("\n📋 Các thao tác sẽ được thực hiện:")
    print("  1. song1.mp3 -> bgm-main.mp3")
    print("  2. multiplier.mp3 -> multiplier-land.mp3")
    print("  3. multiplier-appear.mp3 -> multiplier-activate.mp3")
    print("  4. reelstop1.mp3 -> reel-stop.mp3")
    print("  5. Xóa reelstop2.mp3 -> reelstop5.mp3")
    print("  6. Xóa big-win-increment-ended.mp3")
    print("  7. winning-level-up.mp3 -> duplicate thành mega-win.mp3 & super-win.mp3")
    print("  8. click.mp3 -> duplicate thành click-symbol.mp3")
    print("  9. increment.mp3 -> wincount-increment.mp3")
    print("  10. increment-stop.mp3 -> wincount-stop.mp3")
    print("  11. coin.mp3 -> win.mp3")
    
    response = input(f"\n❓ Bạn có muốn thực hiện rename cho repository '{current_repo_name}'? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("🚫 Đã hủy thao tác.")
        return
    
    # Xử lý repository hiện tại
    print(f"\n🎵 === BẮT ĐẦU XỬ LÝ ===")
    success = process_repo_audio_files(current_repo_path, current_repo_name)
    
    # Kết quả tổng kết
    print(f"\n🏁 === HOÀN THÀNH ===")
    if success:
        print("🎉 Repository đã được rename audio files thành công!")
        print("✅ Đã hoàn thành tất cả các thao tác rename, copy và delete")
    else:
        print("⚠️ Không có thay đổi nào được thực hiện.")
        print("💡 Có thể các file đã được rename trước đó hoặc không tồn tại.")

if __name__ == "__main__":
    main()
