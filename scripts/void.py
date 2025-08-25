"""
Disclaimer:

This entire script was developed by an AI.
I was lazy and didn't want to write it myself.
The code is very ugly and it doesn't represent me.
But, to contribute to this simple blog, just put your content in `/input` and run the script.
If you want to contribute with this code, feel free and good luck!

30 78 44 61 6E 74
"""

import os
import sys
import zipfile
import shutil
import re


TEMPLATE_PATH = "../pages/articles/template.txt"


def remove_md_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.md'):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass


def slugify(name):
    return name.lower().replace(" ", "-").replace("_", "-")


def unslugify(slug):
    # Substitui múltiplos hífens por ' - '
    name = re.sub(r'-{3,}', ' - ', slug)
    # Substitui hífens simples por espaço
    name = re.sub(r'(?<! )-(?! )', ' ', name)
    # Capitaliza cada palavra, preservando siglas e números
    name = ' '.join([w.capitalize() if not w.isupper() else w for w in name.split()])
    return name


def read_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove the first comment block (including all lines between <!-- and -->)
    new_lines = []
    in_comment = False
    for line in lines:
        if '<!--' in line:
            in_comment = True
            continue
        if '-->' in line and in_comment:
            in_comment = False
            continue
        if not in_comment:
            new_lines.append(line)
    return "".join(new_lines)


def create_html(md_path, html_path, template, language, paper_topic):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    # Calculate depth for relative paths
    html_dir = os.path.dirname(html_path)
    # Find how many levels from output root
    rel_to_output = os.path.relpath(html_dir, os.path.dirname(TEMPLATE_PATH))
    depth = len([p for p in rel_to_output.split(os.sep) if p and p != '.'])
    # Default: ../../../ for root, add ../ for each sublevel
    css_prefix = '../' * (3 + depth)
    papers_prefix = '../' * (2 + depth)
    html_content = template.replace("PAPER_LANGUAGE", language).replace("PAPER_TOPIC", paper_topic)
    html_content = html_content.replace("../../../assets/css/markdown.css", f"{css_prefix}assets/css/markdown.css")
    html_content = html_content.replace("../../../assets/images/sterile-box.ico", f"{css_prefix}assets/images/sterile-box.ico")
    html_content = html_content.replace("../../papers.html", f"{papers_prefix}pages/papers.html")
    html_content = html_content.replace("<<$PUT_YOUR_CONTENT_HERE>>", md_content)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def zip_folder(folder, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), folder))


def build_html_list(folder, rel_path, author, level=0, prefix="0x0000", topic_name=None, language="pt-BR"):
    items = []
    entries = sorted(os.listdir(folder))
    # Separar diretórios e arquivos .html
    skip_folders = ["docs", "DOCS", "zDocs", "zdocs", "documentation", "Documentation"]
    dirs = [e for e in entries if os.path.isdir(os.path.join(folder, e)) and e not in skip_folders]
    htmls = [e for e in entries if e.endswith('.html')]
    # Diretórios: índice incremental
    for d_idx, entry in enumerate(dirs):
        full_path = os.path.join(folder, entry)
        sub_prefix = f"0x{str(d_idx+1).zfill(4)}"
        sublist = build_html_list(full_path, os.path.join(rel_path, entry), author, level+1, sub_prefix, entry)
        items.append(f'{"    "*level}<li>{sub_prefix} .......... {entry}\n{"    "*(level+1)}<ul class="list-nested">\n{sublist}\n{"    "*(level+1)}</ul>\n{"    "*level}</li>')
    # Arquivos: índice incremental por tópico pai
    # Se prefix for 0x0000, use 0, senão use o número do prefixo
    topic_num = int(prefix[2:]) if prefix.startswith('0x') else 0
    for f_idx, entry in enumerate(htmls):
        html_rel = os.path.join(rel_path, entry)
        # Buscar nome original do arquivo .md
        md_candidates = [f for f in os.listdir(folder) if f.lower().endswith('.md') and slugify(os.path.splitext(f)[0]) + '.html' == entry]

        if md_candidates:
            md_name = os.path.splitext(md_candidates[0])[0]
        else:
            md_name = os.path.splitext(entry)[0]
        file_prefix = f"{topic_num}.{f_idx}"
        items.append(f'{"    "*level}<li><a href="../pages/articles/{html_rel}" target="_blank">{file_prefix} - {language} - {unslugify(md_name)} | {author}</a></li>')
    return "\n".join(items)


