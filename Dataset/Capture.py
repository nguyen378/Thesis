import time
from PIL import ImageGrab
import os

def capture_screen(region):
    return ImageGrab.grab(region)

def save_screenshot(img, folder, filename):
    if not os.path.exists(folder):
        os.makedirs(folder)
    img.save(os.path.join(folder, filename))

def main():
    # Define the region to capture (left, top, right, bottom)
    region = (400, 130, 1450, 980)

    # Capture and save screenshots every 10 seconds
    while True:
        current_time = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{current_time}.png"
        screenshot = capture_screen(region)
        save_screenshot(screenshot,'nga7' , filename)
        print(f"Screenshot captured: {filename}")
        time.sleep(1)  # Capture every 10 seconds

if __name__ == "__main__":
    main()
