"""
Excel自动化处理模块
支持多文件批量读取、合并、去重与分组统计
"""

import os
import pandas as pd


def merge_excel_files(folder_path, output_path="合并总表.xlsx"):
    """
    合并指定文件夹内所有Excel文件
    参数：folder_path - 文件夹路径
          output_path - 输出文件路径
    返回：tuple - (输出路径, 合并的总行数)
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"文件夹不存在：{folder_path}")

    all_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    if not all_files:
        raise ValueError(f"文件夹中未找到Excel文件：{folder_path}")

    df_list = []

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path, engine='openpyxl')  # 修复点
            df['数据来源'] = file.replace('.xlsx', '')
            df_list.append(df)
        except Exception as e:
            print(f"读取文件 {file} 失败：{str(e)}")

    if not df_list:
        raise ValueError("未能成功读取任何Excel文件")

    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df = merged_df.drop_duplicates()
    merged_df.to_excel(output_path, index=False)

    return output_path, len(merged_df)