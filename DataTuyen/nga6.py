import os
import numpy as np
from PIL import Image, ImageDraw

def capture_screen(region):
    """Chụp ảnh màn hình trong vùng xác định."""
    return ImageGrab.grab(region)

def create_y_shape_masks(size, thickness=200):
    """Tạo các mặt nạ cho từng phần của hình chữ Y."""
    width, height = size
    middle_x = width // 2

    # Tạo mặt nạ cho thân Y
    mask_body = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_body)
    draw.line([(middle_x, 0), (middle_x, height)], fill=255, width=thickness)

    # Tạo mặt nạ cho nhánh trái Y
    mask_left = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_left)
    draw.line([(width, height //7 ), (0, height -150)], fill=255, width=thickness)

    # Tạo mặt nạ cho nhánh phải Y
    mask_right = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_right)
    draw.line([(-width, -height +400 ), (width, height -125)], fill=255, width=thickness)

    return mask_body, mask_left, mask_right

def apply_mask(image, mask):
    """Áp dụng mặt nạ lên ảnh."""
    result = Image.new("RGBA", image.size)
    result.paste(image, mask=mask)
    return result

def save_screenshot(img, folder, filename):
    """Lưu ảnh màn hình vào thư mục."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    img.save(os.path.join(folder, filename))


input_folder = 'F:\\Project\\Thesis\\Thesis\\Dataset\\nga6'
output_folder = 'F:\\Project\\Thesis\\Thesis\\DataTuyen\\nga6'

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Lặp qua tất cả các file trong thư mục
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Đường dẫn tới file ảnh
        input_path = os.path.join(input_folder, filename)
        
        # Mở ảnh gốc
        image = Image.open(input_path)

        # Kích thước ảnh
        width, height = image.size
        

        mask_body, mask_left, mask_right = create_y_shape_masks((width, height))
        
        # Áp dụng từng mặt nạ lên ảnh
        body_image = apply_mask(image, mask_body)
        left_image = apply_mask(image, mask_left)
        right_image = apply_mask(image, mask_right)
        
        # Lưu các ảnh
        base_filename = os.path.splitext(filename)[0]
        body_output_path = os.path.join(output_folder, f'{base_filename}_1.png')
        left_output_path = os.path.join(output_folder, f'{base_filename}_2.png')
        right_output_path = os.path.join(output_folder, f'{base_filename}_3.png')

        body_image.save(body_output_path)
        left_image.save(left_output_path)
        right_image.save(right_output_path)

        print(f"Ảnh đã được cắt và lưu thành công: {filename}")

print("Tất cả ảnh đã được cắt và lưu thành công.")
