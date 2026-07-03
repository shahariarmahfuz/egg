import os
import glob
import re

template_dir = '/workspaces/egg/templates'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    def replacer(match):
        cls_str = match.group(1)
        classes = cls_str.split()
        
        # Don't touch stat-card
        if 'stat-card' in classes or 'stat-card-gradient' in classes:
            return match.group(0)
            
        new_classes = []
        is_card = False
        is_header = False
        
        for c in classes:
            if c == 'card':
                is_card = True
            elif c == 'card-header':
                is_header = True
                new_classes.append('mb-3') # Add margin bottom to replace header spacing
            elif c in ['card-body', 'shadow', 'bg-white']:
                continue # Strip these
            else:
                new_classes.append(c)
                
        if is_card:
            # If it was a card, it usually had mb-4. Ensure mb-4 exists
            if 'mb-4' not in new_classes and 'mb-3' not in new_classes:
                new_classes.append('mb-4')
                
        new_cls_str = ' '.join(new_classes)
        return f'class="{new_cls_str}"'

    content = re.sub(r'class="([^"]*)"', replacer, content)
    
    # Filter panels logic
    parts = content.split('<form ')
    new_content = parts[0]
    for part in parts[1:]:
        if part.startswith('method="GET"') or (part.startswith('action=') and 'method="GET"' in part.split('>')[0]):
            if '</form>' in part:
                sub_parts = part.split('</form>', 1)
                new_content += f'<div class="compact-filter"><form {sub_parts[0]}</form></div>{sub_parts[1]}'
            else:
                new_content += '<form ' + part
        else:
            new_content += '<form ' + part
            
    content = new_content
    
    # Column widths for report tables (Customer 25%, short columns 1%)
    if filepath.endswith('_report.html') or 'list.html' in filepath or 'ledger.html' in filepath or 'manage_' in filepath:
        content = re.sub(r'<th>Customer</th>', r'<th style="width: 25%;">Customer</th>', content)
        content = re.sub(r'<th>Supplier</th>', r'<th style="width: 25%;">Supplier</th>', content)
        
        short_columns = ['SL', 'Due', 'Paid', 'Discount', 'VAT', 'Labour', 'Profit', 'Total']
        for col in short_columns:
            content = re.sub(r'<th>' + col + r'</th>', r'<th style="width: 1%; white-space: nowrap;">' + col + r'</th>', content)
            
    # Remove old compact-filter styles from templates
    content = re.sub(r'<style>.*?/\* Compact Filter Section \*/.*?</style>\s*', '', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filepath in html_files:
    if 'login.html' in filepath or 'dashboard.html' in filepath:
        continue
    process_file(filepath)

print("Done universal fix.")
