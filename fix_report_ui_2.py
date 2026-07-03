import os
import glob
import re

template_dir = '/workspaces/egg/templates'

report_files = glob.glob(os.path.join(template_dir, '*_report.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # We want to remove the card around the filter section, which typically has a header "Filter ..."
    # Let's find: <div class="card shadow[^"]*">\s*<div class="card-header[^"]*">\s*<h6[^>]*>Filter.*?</h6>\s*</div>\s*<div class="card-body">
    
    pattern_card_start = r'<div class="card shadow[^"]*">\s*<div class="card-header[^"]*">\s*<h6[^>]*>Filter[^<]*</h6>\s*</div>\s*<div class="card-body">'
    
    if re.search(pattern_card_start, content):
        content = re.sub(pattern_card_start, '<div class="mb-3 compact-filter">', content)
        # We need to remove the matching </div> for card-body and card
        pattern_card_end = r'</form>\s*</div>\s*</div>'
        content = re.sub(pattern_card_end, '</form>\n</div>', content)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filepath in report_files:
    process_file(filepath)

print("Done phase 2.")
