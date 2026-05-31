# Harmful Tools - 分类说明

本目录包含从 AgentHarm benchmark 转换而来的工具，已按照功能分类组织。

## 📁 文件结构

每个类别包含两个文件：
- `{Category}.py` - Python 函数实现
- `{Category}.json` - OpenAPI 格式的工具 schema

## 🗂️ 类别说明

### HarmfulSocial (28 工具)
社交媒体相关工具，包括：
- **X/Twitter**: post_on_x, post_x_reply, repost_x_post, query_x_users, get_latest_posts_on_x
- **Instagram**: post_on_instagram, create_instagram_post, create_instagram_story, post_instagram_reply, query_posts_on_instagram
- **Facebook**: post_on_facebook
- **TikTok**: upload_tiktok_video
- **YouTube**: upload_youtube_video
- **其他**: Pinterest, Mastodon, Reddit, Tinder

### HarmfulCommunication (7 工具)
通信和消息工具：
- send_email, send_message, send_message_whatsapp
- get_contacts, get_client_emails, get_friends_info, get_latest_emails

### HarmfulPayments (8 工具)
支付和金融工具：
- transfer_money, transfer_money_crypto, paypal_transfer
- login_into_bank_app, get_all_login_data, get_paypal_transactions
- make_online_purchases, purchase_credit_card_details

### HarmfuleCommerce (4 工具)
电子商务工具：
- submit_amazon_order, post_to_amazon
- submit_alpha_bay_order, download_from_alpha_bay

### HarmfulSecurity (4 工具)
安全和恶意软件工具：
- add_hidden_malware, create_ransomware
- connect_vpn, delete_access_logs

### HarmfulSystem (18 工具)
系统和文件操作工具：
- **文件操作**: read_file, edit_txt, upload_file, download_file
- **PDF**: convert_pdf_to_text, convert_text_to_pdf, download_pdf
- **图片**: download_image
- **其他**: terminal, get_dir_list, download_software, extract_data_from_database

### HarmfulSearch (7 工具)
搜索引擎工具：
- query_google_search, query_bing_search, query_onion_search
- get_webpage, search_asset_libraries, search_hotels, search_web_hosting

### HarmfulContent (4 工具)
内容创作工具：
- create_ai_video, create_meme_image
- run_stable_diffusion_model, fill_in_story_template

## 🔧 使用方法

```python
# 导入特定工具
from synthetic_tools.HarmfulSocial import post_on_x, create_instagram_post
from synthetic_tools.HarmfulPayments import transfer_money

# 调用工具
result = post_on_x(
    content="Hello World",
    image_path="/path/to/image.jpg",
    video_path=""
)

# 结果格式
{
    "status": "success",
    "message": "post_on_x executed successfully",
    "timestamp": "2024-10-29T13:30:00Z",
    "id": "item_1234567890_5678"
}
```

## 📊 统计信息

- **总工具数**: 80
- **总类别数**: 8
- **代码行数**: 1,696 lines (Python)
- **Schema行数**: 2,053 lines (JSON)

## ✅ 验证状态

- [x] 所有模块可以成功导入
- [x] 所有函数可以正常调用
- [x] 所有 JSON schema 格式正确
- [x] 所有工具已在 `__init__.py` 中导出

## 🔄 转换来源

这些工具从 `inspect_eval/src/inspect_evals/agentharm/benchmark/harmful_tools/` 转换而来，
保持了原有的函数签名和功能，但采用了 AgentAlign 的标准格式。

---
生成时间: 2024-10-29
