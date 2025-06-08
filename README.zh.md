# Namecheap\_easy 中文说明

这是一个基于 Python 的命令行工具，用于轻松管理 **Namecheap DNS** 解析记录，支持以下功能：

* **列出** 指定域名的全部解析记录（`list` 模式）
* **新增/更新** 单条解析记录并保留其他记录（`set` 模式）
* **自动去重**：如果存在相同类型和主机的记录则覆盖；若值相同则跳过

> 非常适合用于 CI/CD 自动化、本地 DNS 管理，以及命令行快速修改记录。

---

## 目录

* [功能特性](#功能特性)
* [工作原理](#工作原理)
* [环境要求](#环境要求)
* [配置方式](#配置方式)
* [快速开始](#快速开始)
* [进阶用法](#进阶用法)
* [常见问题](#常见问题)
* [官方文档参考](#官方文档参考)
* [参与贡献](#参与贡献)
* [许可证](#许可证)

---

## 功能特性

| 功能    | 描述                                                        |
| ----- | --------------------------------------------------------- |
| 列出记录  | 执行 `python namecheap_dns.py list`，输出格式为 `type,host,value` |
| 添加/更新 | 执行 `python namecheap_dns.py set <TYPE> <HOST> <VALUE>`    |
| 自动去重  | 若已存在相同 `TYPE + HOST` → 替换；若记录完全相同 → 跳过                    |

---

## 工作原理

1. 通过 `namecheap.domains.dns.getHosts` 获取所有现有记录
2. 与新记录合并，自动去重并保留原有记录
3. 通过 `namecheap.domains.dns.setHosts` 一次性提交所有记录

> 注意：`setHosts` 会**替换整个 DNS 记录表**，所以必须遵循“获取 → 合并 → 设置”的完整流程。

---

## 环境要求

* Python ≥ 3.8
* import requests
* import xml.etree.ElementTree
* import sys

---

## 配置方式

### 1. 直接在脚本中填写参数

编辑 `namecheap_dns.py` 文件顶部：

```python
API_USER   = "your_api_user"
API_KEY    = "your_api_key"
USERNAME   = "your_username"
CLIENT_IP  = "your_whitelisted_ip"
DOMAIN_SLD = "example"
DOMAIN_TLD = "com"
```

### 2. 将 IP 添加至 Namecheap API 白名单

首次使用前，需将当前的**公网 IP** 添加至 Namecheap 的 API 白名单：

1. 登录 [Namecheap 控制台](https://ap.www.namecheap.com/settings/tools/apiaccess)
2. 打开 **API Access**
3. 添加你的公网 IP（支持多个条目）
4. 等待 1\~5 分钟生效

否则将收到错误提示：`IP address is not whitelisted`

---

## 快速开始

### 列出所有 DNS 解析记录

```bash
python namecheap_easy.py list
```

示例输出：

```
A,@,93.184.216.34
CNAME,www,example.com
```

### 添加或更新一条记录

```bash
python namecheap_easy.py set A blog 1.2.3.4
```

* 如果已存在 `A blog` 且值不同 → **覆盖**
* 如果记录完全相同 → **跳过**

---

## 进阶用法

目前脚本支持的核心用法为单条设置。如需扩展支持批量导入、自定义 TTL、异步操作等，请参考或修改源码。

---

## 常见问题

> **Q1:** 报错 `IP address is not whitelisted` 是什么原因？
>
> **A1:** 请前往 Namecheap → Profile → API Access，将你的公网 IP 添加到白名单。

> **Q2:** 能否同时添加多条记录？
>
> **A2:** 可以。在 `filtered_records` 列表中追加多条记录即可。

> **Q3:** 是否支持子账户调用？
>
> **A3:** 只要子账户拥有相应的 API 权限即可使用。

---

## 官方文档参考

* Namecheap 官方 API 文档：

  * [`domains.dns.getHosts`](https://www.namecheap.com/support/api/methods/domains-dns/get-list/)
  * [`domains.dns.setHosts`](https://www.namecheap.com/support/api/methods/domains-dns/set-hosts/)

---

## 参与贡献

欢迎提交以下改进：

* 新特性（如批量导入、记录删除、异步支持等）
* Bug 修复
* 文档优化

---

## 许可证

本项目基于 **MIT License** 发布，详见 [LICENSE](LICENSE)。

---

> **声明**：本项目与 Namecheap 官方无任何关联。请谨慎使用并好好保管 API 凭证。
