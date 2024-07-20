# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
from joblib import Parallel, delayed
import time
import random, os
from http.client import IncompleteRead, RemoteDisconnected


year_data_dict = dict()

findTitle = re.compile(r'<a class="l" href=.*>(.*?)</a>')#匹配标题
#eg = '<a class="l" href="/subject/253">星际牛仔</a> <small class="grey">カウボーイビバップ</small>'
#title = re.findall(findTitle,eg)
#print(title)

findRating = re.compile(r'<span class.*"fade">(.*?)<')#匹配评分
#eg = '<span class="starstop-s"><span class="starlight stars9"></span></span> <small class="fade">9.1</small> <span class="tip_j">(9075人评分)</span>'
#rating = re.findall(findRating,eg)
#print(rating)

findJudge = re.compile(r'<span class.*"tip_j">\((.*?)人评分\)<')#匹配评价人数
#eg = '<span class="starstop-s"><span class="starlight stars9"></span></span> <small class="fade">9.1</small> <span class="tip_j">(4936人评分)</span>'
#judge = re.findall(findJudge,eg)
#print(judge)

findTip = re.compile(r'<p class="info tip">(.*?)</p>', re.S)#匹配标签
#eg = '<p class="info tip">26话 / 1998年10月23日 / 渡辺信一郎 / 矢立肇 / 川元利浩 </p>'
#tip = re.findall(findTip,eg)
#print(tip)

findRank = re.compile(r'<span class="rank"><small>Rank </small>(.*?)</span>')#匹配排名
#eg = '<span class="rank"><small>Rank </small>1</span>'
#rank = re.findall(findRank,eg)
#print(rank)

findSubject = re.compile(r'<a class="l" href="(.*?)">')


#subject中找人物名
findMainCharacter = re.compile(r'<span class="badge_job_tip">主角</span></small> <span class="tip">(.*?)</span><br/>')


def getMainCharacterName(subject_id):
    url = 'https://bgm.tv' + subject_id
    html = askURL(url)# 保存获取到的网页源码
    # soup = BeautifulSoup(html, 'html.parser')
    
    main_character_names = re.findall(findMainCharacter, html)
    
    return main_character_names


# def getItemData(item):
#     data = []  # 保存信息
#     # item = str(item)
#     #print(item)

#     titles = re.findall(findTitle, item)   
#     data.append(titles)

#     rank = re.findall(findRank, item)
#     data.append(rank)

#     rating = re.findall(findRating, item)
#     data.append(rating)

#     judgeNum = re.findall(findJudge, item)
#     data.append(judgeNum)

#     tip = re.findall(findTip, item)
#     if len(tip) != 0:
#         tip = tip[0].replace("/", "")
#         data.append(tip)
#     else:
#         data.append(" ")

#     subject = re.findall(findSubject, item)
#     # subject[0]=subject[0].replace("\n","")
#     # print(subject[0])
#     data.append(subject)

#     #爬取主页中的人物名称
#     # MainCharacterNames = getMainCharacterName(subject[0])
#     # data.append(str(list(MainCharacterNames)))
#     # datalist.append(data)

#     return data


def getPageData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    html = askURL(baseurl)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('div', class_="inner"):  # 查找符合要求的字符串
        data = []  # 保存信息
        item = str(item)
        #print(item)

        titles = re.findall(findTitle, item)   
        if len(titles) == 0:#无数据
            continue
        data.append(titles)

        rank = re.findall(findRank, item)
        data.append(rank)

        rating = re.findall(findRating, item)
        data.append(rating)

        judgeNum = re.findall(findJudge, item)
        data.append(judgeNum)

        tip = re.findall(findTip, item)
        if len(tip) != 0:
            tip = tip[0].replace("/", "")
            data.append(tip)
        else:
            data.append(" ")

        subject = re.findall(findSubject, item)
        data.append(subject)

        #爬取主页中的人物名称
        # MainCharacterNames = getMainCharacterName(subject[0])
        # data.append([MainCharacterNames])

        datalist.append(data)

    return datalist

def askURL(url):
    while True:
        try:
            time.sleep(random.randint(25,35))
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
        except IncompleteRead as e:
            print("IncompleteRead error:", e)
        except RemoteDisconnected as e:
            print("RemoteDisconnected error:", e)
        except:
            print('unknown error')

def saveData(datalist, book, year):
    print("save.......")
    sheet = book.add_sheet(f'{str(year)}', cell_overwrite_ok=True) #创建工作表
    col = ("标题","排名","评分","评分人数","标签","主页subjectID")
    for i in range(0,len(col)):
        sheet.write(0,i,col[i])  #列名
    for i, data in enumerate(datalist):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        for j, d in enumerate(data):
            sheet.write(i+1,j,d)  #数据
    print(f'year{year} saved')

def getYearData(year, baseurl, search_page_num):
    datalist = []
    for page in range(1, search_page_num+1):
        # baseurl = f"https://bgm.tv/anime/browser/airtime/{}?sort=rank&page={}"  #要爬取的网页链接
        url = baseurl.format(str(year), str(page))
        # 爬取网页
        datalist += getPageData(url)
    return datalist
    
def saveYearData(year, baseurl, search_page_num):
    datalist = getYearData(year, baseurl, search_page_num)
    # saveData(datalist, sheet)
    # print(f'year{year} success')
    return year, datalist

def main():
    search_page_num = 5 #1页24个内容
    start_year=2005
    end_year=2024
    year_list = [i for i in range(start_year,end_year+1)]
    savepath = 'D:/MyCode/Python/bangumi'
    baseurl = 'https://bgm.tv/anime/browser/tv/airtime/{}?sort=rank&page={}'
    savepath_score = os.path.join(savepath, f"bangumi中{start_year}-{end_year}年代评分前{24*search_page_num}动画_按评分排序.xls")  #当前目录新建XLS，存储进去
    savepath_member = os.path.join(savepath, f"bangumi中{start_year}-{end_year}年代评分前{24*search_page_num}动画_按打分人数排序.xls") 
    book_score = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    book_member = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象

    # # ###并行###
    # results= Parallel(n_jobs=1, backend='loky')(delayed(saveYearData)(year, baseurl, search_page_num) for year in year_list)
    # # 按年份排序结果
    # sorted_results = sorted(results, key=lambda x: x[0])
    # # 提取排序后的结果
    # sorted_data = [result for year, result in sorted_results]
    # #创建工作表
    # for i, year in enumerate(year_list):
    #     saveData(sorted_data[i], book, year)
    # book.save(savepath) #保存
    # # ###并行 end###

    # 不用并行
    for year in year_list:
        datalist = getYearData(year, baseurl, search_page_num)
        datalist_member = sorted(datalist, key=lambda x: int(x[3][0]), reverse=True)
        saveData(datalist, book_score, year)
        saveData(datalist_member, book_member, year)
        book_score.save(savepath_score)
        book_member.save(savepath_member)

if __name__ == "__main__":  
    main()
    print("爬取完毕！")