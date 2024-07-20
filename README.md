# 动漫高手（简易版）

## 引言

该项目纯粹是和Monignt在看完b站一些up猜动漫人物后，意犹未尽油然而生的想法 ，于是乎两个人花了两个晚上，~~在gpt的帮助下~~写完了Bangumi和萌娘的爬虫以及对图片进行随机破坏的程序，写得很烂，轻喷2333333

## 项目流程图

![image-20240720231311912](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720231311912.png)

## 介绍

### Bangumi 爬虫

Bangumi中，我们通过年份，爬取了各个年份番剧的信息，一并存储在了一个excel表当中。参考程序：`bangumi_crawler/get_each_year_anime_list.py`

![image-20240720231640591](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720231640591.png)



随后，考虑到这是一个面向一般二刺猿浓度的项目，过于冷门的番可能不太好猜，于是我们根据评分人数进一步对番剧进行筛选，收集了对应的番剧封面图以及主角的名字。参考程序：`bangumi_crawler/add_main_character_name.py`![image-20240720231814209](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720231814209.png)

---

### 萌娘百科爬虫

在得到了需要爬取的番剧名字以及对应的主角名字是，我们可以通过爬取萌娘百科来获取对应人物封面的url。参考程序：`moegirl_crawler/moegirl_crawler.py`

![image-20240720232654873](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720232654873.png)

随后也将这些url写进excel中存储。

![image-20240720232848060](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720232848060.png)

最后写一个程序遍历读取这些url进行爬取，存进一个文件夹中。参考程序：`moegirl_crawler/get_pic.py`

![image-20240720233012011](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233012011.png)

![image-20240720233038812](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233038812.png)

---

### 随机图片破坏

得到了爬取下来的图片后，我们对图片进行了不同程度、不同效果的破坏，每次鼠标点击后，破坏程度都会减轻（反色会直接变回原图），直到变回原图显示答案（番名或者人名）。参考程序：`image_currptions.py` 和 `game.py` 。效果图如下：

#### 高斯模糊

![image-20240720233653013](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233653013.png)

![image-20240720233700288](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233700288.png)

![image-20240720233715705](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233715705.png)

#### 遮挡

![image-20240720233543312](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233543312.png)

![image-20240720233556481](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233556481.png)

![image-20240720233605609](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233605609.png)

#### 马赛克

![image-20240720233622099](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233622099.png)

![image-20240720233629134](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233629134.png)

![image-20240720233635356](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233635356.png)

#### 颜色反转

![image-20240720233743344](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233743344.png)

![image-20240720233750760](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233750760.png)

### 游戏开始

执行`game.py`程序后，只需上传需要猜的图库

![image-20240720233958170](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720233958170.png)

选择对应的年份即可开始游戏

![image-20240720234022294](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720234022294.png)

![image-20240720234036162](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720234036162.png)

通过点击减轻图片破坏程度，最终显示答案，再次点击即可跳转下一张图片

![image-20240720234115633](https://davychen-imgsubmit.oss-cn-shenzhen.aliyuncs.com/img/image-20240720234115633.png)


## 贡献者
<a href="https://github.com/Davy-Chendy/Anime_Game/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Davy-Chendy/Anime_Game" />
</a>
