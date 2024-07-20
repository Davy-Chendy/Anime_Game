import os
import random
from PIL import Image, ImageFilter, ImageOps, ImageTk
from image_currptions import apply_gaussian_blur, apply_mosaic, apply_color_inversion, apply_visible_squares
import tkinter as tk
from tkinter import filedialog

# 递归读取所有子文件夹中的图片
def load_images_from_folder(folder):
    images = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                if img is not None:
                    images.append((img_path, img))
    return images

# 随机选择损坏类型并应用
def apply_random_damage(img, damage_type, level, used_regions):
    if damage_type == 'gaussian_blur':
        return apply_gaussian_blur(img, level)
    elif damage_type == 'mosaic':
        return apply_mosaic(img, level)
    elif damage_type == 'color_inversion':
        global current_damage_level
        current_damage_level = 1
        return apply_color_inversion(img)
    elif damage_type == 'visible_squares':
        return apply_visible_squares(img, level, used_regions)
    return img

# 更新显示图像
def update_image(img, damage_type, damage_level, used_regions):
    global current_damage_level
    current_damage_level = damage_level
    damaged_img = apply_random_damage(img, damage_type, damage_level, used_regions)
    display_image(damaged_img)

# 显示图像
def display_image(img):
    global img_label, current_image_name, img_name_label
    img = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk
    img_name_label.config(text="")

# 处理鼠标点击事件
def on_click(event):
    global current_damage_level, current_image_name, current_image_path, current_image_index, images, damage_type, used_regions
    if current_damage_level > 1:
        current_damage_level -= 1
        update_image(images[current_image_index][1], damage_type, current_damage_level, used_regions)
    elif current_damage_level == 1:
        display_image(images[current_image_index][1])  # 显示原图
        img_name_label.config(text=current_image_name)
        current_damage_level -= 1
    else:
        img_label.config(image="")
        img_name_label.config(text="")
        current_image_index += 1
        if current_image_index < len(images):
            load_next_image()
        else:
            img_name_label.config(text="游戏结束！")

# 加载下一张图片
def load_next_image():
    global current_damage_level, current_image_name, current_image_path, current_image_index, images, damage_type, used_regions
    current_image_path, img = images[current_image_index]
    current_image_name = os.path.basename(current_image_path)
    current_damage_level = 3
    damage_type = random.choice(['gaussian_blur', 'mosaic', 'color_inversion', 'visible_squares'])
    used_regions = set()
    update_image(img, damage_type, current_damage_level, used_regions)

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    root.title("动漫高手")
    root.geometry("600x650")

    folder = filedialog.askdirectory(title="pic")
    images = load_images_from_folder(folder)
    random.shuffle(images)

    current_image_index = 0
    current_damage_level = 3 # 当前图片破坏程度
    current_image_name = ""
    current_image_path = ""
    damage_type = ""
    used_regions = set()

    img_label = tk.Label(root)
    img_label.pack(expand=True)

    img_name_label = tk.Label(root, text="", font=("Arial", 14), fg="black")
    img_name_label.pack()

    root.bind("<Button-1>", on_click)

    load_next_image()
    root.mainloop()




