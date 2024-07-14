# coding=utf-8
import urllib.request
import os
import wget

# 获取当前文件路径并检查 main_url.txt
url_file_path = os.getcwd()
print("当前文件路径：", url_file_path)
url_path = os.path.join(url_file_path, 'main_url.txt')
if os.path.exists(url_path):
    print("OK!")
    print("--------------------")
else:
    print("文件不存在！正在创建中......")
    main_url = "https://raw.githubusercontent.com/phishinqi/phishinqi.github.io/main/assets/txt/trackers_url.txt"
    wget.download(main_url, "./main_url.txt")
    print("OK!")
    print("--------------------")

# 读取 main_url.txt 文件内容并输出 URL 列表
print("读取URL中......")
result = []
with open('main_url.txt', 'r') as f:
    for line in f:
        result.append(list(line.strip('\n').split(',')))
url_number = len(result)
print("OK!")
print("URL列表：", result)
print("--------------------")

# 检查并创建 trackers.txt 文件
file_path = os.getcwd()
path = os.path.join(file_path, 'trackers.txt')
print("正在输出trackers至trackers.txt")
if os.path.exists(path):
    print("文件存在！正在删除原始内容......")
    with open(path, 'r+') as files:
        files.truncate(0)
    print("OK!")
    print("--------------------")
else:
    print("文件不存在！正在创建中......")
    with open(path, 'w') as file_trackers:
        pass
    print("OK!")
    print("--------------------")

# 读取 main_url.txt 中的 URL 并写入 trackers.txt
trackers_list = []
for url_line in open("./main_url.txt"):
    url_line = url_line.strip()  # 去除空白行
    if not url_line:
        continue
    print(url_line)
    try:
        headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        req = urllib.request.Request(url=url_line, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        trackers_list.append(html)
        with open(path, 'a') as f:
            f.writelines(html + '\n')
            print("OK!")
        try:
            os.remove(url_path)
        except OSError as e:
            print(e)
        else:
            print("File is deleted successfully")
    except Exception as e:
        print(e)
        continue

# 去除 trackers.txt 文件中的重复行，并在行与行之间添加空白行
def remove_duplicates_and_add_blank_lines():
    print("--------------------")
    print("正在准备去重中...")
    with open('./trackers.txt', 'r') as f_read, open('./output_trackers.txt', 'w') as f_write:
        data = set()
        for line in f_read:
            stripped_line = line.strip()
            if stripped_line and stripped_line not in data:
                f_write.write(stripped_line + '\n\n')  # 添加空白行
                data.add(stripped_line)
    print("OK!")

remove_duplicates_and_add_blank_lines()
