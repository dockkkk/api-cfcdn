import requests
import csv

# Cloudflare API参数
api_token = "****"
zone_id = "****"
domain = "****"  # 您的二级域名

# Cloudflare API端点
api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

# 请求标头
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# 删除指定二级域名下的所有 DNS 记录
def delete_all_dns_records():
    response = requests.get(api_url, headers=headers, params={"name": domain})
    if response.status_code == 200:
        result = response.json()
        dns_records = result["result"]
        dns_record_ids = [record["id"] for record in dns_records]

        for record_id in dns_record_ids:
            delete_response = requests.delete(f"{api_url}/{record_id}", headers=headers)
            if delete_response.status_code == 200:
                print(f"已删除 DNS 记录: {record_id}")
            else:
                print(f"删除 DNS 记录时出错：{delete_response.text}")
    else:
        print("获取 DNS 记录时出错：", response.text)

# 获取优选 IP 数据并筛选延迟最低的 3 个数据
def fetch_and_filter_ips():
    url = "https://api.345673.xyz/get_data"
    key = "o1zrmHAF"
    data = {"key": key}

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result["code"] == 200:
            info = result["info"]

            ip_list = []
            for category_name, ips in info.items():
                for ip_info in ips:
                    delay_str = ip_info["delay"].replace("ms", "")
                    try:
                        delay = float(delay_str)
                        ip_info["delay"] = delay
                        ip_info["category"] = category_name  # 添加 category 信息
                        ip_list.append(ip_info)
                    except ValueError:
                        print("无法转换延迟值为浮点数：{}".format(ip_info['delay']))

            # 按延迟排序并取前 3 个
            ip_list.sort(key=lambda x: x["delay"])
            top_3_ips = ip_list[:3]

            with open('ip.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["节点类别", "IP地址", "线路", "节点", "延迟", "下载速度", "时间"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for ip_info in top_3_ips:
                    writer.writerow({
                        "节点类别": ip_info["category"],
                        "IP地址": ip_info["ip"],
                        "线路": ip_info["line"],
                        "节点": ip_info["node"],
                        "延迟": ip_info["delay"],
                        "下载速度": ip_info["downloadspeed"],
                        "时间": ip_info["time"]
                    })

            return [ip_info["ip"] for ip_info in top_3_ips]
        else:
            print("请求失败，错误信息：{}".format(result['info']))
    else:
        print("请求失败，状态码：{}".format(response.status_code))
    return []

# 将筛选后的 IP 地址解析到 Cloudflare 域名下
def add_dns_records(ip_addresses):
    for ip_address in ip_addresses:
        data = {
            "type": "A",
            "name": domain,
            "content": ip_address,
            "ttl": 1,
            "proxied": False
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"IP地址 {ip_address} 已成功解析到 Cloudflare 域名下")
        else:
            print(f"解析IP地址 {ip_address} 时出错：{response.text}")

# 主函数
def main():
    delete_all_dns_records()
    ip_addresses = fetch_and_filter_ips()
    if ip_addresses:
        add_dns_records(ip_addresses)
        print("所有操作已完成")
    else:
        print("没有符合条件的 IP 地址")

if __name__ == "__main__":
    main()
