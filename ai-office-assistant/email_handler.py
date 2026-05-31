"""
邮件自动化发送模块
支持从Excel通讯录读取收件人信息，批量发送带附件的邮件
"""

import os
import yagmail
import pandas as pd


def send_bulk_emails(sender_email, sender_password,
                     contacts_file, attachment_path=None):
    """
    批量发送邮件
    参数：sender_email - 发件人邮箱地址
          sender_password - 邮箱授权码
          contacts_file - 通讯录Excel文件路径（需包含"邮箱"列）
          attachment_path - 附件文件路径（可选）
    返回：list - 发送结果列表 [{"email": xxx, "status": "成功/失败"}]
    """
    if not os.path.exists(contacts_file):
        raise FileNotFoundError(f"通讯录文件不存在：{contacts_file}")
    if attachment_path and not os.path.exists(attachment_path):
        raise FileNotFoundError(f"附件文件不存在：{attachment_path}")

    yag = yagmail.SMTP(
    user=sender_email,
    password=sender_password,
    host='smtp.qq.com',
    port=465,
    smtp_ssl=True
)
    contacts = pd.read_excel(contacts_file, engine='openpyxl')  # 修复点

    if '邮箱' not in contacts.columns:
        raise ValueError("通讯录中缺少'邮箱'列")

    results = []
    for _, row in contacts.iterrows():
        name = row.get('姓名', '用户')
        email = row['邮箱']
        content = f"{name}，您好！附件是您需要的工作文件，请查收。"

        try:
            yag.send(
                to=email,
                subject="工作文件发送",
                contents=content,
                attachments=attachment_path
            )
            results.append({"email": email, "status": "成功"})
        except Exception as e:
            results.append({"email": email, "status": f"失败: {str(e)}"})

    return results