import time
from PIL import ImageGrab, Image, ImageDraw
import os

class Capture:
    def __init__(self, region):
        self.region = region
    def capture_screen(self):
        return ImageGrab.grab(self.region)
    def capture_road3(self, image):
        width, height = image.size
        
    