#增加了main_url的判断
# coding=utf-8
import urllib.request
import os



url_file_path = os.getcwd()
print("当前文件路径：", url_file_path)
url_path = url_file_path + '\\main_url.txt'
if os.path.exists(url_path):
    print("OK!")
    print("--------------------")
else:
    print("文件不存在！正在创建中......")
    file_url = open('./main_url.txt','w')
    file_url.write('https://newtrackon.com/api/all')
    #os.mkdir(url_path)
    print("OK!")
    print("--------------------")



print("读取URL中......")
result = []
with open('main_url.txt', 'r') as f:
    for line in f:
        result.append(list(line.strip('\n').split(',')))
url_number = len(result)
print("OK!")
print("URL列表：", result)
print("--------------------")


#打印網頁至trackers.txt
file_path = os.getcwd()
#print("當前文件路徑：", file_path)
path = file_path + '\\trackers.txt'
print("正在输出trackers至trackers.txt")
if os.path.exists(path):
    print("文件存在！正在删除原始内容......")
    with open("./trackers.txt", 'r+') as files:
        files.truncate(0)
    print("OK!")
    print("--------------------")
else:
    print("文件不存在！正在创建中......")
    file_trackers = open('./trackers.txt','w')
    #os.mkdir(path)
    print("OK!")
    print("--------------------")

#file = open('./trackers.txt', 'w')
#file.write(html)



#打開網頁
#print("正在嘗試獲取trackers......")
trackers_list = []
for url_line in open("./main_url.txt"):
    print(url_line)
    try:
        #html = urllib.request.urlopen(url_line).read().decode()
        headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        req = urllib.request.Request(url=url_line,headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        trackers_list.append(html)
        #print(trackers_list)
        with open('./trackers.txt', 'a') as f:
            f.writelines(html)
            print("OK!")
    except:
        continue
#print(html)



def remove_duplicates():
    print("--------------------")
    print("正在准备去重中...")
    f_read=open(r'./trackers.txt','r')     #将需要去除重复值的txt文本重命名text.txt
    f_write=open(r'./output_trackers.txt','w')  #去除重复值之后，生成新的txt文本 --“去除重复值后的文本.txt”
    data=set()
    for a in [a.strip('\n') for a in list(f_read)]:
        if a not in data:
            f_write.write(a+'\n')
            data.add(a)
    f_read.close()
    f_write.close()
    print("OK!")
remove_duplicates()