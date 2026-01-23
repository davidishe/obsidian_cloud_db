#!/usr/bin/env python3
"""
Generate PDF from markdown shorts for review
"""

import os
from pathlib import Path

def generate_html():
    """Generate HTML from markdown files"""
    
    shorts_dir = Path("Контент-завод/Шортзы")
    new_shorts = [
        "06_Shorts_NFT_pravo.md",
        "07_Shorts_Dohodnost.md",
        "08_Shorts_Ne_fond.md",
        "09_Shorts_Villa_50_dollarov.md",
        "10_Shorts_Kakie_aktivy.md"
    ]
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokenova - Новые шортзы для ревью</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            color: #e91e63;
            border-bottom: 3px solid #e91e63;
            padding-bottom: 10px;
            page-break-before: always;
        }
        
        h1:first-of-type {
            page-break-before: avoid;
        }
        
        h2 {
            color: #424242;
            margin-top: 30px;
            border-left: 4px solid #e91e63;
            padding-left: 15px;
        }
        
        h3 {
            color: #616161;
            margin-top: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px 8px;
            text-align: left;
        }
        
        th {
            background-color: #f5f5f5;
            font-weight: 600;
            color: #424242;
        }
        
        tr:nth-child(even) {
            background-color: #fafafa;
        }
        
        .metadata {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        
        .voiceover {
            background-color: #fff3e0;
            padding: 15px;
            border-left: 4px solid #ff9800;
            margin: 20px 0;
            font-style: italic;
        }
        
        .description {
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196f3;
            margin: 20px 0;
        }
        
        .hashtags {
            color: #1976d2;
            font-weight: 500;
        }
        
        .cover {
            text-align: center;
            padding: 100px 0;
        }
        
        .cover h1 {
            font-size: 2.5em;
            border: none;
            page-break-before: avoid;
        }
        
        .cover .subtitle {
            font-size: 1.2em;
            color: #757575;
            margin-top: 20px;
        }
        
        .cover .date {
            color: #9e9e9e;
            margin-top: 40px;
        }
        
        @media print {
            body {
                padding: 0;
            }
            
            .page-break {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    <div class="cover">
        <h1>Tokenova</h1>
        <div class="subtitle">Новые шортзы для ревью</div>
        <div class="date">Январь 2026</div>
    </div>
    
    <div class="page-break"></div>
"""
    
    for filename in new_shorts:
        filepath = shorts_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown content
        lines = content.split('\n')
        
        html_content += '<div class="short-section">\n'
        
        in_table = False
        in_voiceover = False
        in_description = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if in_voiceover:
                    html_content += '</div>\n'
                    in_voiceover = False
                if in_description:
                    html_content += '</div>\n'
                    in_description = False
                continue
            
            # Headers
            if line.startswith('# '):
                html_content += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                section_title = line[3:]
                if 'Озвучка' in section_title:
                    html_content += f'<h2>{section_title}</h2>\n<div class="voiceover">\n'
                    in_voiceover = True
                elif 'Описание' in section_title:
                    html_content += f'<h2>{section_title}</h2>\n<div class="description">\n'
                    in_description = True
                else:
                    html_content += f'<h2>{section_title}</h2>\n'
            elif line.startswith('### '):
                html_content += f'<h3>{line[4:]}</h3>\n'
            
            # Tables
            elif line.startswith('|'):
                if not in_table:
                    html_content += '<table>\n'
                    in_table = True
                
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                
                if all(cell.replace('-', '').strip() == '' for cell in cells):
                    continue
                
                if in_table and '---' not in line:
                    if 'Время' in line or 'Видеоряд' in line:
                        html_content += '<thead><tr>'
                        for cell in cells:
                            html_content += f'<th>{cell}</th>'
                        html_content += '</tr></thead><tbody>\n'
                    else:
                        html_content += '<tr>'
                        for cell in cells:
                            html_content += f'<td>{cell}</td>'
                        html_content += '</tr>\n'
            else:
                if in_table:
                    html_content += '</tbody></table>\n'
                    in_table = False
                
                # Metadata
                if line.startswith('**') and '**' in line[2:]:
                    html_content += f'<div class="metadata">{line}</div>\n'
                # Hashtags
                elif 'Хештеги' in content and line and not line.startswith('#') and not line.startswith('|'):
                    if any(word in ['rwa', 'ton', 'tokenova', 'инвестиции'] for word in line.split()):
                        html_content += f'<p class="hashtags">#{line.replace(", ", " #")}</p>\n'
                    else:
                        html_content += f'<p>{line}</p>\n'
                # Regular text
                elif line and not line.startswith('---'):
                    html_content += f'<p>{line}</p>\n'
        
        if in_table:
            html_content += '</tbody></table>\n'
        if in_voiceover:
            html_content += '</div>\n'
        if in_description:
            html_content += '</div>\n'
        
        html_content += '</div>\n<div class="page-break"></div>\n'
    
    html_content += """
</body>
</html>
"""
    
    return html_content

def main():
    html = generate_html()
    
    output_file = "Контент-завод/Новые_шортзы_ревью.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML created: {output_file}")
    print("Converting to PDF...")
    
    # Try to convert to PDF using wkhtmltopdf or weasyprint
    pdf_output = "Контент-завод/Новые_шортзы_ревью.pdf"
    
    # Try wkhtmltopdf first
    result = os.system(f'wkhtmltopdf "{output_file}" "{pdf_output}" 2>/dev/null')
    
    if result != 0:
        # Try weasyprint
        result = os.system(f'weasyprint "{output_file}" "{pdf_output}" 2>/dev/null')
    
    if result == 0:
        print(f"✅ PDF created: {pdf_output}")
    else:
        print(f"⚠️  PDF conversion failed. HTML file available: {output_file}")
        print("You can open the HTML file in a browser and print to PDF manually.")

if __name__ == "__main__":
    main()
