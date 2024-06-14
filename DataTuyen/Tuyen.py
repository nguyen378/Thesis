import os
from PIL import Image

# Đường dẫn tới thư mục chứa ảnh
input_folder = 'F:\\Project\\Thesis\\Thesis\\Dataset\\nga4'
output_folder = 'F:\\Project\\Thesis\\Thesis\\DataTuyen\\nga4'

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
        # regionX = (0, 0, width // 2 + width // 13, height)
        # regionY = (width // 2, 0, width, height // 2)
        
        # nga3T
        # regionX = (0, height // 1.5, width, height)
        # regionY = (width // 3, 0, 2 * width // 3, height // 1.5)
        
        # nga4
        regionX = (0, height // 2.5, width, 2 * height // 3.25)
        regionY = (width // 2.50, 0, 2 * width // 3.5, height)

        # Cắt các vùng ảnh
        left_road_image = image.crop(regionX)
        right_road_image = image.crop(regionY)

        # Lưu ảnh đã cắt với tên mới
        base_filename = os.path.splitext(filename)[0]
        left_output_path = os.path.join(output_folder, f'{base_filename}_2.png')
        right_output_path = os.path.join(output_folder, f'{base_filename}_1.png')

        left_road_image.save(left_output_path)
        right_road_image.save(right_output_path)

        print(f"Ảnh đã được cắt và lưu thành công: {filename}")

print("Tất cả ảnh đã được cắt và lưu thành công.")
