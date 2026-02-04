#!/usr/bin/env python3
"""
GitHub-style Markdown Previewer
Preview markdown files with GitHub-flavored markdown support
"""

import sys
import http.server
import socketserver
import webbrowser
from pathlib import Path
import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc

PORT = 8000

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Preview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
            background-color: #ffffff;
            color: #24292e;
        }}

        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}

        h1 {{ font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.25em; }}

        a {{
            color: #0366d6;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        code {{
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
            font-size: 85%;
            margin: 0;
            padding: 0.2em 0.4em;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }}

        pre {{
            background-color: #f6f8fa;
            border-radius: 3px;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 16px;
        }}

        pre code {{
            background-color: transparent;
            border: 0;
            display: inline;
            line-height: inherit;
            margin: 0;
            overflow: visible;
            padding: 0;
            word-wrap: normal;
        }}

        blockquote {{
            border-left: 0.25em solid #dfe2e5;
            color: #6a737d;
            padding: 0 1em;
            margin: 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}

        table th, table td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }}

        table th {{
            font-weight: 600;
            background-color: #f6f8fa;
        }}

        table tr {{
            background-color: #ffffff;
            border-top: 1px solid #c6cbd1;
        }}

        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}

        img {{
            max-width: 100%;
            box-sizing: content-box;
            background-color: #fff;
        }}

        hr {{
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }}

        ul, ol {{
            padding-left: 2em;
        }}

        li + li {{
            margin-top: 0.25em;
        }}

        .codehilite {{
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""


class MarkdownHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.endswith('.md'):
            # Determine which markdown file to serve
            if self.path == '/':
                md_file = Path('README.md')
            else:
                md_file = Path(self.path[1:])  # Remove leading slash

            if md_file.exists() and md_file.suffix == '.md':
                # Read and convert markdown
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                # Convert markdown to HTML with extensions
                html_content = markdown.markdown(
                    md_content,
                    extensions=[
                        'fenced_code',
                        'codehilite',
                        'tables',
                        'toc',
                        'nl2br',
                        'sane_lists'
                    ]
                )

                # Wrap in HTML template
                full_html = HTML_TEMPLATE.format(content=html_content)

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(full_html.encode('utf-8'))
            else:
                self.send_error(404, 'File Not Found')
        else:
            # Serve other files normally (images, etc.)
            super().do_GET()


def main():
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
        if not Path(md_file).exists():
            print(f"Error: File '{md_file}' not found")
            sys.exit(1)
        # Change to the directory of the markdown file
        Path(md_file).parent.absolute()

    print(f"Starting markdown preview server on http://localhost:{PORT}")
    print("Press Ctrl+C to stop")

    with socketserver.TCPServer(("", PORT), MarkdownHandler) as httpd:
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    main()
