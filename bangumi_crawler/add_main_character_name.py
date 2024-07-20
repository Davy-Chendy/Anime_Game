import xlrd
import xlwt
# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
from joblib import Parallel, delayed
import time
import random, os
from http.client import IncompleteRead, RemoteDisconnected

#subject中找人物名
findMainCharacter = re.compile(r'<span class="badge_job_tip">主角</span></small> <span class="tip">(.*?)</span><br/>')

findCover = re.compile(r'<div class="infobox">.*?<a href="(.*?)" title=.*?<ul id="infobox">', re.DOTALL) #re.DOTALL使.能匹配换行符

def askURL(url):
    while True:
        try:
            time.sleep(random.randint(5,20))
            head = { 
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.41"
            }
            print(url)
            request = urllib.request.Request(url, headers=head)
            html = ""
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            return html
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            time.sleep(random.randint(10,20))
        except IncompleteRead as e:
            print("IncompleteRead error:", e)
            time.sleep(random.randint(10,20))
        except RemoteDisconnected as e:
            print("RemoteDisconnected error:", e)
            time.sleep(random.randint(10,20))
        except:
            print('unknown error')
            time.sleep(random.randint(10,20))

# 定义函数 f(content)，该函数将处理每一行第5列的内容
def f(content):
    # 在这里实现你的逻辑，例如简单的内容转换
    return content[::-1]  # 示例：将字符串反转

def getCoverAndMainCharacterName(subject_id):
    url = 'https://bgm.tv' + subject_id
    html = askURL(url)# 保存获取到的网页源码
    
    main_character_names = re.findall(findMainCharacter, html)
    cover_url = re.findall(findCover, html)

    return str(main_character_names), cover_url

def main():
    # 打开现有的 Excel 文件
    input_file = r'D:\MyCode\Python\bangumi\bangumi中2005-2024年代评分前120动画_按打分人数排序.xls'
    workbook = xlrd.open_workbook(input_file)

    # 创建一个新的 Excel 文件
    output_file = r'D:\MyCode\Python\bangumi\bangumi中2005-2024年代评分前120动画_按打分人数排序_含主角名字.xls'
    new_workbook = xlwt.Workbook()

    # get_name_num = 20

    # 遍历每个工作表
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        year = int(sheet_name)
        print('year:',year)    
        if year < 2010:
            get_name_num=15
        elif year < 2016:
            get_name_num=25
        else:
            get_name_num=40

        # 创建新的工作表
        new_sheet = new_workbook.add_sheet(sheet_name)
        
        # 复制标题行
        for col_index in range(sheet.ncols):
            new_sheet.write(0, col_index, sheet.cell_value(0, col_index))
        # 添加新列的标题
        new_sheet.write(0, sheet.ncols, 'cover_url')
        new_sheet.write(0, sheet.ncols+1, '主角')
        
        # 遍历每一行数据，从第二行开始
        for row_index in range(1, sheet.nrows):
            # 复制原始数据
            for col_index in range(sheet.ncols):
                new_sheet.write(row_index, col_index, sheet.cell_value(row_index, col_index))
            
            if row_index <= get_name_num:
            # 提取第6列的内容并应用函数 
                subject_id = sheet.cell_value(row_index, 5)
                main_character_names, cover_url = getCoverAndMainCharacterName(subject_id)
                
                # 将新内容写入新列
                new_sheet.write(row_index, sheet.ncols, cover_url)
                new_sheet.write(row_index, sheet.ncols+1, main_character_names)

        # 保存新的 Excel 文件
        new_workbook.save(output_file)

    print(f"数据已成功处理并保存至 {output_file}")

if __name__ == "__main__":  
    main()
