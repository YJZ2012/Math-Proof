import markdown
import sys
import os
import re

file = sys.argv[1]
base = os.path.splitext(file)[0]

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 预处理：将 $$ \begin{aligned} ... \end{aligned} $$ 包裹的公式单独处理
# 避免 markdown 库破坏 LaTeX 语法
def process_aligned(match):
    inner = match.group(1)
    # 确保换行符被保留
    inner = inner.replace('\\\\', '\\\\\\\\')
    return f'<div class="math-block">\\[\\begin{{aligned}}{inner}\\end{{aligned}}\\]</div>'

# 匹配 $$ \begin{aligned} ... \end{aligned} $$ 模式
pattern = r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$'
content = re.sub(pattern, process_aligned, content, flags=re.DOTALL)

# 使用 markdown 转换
html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'md_in_html'])

# 完整的 HTML 模板，包含正确的 MathJax 配置
full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{base}</title>
    <style>
        body {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        pre {{
            background: #f4f4f4;
            padding: 10px;
            overflow-x: auto;
            border-radius: 4px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
        }}
        .math-block {{
            overflow-x: auto;
            margin: 1em 0;
        }}
        /* 公式内部样式 */
        .MathJax {{
            font-size: 1.05em;
        }}
        /* 让 aligned 环境中的公式更紧凑 */
        mjx-container[jax="CHTML"][display="true"] {{
            margin: 0.5em 0;
        }}
    </style>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                processEnvironments: true,
                tags: 'ams',
                packages: {{'[+]': ['ams', 'boldsymbol', 'newcommand', 'mathtools']}}
            }},
            options: {{
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            }},
            loader: {{
                load: ['[tex]/ams', '[tex]/boldsymbol', '[tex]/mathtools']
            }}
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script"></script>
</head>
<body>
{html}
</body>
</html>'''

# 写入 HTML 文件
with open(f'{base}.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Converted {file} to {base}.html')
