import os
import glob
import re

template_dir = '/workspaces/egg/templates'

report_files = glob.glob(os.path.join(template_dir, '*_report.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Remove the card around the table data
    # <div class="card shadow[^"]*">\s*<div class="card-header[^"]*">.*?</div>\s*<div class="card-body">
    # we need to be careful to match the outer card and remove its closing tags.
    # It's safer to just replace:
    # <div class="card shadow[^"]*">\s*<div class="card-header[^"]*">\s*<h6[^>]*>(Report Data|Expense Data|Income Data).*?</h6>\s*</div>\s*<div class="card-body">
    # with nothing, and then remove the final two </div> before {% endblock %}
    
    pattern_table_card_start = r'<div class="card shadow[^"]*">\s*<div class="card-header[^"]*">\s*<h6[^>]*>(Report Data|Expense Data|Income Data|Report Details).*?</h6>\s*(?:<a[^>]*>.*?</a>\s*)?</div>\s*<div class="card-body">'
    
    if re.search(pattern_table_card_start, content):
        content = re.sub(pattern_table_card_start, '', content)
        # We need to remove the matching two </div>. These are usually right before {% endblock %} or {% block scripts %}
        # The safest way is to replace the last `</div>\n    </div>\n{% endblock %}`
        pattern_table_card_end = r'</div>\s*</div>\s*(?:</div>\s*)?{% endblock %}'
        content = re.sub(pattern_table_card_end, '{% endblock %}', content)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filepath in report_files:
    process_file(filepath)

print("Done phase 3.")
