import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import random

# 定义请求函数
def fetch_image_src(character_name):
    encoded_character_name = quote(character_name)
    url = f'https://zh.moegirl.org.cn/{encoded_character_name}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    time.sleep(random.randint(10, 15))
    # 重试机制
    retries = 5
    for i in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            print("Too many requests. Retrying...")
            time.sleep(2 ** i)  # 指数退避
        else:
            # response.raise_for_status()  # 如果不是429错误，则抛出异常
            return None # 萌娘百科如果不能根据名字找到人物返回None
    
    # 检查最终的响应状态码
    if response.status_code != 200:
        print(f"Failed to fetch the page after {retries} retries.")
        return None
    
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 检查<tr class="infobox-image-container">是否存在
    infobox_image_container = soup.find('tr', class_='infobox-image-container')
    if infobox_image_container is None:
        print("Error: <tr class='infobox-image-container'> not found.")
        # 打印部分HTML内容以进行调试
        print(soup.prettify()[:1000])  # 打印前1000个字符
        return None
    else:
        # 在该标签下找到<img>标签
        img_tag = infobox_image_container.find('img')
        if img_tag is None:
            print("Error: <img> tag not found within the infobox image container.")
            return None
        else:
            # 获取src属性值
            img_src = img_tag['src']
            return img_src

import pandas as pd

###############参数设置###################

file_path = 'bangumi.xls' # 加载的Excel文件
save_path = 'test.xlsx' # 保存的Excel文件
selection_nums = 1 # 每一年选取的热门番数
max_characters_nums = 3 # 每一部番剧选取的主角数

#########################################


xls = pd.ExcelFile(file_path)

# 遍历所有的sheet
with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
    for sheet_name in xls.sheet_names:
        print(sheet_name)
        characters_list = []
        # 读取当前sheet
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if '图片url' not in df.columns:
            df['图片url'] = None

        # 筛选评分人数大于10000的行
        # filtered_df = df[df['评分人数'] > 10000]
        # 筛选前20行评分人数最多的记录
        filtered_df = df.nlargest(selection_nums, '评分人数')
        # print(filtered_df)

        # 提取主角列并添加到结果列表中
        characters_list.extend(filtered_df['主角'].apply(eval).tolist())

        all_img_urls = []

        for all_character_names in characters_list:
            img_urls = []
            cnt = 0
            for character_names in all_character_names:
                cnt += 1
                if cnt > max_characters_nums:
                    break
                img_url = fetch_image_src(character_names)
                if img_url:
                    print(f'{character_names}: {img_url}')
                    img_urls.append({character_names: img_url})
                else:
                    cnt -= 1 # 如果没有找到图片，不计数
            all_img_urls.append(img_urls)

        print(all_img_urls)

        # # 将新内容写入到筛选后的行的“图片url”列
        # df.loc[filtered_df.index, '图片url'] = all_img_urls[:len(filtered_df)]
        # 检查并调整new_content的长度
        if len(all_img_urls) < len(filtered_df):
            raise ValueError("new_content长度不足，无法匹配筛选出的行数")
        elif len(all_img_urls) > len(filtered_df):
            all_img_urls = all_img_urls[:len(filtered_df)]
        print(all_img_urls)

        # 将新内容写入到筛选后的行的“图片url”列
        # df.loc[filtered_df.index, '图片url'] = all_img_urls
        for idx, content in zip(filtered_df.index, all_img_urls):
            df.at[idx, '图片url'] = content

        # 将修改后的数据写回Excel文件
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        # 打印结果列表
        print(characters_list)
