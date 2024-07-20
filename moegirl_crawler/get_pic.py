import os
import pandas as pd
import requests
from pathlib import Path

def download_image(url, save_path):
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image from {url}, status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading image from {url}: {e}")

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def process_sheet(sheet_name, df, save_dir):
    # Create directory for the sheet
    sheet_dir = save_dir / sheet_name
    sheet_dir.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        title = row['标题']
        sanitized_title = sanitize_filename(title)
        
        # Download cover image
        cover_url = row['cover_url'] if pd.notna(row['cover_url']) else None
        if cover_url:
            cover_save_path = sheet_dir / f"{sheet_name}_{sanitized_title}_cover.jpg"
            download_image("https:" + cover_url, cover_save_path)
        
        # Download images from '图片url' column
        image_list_str = row['图片url'] if pd.notna(row['图片url']) else None
        if image_list_str:
            try:
                image_list = eval(image_list_str)
                for image_info in image_list:
                    for character, image_url in image_info.items():
                        sanitized_character = sanitize_filename(character)
                        image_save_path = sheet_dir / f"{sheet_name}_{sanitized_title}_{sanitized_character}.jpg"
                        download_image(image_url, image_save_path)
            except Exception as e:
                print(f"Failed to process images for title {title} in sheet {sheet_name}: {e}")

def main(excel_file_path, save_dir_path):
    # Load the Excel file
    xls = pd.ExcelFile(excel_file_path)
    save_dir = Path(save_dir_path)

    # Process each sheet
    for sheet_name in xls.sheet_names:
        print('year:', sheet_name)
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        process_sheet(sheet_name, df, save_dir)

if __name__ == "__main__":
    # User-defined parameters
    excel_file_path = r'D:\MyCode\Python\bangumi\bangumi中2005-2024年代评分前120动画_按打分人数排序_含主角名字(2005-2024)与图片链接.xlsx'  # Excel file path
    save_dir_path = r'D:\MyCode\Python\bangumi\pic'  # Directory to save images

    main(excel_file_path, save_dir_path)
