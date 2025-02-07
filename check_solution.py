import nbformat
import subprocess

notebook_file = "Testbook.ipynb" #evtl. dynamisch gestalten: der Student muss den Dateinamen angeben
# cell_marker = ["###Aufgabe 1", "###Aufgabe 2"]
# solution = [2, "Hello World"]
solution_per_task = {
    "###Aufgabe 1": 2,
    "###Aufgabe 2": "Hello World"
}

with open("Bewertung.txt", "w", encoding="utf-8") as f:
    pass

def finde_loesung_zelle(notebook, marker):
    with open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for cell in nb.cells:
        if cell.cell_type == "code" and marker in cell.source:
            return cell.source  
    return None

def fuehre_code_aus(code):
    try:
        result = subprocess.run(
            ["python", "-c", code],  
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Fehler: {str(e)}"

def schreibe_bewertung(output, erwartet):
    with open("Bewertung.txt", "a", encoding="utf-8") as f:
        if output == erwartet:
            f.write("Das Ergebnis ist richtig.\n")
        else:
            f.write(f"Die Lösung ist falsch. Die richtige Lösung lautet: '{erwartet}' \n")

for key in solution_per_task:
    if __name__ == "__main__":
        code = finde_loesung_zelle(notebook_file, key)
        
        if code:
            output = fuehre_code_aus(code)
            schreibe_bewertung(output, solution_per_task[key])
        else:
            with open("Bewertung.txt", "a", encoding="utf-8") as f:
                f.write("Keine passende Zelle gefunden.\n")

