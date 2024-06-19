import time
from PIL import ImageGrab, Image, ImageDraw
import os
import win32gui
import win32ui
from ctypes import windll

class Capture:
    def __init__(self):
        self.region = (400, 130, 1450, 980)
    
    def capture_screen(self):
        hwnd = win32gui.FindWindow(None, "new.sumocfg - SUMO 1.20.0")  # Adjust as necessary
        if hwnd:
            # Uncomment the following line if you use a high DPI display or >100% scaling size
            windll.user32.SetProcessDPIAware()

            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            w = right - left
            h = bot - top

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

            saveDC.SelectObject(saveBitMap)

            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            image = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            if result == 1:
                # Crop the image to the region
                x_start, y_start, x_end, y_end = self.region
                image = image.crop((x_start - left, y_start - top, x_end - left, y_end - top))
                image.save('nga.png')
                return image
    
    def capture_road3T(self, image):
        width, height = image.size
        # Xác định các vùng để cắt
        horizontal_road_region = (0, height // 1.3, width, height)
        vertical_road_region = (width // 3, 0, 2 * width // 3, height // 1.3)
        # Cắt hình ảnh 
        horizontal_road_image = image.crop(horizontal_road_region)
        vertical_road_image = image.crop(vertical_road_region)
        horizontal_road_image.save('image\\nga3T1.png')
        vertical_road_image.save('image\\nga3T2.png')
        return horizontal_road_image, vertical_road_image
    
    def capture_road3Y(self, image):
        width, height = image.size
        # nga3Y
        regionX = (0, 0, width // 2 + width // 13, height)
        regionY = (width // 2, 0, width, height // 2)
        left_road_image = image.crop(regionX)
        right_road_image = image.crop(regionY)
        return left_road_image, right_road_image
    
    def capture_road4(self, image):
        width, height = image.size
        # nga4
        regionX = (0, height // 2.5, width, 2 * height // 3.25)
        regionY = (width // 2.50, 0, 2 * width // 3.5, height)
        left_road_image = image.crop(regionX)
        right_road_image = image.crop(regionY)
        return left_road_image, right_road_image
    
    def capture_road5(self, image):
        width, height = image.size
        # nga5
        regionX = (0, height // 2.25, width, 2 * height // 3)
        regionY = (0, 0, 2 * width // 4, height // 2.25)
        regionZ = (width // 1.75, 0, 2 * width // 2, height // 2.25)
        regionW = (width //3, height // 1.5, width //1.5, height)
        X_road_image = image.crop(regionX)
        Y_road_image = image.crop(regionY)
        Z_road_image = image.crop(regionZ)
        W_road_image = image.crop(regionW)
        return X_road_image, Y_road_image, Z_road_image, W_road_image
    
    def create_shape_masks_6(self,size, thickness=200):
 
        width, height = size
        middle_x = width // 2

        mask_body = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask_body)
        draw.line([(middle_x, 0), (middle_x, height)], fill=255, width=thickness)

        mask_left = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask_left)
        draw.line([(width, height //7 ), (0, height -150)], fill=255, width=thickness)

        mask_right = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask_right)
        draw.line([(-width, -height +400 ), (width, height -125)], fill=255, width=thickness)

        return mask_body, mask_left, mask_right

    def apply_mask(self,image, mask):
        """Áp dụng mặt nạ lên ảnh."""
        result = Image.new("RGBA", image.size)
        result.paste(image, mask=mask)
        return result
    def create_shape_masks_7(self, size, thickness=200):
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
    
    def capture_road6(self, image):
        width, height = image.size
        # nga6
        mask_1, mask_2, mask_3 = self.create_shape_masks_6((width, height))
        
        # Áp dụng từng mặt nạ lên ảnh
        image_1 = self.apply_mask(image, mask_1)
        image_2 = self.apply_mask(image, mask_2)
        image_3 = self.apply_mask(image, mask_3)
        return image_1, image_2, image_3
    
    def capture_road7(self, image):
        width, height = image.size
        # nga7

        mask_1, mask_3, mask_2, mask_4 = self.create_shape_masks_7((width, height))
        
        # Áp dụng từng mặt nạ lên ảnh
        image_1 = self.apply_mask(image, mask_1)
        image_3 = self.apply_mask(image, mask_3)
        image_2 = self.apply_mask(image, mask_2)
        image_4 = self.apply_mask(image, mask_4)
        return image_1, image_3, image_2, image_4

