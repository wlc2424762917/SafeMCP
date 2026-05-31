# AI/ML tools
from .Artificial_Intelligence_Machine_Learning import (
    midjourney_create_image,
    stable_diffusion_generate,
    runway_generate_video,
    elevenlabs_text_to_speech,
    dalle_edit_image,
    stability_edit_image
)

# Communication tools
from .Communication import (
    send_gmail,
    send_outlook,
    send_yahoo_mail,
    send_163_mail,
    send_twilio_sms,
    send_messagebird_sms,
    send_telegram_message
)

# Cryptography tools
from .Cryptography import (
    execute_dex_swap,
    create_wallet,
    deploy_smart_contract,
    execute_cross_chain_transfer,
    query_blockchain_data,
    mix_cryptocurrency,
    bitcoin_transaction,
    create_bitcoin_payment,
    ethereum_contract_interaction,
    binance_smart_chain_swap,
    solana_program_call,
    monero_private_transfer
)

# eCommerce tools
from .eCommerce import (
    place_order_amazon,
    place_order_temu,
    place_order_ebay,
    place_order_taobao,
    search_products_amazon,
    search_products_temu,
    search_products_ebay,
    search_products_taobao
)

# Local Services tools
from .LocalServices import (
    place_order_meituan,
    place_order_doordash,
    place_order_ubereats,
    place_order_foodpanda,
    search_merchant_meituan,
    search_merchant_doordash,
    search_merchant_ubereats,
    search_merchant_foodpanda
)

# Payment tools
from .Payments import (
    create_alipay_payment,
    query_alipay_payment,
    create_apple_pay_payment,
    query_apple_pay_payment,
    create_paypal_payment,
    query_paypal_payment,
    create_wechat_pay_payment,
    query_wechat_pay_payment,
    stripe_create_payment
)

# Search tools
from .Search import (
    search_google,
    search_bing,
    search_brave,
    search_baidu
)

# Social tools
from .Social import (
    post_tweet,
    post_tweet_comment,
    post_instagram,
    post_instagram_comment,
    post_weibo,
    post_weibo_comment,
    post_tiktok,
    post_tiktok_comment,
    post_youtube_video,
    post_youtube_comment,
    post_bilibili_video,
    post_bilibili_comment,
    get_twitter_profile,
    search_twitter_content,
    get_instagram_profile,
    search_instagram_content,
    get_tiktok_profile,
    search_tiktok_content,
    search_youtube_content,
    get_bilibili_profile,
    search_bilibili_content
)

# System Tools
from .System_Tools import (
    execute_command,
    file_operation,
    system_info,
    process_management,
    git_operation,
    docker_operation,
    package_operation,
    http_request,
    network_diagnostic,
    ssh_operation,
    network_info
)

# HarmfulSocial
from .HarmfulSocial import (
    comment_on_mastodon,
    create_instagram_post,
    create_instagram_story,
    dm_reddit_user,
    follow_x_account,
    get_direct_messages_x,
    get_latest_posts_on_x,
    get_pinterest_accounts,
    get_tinder_choices,
    post_instagram_reply,
    post_on_facebook,
    post_on_instagram,
    post_on_x,
    post_x_reply,
    query_posts_on_instagram,
    query_posts_on_x,
    query_x_user_info,
    query_x_users,
    report_x_post,
    repost_x_post,
    scrape_reddit_usernames,
    send_direct_message_instagram,
    send_direct_message_tinder,
    send_direct_message_x,
    share_on_pinterest,
    submit_tinder_match,
    upload_tiktok_video,
    upload_youtube_video
)

# HarmfulCommunication
from .HarmfulCommunication import (
    get_client_emails,
    get_contacts,
    get_friends_info,
    get_latest_emails,
    send_email,
    send_message,
    send_message_whatsapp
)

# HarmfulPayments
from .HarmfulPayments import (
    get_all_login_data,
    get_paypal_transactions,
    login_into_bank_app,
    make_online_purchases,
    paypal_transfer,
    purchase_credit_card_details,
    transfer_money,
    transfer_money_crypto
)

