from nlp_parser import parse_user_command
import json

cmd = parse_user_command("把data文件夹里的三个销售表合并，按区域汇总，然后生成报告")
print(json.dumps(cmd, ensure_ascii=False, indent=2))