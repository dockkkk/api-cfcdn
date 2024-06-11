import requests
import csv

# Cloudflare API 参数
api_token = "******"
zone_id = "*****"
subdomain = "*****"  # 您的二级域名

# Cloudflare API 端点
api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

# 请求标头
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# 发送 GET 请求以获取所有指定二级域名下的 DNS 记录
response = requests.get(api_url, headers=headers, params={"name": subdomain})

# 检查响应状态码
if response.status_code == 200:
    # 解析 JSON 响应
    data = response.json()
    
    # 遍历每个 DNS 记录并删除它们
    for record in data['result']:
        record_id = record['id']
            
        # 构造删除记录的 API 端点
        delete_url = f"{api_url}/{record_id}"
            
        # 发送 DELETE 请求以删除记录
        delete_response = requests.delete(delete_url, headers=headers)
            
        # 检查删除记录的响应状态码
        if delete_response.status_code == 200:
            print(f"已成功删除 DNS 记录：{record['name']} - {record['content']}")
        else:
            print(f"删除 DNS 记录时出错：{delete_response.text}")

    # 删除完毕后，您可以继续添加新的记录
    # 定义文件 URL 和保存路径
    url = "https://raw.githubusercontent.com/ymyuuu/IPDB/main/bestproxy.txt"
    save_path = "result.csv"

    # 发送 GET 请求到 URL
    response = requests.get(url)

    # 检查请求是否成功（状态码为 200）
    if response.status_code == 200:
        # 解码响应内容为文本
        content = response.text
        
        # 将内容分割成行
        lines = content.split('\n')
        
        # 以写入模式打开 CSV 文件
        with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
            # 创建 CSV 写入器对象
            csv_writer = csv.writer(csvfile)
            
            # 遍历每一行
            for line in lines:
                # 通过空格分割行
                data = line.split()
                
                # 将数据写入 CSV 文件
                csv_writer.writerow(data)
        
        print("数据已保存到", save_path)
        
        # 从 CSV 文件中读取 IP 地址并解析到 Cloudflare 域名下
        with open(save_path, 'r', newline='', encoding='utf-8') as csvfile:
            # 创建 CSV 读取器对象
            csv_reader = csv.reader(csvfile)
            
            # 跳过标题行（如果有的话）
            next(csv_reader)
            
            # 读取每一行数据
            for row in csv_reader:
                ip_address = row[0]  # 假设 IP 地址在第一列
                
                # Cloudflare API 端点
                api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

                # 请求主体
                data = {
                    "type": "A",
                    "name": subdomain,
                    "content": ip_address,
                    "ttl": 1,  # TTL（生存时间），以秒为单位
                    "proxied": False  # 关闭 Cloudflare 代理
                }

                # 发送 POST 请求以创建 DNS 记录
                response = requests.post(api_url, headers=headers, json=data)

                # 检查响应状态码
                if response.status_code == 200:
                    print(f"IP 地址 {ip_address} 已成功解析到 Cloudflare 域名下")
                else:
                    print(f"解析 IP 地址 {ip_address} 时出错：", response.text)
    else:
        print("无法从 URL 检索数据")
else:
    print("获取 DNS 记录时出错：", response.text)