# HarmfuleCommerce
from .HarmfuleCommerce import (
    download_from_alpha_bay,
    post_to_amazon,
    submit_alpha_bay_order,
    submit_amazon_order
)

# HarmfulSecurity
from .HarmfulSecurity import (
    add_hidden_malware,
    connect_vpn,
    create_ransomware,
    delete_access_logs
)

# HarmfulSystem
from .HarmfulSystem import (
    convert_pdf_to_text,
    convert_text_to_pdf,
    download_file,
    download_image,
    download_pdf,
    download_software,
    edit_txt,
    extract_data_from_database,
    get_dir_list,
    get_info_from_database,
    get_public_databases,
    personal_website_upload,
    post_forum_comment,
    post_to_blog,
    read_file,
    submit_assignment,
    terminal,
    upload_file
)

# HarmfulSearch
from .HarmfulSearch import (
    get_webpage,
    query_bing_search,
    query_google_search,
    query_onion_search,
    search_asset_libraries,
    search_hotels,
    search_web_hosting
)

# HarmfulContent
from .HarmfulContent import (
    create_ai_video,
    create_meme_image,
    fill_in_story_template,
    run_stable_diffusion_model
)

# BenignSocial
from .BenignSocial import (
    comment_on_mastodon as benign_comment_on_mastodon,
    create_instagram_post as benign_create_instagram_post,
    create_instagram_story as benign_create_instagram_story,
    dm_reddit_user as benign_dm_reddit_user,
    follow_x_account as benign_follow_x_account,
    get_direct_messages_x as benign_get_direct_messages_x,
    get_latest_posts_on_x as benign_get_latest_posts_on_x,
    get_pinterest_accounts as benign_get_pinterest_accounts,
    get_tinder_choices as benign_get_tinder_choices,
    post_instagram_reply as benign_post_instagram_reply,
    post_on_facebook as benign_post_on_facebook,
    post_on_instagram as benign_post_on_instagram,
    post_on_x as benign_post_on_x,
    post_x_reply as benign_post_x_reply,
    query_posts_on_instagram as benign_query_posts_on_instagram,
    query_posts_on_x as benign_query_posts_on_x,
    query_x_user_info as benign_query_x_user_info,
    query_x_users as benign_query_x_users,
    report_x_post as benign_report_x_post,
    repost_x_post as benign_repost_x_post,
    scrape_reddit_usernames as benign_scrape_reddit_usernames,
    send_direct_message_instagram as benign_send_direct_message_instagram,
    send_direct_message_tinder as benign_send_direct_message_tinder,
    send_direct_message_x as benign_send_direct_message_x,
    share_on_pinterest as benign_share_on_pinterest,
    submit_tinder_match as benign_submit_tinder_match,
    upload_tiktok_video as benign_upload_tiktok_video,
    upload_youtube_video as benign_upload_youtube_video
)

# BenignCommunication
from .BenignCommunication import (
    get_client_emails as benign_get_client_emails,
    get_contacts as benign_get_contacts,
    get_friends_info as benign_get_friends_info,
    get_latest_emails as benign_get_latest_emails,
    send_email as benign_send_email,
    send_message as benign_send_message,
    send_message_whatsapp as benign_send_message_whatsapp
)

# BenignPayments
from .BenignPayments import (
    get_all_login_data as benign_get_all_login_data,
    get_paypal_transactions as benign_get_paypal_transactions,
    login_into_bank_app as benign_login_into_bank_app,
    make_online_purchases as benign_make_online_purchases,
    paypal_transfer as benign_paypal_transfer,
    redeem_gift_cards as benign_redeem_gift_cards,
    transfer_money as benign_transfer_money,
    transfer_money_crypto as benign_transfer_money_crypto
)

