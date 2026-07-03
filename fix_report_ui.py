import os
import glob
import re

template_dir = '/workspaces/egg/templates'

report_files = glob.glob(os.path.join(template_dir, '*_report.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Remove inline style block
    content = re.sub(r'<style>.*?/\* Compact Filter Section \*/.*?</style>\s*', '', content, flags=re.DOTALL)
    
    # Replace card container with simple div
    # Find <div class="card shadow mb-3 compact-filter"> ... <div class="card-body">
    pattern_card_start = r'<div class="card shadow mb-3 compact-filter">\s*<div class="card-header bg-white">\s*<h6[^>]*>.*?</h6>\s*</div>\s*<div class="card-body">'
    if re.search(pattern_card_start, content):
        content = re.sub(pattern_card_start, '<div class="mb-3 compact-filter">', content)
        
        # We need to remove the matching </div> for card-body and card
        # The easiest way is to look for the end of the form, which is followed by </div>\n    </div>
        pattern_card_end = r'</form>\s*</div>\s*</div>'
        content = re.sub(pattern_card_end, '</form>\n</div>', content)

    # Now fix column widths
    # For columns: SL, Due, Paid, Discount, VAT, Labour, Profit
    short_columns = ['SL', 'Due', 'Paid', 'Discount', 'VAT', 'Labour', 'Profit', 'Total']
    
    # We want to replace <th>Customer</th> with <th style="width: 25%;">Customer</th>
    # And <th>Due</th> with <th style="width: 1%; white-space: nowrap;">Due</th>
    
    content = re.sub(r'<th>Customer</th>', r'<th style="width: 25%;">Customer</th>', content)
    content = re.sub(r'<th>Supplier</th>', r'<th style="width: 25%;">Supplier</th>', content)
    
    for col in short_columns:
        content = re.sub(r'<th>' + col + r'</th>', r'<th style="width: 1%; white-space: nowrap;">' + col + r'</th>', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filepath in report_files:
    process_file(filepath)

print("Done.")
