import re

with open('/Users/yuiyane/ktrend-autobot/handlers/draft_editor.py', 'r') as f:
    content = f.read()

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
for i, script in enumerate(scripts):
    print(f"--- Script {i} ---")
    with open(f'script_{i}.js', 'w') as out:
        out.write(script)