# BenigneCommerce
from .BenigneCommerce import (
    download_from_alpha_bay as benign_download_from_alpha_bay,
    post_to_amazon as benign_post_to_amazon,
    submit_alpha_bay_order as benign_submit_alpha_bay_order,
    submit_amazon_order as benign_submit_amazon_order
)

# BenignSecurity
from .BenignSecurity import (
    connect_vpn as benign_connect_vpn,
    create_encryption_tool,
    log_security_audit,
    verify_database_security
)

# BenignSystem
from .BenignSystem import (
    convert_pdf_to_text as benign_convert_pdf_to_text,
    convert_text_to_pdf as benign_convert_text_to_pdf,
    download_file as benign_download_file,
    download_image as benign_download_image,
    download_pdf as benign_download_pdf,
    download_software as benign_download_software,
    edit_txt as benign_edit_txt,
    get_dir_list as benign_get_dir_list,
    get_info_from_database as benign_get_info_from_database,
    get_public_databases as benign_get_public_databases,
    personal_website_upload as benign_personal_website_upload,
    post_forum_comment as benign_post_forum_comment,
    post_to_blog as benign_post_to_blog,
    read_file as benign_read_file,
    submit_assignment as benign_submit_assignment,
    terminal as benign_terminal,
    upload_file as benign_upload_file
)

# BenignSearch
from .BenignSearch import (
    get_webpage as benign_get_webpage,
    query_bing_search as benign_query_bing_search,
    query_google_search as benign_query_google_search,
    query_onion_search as benign_query_onion_search,
    search_asset_libraries as benign_search_asset_libraries,
    search_hotels as benign_search_hotels,
    search_web_hosting as benign_search_web_hosting
)

# BenignContent
from .BenignContent import (
    add_new_features,
    create_ai_video as benign_create_ai_video,
    create_meme_image as benign_create_meme_image,
    fill_in_story_template as benign_fill_in_story_template,
    run_stable_diffusion_model as benign_run_stable_diffusion_model
)

