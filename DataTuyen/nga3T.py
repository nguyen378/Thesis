from PIL import Image

# Đường dẫn tới ảnh ngã ba
input_path = 'F:\\Project\\Thesis\\Thesis\\Dataset\\nga3T\\20240608_133307.png'
output_folder = 'F:\\Project\\Thesis\\Thesis\\DataTuyen\\nga3'  # Thư mục đầu ra

# Mở ảnh gốc
image = Image.open(input_path)

# Kích thước ảnh
width, height = image.size

# Xác định các vùng để cắt
# Vùng tuyến đường ngang: Chiều rộng đầy đủ, chỉ lấy phần trên
horizontal_road_region = (0, height // 1.5, width, height)

# Vùng tuyến đường dọc: Chiều cao đầy đủ, chỉ lấy phần giữa
vertical_road_region = (width // 3, 0, 2 * width // 3, height // 1.5)

# Cắt các vùng ảnh
horizontal_road_image = image.crop(horizontal_road_region)
vertical_road_image = image.crop(vertical_road_region)

# Lưu ảnh đã cắt
horizontal_road_output_path = f'{output_folder}/horizontal_road.png'
vertical_road_output_path = f'{output_folder}/vertical_road.png'

horizontal_road_image.save(horizontal_road_output_path)
vertical_road_image.save(vertical_road_output_path)

print("Ảnh đã được cắt và lưu thành công.")
