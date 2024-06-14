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
    mask_1 = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_1)
    draw.line([(middle_x +30, 0), (middle_x+30, height//1.75)], fill=255, width=thickness)
    draw.line([(middle_x , height//2), (width -200, height)], fill=255, width=thickness)

    # Tạo mặt nạ cho nhánh trái Y
    mask_3 = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_3)
    draw.line([(width//1.85, height//2 ), (-100, height -150)], fill=255, width=thickness)
    draw.line([(width, height//1.5 ), (width//2.15, height//2)], fill=255, width=thickness)

    # Tạo mặt nạ cho nhánh phải Y
    mask_2 = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_2)
    draw.line([(width//1.85, height//2 ), (225, height)], fill=255, width=thickness)
    draw.line([(width//2 , height//2 ), (width, 150)], fill=255, width=thickness)
    
    mask_4 = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask_4)
    draw.line([(0, 100), (width//2, height//2)], fill=255, width=thickness)

    return mask_1, mask_3, mask_2, mask_4

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


input_folder = 'F:\\Project\\Thesis\\Thesis\\Dataset\\nga7'
output_folder = 'F:\\Project\\Thesis\\Thesis\\DataTuyen\\nga7'

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
        

        mask_1, mask_3, mask_2, mask_4 = create_y_shape_masks((width, height))
        
        # Áp dụng từng mặt nạ lên ảnh
        image_1 = apply_mask(image, mask_1)
        image_3 = apply_mask(image, mask_3)
        image_2 = apply_mask(image, mask_2)
        image_4 = apply_mask(image, mask_4)
        # Lưu các ảnh
        base_filename = os.path.splitext(filename)[0]
        output_path_1 = os.path.join(output_folder, f'{base_filename}_1.png')
        output_path_3 = os.path.join(output_folder, f'{base_filename}_3.png')
        output_path_2 = os.path.join(output_folder, f'{base_filename}_2.png')
        output_path_4 = os.path.join(output_folder, f'{base_filename}_4.png')

        image_1.save(output_path_1)
        image_3.save(output_path_3)
        image_2.save(output_path_2)
        image_4.save(output_path_4)

        print(f"Ảnh đã được cắt và lưu thành công: {filename}")

print("Tất cả ảnh đã được cắt và lưu thành công.")