def process_folder(folder, output, language, author):
    # Após todo processamento, remove arquivos .md do diretório de saída
    for root, dirs, files in os.walk(output):
        for file in files:
            if file.lower().endswith('.md'):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass
    # ...existing code...
    # Após todo processamento, remove arquivos .md do diretório de saída
    for root, dirs, files in os.walk(output):
        for file in files:
            if file.lower().endswith('.md'):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass
    # Skip unwanted folders
    skip_folders = ["docs", "DOCS", "zDocs", "zdocs", "documentation", "Documentation"]
    if os.path.basename(folder) in skip_folders:
        return
    # Prepare output folder
    if os.path.exists(output):
        shutil.rmtree(output)
    template = read_template()
    for root, dirs, files in os.walk(folder):
        rel_root = os.path.relpath(root, folder)
        out_root = os.path.join(output, rel_root)
        os.makedirs(out_root, exist_ok=True)
        # PAPER_TOPIC logic
        if rel_root == ".":
            paper_topic = os.path.basename(folder)
        else:
            paper_topic = f"{os.path.basename(folder)} - {rel_root}"
            for file in files:
                if file.endswith(".md"):
                    md_path = os.path.join(root, file)
                    html_name = slugify(os.path.splitext(file)[0]) + ".html"
                    html_path = os.path.join(out_root, html_name)
                    create_html(md_path, html_path, template, language, paper_topic)
                elif not file.lower().endswith('.md'):
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(out_root, file)
                    shutil.copy2(src_path, dst_path)
        # Copia subdiretórios (ex: pasta de imagens)
        for d in dirs:
            if d.lower() in ["images", "imagens", "imgs"]:
                continue
            src_dir = os.path.join(root, d)
            dst_dir = os.path.join(out_root, d)
            if not os.path.exists(dst_dir):
                shutil.copytree(src_dir, dst_dir)
                remove_md_files(dst_dir)
    # Remove arquivos .md do diretório de saída ao final do processamento
    remove_md_files(output)
    # Create zip
    zip_path = os.path.join(output, os.path.basename(output) + ".zip")
    zip_folder(output, zip_path)
    # Print HTML tree
    print(f'<li id="{slugify(os.path.basename(folder))}">0x0000 .......... {os.path.basename(folder)}')
    print('    <ul>')
    print(f'        <li><a href="../pages/articles/{os.path.basename(output)}/{os.path.basename(output)}.zip" target="_blank">Download topic content (.zip)!</a></li>')
    print(build_html_list(output, os.path.basename(output), author, language=language))
    print('    </ul>')
    print('</li>')


def print_navbar(topics):
    skip_folders = ["docs", "DOCS", "zDocs", "zdocs", "documentation", "Documentation"]
    filtered_topics = [t for t in topics if t not in skip_folders]
    print('\n<nav id="papers-navbar">')
    print('    ' + ' -\n    '.join([f'<a href="#{slugify(t)}">{t}</a>' for t in filtered_topics]) + '\n</nav>')


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python void.py <folder_path|input_dir> <output_folder> <PAPER_LANGUAGE> <AUTHOR>")
        sys.exit(1)
    folder = sys.argv[1]
    output = sys.argv[2]
    language = sys.argv[3]
    author = sys.argv[4]

    # Se folder for um diretório chamado 'input', processa todos os subdiretórios
    if os.path.basename(folder) == "input" and os.path.isdir(folder):
        topics = []
        for sub in sorted(os.listdir(folder)):
            sub_path = os.path.join(folder, sub)
            if os.path.isdir(sub_path):
                if sub in ["docs", "DOCS", "zDocs", "zdocs", "documentation", "Documentation"]:
                    continue
                out_sub = os.path.join(output, sub)
                process_folder(sub_path, out_sub, language, author)
                topics.append(sub)
        print_navbar(topics)
    else:
        process_folder(folder, output, language, author)
        print_navbar([os.path.basename(folder)])
