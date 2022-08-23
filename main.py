from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pathlib import Path

PATH="/Users/vishal/Python-Projects/selenium_projects/chromedriver"

scope = {"cpp": "<scope>source.c++</scope>", "python": "<scope>source.python</scope>", "c": "<scope>source.c</scope>"}

sublime_snippet_path = Path.home() / "Library/Application Support/Sublime Text/Packages/User/snippets/"


def parse_snippet(snippet_data, lang):
    snippet_data = snippet_data.split("\n")
    len_prefix = len("// @prefix ")
    tabt = snippet_data[0][len_prefix:]
    len_desc = len("// @description ")
    desc = snippet_data[1][len_desc:]
    snippet_data = "\n".join(snippet_data[3:])
    launch_website(desc, tabt, snippet_data, lang)

def make_sublime_snippet(snippet, lang, prefix):
    global sublime_snippet_path
    snippet = snippet.split("\n")[:-3]
    snippet.append("  " + scope[lang])
    snippet.append("</snippet>")
    snippet = "\n".join(snippet)

    snippet_path = sublime_snippet_path / lang
    snippet_path.mkdir(parents=True, exist_ok=True)
    new_snippet_path = snippet_path / ("_".join(prefix.split()) + ".sublime-snippet")
    new_snippet_path.write_text(snippet)

def launch_website(desc, tabt, in_snippet, lang):
    service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=service)

    driver.get(f"https://snippet-generator.app/?mode=sublimetext")
    main = driver.find_element(By.CLASS_NAME, "app__main")
    desc_el = main.find_element(By.NAME, "description")
    tabt_el = main.find_element(By.NAME, "tabTrigger")
    in_snippet_el = main.find_element(By.NAME, "snippet")

    desc_el.send_keys(desc)
    tabt_el.send_keys(tabt)
    in_snippet_el.send_keys(in_snippet)

    out_snippet = driver.find_element(By.CLASS_NAME, "app__pre")
    make_sublime_snippet(out_snippet.text, lang, tabt)
    
    driver.quit()

if __name__=="__main__":
    root = Path.home() / "snippets"
    for file in root.iterdir():
        file_data = file.read_text()
        parse_snippet(file_data, file.suffixes[0][1:])