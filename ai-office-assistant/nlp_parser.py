"""
自然语言指令解析模块
调用 DeepSeek 大语言模型 API，将用户自然语言转换为结构化 JSON 操作指令
"""

import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()


def parse_user_command(user_input):
    """
    调用大模型API解析用户自然语言指令
    参数：user_input - 用户输入的自然语言描述
    返回：dict - 解析后的结构化操作指令
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")

    system_prompt = """
你是一个办公自动化助手。根据用户的需求，请只输出以下格式的JSON，不要添加任何解释性文字：
{
"task_type": "excel_merge|word_generate|email_send|full_workflow",
"operation": "具体操作描述",
"parameters": {
"source_files": "文件路径或文件夹路径",
"template": "模板文件路径",
"recipients": "收件人列表或通讯录文件路径"
}
}
"""

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # 容错处理：正则提取纯JSON部分
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"task_type": "unknown", "operation": content, "parameters": {}}

    except Exception as e:
        return {"task_type": "error", "operation": str(e), "parameters": {}}