import markdown
import sys
import os
import re

file = sys.argv[1]
base = os.path.splitext(file)[0]

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 关键步骤：保护所有 LaTeX 公式块 ---
# 1. 保护行间公式 $$ ... $$
def protect_display_math(match):
    inner = match.group(1)
    # 将内部的换行符和反斜杠保护起来，避免被后续处理破坏
    inner = inner.replace('\\', '\\\\')
    # 使用一个特殊标记来包裹，并保留原始格式
    return f'<display-math>\n\\[\n{inner}\n\\]\n</display-math>'

content = re.sub(r'\$\$(.*?)\$\$', protect_display_math, content, flags=re.DOTALL)

# 2. 保护行间公式 \[ ... \]
def protect_display_math_bracket(match):
    inner = match.group(1)
    inner = inner.replace('\\', '\\\\')
    return f'<display-math>\n\\[\n{inner}\n\\]\n</display-math>'

content = re.sub(r'\\\[(.*?)\\\]', protect_display_math_bracket, content, flags=re.DOTALL)

# 3. 保护行内公式 $...$ (可选，但为了避免意外，也做简单保护)
def protect_inline_math(match):
    inner = match.group(1)
    inner = inner.replace('\\', '\\\\')
    return f'<inline-math>{inner}</inline-math>'

content = re.sub(r'\$(.*?)\$', protect_inline_math, content, flags=re.DOTALL)

# --- 现在让 markdown 库处理非公式内容 ---
html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'md_in_html'])

# --- 恢复被保护的 LaTeX 代码 ---
# 将保护标记还原为正常的 LaTeX 语法
html = html.replace('<display-math>', '')
html = html.replace('</display-math>', '')
html = html.replace('<inline-math>', '$')
html = html.replace('</inline-math>', '$')
# 修复被过度转义的反斜杠
html = html.replace('\\\\', '\\')

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

with open(f'{base}.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Converted {file} to {base}.html')
