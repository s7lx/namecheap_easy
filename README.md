# Namecheap_easy

[![EN doc](https://img.shields.io/badge/document-English-blue.svg)](README.md)
[![CN doc](https://img.shields.io/badge/文档-中文版-blue.svg)](README.zh.CN.md)

A Python-based command-line tool for managing **Namecheap DNS** records easily. It supports:

* **Listing** all DNS records for a given domain (`list` mode)
* **Adding/updating** a single DNS record while preserving others (`set` mode)
* **Deduplication**: if a record with the same type and host exists, it will be replaced; if value is the same, it will be skipped


> Ideal for CI/CD automation, local DNS management, and quick CLI modifications.

---

## Table of Contents

* [Features](#features)
* [How It Works](#how-it-works)
* [Requirements](#requirements)
* [Configuration](#configuration)
* [Quick Start](#quick-start)
* [Advanced Usage](#advanced-usage)
* [FAQ](#faq)
* [References](##References)
* [Contributing](#contributing)
* [License](#license)

---

## Features

| Feature           | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| List Records      | `python namecheap_dns.py list` prints records as `type,host,value` |
| Add/Update Record | `python namecheap_dns.py set <TYPE> <HOST> <VALUE>`                |
| Deduplication     | Same `TYPE + HOST` → overwrite; identical record → skip            |


---

## How It Works

1. **Fetch** records using `namecheap.domains.dns.getHosts`
2. **Merge** with the new one, replacing duplicates
3. **Submit** all records with `namecheap.domains.dns.setHosts`

> Note: `setHosts` **replaces the entire DNS table**. Always fetch-merge-set.

---

## Requirements

* Python ≥ 3.8
* import requests
* import xml.etree.ElementTree
* import sys


---

## Configuration

### 1. Hardcoded in Script

Edit the top of `namecheap_dns.py`:

```python
API_USER   = "your_api_user"
API_KEY    = "your_api_key"
USERNAME   = "your_username"
CLIENT_IP  = "your_whitelisted_ip"
DOMAIN_SLD = "example"
DOMAIN_TLD = "com"
```


### 2. Add Your IP to Namecheap API Whitelist

Before using the API, your current **public IP** must be whitelisted:

1. Log in to [Namecheap Dashboard](https://ap.www.namecheap.com/settings/tools/apiaccess)
2. Go to **API Access**
3. Add your **current public IP** to the whitelist (multiple entries allowed)
4. Wait 1-5 minutes to take effect

Otherwise, you'll receive the error: `IP address is not whitelisted`

---

## Quick Start

### List All DNS Records

```bash
python namecheap_easy.py list
```

Example output:

```
A,@,93.184.216.34
CNAME,www,example.com
```

### Add or Update a Record

```bash
python namecheap_easy.py set A blog 1.2.3.4
```

* If `A blog` exists with different value → **overwrite**
* If identical record exists → **skip**

---


## FAQ

> **Q1:** Why am I getting `IP address is not whitelisted`?
>
> **A1:** Go to Namecheap → Profile → API Access and add your public IP.

> **Q2:** Can I add more than one record?
>
> **A2:** Yes. Just append more entries to the `filtered_records` list.

> **Q3:** Can this be used with sub-accounts?
>
> **A3:** Yes, as long as they have proper API permissions.

---

## References

- Official Namecheap API Documentation:
  - [`domains.dns.getHosts`](https://www.namecheap.com/support/api/methods/domains-dns/get-list/)
  - [`domains.dns.setHosts`](https://www.namecheap.com/support/api/methods/domains-dns/set-hosts/)


## Contributing

Welcomed contributions:

* Features (batch import, deletion, async)
* Bug fixes
* Docs improvements

---

## License

MIT License. See [LICENSE](LICENSE).

---

> **Disclaimer**: This project is not affiliated with Namecheap. Use at your own risk and store your API credentials securely.

---

# 中文说明

请查看本仓库中的 [![CN doc](https://img.shields.io/badge/文档-中文版-blue.svg)](README.zh.CN.md) 获取中文使用说明。

---

