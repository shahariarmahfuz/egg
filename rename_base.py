import os
import glob

template_dir = '/workspaces/egg/templates'
layout_path = os.path.join(template_dir, 'layout.html')
base_path = os.path.join(template_dir, 'base.html')

if os.path.exists(layout_path):
    os.rename(layout_path, base_path)

for filepath in glob.glob(os.path.join(template_dir, '*.html')):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'layout.html' in content:
        content = content.replace('layout.html', 'base.html')
        with open(filepath, 'w') as f:
            f.write(content)
print("Done renaming and replacing.")
