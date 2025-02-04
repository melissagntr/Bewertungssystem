import nbformat

notebook_file = "Testbook.ipynb" #Dateiname des Jupyter Notebooks mit studentischer Lösung
search_marker = "###Aufgabe 1"

def check_notebook_for_task(notebook_path, marker):
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == "code" and marker in cell.source:
                return True

        return False
    except Exception as e:
        return f"Fehler beim Lesen des Notebooks: {e}"

result = check_notebook_for_task(notebook_file, search_marker)

with open("result.txt", "w", encoding="utf-8") as f:
    if result is True:
        f.write(f" Die Zelle mit '{search_marker}' wurde gefunden.\n")
    elif result is False:
        f.write(f" Die Zelle mit '{search_marker}' wurde NICHT gefunden.\n")
    else:
        f.write(f" {result}\n")

print("Ergebnis wurde in 'result.txt' gespeichert.")
