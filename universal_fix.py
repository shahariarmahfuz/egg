import os
import glob
import re

template_dir = '/workspaces/egg/templates'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # 1. We want to find ALL card containers.
    # To do this safely, we will iterate over every div that has 'card' in its class,
    # EXCEPT 'stat-card' which is used in dashboard.
    
    # We will use simple string replacement for the classes, since we just want to strip the styles.
    # But wait, if we just do string replacement, we might affect things we don't want to.
    # Actually, replacing class="card shadow mb-4" with class="mb-4" is very safe.
    
    # Strip card classes
    # We want to replace:
    # class="card shadow mb-4" -> class="mb-4"
    # class="card shadow mb-3 compact-filter" -> class="mb-4 compact-filter"
    # class="card-header py-3 bg-white" -> class="mb-3"
    # class="card-body" -> class=""
    
    # A generic regex to remove 'card', 'shadow', 'bg-white', 'card-header', 'card-body' from class attributes
    def replacer(match):
        cls_str = match.group(1)
        # Don't touch stat-card
        if 'stat-card' in cls_str:
            return match.group(0)
            
        cls_str = re.sub(r'\bcard\b', '', cls_str)
        cls_str = re.sub(r'\bshadow\b', '', cls_str)
        cls_str = re.sub(r'\bcard-header\b', 'mb-3', cls_str)
        cls_str = re.sub(r'\bcard-body\b', '', cls_str)
        cls_str = re.sub(r'\bbg-white\b', '', cls_str)
        # Clean up extra spaces
        cls_str = ' '.join(cls_str.split())
        return f'class="{cls_str}"'

    content = re.sub(r'class="([^"]*)"', replacer, content)
    
    # For forms (filter sections), we want to add `compact-filter` to their wrapper.
    # We can do this by finding forms and checking if they are the only thing in a wrapper.
    # Actually, let's just use the previous logic for compact-filter: 
    # If it's a report page and has a filter form.
    # The user said: "All Filter Report / Search / Filter panels should also follow the same design... Use a compact layout with minimal spacing. Apply this to every page that has a filter/search section."
    # How to distinguish a filter section from an "Add Customer" form?
    # Filter sections usually have method="GET". Add forms have method="POST".
    # This is a very reliable heuristic!
    
    # Let's find <form method="GET" ...> and see if its parent div can get `compact-filter`.
    # Instead of complex HTML parsing, let's just append `<div class="compact-filter">` around `<form method="GET" ...>`
    # Wait, the form itself might have row/cols. Wrapping the form in a div with compact-filter is easy.
    
    # Let's replace <form method="GET" with <div class="compact-filter"><form method="GET"
    # and replace </form> with </form></div> IF it was a GET form.
    # Let's do this carefully.
    
    parts = content.split('<form ')
    new_content = parts[0]
    for part in parts[1:]:
        if part.startswith('method="GET"') or part.startswith('action=') and 'method="GET"' in part.split('>')[0]:
            # This is a GET form
            # Find the closing </form>
            if '</form>' in part:
                sub_parts = part.split('</form>', 1)
                new_content += f'<div class="compact-filter"><form {sub_parts[0]}</form></div>{sub_parts[1]}'
            else:
                new_content += '<form ' + part
        else:
            new_content += '<form ' + part
            
    content = new_content
    
    # Also adjust column widths for report tables (Customer 25%, short columns 1%)
    if filepath.endswith('_report.html') or 'list.html' in filepath or 'ledger.html' in filepath or 'manage_' in filepath:
        content = re.sub(r'<th>Customer</th>', r'<th style="width: 25%;">Customer</th>', content)
        content = re.sub(r'<th>Supplier</th>', r'<th style="width: 25%;">Supplier</th>', content)
        
        short_columns = ['SL', 'Due', 'Paid', 'Discount', 'VAT', 'Labour', 'Profit', 'Total']
        for col in short_columns:
            content = re.sub(r'<th>' + col + r'</th>', r'<th style="width: 1%; white-space: nowrap;">' + col + r'</th>', content)
            
    # Remove old compact-filter styles from templates since it is in style.css
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
