# coding=utf-8
import urllib.request
import os

# 获取当前文件路径并检查 main_url.txt
def check_and_download_main_url():
    url_file_path = os.getcwd()
    print("当前文件路径：", url_file_path)
    url_path = os.path.join(url_file_path, 'main_url.txt')
    if os.path.exists(url_path):
        print("main_url.txt 文件已存在。")
    else:
        print("main_url.txt 文件不存在，正在下载...")
        main_url = "https://raw.githubusercontent.com/phishinqi/phishinqi.github.io/main/assets/txt/trackers_url.txt"
        with urllib.request.urlopen(main_url) as response, open(url_path, 'wb') as out_file:
            out_file.write(response.read())
        print("main_url.txt 文件下载完成。")

# 读取 main_url.txt 文件内容并输出 URL 列表
def read_urls():
    print("读取 URL 中...")
    with open('main_url.txt', 'r') as f:
        urls = [line.strip('\n') for line in f if line.strip('\n')]
    return urls

# 检查并创建 trackers.txt 文件
def prepare_trackers_file(file_path):
    if os.path.exists(file_path):
        print("trackers.txt 文件存在，正在清空内容...")
        with open(file_path, 'w') as files:
            pass  # 清空文件内容
    else:
        print("trackers.txt 文件不存在，正在创建...")
        with open(file_path, 'w') as file_trackers:
            pass  # 创建空文件

# 读取 URL 并写入 trackers.txt
def fetch_and_write_trackers(urls, trackers_file_path):
    for url in urls:
        print(f"正在处理 URL: {url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            req = urllib.request.Request(url=url, headers=headers)
            res = urllib.request.urlopen(req)
            html = res.read().decode('utf-8')
            with open(trackers_file_path, 'a') as f:
                f.write(html + '\n')
            print("处理完成。")
        except Exception as e:
            print(f"处理 URL {url} 时发生错误: {e}")

# 去除 trackers.txt 文件中的重复行，并在行与行之间添加空白行
def remove_duplicates(input_file, output_file):
    print("正在去重...")
    with open(input_file, 'r') as f_read, open(output_file, 'w') as f_write:
        seen = set()
        for line in f_read:
            stripped_line = line.strip()
            if stripped_line not in seen:
                f_write.write(stripped_line + '\n\n')
                seen.add(stripped_line)
    print("去重完成。")

# 主函数
def main():
    check_and_download_main_url()
    urls = read_urls()
    trackers_file_path = os.path.join(os.getcwd(), 'trackers.txt')
    prepare_trackers_file(trackers_file_path)
    fetch_and_write_trackers(urls, trackers_file_path)
    remove_duplicates('./trackers.txt', './output_trackers.txt')

if __name__ == "__main__":
    main()
