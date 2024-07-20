import random
from PIL import Image, ImageFilter, ImageOps, ImageTk

# 高斯模糊
def apply_gaussian_blur(img, level):
    radius = level * 5  # 损坏程度越高，模糊半径越大
    return img.filter(ImageFilter.GaussianBlur(radius))

# 马赛克
def apply_mosaic(img, level):
    corrupt_level = 5 - level
    pixel_size = max(1, int(max(img.size) / (corrupt_level * 20)))  # 损坏程度越高，马赛克越小，范围从1到较大值
    width, height = img.size
    mosaic_img = Image.new('RGB', (width, height))

    for y in range(0, height, pixel_size):
        for x in range(0, width, pixel_size):
            crop = img.crop((x, y, x + pixel_size, y + pixel_size))
            avg_color = crop.resize((1, 1)).resize((pixel_size, pixel_size))
            mosaic_img.paste(avg_color, (x, y))

    return mosaic_img

# 颜色反转
def apply_color_inversion(img):
    return ImageOps.invert(img.convert('RGB'))

# 漏方形区域
def apply_visible_squares(img, level, used_regions):
    width, height = img.size
    visible_img = Image.new('RGB', (width, height), (0, 0, 0))
    num_squares = 10 - level  # 损坏程度越高，展示的区域越少
    square_size = (width // 10, height // 10)  # 固定方形区域大小

    for i in range(num_squares):
        while True:
            top_left_x = random.randint(0, width - square_size[0])
            top_left_y = random.randint(0, height - square_size[1])
            region_coords = (top_left_x, top_left_y, top_left_x + square_size[0], top_left_y + square_size[1])
            if region_coords not in used_regions:
                used_regions.add(region_coords)
                region = img.crop(region_coords)
                visible_img.paste(region, (top_left_x, top_left_y))
                break

    for region_coords in used_regions:
        region = img.crop(region_coords)
        visible_img.paste(region, region_coords[:2])

    return visible_img