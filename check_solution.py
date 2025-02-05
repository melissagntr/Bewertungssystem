import nbformat
import subprocess

notebookDatei = "Testbook.ipynb"  
cellMarker = "###Aufgabe 1" 
solution = "2" 

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
    with open("Bewertung.txt", "w", encoding="utf-8") as f:
        if output == erwartet:
            f.write("Das Ergebnis ist richtig.\n")
        else:
            f.write(f"Die Lösung ist falsch. Die richtige Lösung lautet: '{erwartet}' \n")

if __name__ == "__main__":
    code = finde_loesung_zelle(notebookDatei, cellMarker)
    
    if code:
        output = fuehre_code_aus(code)
        schreibe_bewertung(output, solution)
    else:
        with open("Bewertung.txt", "w", encoding="utf-8") as f:
            f.write("Keine passende Zelle gefunden.\n")

