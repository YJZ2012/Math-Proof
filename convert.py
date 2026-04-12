import markdown
import sys
import os

file = sys.argv[1]
base = os.path.splitext(file)[0]

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

html = markdown.markdown(content, extensions=['fenced_code', 'tables'])

full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{base}</title>
    <style>
        body {{ max-width: 900px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; line-height: 1.6; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 2px 4px; }}
    </style>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
            }},
            options: {{
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            }},
            loader: {{
                load: ['[tex]/ams']
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