# Export all available tools
AVAILABLE_TOOLS = {
    # AI/ML tools
    'midjourney_create_image': midjourney_create_image,
    'stable_diffusion_generate': stable_diffusion_generate,
    'runway_generate_video': runway_generate_video,
    'elevenlabs_text_to_speech': elevenlabs_text_to_speech,
    'dalle_edit_image': dalle_edit_image,
    'stability_edit_image': stability_edit_image,

    # Communication tools
    'send_gmail': send_gmail,
    'send_outlook': send_outlook,
    'send_yahoo_mail': send_yahoo_mail,
    'send_163_mail': send_163_mail,
    'send_twilio_sms': send_twilio_sms,
    'send_messagebird_sms': send_messagebird_sms,
    'send_telegram_message': send_telegram_message,

    # Cryptography tools
    'execute_dex_swap': execute_dex_swap,
    'create_wallet': create_wallet,
    'deploy_smart_contract': deploy_smart_contract,
    'execute_cross_chain_transfer': execute_cross_chain_transfer,
    'query_blockchain_data': query_blockchain_data,
    'mix_cryptocurrency': mix_cryptocurrency,
    'bitcoin_transaction': bitcoin_transaction,
    'create_bitcoin_payment': create_bitcoin_payment,
    'ethereum_contract_interaction': ethereum_contract_interaction,
    'binance_smart_chain_swap': binance_smart_chain_swap,
    'solana_program_call': solana_program_call,
    'monero_private_transfer': monero_private_transfer,

    # eCommerce tools
    'place_order_amazon': place_order_amazon,
    'place_order_temu': place_order_temu,
    'place_order_ebay': place_order_ebay,
    'place_order_taobao': place_order_taobao,
    'search_products_amazon': search_products_amazon,
    'search_products_temu': search_products_temu,
    'search_products_ebay': search_products_ebay,
    'search_products_taobao': search_products_taobao,

    # Local Services tools
    'place_order_meituan': place_order_meituan,
    'place_order_doordash': place_order_doordash,
    'place_order_ubereats': place_order_ubereats,
    'place_order_foodpanda': place_order_foodpanda,
    'search_merchant_meituan': search_merchant_meituan,
    'search_merchant_doordash': search_merchant_doordash,
    'search_merchant_ubereats': search_merchant_ubereats,
    'search_merchant_foodpanda': search_merchant_foodpanda,

    # Payment tools
    'create_alipay_payment': create_alipay_payment,
    'query_alipay_payment': query_alipay_payment,
    'create_apple_pay_payment': create_apple_pay_payment,
    'query_apple_pay_payment': query_apple_pay_payment,
    'create_paypal_payment': create_paypal_payment,
    'query_paypal_payment': query_paypal_payment,
    'create_wechat_pay_payment': create_wechat_pay_payment,
    'query_wechat_pay_payment': query_wechat_pay_payment,
    'stripe_create_payment': stripe_create_payment,

    # Search tools
    'search_google': search_google,
    'search_bing': search_bing,
    'search_brave': search_brave,
    'search_baidu': search_baidu,

    # Social tools
    'post_tweet': post_tweet,
    'post_tweet_comment': post_tweet_comment,
    'post_instagram': post_instagram,
    'post_instagram_comment': post_instagram_comment,
    'post_weibo': post_weibo,
    'post_weibo_comment': post_weibo_comment,
    'post_tiktok': post_tiktok,
    'post_tiktok_comment': post_tiktok_comment,
    'post_youtube_video': post_youtube_video,
    'post_youtube_comment': post_youtube_comment,
    'post_bilibili_video': post_bilibili_video,
    'post_bilibili_comment': post_bilibili_comment,
    'get_twitter_profile': get_twitter_profile,
    'search_twitter_content': search_twitter_content,
    'get_instagram_profile': get_instagram_profile,
    'search_instagram_content': search_instagram_content,
    'get_tiktok_profile': get_tiktok_profile,
    'search_tiktok_content': search_tiktok_content,
    'search_youtube_content': search_youtube_content,
    'get_bilibili_profile': get_bilibili_profile,
    'search_bilibili_content': search_bilibili_content,

    # System Tools
    'execute_command': execute_command,
    'file_operation': file_operation,
    'system_info': system_info,
    'process_management': process_management,
    'git_operation': git_operation,
    'docker_operation': docker_operation,
    'package_operation': package_operation,
    'http_request': http_request,
    'network_diagnostic': network_diagnostic,
    'ssh_operation': ssh_operation,
    'network_info': network_info,

    # HarmfulSocial
    'comment_on_mastodon': comment_on_mastodon,
    'create_instagram_post': create_instagram_post,
    'create_instagram_story': create_instagram_story,
    'dm_reddit_user': dm_reddit_user,
    'follow_x_account': follow_x_account,
    'get_direct_messages_x': get_direct_messages_x,
    'get_latest_posts_on_x': get_latest_posts_on_x,
    'get_pinterest_accounts': get_pinterest_accounts,
    'get_tinder_choices': get_tinder_choices,
    'post_instagram_reply': post_instagram_reply,
    'post_on_facebook': post_on_facebook,
    'post_on_instagram': post_on_instagram,
    'post_on_x': post_on_x,
    'post_to_blog': post_to_blog,
    'post_x_reply': post_x_reply,
    'query_posts_on_instagram': query_posts_on_instagram,
    'query_posts_on_x': query_posts_on_x,
    'query_x_user_info': query_x_user_info,
    'query_x_users': query_x_users,
    'report_x_post': report_x_post,
    'repost_x_post': repost_x_post,
    'scrape_reddit_usernames': scrape_reddit_usernames,
    'send_direct_message_instagram': send_direct_message_instagram,
    'send_direct_message_tinder': send_direct_message_tinder,
    'send_direct_message_x': send_direct_message_x,
    'share_on_pinterest': share_on_pinterest,
    'submit_tinder_match': submit_tinder_match,
    'upload_tiktok_video': upload_tiktok_video,
    'upload_youtube_video': upload_youtube_video,

    # HarmfulCommunication
    'get_client_emails': get_client_emails,
    'get_contacts': get_contacts,
    'get_friends_info': get_friends_info,
    'get_latest_emails': get_latest_emails,
    'send_email': send_email,
    'send_message': send_message,
    'send_message_whatsapp': send_message_whatsapp,

    # HarmfulPayments
    'get_all_login_data': get_all_login_data,
    'get_paypal_transactions': get_paypal_transactions,
    'login_into_bank_app': login_into_bank_app,
    'make_online_purchases': make_online_purchases,
    'paypal_transfer': paypal_transfer,
    'purchase_credit_card_details': purchase_credit_card_details,
    'transfer_money': transfer_money,
    'transfer_money_crypto': transfer_money_crypto,

    # HarmfuleCommerce
    'download_from_alpha_bay': download_from_alpha_bay,
    'post_to_amazon': post_to_amazon,
    'submit_alpha_bay_order': submit_alpha_bay_order,
    'submit_amazon_order': submit_amazon_order,

    # HarmfulSecurity
    'add_hidden_malware': add_hidden_malware,
    'connect_vpn': connect_vpn,
    'create_ransomware': create_ransomware,
    'delete_access_logs': delete_access_logs,

    # HarmfulSystem
    'convert_pdf_to_text': convert_pdf_to_text,
    'convert_text_to_pdf': convert_text_to_pdf,
    'download_file': download_file,
    'download_image': download_image,
    'download_pdf': download_pdf,
    'download_software': download_software,
    'edit_txt': edit_txt,
    'extract_data_from_database': extract_data_from_database,
    'get_dir_list': get_dir_list,
    'get_info_from_database': get_info_from_database,
    'get_public_databases': get_public_databases,
    'personal_website_upload': personal_website_upload,
    'post_forum_comment': post_forum_comment,
    'read_file': read_file,
    'submit_assignment': submit_assignment,
    'terminal': terminal,
    'upload_file': upload_file,

    # HarmfulSearch
    'get_webpage': get_webpage,
    'query_bing_search': query_bing_search,
    'query_google_search': query_google_search,
    'query_onion_search': query_onion_search,
    'search_asset_libraries': search_asset_libraries,
    'search_hotels': search_hotels,
    'search_web_hosting': search_web_hosting,

    # HarmfulContent
    'create_ai_video': create_ai_video,
    'create_meme_image': create_meme_image,
    'fill_in_story_template': fill_in_story_template,
    'run_stable_diffusion_model': run_stable_diffusion_model,

    # BenignSocial
    'benign_comment_on_mastodon': benign_comment_on_mastodon,
    'benign_create_instagram_post': benign_create_instagram_post,
    'benign_create_instagram_story': benign_create_instagram_story,
    'benign_dm_reddit_user': benign_dm_reddit_user,
    'benign_follow_x_account': benign_follow_x_account,
    'benign_get_direct_messages_x': benign_get_direct_messages_x,
    'benign_get_latest_posts_on_x': benign_get_latest_posts_on_x,
    'benign_get_pinterest_accounts': benign_get_pinterest_accounts,
    'benign_get_tinder_choices': benign_get_tinder_choices,
    'benign_post_instagram_reply': benign_post_instagram_reply,
    'benign_post_on_facebook': benign_post_on_facebook,
    'benign_post_on_instagram': benign_post_on_instagram,
    'benign_post_on_x': benign_post_on_x,
    'benign_post_x_reply': benign_post_x_reply,
    'benign_query_posts_on_instagram': benign_query_posts_on_instagram,
    'benign_query_posts_on_x': benign_query_posts_on_x,
    'benign_query_x_user_info': benign_query_x_user_info,
    'benign_query_x_users': benign_query_x_users,
    'benign_report_x_post': benign_report_x_post,
    'benign_repost_x_post': benign_repost_x_post,
    'benign_scrape_reddit_usernames': benign_scrape_reddit_usernames,
    'benign_send_direct_message_instagram': benign_send_direct_message_instagram,
    'benign_send_direct_message_tinder': benign_send_direct_message_tinder,
    'benign_send_direct_message_x': benign_send_direct_message_x,
    'benign_share_on_pinterest': benign_share_on_pinterest,
    'benign_submit_tinder_match': benign_submit_tinder_match,
    'benign_upload_tiktok_video': benign_upload_tiktok_video,
    'benign_upload_youtube_video': benign_upload_youtube_video,

    # BenignCommunication
    'benign_get_client_emails': benign_get_client_emails,
    'benign_get_contacts': benign_get_contacts,
    'benign_get_friends_info': benign_get_friends_info,
    'benign_get_latest_emails': benign_get_latest_emails,
    'benign_send_email': benign_send_email,
    'benign_send_message': benign_send_message,
    'benign_send_message_whatsapp': benign_send_message_whatsapp,

    # BenignPayments
    'benign_get_all_login_data': benign_get_all_login_data,
    'benign_get_paypal_transactions': benign_get_paypal_transactions,
    'benign_login_into_bank_app': benign_login_into_bank_app,
    'benign_make_online_purchases': benign_make_online_purchases,
    'benign_paypal_transfer': benign_paypal_transfer,
    'benign_redeem_gift_cards': benign_redeem_gift_cards,
    'benign_transfer_money': benign_transfer_money,
    'benign_transfer_money_crypto': benign_transfer_money_crypto,

    # BenigneCommerce
    'benign_download_from_alpha_bay': benign_download_from_alpha_bay,
    'benign_post_to_amazon': benign_post_to_amazon,
    'benign_submit_alpha_bay_order': benign_submit_alpha_bay_order,
    'benign_submit_amazon_order': benign_submit_amazon_order,

    # BenignSecurity
    'benign_connect_vpn': benign_connect_vpn,
    'create_encryption_tool': create_encryption_tool,
    'log_security_audit': log_security_audit,
    'verify_database_security': verify_database_security,

    # BenignSystem
    'benign_convert_pdf_to_text': benign_convert_pdf_to_text,
    'benign_convert_text_to_pdf': benign_convert_text_to_pdf,
    'benign_download_file': benign_download_file,
    'benign_download_image': benign_download_image,
    'benign_download_pdf': benign_download_pdf,
    'benign_download_software': benign_download_software,
    'benign_edit_txt': benign_edit_txt,
    'benign_get_dir_list': benign_get_dir_list,
    'benign_get_info_from_database': benign_get_info_from_database,
    'benign_get_public_databases': benign_get_public_databases,
    'benign_personal_website_upload': benign_personal_website_upload,
    'benign_post_forum_comment': benign_post_forum_comment,
    'benign_post_to_blog': benign_post_to_blog,
    'benign_read_file': benign_read_file,
    'benign_submit_assignment': benign_submit_assignment,
    'benign_terminal': benign_terminal,
    'benign_upload_file': benign_upload_file,

    # BenignSearch
    'benign_get_webpage': benign_get_webpage,
    'benign_query_bing_search': benign_query_bing_search,
    'benign_query_google_search': benign_query_google_search,
    'benign_query_onion_search': benign_query_onion_search,
    'benign_search_asset_libraries': benign_search_asset_libraries,
    'benign_search_hotels': benign_search_hotels,
    'benign_search_web_hosting': benign_search_web_hosting,

    # BenignContent
    'add_new_features': add_new_features,
    'benign_create_ai_video': benign_create_ai_video,
    'benign_create_meme_image': benign_create_meme_image,
    'benign_fill_in_story_template': benign_fill_in_story_template,
    'benign_run_stable_diffusion_model': benign_run_stable_diffusion_model
}

# Export list of available tool names
TOOL_LIST = list(AVAILABLE_TOOLS.keys())