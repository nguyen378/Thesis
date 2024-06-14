import os
import numpy as np
from PIL import Image, ImageDraw

input_folder = 'F:\\Project\\Thesis\\Thesis\\Dataset\\nga5'
output_folder = 'F:\\Project\\Thesis\\Thesis\\DataTuyen\\nga5'

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

        # nga3Y
        # region = (0, 0, width // 2 + width // 13, height)
        # region = (width // 2, 0, width, height // 2)
        
        # nga3T
        # regionX = (0, height // 1.5, width, height)
        # regionY = (width // 3, 0, 2 * width // 3, height // 1.5)
        
        # nga4
        # regionX = (0, height // 2.5, width, 2 * height // 3.5)
        # regionY = (width // 2.25, 0, 2 * width // 3.5, height)

        # nga5
        regionX = (0, height // 2.25, width, 2 * height // 3)
        regionY = (0, 0, 2 * width // 4, height // 2.25)
        regionZ = (width // 1.75, 0, 2 * width // 2, height // 2.25)
        regionW = (width //3, height // 1.5, width //1.5, height)
        
        # Cắt các vùng ảnh
        X_road_image = image.crop(regionX)
        Y_road_image = image.crop(regionY)
        Z_road_image = image.crop(regionZ)
        W_road_image = image.crop(regionW)

        # Lưu ảnh đã cắt với tên mới
        base_filename = os.path.splitext(filename)[0]
        X_output_path = os.path.join(output_folder, f'{base_filename}_2.png')
        Y_output_path = os.path.join(output_folder, f'{base_filename}_4.png')
        Z_output_path = os.path.join(output_folder, f'{base_filename}_1.png')
        W_output_path = os.path.join(output_folder, f'{base_filename}_3.png')

        X_road_image.save(X_output_path)
        Y_road_image.save(Y_output_path)
        Z_road_image.save(Z_output_path)
        W_road_image.save(W_output_path)
        

        print(f"Ảnh đã được cắt và lưu thành công: {filename}")

print("Tất cả ảnh đã được cắt và lưu thành công.")

