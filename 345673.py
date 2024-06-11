import requests
import csv

# Cloudflare API参数
api_token = "******"
zone_id = "*******"
domain = "*******"  # 您的二级域名

# Cloudflare API端点
api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

# 请求标头
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# 发送 GET 请求以获取指定二级域名下的所有 DNS 记录
response = requests.get(api_url, headers=headers, params={"name": domain})

# 检查响应状态码
if response.status_code == 200:
    # 解析 JSON 响应
    result = response.json()
    # 提取 DNS 记录 ID
    dns_records = result["result"]
    dns_record_ids = [record["id"] for record in dns_records]

    # 删除指定二级域名下的所有 DNS 记录
    for record_id in dns_record_ids:
        delete_response = requests.delete(f"{api_url}/{record_id}", headers=headers)
        # 检查删除响应状态码
        if delete_response.status_code == 200:
            print(f"已删除 DNS 记录: {record_id}")
        else:
            print(f"删除 DNS 记录时出错：{delete_response.text}")

    # 接口地址
    url = "https://api.345673.xyz/get_data"

    # 免费 key
    key = "o1zrmHAF"

    # 请求体数据
    data = {
        "key": key
    }

    # 发送 POST 请求获取 IP 数据
    response = requests.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析 JSON 响应
        result = response.json()

        # 提取数据信息
        code = result["code"]
        if code == 200:
            info = result["info"]

            # 读取 CSV 文件并解析 IP 地址
            with open('ip.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["节点类别", "IP地址", "线路", "节点", "延迟", "下载速度", "时间"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # 循环遍历 API 返回的 IP 数据
                for category, ips in info.items():
                    for ip_info in ips:
                        delay_str = ip_info["delay"]  # 获取延迟字符串
                        # 去掉单位并尝试转换为浮点数
                        delay_str = delay_str.replace("ms", "")  # 去除单位
                        try:
                            delay = float(delay_str)
                            if delay <= 100:  # 筛选延迟不高于100的数据
                                # 将 IP 数据写入 CSV 文件
                                writer.writerow({
                                    "节点类别": category,
                                    "IP地址": ip_info["ip"],
                                    "线路": ip_info["line"],
                                    "节点": ip_info["node"],
                                    "延迟": delay,
                                    "下载速度": ip_info["downloadspeed"],
                                    "时间": ip_info["time"]
                                })

                                # 请求主体
                                data = {
                                    "type": "A",
                                    "name": domain,
                                    "content": ip_info["ip"],
                                    "ttl": 1,  # TTL（生存时间），以秒为单位
                                    "proxied": False  # 关闭 Cloudflare 代理
                                }

                                # 发送 POST 请求以创建DNS记录
                                response = requests.post(api_url, headers=headers, json=data)

                                # 检查响应状态码
                                if response.status_code == 200:
                                    print(f"IP地址 {ip_info['ip']} 已成功解析到Cloudflare域名下")
                                else:
                                    print(f"解析IP地址 {ip_info['ip']} 时出错：{response.text}")
                        except ValueError:
                            print("无法转换延迟值为浮点数：{}".format(ip_info['delay']))

            print("已将延迟不高于100的数据保存到 ip.csv 文件中")
        else:
            print("请求失败，错误信息：{}".format(result['info']))
    else:
        print("请求失败，状态码：{}".format(response.status_code))
else:
    print("获取 DNS 记录时出错：", response.text)
