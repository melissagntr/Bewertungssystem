import nbformat #Modul, das Jupyter-Notebooks als strukturiertes JSON-Format (Dictionary) speichert
import subprocess
import sys
import json
#import requests
#URL = "http://localhost:8888"


notebook_datei = "Aufgaben/01/01Aufgabe.ipynb"
solution_per_task = {
    "###Aufgabe 1": 2,
    "###Aufgabe 2": "Hello World"
}
#cell_marker = "###Aufgabe 1"
#loesung = 2

def suche_loesungs_zelle(notebook, marker):
    with open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and marker in cell.source:
            return nb, i, cell.source 
    return None, None, None

def fuehre_code_aus(code):
    try:
        result = subprocess.run(
            ["python", "-c", code],  
            capture_output=True, text=True, timeout=5
        )     
        return result.stdout.strip()
    except Exception as e:
        return f"Fehler: {str(e)}"
    
#def erhalte_bewertung(code):
    # headers = {"code": code, "count": try_counter}
    # response = requests.post(URL, headers=headers)

    # result = response.text
    # return result

def schreibe_bewertung(nb, index, output, erwartet, counter):
    # Da der Output als String herauskommt
    try:
        output = eval(output)
    except:
        pass
    
    if output == erwartet:
        text = "Das Ergebnis ist korrekt."
        counter += 1
    else:
        if counter < 3:
            text = "Das Ergebnis ist falsch."
            counter += 1
        else:
            text = "Das Ergebnis ist falsch, das richige Ergebnis lautet: ."
            counter += 1
    
    if index + 1 < len(nb.cells) and nb.cells[index + 1].cell_type == "markdown":
        if nb.cells[index + 1].source.startswith("Das Ergebnis ist"):  
            nb.cells[index + 1].source = text  
        else:
            markdown_zelle = nbformat.v4.new_markdown_cell(text)
            nb.cells.insert(index + 1, markdown_zelle)
    else:
        markdown_zelle = nbformat.v4.new_markdown_cell(text)
        nb.cells.insert(index + 1, markdown_zelle)

    return counter


def speichere_notebook(notebook_path, nb):
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


if __name__ == "__main__":

    for key in solution_per_task:

        with open("userconfig.json", "r") as file:
            userconfig = json.load(file)

        try_counter = userconfig[key]

        nb, index, code = suche_loesungs_zelle(notebook_datei, key)
            
        if code:
            output = fuehre_code_aus(code)
            new_count = schreibe_bewertung(nb, index, output, solution_per_task[key], try_counter)
            speichere_notebook(notebook_datei, nb)
            print("Bewertung wurde in das Notebook eingefügt.")

            userconfig[key] = new_count
            with open("userconfig.json", "w") as file:
                json.dump(userconfig, file, indent=4)
                
        else:
            print("Keine passende Zelle gefunden.")   




