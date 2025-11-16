#!/usr/bin/env python3
"""
PDF Comparison Tool - Struts vs Angular
Compare two PDFs to check if contents are identical
"""
import PyPDF2
import difflib
from pathlib import Path
import sys
from typing import Tuple
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"📄 Reading {Path(pdf_path).name}...")
            print(f"   Total pages: {len(pdf_reader.pages)}")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text += page.extract_text()
                print(f"   Extracted page {page_num}/{len(pdf_reader.pages)}", end='\r')
            
            print()  # New line after progress
            return text
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
        sys.exit(1)

def normalize_text(text: str) -> str:
    """Normalize text for comparison (remove extra spaces, newlines)"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity percentage between two texts"""
    # Use SequenceMatcher for similarity
    matcher = difflib.SequenceMatcher(None, text1, text2)
    return matcher.ratio() * 100

def get_detailed_diff(text1: str, text2: str):
    """Generate detailed line-by-line differences"""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    diff = difflib.HtmlDiff(wrapcolumn=80)
    return diff, lines1, lines2

def generate_html_report(pdf1_path: str, pdf2_path: str, text1: str, text2: str, 
                        similarity: float, diff_html: str, output_file: str):
    """Generate beautiful HTML comparison report"""
    
    # Get file names
    pdf1_name = Path(pdf1_path).name
    pdf2_name = Path(pdf2_path).name
    
    # Calculate stats
    stats1 = {
        'chars': len(text1),
        'words': len(text1.split()),
        'lines': len(text1.splitlines())
    }
    
    stats2 = {
        'chars': len(text2),
        'words': len(text2.split()),
        'lines': len(text2.splitlines())
    }
    
    char_diff = abs(stats1['chars'] - stats2['chars'])
    word_diff = abs(stats1['words'] - stats2['words'])
    
    # Determine status
    if similarity == 100.0:
        status_class = "identical"
        status_text = "✅ IDENTICAL"
        status_desc = "PDFs contain exactly the same content"
    elif similarity >= 95.0:
        status_class = "almost-identical"
        status_text = "✨ ALMOST IDENTICAL"
        status_desc = "PDFs are very similar with minor differences"
    elif similarity >= 80.0:
        status_class = "similar"
        status_text = "⚠️ SIMILAR"
        status_desc = "PDFs have noticeable differences"
    else:
        status_class = "different"
        status_text = "❌ DIFFERENT"
        status_desc = "PDFs have significant differences"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Comparison Report - {pdf1_name} vs {pdf2_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .timestamp {{
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .status-banner {{
            text-align: center;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .status-banner.identical {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }}
        
        .status-banner.almost-identical {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        
        .status-banner.similar {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }}
        
        .status-banner.different {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
        }}
        
        .status-banner h2 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .status-banner p {{
            font-size: 1.2em;
            opacity: 0.95;
        }}
        
        .similarity-score {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
        }}
        
        .score-number {{
            font-size: 4em;
            font-weight: 700;
        }}
        
        .progress-bar {{
            flex: 1;
            max-width: 600px;
        }}
        
        .progress-bar-bg {{
            width: 100%;
            height: 30px;
            background: rgba(255,255,255,0.3);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .progress-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
            border-radius: 15px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            font-size: 1.1em;
            margin-bottom: 15px;
            opacity: 0.9;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .file-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 40px 0;
        }}
        
        .file-info {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #e9ecef;
        }}
        
        .file-info.pdf1 {{
            border-color: #667eea;
        }}
        
        .file-info.pdf2 {{
            border-color: #764ba2;
        }}
        
        .file-info h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .file-info.pdf2 h3 {{
            color: #764ba2;
        }}
        
        .file-name {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            font-weight: 600;
            word-break: break-all;
        }}
        
        .file-stats {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .file-stat {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }}
        
        .file-stat-label {{
            color: #6c757d;
        }}
        
        .file-stat-value {{
            font-weight: 600;
            color: #495057;
        }}
        
        .diff-section {{
            margin-top: 50px;
        }}
        
        .diff-section h2 {{
            font-size: 2em;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .diff-container {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            overflow-x: auto;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        table.diff {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            background: white;
        }}
        
        table.diff td {{
            padding: 8px;
            border: 1px solid #dee2e6;
            vertical-align: top;
            line-height: 1.6;
        }}
        
        table.diff th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            font-weight: 600;
            text-align: left;
        }}
        
        .diff_add {{
            background: #d4edda;
            color: #155724;
        }}
        
        .diff_sub {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .diff_chg {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .diff_next {{
            background: #e7f3ff;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 2px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .file-comparison {{
                grid-template-columns: 1fr;
            }}
            
            .similarity-score {{
                flex-direction: column;
            }}
            
            .score-number {{
                font-size: 3em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 PDF Comparison Report</h1>
            <p>Struts vs Angular - Detailed Content Analysis</p>
            <div class="timestamp">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>
        
        <div class="content">
            <div class="status-banner {status_class}">
                <h2>{status_text}</h2>
                <p>{status_desc}</p>
            </div>
            
            <div class="similarity-score">
                <div class="score-number">{similarity:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {similarity}%;">
                            {similarity:.1f}% Match
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="file-comparison">
                <div class="file-info pdf1">
                    <h3>📄 PDF 1 (Struts)</h3>
                    <div class="file-name">{pdf1_name}</div>
                    <div class="file-stats">
                        <div class="file-stat">
                            <span class="file-stat-label">Characters</span>
                            <span class="file-stat-value">{stats1['chars']:,}</span>
                        </div>
                        <div class="file-stat">
                            <span class="file-stat-label">Words</span>
                            <span class="file-stat-value">{stats1['words']:,}</span>
                        </div>
                        <div class="file-stat">
                            <span class="file-stat-label">Lines</span>
                            <span class="file-stat-value">{stats1['lines']:,}</span>
                        </div>
                    </div>
                </div>
                
                <div class="file-info pdf2">
                    <h3>📄 PDF 2 (Angular)</h3>
                    <div class="file-name">{pdf2_name}</div>
                    <div class="file-stats">
                        <div class="file-stat">
                            <span class="file-stat-label">Characters</span>
                            <span class="file-stat-value">{stats2['chars']:,}</span>
                        </div>
                        <div class="file-stat">
                            <span class="file-stat-label">Words</span>
                            <span class="file-stat-value">{stats2['words']:,}</span>
                        </div>
                        <div class="file-stat">
                            <span class="file-stat-label">Lines</span>
                            <span class="file-stat-value">{stats2['lines']:,}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>📏 Character Difference</h3>
                    <div class="stat-value">{char_diff:,}</div>
                    <div class="stat-label">characters difference</div>
                </div>
                
                <div class="stat-card">
                    <h3>📝 Word Difference</h3>
                    <div class="stat-value">{word_diff:,}</div>
                    <div class="stat-label">words difference</div>
                </div>
                
                <div class="stat-card">
                    <h3>🎯 Match Quality</h3>
                    <div class="stat-value">{similarity:.1f}%</div>
                    <div class="stat-label">similarity score</div>
                </div>
            </div>
            
            {f'''
            <div class="diff-section">
                <h2>🔍 Detailed Line-by-Line Comparison</h2>
                <div class="diff-container">
                    {diff_html}
                </div>
            </div>
            ''' if similarity < 100.0 else '<div class="diff-section"><h2>🎉 No Differences Found!</h2><p style="text-align:center; font-size:1.2em; color:#6c757d;">Both PDFs contain identical content.</p></div>'}
        </div>
        
        <div class="footer">
            <p>PDF Comparison Tool | Generated with Python & PyPDF2</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Color Legend: 
                <span style="background:#f8d7da; padding:4px 8px; border-radius:4px; margin:0 5px;">Removed</span>
                <span style="background:#d4edda; padding:4px 8px; border-radius:4px; margin:0 5px;">Added</span>
                <span style="background:#fff3cd; padding:4px 8px; border-radius:4px; margin:0 5px;">Changed</span>
            </p>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"💾 HTML report saved to: {output_file}")

def compare_pdfs(pdf1_path: str, pdf2_path: str, save_diff: bool = False):
    """Main function to compare two PDFs"""
    
    print("\n" + "="*70)
    print("📊 PDF COMPARISON TOOL - Struts vs Angular")
    print("="*70 + "\n")
    
    # Extract text from both PDFs
    print("Step 1: Extracting text from PDFs...")
    text1 = extract_text_from_pdf(pdf1_path)
    text2 = extract_text_from_pdf(pdf2_path)
    
    # Statistics
    print("\n" + "-"*70)
    print("📈 STATISTICS")
    print("-"*70)
    print(f"PDF 1 (Struts):")
    print(f"  - Characters: {len(text1):,}")
    print(f"  - Words: {len(text1.split()):,}")
    print(f"  - Lines: {len(text1.splitlines()):,}")
    
    print(f"\nPDF 2 (Angular):")
    print(f"  - Characters: {len(text2):,}")
    print(f"  - Words: {len(text2.split()):,}")
    print(f"  - Lines: {len(text2.splitlines()):,}")
    
    # Normalize texts
    print("\nStep 2: Normalizing text for comparison...")
    norm_text1 = normalize_text(text1)
    norm_text2 = normalize_text(text2)
    
    # Calculate similarity
    print("Step 3: Calculating similarity...")
    similarity = calculate_similarity(norm_text1, norm_text2)
    
    # Results
    print("\n" + "="*70)
    print("🎯 COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n📊 Similarity Score: {similarity:.2f}%")
    
    # Progress bar visualization
    bar_length = 50
    filled = int(bar_length * similarity / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"[{bar}] {similarity:.2f}%")
    
    if similarity == 100.0:
        print("\n✅ PDFs are IDENTICAL! Content matches 100%")
    elif similarity >= 95.0:
        print("\n✨ PDFs are ALMOST IDENTICAL (>95% match)")
    elif similarity >= 80.0:
        print("\n⚠️  PDFs are SIMILAR but have some differences (80-95% match)")
    else:
        print("\n❌ PDFs have SIGNIFICANT DIFFERENCES (<80% match)")
    
    # Character and word differences
    char_diff = abs(len(text1) - len(text2))
    word_diff = abs(len(text1.split()) - len(text2.split()))
    
    print(f"\n📏 Differences:")
    print(f"  - Character difference: {char_diff:,}")
    print(f"  - Word difference: {word_diff:,}")
    
    # Generate HTML report if requested
    if save_diff:
        print("\nStep 4: Generating HTML report...")
        diff_generator, lines1, lines2 = get_detailed_diff(text1, text2)
        diff_html = diff_generator.make_table(lines1, lines2, 
                                              fromdesc='PDF 1 (Struts)', 
                                              todesc='PDF 2 (Angular)',
                                              context=True,
                                              numlines=3)
        
        output_file = "pdf_comparison_report.html"
        generate_html_report(pdf1_path, pdf2_path, text1, text2, 
                           similarity, diff_html, output_file)
        
        print(f"\n🌐 Open the HTML file in your browser to view the detailed report!")
    else:
        print("\n💡 Tip: Use --save-diff flag to generate beautiful HTML report")
    
    print("\n" + "="*70)
    print("✅ Comparison completed!")
    print("="*70 + "\n")

def main():
    """Main entry point"""
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python pdf_compare.py <pdf1_path> <pdf2_path> [--save-diff]")
        print("\nExample:")
        print("  python pdf_compare.py struts.pdf angular.pdf")
        print("  python pdf_compare.py struts.pdf angular.pdf --save-diff")
        sys.exit(1)
    
    pdf1_path = sys.argv[1]
    pdf2_path = sys.argv[2]
    save_diff = '--save-diff' in sys.argv
    
    # Check if files exist
    if not Path(pdf1_path).exists():
        print(f"❌ Error: File not found - {pdf1_path}")
        sys.exit(1)
    
    if not Path(pdf2_path).exists():
        print(f"❌ Error: File not found - {pdf2_path}")
        sys.exit(1)
    
    # Run comparison
    compare_pdfs(pdf1_path, pdf2_path, save_diff)

if __name__ == "__main__":
    main()