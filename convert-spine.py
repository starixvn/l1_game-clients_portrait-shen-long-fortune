import os
import shutil


def convert_atlas_format(input_atlas, output_atlas):
    # Chuẩn hóa đường dẫn output để dùng dấu /
    output_atlas = output_atlas.replace('\\', '/')
    
    with open(input_atlas, 'r') as f:
        lines = f.readlines()
    
    with open(output_atlas, 'w') as f:
        # Xử lý header
        f.write('\n')  # Dòng trống đầu tiên
        
        extension = lines[0].split('.')[-1];
        # Lấy tên file từ đường dẫn output và thay đổi phần mở rộng thành .png
        output_filename = output_atlas.split('/')[-1].replace('atlas', extension)
        f.write(f'{output_filename}')  # Ghi tên file mới
        
        f.write(lines[1])  # size
        f.write('format: RGBA8888\n')  # Thêm format
        f.write(lines[2])  # filter
        f.write('repeat: none\n')  # Thêm repeat
        
        current_sprite = None
        i = 4  # Bắt đầu từ dòng sau header
        current_size = None
        has_offsets = False
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                # Nếu gặp dòng trống và có sprite hiện tại nhưng chưa có offsets
                if current_sprite and current_size and not has_offsets:
                    width, height = current_size
                    f.write(f'  orig: {width}, {height}\n')
                    f.write('  offset: 0, 0\n')
                    f.write('  index: -1\n')
                current_sprite = None
                current_size = None
                has_offsets = False
                i += 1
                continue
                
            if not line.startswith('bounds:') and not line.startswith('offsets:'):
                # Đây là tên sprite mới
                # Nếu có sprite trước đó nhưng chưa có offsets
                if current_sprite and current_size and not has_offsets:
                    width, height = current_size
                    f.write(f'  orig: {width}, {height}\n')
                    f.write('  offset: 0, 0\n')
                    f.write('  index: -1\n')
                
                current_sprite = line
                current_size = None
                has_offsets = False
                f.write(f'{current_sprite}\n')
                f.write('  rotate: false\n')
                
            elif line.startswith('bounds:'):
                # Chuyển bounds thành xy và size
                _, values = line.split(':')
                x, y, width, height = map(float, values.split(','))
                f.write(f'  xy: {int(x)}, {int(y)}\n')
                f.write(f'  size: {int(width)}, {int(height)}\n')
                current_size = (int(width), int(height))
                
            elif line.startswith('offsets:'):
                # Chuyển offsets thành orig và offset
                _, values = line.split(':') 
                offset_x, offset_y, orig_width, orig_height = map(float, values.split(','))
                f.write(f'  orig: {int(orig_width)}, {int(orig_height)}\n')
                f.write(f'  offset: {int(offset_x)}, {int(offset_y)}\n')
                f.write('  index: -1\n')
                has_offsets = True
                
            i += 1
            
        # Xử lý sprite cuối cùng nếu chưa có offsets
        if current_sprite and current_size and not has_offsets:
            width, height = current_size
            f.write(f'  orig: {width}, {height}\n')
            f.write('  offset: 0, 0\n')
            f.write('  index: -1\n')

def convert_animation_properties(obj):
    """Đệ quy chuyển đổi các property trong animations"""
    if isinstance(obj, dict):
        translate_x = None
        translate_y = None
        
        for key, value in list(obj.items()):
            if key == "rotate":
                # Xử lý các object trong mảng rotate
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "value" in item:
                            item["angle"] = item.pop("value")
            elif key == "rgba":
                # Đổi tên rgba thành color
                obj["color"] = obj.pop("rgba")
            elif key == "translatex":
                # Lưu giá trị translatex để gộp sau
                translate_x = obj.pop("translatex")
            elif key == "translatey":
                # Lưu giá trị translatey để gộp sau
                translate_y = obj.pop("translatey")
            else:
                convert_animation_properties(value)
        
        # Gộp translatex và translatey thành translate
        if translate_x is not None or translate_y is not None:
            translate_list = []
            
            # Xử lý từng frame trong animation
            if isinstance(translate_x, list) or isinstance(translate_y, list):
                max_frames = max(
                    len(translate_x) if isinstance(translate_x, list) else 0,
                    len(translate_y) if isinstance(translate_y, list) else 0
                )
                
                for i in range(max_frames):
                    frame = {}
                    
                    # Lấy thông tin từ translatex
                    if isinstance(translate_x, list) and i < len(translate_x):
                        tx_frame = translate_x[i]
                        frame.update(tx_frame)
                        if "value" in tx_frame:
                            frame["x"] = frame.pop("value")
                    
                    # Lấy thông tin từ translatey
                    if isinstance(translate_y, list) and i < len(translate_y):
                        ty_frame = translate_y[i]
                        frame.update(ty_frame)
                        if "value" in ty_frame:
                            frame["y"] = frame.pop("value")
                    
                    translate_list.append(frame)
                
            obj["translate"] = translate_list
                
    elif isinstance(obj, list):
        for item in obj:
            convert_animation_properties(item)

def convert_json_format(input_json, output_json):
    # Chuẩn hóa đường dẫn output để dùng dấu /
    output_json = output_json.replace('\\', '/')
    
    import json
    
    with open(input_json, 'r') as f:
        data = json.load(f)
        
    # Cập nhật version spine và các thuộc tính khác
    data['skeleton']['spine'] = '3.8.99'
    if 'x' not in data['skeleton']:
        data['skeleton']['x'] = -801.47
    if 'y' not in data['skeleton']:
        data['skeleton']['y'] = -450
            
    # Chuyển đổi các property trong animations
    if 'animations' in data:
        convert_animation_properties(data['animations'])
            
    # Ghi file mới
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=1)

def process_folder(input_dir, output_dir):
    """Xử lý một thư mục và các thư mục con của nó"""
    
    # Chuẩn hóa đường dẫn thư mục để dùng dấu /
    input_dir = input_dir.replace('\\', '/')
    output_dir = output_dir.replace('\\', '/')
    
    # Tạo thư mục output nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Duyệt qua tất cả file và thư mục trong input_dir
    for item in os.listdir(input_dir):
        input_path = os.path.join(input_dir, item).replace('\\', '/')
        output_path = os.path.join(output_dir, item).replace('\\', '/')
        
        # Nếu là thư mục thì xử lý đệ quy
        if os.path.isdir(input_path):
            process_folder(input_path, output_path)
            continue
            
        # Xử lý file atlas
        if item.endswith('.atlas'):
            convert_atlas_format(input_path, output_path)
            
        # Xử lý file json
        elif item.endswith('.json'):
            convert_json_format(input_path, output_path)
            
        # Copy file texture
        elif item.lower().endswith(('.png', '.jpg', '.webp')):
            shutil.copy2(input_path, output_path)

def convert_spine_files(input_dir, output_dir):
    """Convert tất cả file spine từ thư mục input sang thư mục output"""
    
    # Chuẩn hóa đường dẫn thư mục để dùng dấu /
    input_dir = input_dir.replace('\\', '/')
    output_dir = output_dir.replace('\\', '/')
    
    # Xử lý toàn bộ thư mục
    process_folder(input_dir, output_dir)

# Sử dụng
input_dir = 'src/assets/game/spines/v4'  # Thư mục chứa file spine v4
output_dir = 'src/assets/game/spines/v3'  # Thư mục output cho file spine v3

convert_spine_files(input_dir, output_dir)