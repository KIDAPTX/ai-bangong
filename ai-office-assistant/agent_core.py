"""
Agent任务编排模块
使用 DeepSeek 原生 Function Calling 实现工具调用与任务自动串联
"""

import os
import json
import requests
from dotenv import load_dotenv
from excel_handler import merge_excel_files
from word_handler import fill_word_template
from email_handler import send_bulk_emails

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "merge_excel_files",
            "description": "合并指定文件夹中的所有Excel文件，返回合并后的文件路径和行数",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "包含Excel文件的文件夹路径"
                    }
                },
                "required": ["folder_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fill_word_template",
            "description": "根据Excel数据批量填充Word模板，返回生成的文件数量",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_path": {
                        "type": "string",
                        "description": "Word模板文件路径"
                    },
                    "data_excel_path": {
                        "type": "string",
                        "description": "包含填充数据的Excel文件路径"
                    }
                },
                "required": ["template_path", "data_excel_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_bulk_emails",
            "description": "向通讯录中的联系人批量发送带附件的邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "contacts_path": {
                        "type": "string",
                        "description": "通讯录Excel文件路径"
                    },
                    "attachment_path": {
                        "type": "string",
                        "description": "要发送的附件文件路径"
                    }
                },
                "required": ["contacts_path", "attachment_path"]
            }
        }
    }
]


def execute_function_call(function_name, arguments):
    if function_name == "send_bulk_emails":
        result = send_bulk_emails(
            SENDER_EMAIL, SENDER_PASSWORD,
            arguments["contacts_path"], arguments["attachment_path"]
        )
        success = sum(1 for r in result if r['status'] == '成功')
        return f"邮件发送完成：成功{success}封"
    
    elif function_name == "merge_excel_files":
        output_path, row_count = merge_excel_files(**arguments)
        return f"Excel合并完成：共{row_count}行数据，已保存至{output_path}"
    
    elif function_name == "fill_word_template":
        files = fill_word_template(**arguments)
        return f"Word文档生成完成：已生成{len(files)}份文档"
    
    else:
        return f"未知操作：{function_name}"


def run_agent(user_input: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个办公自动化助手，能够操作Excel、Word和邮件。"
                "根据用户的需求，选择合适的工具完成操作。"
                "如果用户要求多个步骤，请依次调用所需工具。"
            )
        },
        {"role": "user", "content": user_input}
    ]
    
    results = []
    max_steps = 5

    for step in range(max_steps):
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "tools": TOOLS
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]
        
        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]
            func_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])
            
            result_msg = execute_function_call(func_name, arguments)
            results.append(result_msg)
            
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result_msg
            })
        else:
            final_text = message.get("content", "")
            if final_text:
                results.append(final_text)
            break
    
    return "\n".join(results) if results else "任务处理完成。"