import os
import glob
import re

template_dir = '/workspaces/egg/templates'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    
    while True:
        # Find the first card shadow
        match = re.search(r'<div\s+class="card\s+shadow[^"]*"[^>]*>', content)
        if not match:
            break
            
        start_idx = match.start()
        
        # Find the matching closing div for the card
        div_count = 0
        end_idx = -1
        
        # We need to iterate through all div tags after start_idx
        # using a simple regex for <div and </div
        tag_pattern = re.compile(r'<\s*(div|/div)\b[^>]*>', re.IGNORECASE)
        
        for tag_match in tag_pattern.finditer(content, start_idx):
            tag = tag_match.group(1).lower()
            if tag == 'div':
                div_count += 1
            elif tag == '/div':
                div_count -= 1
                
            if div_count == 0:
                end_idx = tag_match.end()
                break
                
        if end_idx == -1:
            print(f"Error parsing divs in {filepath}")
            break
            
        # Extract the entire card HTML
        card_html = content[start_idx:end_idx]
        
        # Now we process the card_html
        # Remove card-header
        # Find <div class="card-header" ... to its closing div
        header_match = re.search(r'<div\s+class="card-header[^"]*"[^>]*>', card_html)
        if header_match:
            h_start = header_match.start()
            h_div_count = 0
            h_end = -1
            for t_match in tag_pattern.finditer(card_html, h_start):
                t = t_match.group(1).lower()
                if t == 'div':
                    h_div_count += 1
                elif t == '/div':
                    h_div_count -= 1
                if h_div_count == 0:
                    h_end = t_match.end()
                    break
            
            if h_end != -1:
                # Remove header from card_html
                card_html = card_html[:h_start] + card_html[h_end:]
        
        # Remove card-body wrapper
        body_match = re.search(r'<div\s+class="card-body"[^>]*>', card_html)
        if body_match:
            b_start = body_match.start()
            b_end = body_match.end()
            # The closing div for card-body is the second to last closing div in the card
            # Or we can just find its exact matching div
            b_div_count = 0
            b_close_start = -1
            b_close_end = -1
            for t_match in tag_pattern.finditer(card_html, b_start):
                t = t_match.group(1).lower()
                if t == 'div':
                    b_div_count += 1
                elif t == '/div':
                    b_div_count -= 1
                if b_div_count == 0:
                    b_close_start = t_match.start()
                    b_close_end = t_match.end()
                    break
                    
            if b_close_start != -1:
                inner_html = card_html[b_end:b_close_start]
                # Also remove the card wrapper itself
                # card_html starts with <div class="card shadow... and ends with </div>
                
                # Check if it's a filter/form card or a table card
                # If it has a <form> inside, let's wrap it in mb-3 compact-filter
                # Unless it's a large form like add_sale.html, but the user said "Remove the surrounding card/container ... from ALL management and report pages"
                
                if '<form' in inner_html and '<table' not in inner_html:
                    new_html = f'<div class="mb-4 compact-filter">\n{inner_html}\n</div>'
                else:
                    new_html = f'<div class="mb-4">\n{inner_html}\n</div>'
                
                content = content[:start_idx] + new_html + content[end_idx:]
            else:
                print("Failed to find card-body closing div")
                break
        else:
            # No card-body, just replace the card wrapper
            inner_html = card_html[match.end():-6] # remove opening tag and </div>
            new_html = f'<div class="mb-4">\n{inner_html}\n</div>'
            content = content[:start_idx] + new_html + content[end_idx:]

    # Remove lingering <style> tags related to compact-filter, as they are now global
    content = re.sub(r'<style>\s*/\*\s*Compact Filter Section\s*\*/.*?</style>\s*', '', content, flags=re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for filepath in html_files:
    # login.html doesn't need to be touched as it's the auth page, the user is talking about ERP inner pages
    if 'login.html' in filepath:
        continue
    process_file(filepath)

print("Done stripping cards.")
