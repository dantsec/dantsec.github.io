import os
import shutil


"""
Edit the following variables to match your needs.

Instructions:

1. Edit variables.
2. Put .MD files in `/input` folder.
3. Create directory int `pages/articles/TOPIC_NAME_IN_KEBAB_CASE/`.
4. Run the script.
5. Edit pages/papers.html file with new content.
6. Clean folder `input`.
"""
# PATHS
TEMPLATE_PATH = '../../pages/articles/template.txt'
INPUT_FILES_PATH = 'input/'
OUTPUT_FILES_PATH = '../../pages/articles/php/'
ZIP_OUTPUT_PATH = '../../pages/backups/'
PAPER_HTML_PATH = '../pages/articles/php/'
# PAPER
PAPER_AUTHOR = '0xDant'
PAPER_INDEX = '0x06'
PAPER_LANGUAGE = 'pt-BR'
PAPER_TOPIC = 'PHP'
# OUTPUT
ZIP_FILE_NAME = 'php'


def get_text_from_file(file_path: str = '') -> str:
    """Get content from given file.
    """
    with open(file_path, 'r') as file:
        return file.read()


def process_file(
        file_path: str = '',
        template: str = '',
        paper_language: str = '',
        paper_topic: str = '') -> str:
    """Replace template with paper content.
    """
    file_content = get_text_from_file(file_path).rstrip('\n')

    template = template.replace('PAPER_LANGUAGE', paper_language)
    template = template.replace('PAPER_TOPIC', paper_topic)
    template = template.replace('PAPER_TEXT', file_content)

    return template


def write_text_to_file(file_path: str = '', text: str = ''):
    """Write text to file.
    """
    with open(file_path, 'w') as file:
        file.write(text)


def generate_html_list(files: list = []) -> str:
    """Generate html list with all processed files.
    """
    html_list = f"""<li>{PAPER_INDEX} .......... {PAPER_TOPIC}
    <ul>
    """

    html_list += f'    <li><a href="{ZIP_OUTPUT_PATH[3:]}{ZIP_FILE_NAME}.zip">0.0 - Download topic content (.zip)!</a></li>\n'

    for index, file in enumerate(files):
        html_list += f'        <li><a href="{PAPER_HTML_PATH}{file.replace('md', 'html')}">{index + 1}.0 - {PAPER_LANGUAGE.upper()} - {file.rstrip('.md')} | {PAPER_AUTHOR}</a></li>\n'

    html_list += '    </ul>\n</li>'

    return html_list


def create_zip_file():
    """Create zip file with all processed files.
    """
    zip_file_path = shutil.make_archive(f'{ZIP_FILE_NAME}', 'zip', OUTPUT_FILES_PATH)

    zip_file_name = os.path.basename(zip_file_path)

    destination_path = os.path.join(ZIP_OUTPUT_PATH, zip_file_name)

    shutil.move(zip_file_path, destination_path)


if __name__ == '__main__':
    template_content = get_text_from_file(TEMPLATE_PATH)

    files_to_proccess = os.listdir(INPUT_FILES_PATH)

    html_list = generate_html_list(files_to_proccess)

    print(html_list)

    for file in files_to_proccess:
        paper_path = f'{INPUT_FILES_PATH}{file}'

        processed_file = process_file(
            file_path=paper_path,
            template=template_content,
            paper_language=PAPER_LANGUAGE,
            paper_topic=PAPER_TOPIC,
        )

        new_file_path = f'{OUTPUT_FILES_PATH}{file}'.replace('.md', '.html')

        write_text_to_file(new_file_path, processed_file)

    create_zip_file()
