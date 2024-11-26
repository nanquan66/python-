import string
import requests
import re
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

# 设置matplotlib显示中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

if __name__ == '__main__':

    url = 'https://www.gov.cn/gongbao/2024/issue_11246/202403/content_6941846.html'     # 目标网址
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }       # 修改请求的 headers 以伪装成浏览器访问
    req = requests.get(url=url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text

    # 将爬取的文本写入文件news.txt
    with open("news.txt", "w", encoding="utf-8") as file:
        file.write(html)

    # 读取并处理文本
    with open("news.txt", "r", encoding="utf-8") as file:
        txt1 = file.read()  # 原始文本
    txt2 = re.sub(r"[^\u4e00-\u9fa5]", "", txt1)  # 过滤噪音
    txt3 = jieba.cut(txt2)  # 使用cut方法进行中文分词
    txt4 = {}
    for i in txt3:
        if i not in txt4:
            txt4[i] = 1
        else:
            txt4[i] += 1        # 统计文本中每个词的出现次数
    txt5 = sorted(txt4.items(), key=lambda x: x[1], reverse=True)       # 将txt4按词出现的次数进行降序排列
    txt6 = {word: count for word, count in txt5 if len(word) >= 2}      # 过滤停用词（去除单个字）

    # 设置背景蒙版
    bgc_img = np.array(Image.open("ChinaMap.png"))

    # 生成词云
    wordcloud = WordCloud(
        background_color="white",
        font_path="fonts/msyh.ttc",  # 设置中文字体路径
        max_words=500,
        max_font_size=300,
        colormap="Reds",
        contour_width=8,
        contour_color="red",
        mask=bgc_img,  #
        width=800,
        height=800,
    ).generate_from_frequencies(txt6)

    # 显示词云图像
    image = wordcloud.to_image()
    image.show()

    # 绘制词频统计图表
    top_words = list(txt6.keys())[:10]  # 选择出现频率最高的10个词
    top_freqs = [txt6[word] for word in top_words]

    plt.figure(figsize=(10, 6))
    plt.bar(top_words, top_freqs, color='skyblue')
    plt.title('词频统计图表', fontsize=16)  # 设置标题为中文
    plt.xlabel('词汇', fontsize=14)  # 设置x轴标签为中文
    plt.ylabel('频率', fontsize=14)  # 设置y轴标签为中文
    plt.xticks(rotation=45, fontsize=12)  # 设置x轴刻度标签为中文
    plt.tight_layout()
    plt.show()
