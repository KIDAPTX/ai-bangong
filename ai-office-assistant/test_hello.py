import pandas as pd

files = [
    "data/销售表A.xlsx",
    "data/销售表B.xlsx",
    "data/销售表C.xlsx",
    "data/填充数据.xlsx",
    "data/通讯录.xlsx",
    "合并总表.xlsx"  # 如果已存在
]

for f in files:
    try:
        df = pd.read_excel(f, engine='openpyxl')
        print(f"✅ {f} 读取成功，{len(df)} 行")
    except Exception as e:
        print(f"❌ {f} 读取失败：{e}")