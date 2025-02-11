import nbformat
import subprocess
import os
#import requests
#URL = "http://localhost:8888"


notebook_file = "Testbook.ipynb" #evtl. dynamisch gestalten: der Student muss den Dateinamen angeben
# cell_marker = ["###Aufgabe 1", "###Aufgabe 2"]
# solution = [2, "Hello World"]
cell_marker = "###Aufgabe 1"
solution = 2

os.remove("Bewertung.txt") # Löscht die Datei, falls sie schon existiert

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
    
    # headers = {"code": code}
    # response = requests.post(URL, headers=headers)

    # result = response.text
    # return result


def schreibe_bewertung(output, erwartet):
    # Da der Output als String herauskommt
    try:
        output = eval(output)
    except:
        pass

    with open("Bewertung.txt", "a", encoding="utf-8") as f:
        if output == erwartet:
            f.write(f"Das Ergebnis {output} ist richtig.\n")
        else:
            f.write(f"Die Lösung {output} ist falsch. Die richtige Lösung lautet: {erwartet} \n")


if __name__ == "__main__":
    code = finde_loesung_zelle(notebook_file, cell_marker)
        
    if code:
            output = fuehre_code_aus(code)
            schreibe_bewertung(output, solution)
    else:
        with open("Bewertung.txt", "w", encoding="utf-8") as f:
                f.write("Keine passende Zelle gefunden.\n")

print("Fertig!")

