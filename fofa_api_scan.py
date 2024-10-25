import requests
import base64
import os
from colorama import init, Fore
import pandas as pd
import openpyxl

init(autoreset=True)


# 定义 Fofa 查询函数
def fofa_query(email, key, target, country):
    query = f'domain="{target}" && country="{country}" 2239304286@qq.com&& status_code=200'  # fofa查询的语法
    query_b64 = base64.b64encode(query.encode('utf-8')).decode('utf-8')  # 语法需要经过base64编码
    url_api = f'https://fofa.info/api/v1/search/all?email={email}&key={key}&qbase64={query_b64}&size=10000&fields=host,ip,port'

    print(Fore.BLUE + f"[INFO] 开始调用 Fofa API 查询 {target} 的子域...")
    try:
        response = requests.get(url=url_api, headers=headers, timeout=15, verify=False).json()
        if response.get('error'):
            print(Fore.RED + f"Fofa 查询失败: {response.get('error_msg')}")
            return []
        print(Fore.GREEN + "Fofa 查询成功!")
        subdomains = [item[0] for item in response.get("results", [])]
        return subdomains
    except Exception as e:
        print(Fore.RED + f"请求出错: {e}")
        return []

#将txt文本转换为Excel表格
def txt_to_excel(txt_file, excel_file):
    # 读取 txt 文件
    data = pd.read_csv(txt_file, header=None, names=['Subdomains'])
    # 写入 Excel 文件
    data.to_excel(excel_file, index=False)
    print(Fore.GREEN + f"子域名已保存至 Excel 文件: {excel_file}")



# 主程序入口
if __name__ == '__main__':
    # 提示用户输入 Fofa 邮箱、API 密钥、目标域名和国家
    fofa_email = input(Fore.CYAN + "请输入 Fofa 邮箱: ")
    fofa_key = input(Fore.CYAN + "请输入 Fofa API 密钥: ")
    target_domain = input(Fore.CYAN + "请输入目标域名: ")
    target_country = input(Fore.CYAN + "请输入目标国家 (例如 CN): ")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    # 清除代理设置
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)

    # 调用 Fofa 查询函数
    subdomains = fofa_query(fofa_email, fofa_key, target_domain, target_country)

    # 创建一个集合来存储去重后的子域名
    subdomains_set = set(subdomains)

    # 将结果保存到文件
    output_file = "fofa_subdomains.txt"
    with open(output_file, 'w') as file:
        for subdomain in subdomains_set:
            file.write(subdomain + '\n')

    print(Fore.GREEN + f"获取去重后子域名个数为: {len(subdomains_set)}")
    print(Fore.GREEN + f"结果已保存到 {output_file}")

    # 调用函数，将 txt 文件转换为 Excel
    excel_output_file = "fofa_subdomains.xlsx"
    txt_to_excel(output_file, excel_output_file)

