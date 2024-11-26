import os
from datetime import datetime
import sys


def scan_directory(start_path):
    """扫描目录并返回层级结构"""
    tree_content = []

    for root, dirs, files in os.walk(start_path):
        # 计算当前路径相对于起始路径的深度
        level = root[len(start_path):].count(os.sep)
        indent = '&nbsp;&nbsp;&nbsp;&nbsp;' * level

        # 添加目录名
        relative_path = os.path.relpath(root, start_path)
        if relative_path != '.':
            tree_content.append(f'{indent}📁 {os.path.basename(root)}')

        # 添加文件
        sub_indent = '&nbsp;&nbsp;&nbsp;&nbsp;' * (level + 1)
        for file in sorted(files):
            tree_content.append(f'{sub_indent}📄 {file}')

    return tree_content


def generate_html(tree_content, start_path):
    """生成HTML文档"""
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>目录结构 - {os.path.basename(start_path)}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .header {{
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }}
            .tree {{
                line-height: 1.5;
            }}
            .tree-item {{
                margin: 5px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.8em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>目录结构：{os.path.basename(start_path)}</h2>
                <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div class="tree">
    '''

    # 添加树形结构
    for item in tree_content:
        html_content += f'<div class="tree-item">{item}</div>\n'

    # 添加页脚和结束标签
    html_content += f'''
            </div>
            <div class="footer">
                <p>总计：{len(tree_content)} 个项目</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return html_content


def main():
    try:
        # 获取程序所在目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            current_dir = os.path.dirname(sys.executable)
        else:
            # 如果是python脚本
            current_dir = os.path.dirname(os.path.abspath(__file__))

        # 扫描目录
        tree_content = scan_directory(current_dir)

        # 生成HTML
        html_content = generate_html(tree_content, current_dir)

        # 保存HTML文件
        output_file = os.path.join(current_dir, 'directory_structure.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # 自动打开生成的文件
        os.startfile(output_file)

    except Exception as e:
        # 如果发生错误，创建错误日志文件
        with open(os.path.join(current_dir, 'error_log.txt'), 'w', encoding='utf-8') as f:
            f.write(f"错误时间：{datetime.now()}\n错误信息：{str(e)}")
        input("程序运行出错，请查看error_log.txt了解详情。按回车键退出...")


if __name__ == "__main__":
    main()