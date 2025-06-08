#!/usr/bin/python3
import requests
import xml.etree.ElementTree as ET
import sys

# 替换为你的 Namecheap 账号信息和域名
API_USER   = "your_api_user"
API_KEY    = "your_api_key"
USERNAME   = "your_username"
CLIENT_IP  = "your_whitelisted_ip"
DOMAIN_SLD = "example"  # 主域名（不含 .com/.net 等）
DOMAIN_TLD = "com"      # 后缀


# 获取现有 DNS 记录
def get_dns_records():
    url = "https://api.namecheap.com/xml.response"
    params = {
        'ApiUser': API_USER,
        'ApiKey': API_KEY,
        'UserName': USERNAME,
        'ClientIp': CLIENT_IP,
        'Command': 'namecheap.domains.dns.getHosts',
        'SLD': DOMAIN_SLD,
        'TLD': DOMAIN_TLD
    }

    response = requests.post(url, params=params)
    print(response.text)
    if response.status_code != 200:
        raise Exception("Failed to contact Namecheap API.")

    root = ET.fromstring(response.content)
    namespace = {'nc': 'http://api.namecheap.com/xml.response'}
    if root.attrib.get('Status') != 'OK':
        raise Exception("API Error:\n" + response.text)

    hosts = []
    for host in root.findall(".//nc:host",namespace):
        hosts.append({
            'Type': host.attrib.get('Type', ''),
            'Name': host.attrib.get('Name', ''),
            'Address': host.attrib.get('Address', ''),
            'TTL': host.attrib.get('TTL', '1799')
        })

    return hosts

# 打印 DNS 记录
def print_dns_records():
    try:
        records = get_dns_records()
        for rec in records:
            print(f"{rec['Type']},{rec['Name']},{rec['Address']}")
    except Exception as e:
        print("Error:", e)

# 添加或更新记录（带去重）
def add_dns_record(new_type, new_host, new_value, new_ttl='1799'):
    try:
        existing_records = get_dns_records()

        # 过滤掉同类型+同主机的记录（即将被替换的）
        filtered_records = [
            rec for rec in existing_records
            if not (rec['Type'] == new_type and rec['Name'] == new_host)
        ]

        # 添加新的记录
        filtered_records.append({
            'Type': new_type,
            'Name': new_host,
            'Address': new_value,
            'TTL': new_ttl
        })

        # 组装 setHosts 请求
        url = "https://api.namecheap.com/xml.response"
        params = {
            'ApiUser': API_USER,
            'ApiKey': API_KEY,
            'UserName': USERNAME,
            'ClientIp': CLIENT_IP,
            'Command': 'namecheap.domains.dns.setHosts',
            'SLD': DOMAIN_SLD,
            'TLD': DOMAIN_TLD
        }

        for idx, rec in enumerate(filtered_records, start=1):
            params[f'HostName{idx}'] = rec['Name']
            params[f'RecordType{idx}'] = rec['Type']
            params[f'Address{idx}'] = rec['Address']
            params[f'TTL{idx}'] = rec['TTL']

        response = requests.post(url, params=params)
        print(response.text)
        root = ET.fromstring(response.content)
        namespace = {'nc': 'http://api.namecheap.com/xml.response'}
        if root.attrib.get('Status') != 'OK':
            raise Exception("API Error:\n" + response.text)

        print(f"Successfully added/updated DNS record: {new_type},{new_host},{new_value}")

    except Exception as e:
        print("Error:", e)

# 命令行主入口
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"{sys.argv[0]} list")
        print(f"{sys.argv[0]} set <type> <host> <value>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        print_dns_records()
    elif action == "set" and len(sys.argv) == 5:
        record_type = sys.argv[2].upper()
        host = sys.argv[3]
        value = sys.argv[4]
        add_dns_record(record_type, host, value)
    else:
        print("Invalid usage.")
        print(f"{sys.argv[0]} list")
        print(f"{sys.argv[0]} set <type> <host> <value>")

if __name__ == "__main__":
    main()



