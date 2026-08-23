from blocks import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_md = f.read()
    with open(template_path) as f:
        template_file = f.read()
    title = extract_title(from_md)
    from_html = markdown_to_html_node(from_md)
    html_string = from_html.to_html()
    page = template_file.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files_in_dir = os.listdir(dir_path_content)
    for file in files_in_dir:
        source_path = os.path.join(dir_path_content, file)
        destination_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(source_path):
            destination_path = destination_path.replace(".md", ".html")
            generate_page(source_path, template_path, destination_path)
        else:
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            generate_pages_recursive(source_path, template_path, destination_path)
