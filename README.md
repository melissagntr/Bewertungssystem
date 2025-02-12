Die folgenden Kommentare dienen dazu, die einzelnen Zeilen des GitHub Workflows zu erklären.

    name: Automatische Bewertung des Jupyter Notebooks
    --> Name des Workflows, welcher unter GitHub Actions angezeigt wird

    on:
      push:
        branches:
          - main 
    --> Definition des Events, welches den Workflow auslösen soll
    --> in diesem Fall sobald ein push auf den main-Branch erfolgt

    jobs:
      bewerten_notebook:
      --> Name des Jobs, welches bei Auslösen des Events ausgeführt werden soll
        runs-on: ubuntu-latest
        --> Angabe auf welchem Betriebssystem der Job ausgeführt werden soll
        --> die neueste Version von Ubuntu in einer virutellen Umgebung
        permissions:
          contents: write
        --> Definition von Berechtigungen
        --> mittels write auf contents erhält der Workflow ein Schreibrecht auf das Repository (somit hat der Workflow das Recht, das neue Jupyter Notebook auf das Repo zu pushen

    steps:
    --> da der Job aus mehreren Abfolgen besteht, werden diese in verschiedene Steps unterteilt
      - name: Repository auschecken
        uses: actions/checkout@v3
        --> eine vorgefertigte GitHub Action, mit der der Code aus dem Repository in die virtuelle Maschine (Runner) zu laden, ohne diese  Angabe könnte der Workflow nicht auf die Daten des Repositorys zugreifen

      - name: Installiere Abhängigkeiten
        run: pip install nbformat
        --> führt den angegebenen Shell-Befehl aus, um die Python Bibliothek nbformat zu installieren, mit der Jupyter Notebooks analysiert und verarbeitet werden können; ohne diesen Befehl, könnte das darauffolgende Python Programm nicht ausgeführt werden

      - name: Führe Code aus und bewerte das Ergebnis
        run: python Bewertung/Bewertung.py
        --> führt die Python-Datei, welche sich im Repo befindet, aus 

      - name: Pushe das aktualisierte Jupyter Notebook ins Repository
        run: |
          --> senkrechter Strich als Shell-Befehl welcher angibt, dass nun mehrere Shell-Befehle nacheinander ausgeführt werden sollen
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
           --> beide Schritte dienen der Konfiguration eine Git-Nutzes, welche den darauffolgenden Commits zugeordnet werden (ohne diese, könnten keine Commits aus das Repo erfolgen, da Git diese einem Nutzer zuweisen muss)
          git add Aufgaben/01/01Aufgabe.ipynb
          --> das durch die Python-Datei veränderte Jupyter Notebook wird für den nächsten Commit registirert
          git commit -m "Automatische Bewertung ins Notebook eingefügt" --allow-empty
          --> erstellt einen neuen Git-Commit mit der eingegebenen Nachricht, zusätzlich wird mittels allow-empty angegeben, dass auch dann ein Commit erstellt werden darf, wenn keine Änderungen bezüglich des Jupyter Noteboosk festzustellen sind; ohne eine Änderung an der Datei würde sonst kein Commit erstellt werden
          git pull --rebase origin main || (git rebase --abort && echo "Rebase fehlgeschlagen, führe Merge durch")
          --> der erste Befehl versucht, die neuesten Änderungen aus dem main Branch zu pullen und in den aktuellen Stand einzuführen
          --> der zweite Befehl wir dann ausgeführt, wenn beim ersten ein Fehler auftritt, dieser bricht --rebase ab und gibt den Text wieder, dass ein normaler Merge durchgeführt werden soll
          git pull --no-rebase
          --> hiermit wird ein normale Git-Pull ausgeführt 
          git push
          --> push den neu erstellten Commit mitsamt des Jupyter Notebooks in das Repo

Die folgenden Kommentare dienen dazu, die Python-Datei näher zu erläutern:

    import nbformat
    import subprocess
    import os
    #import requests
    #URL = "http://localhost:8888"


    notebook_datei = "Aufgaben/01/01Aufgabe.ipynb"
    solution_per_task = {
        "Aufgabe 1": 2,
        "Aufgabe 2": "Hello World"
    }
    #cell_marker = "###Aufgabe 1"
    #loesung = 2

    def suche_loesungs_zelle(notebook, marker):
        with open(notebook, 'r', encoding='utf-8') as f:  --> das Notebook wird im Lesemodus geöffnet
            nb = nbformat.read(f, as_version=4)           --> die Variable enthält das Jupyter Notebooks als Dictionary, welches als
                                                              eine Liste von Zellen aufgeteilt ist

        for i, cell in enumerate(nb.cells):                         --> das Dictionary wird Zelle für Zelle durchgegangen, die aktuelle
                                                                        Zelle wird mit einem Index i versehen
            if cell.cell_type == "code" and marker in cell.source:  --> wenn es sich bei der Zelle um eine Codezelle handelt, und auch
                                                                        der oben definierte marker im Source-Code enthalten sind
                return nb, i, cell.source                               werden nb (siehe unten), der index der Zelle, welcher mit der
        return None, None, None                                         for-Schleife generiert wird und der Inhalr der Code-Zelle
                                                                        zurückgegeben werden
    nb ist wie folgt aufgebaut:
    {'cells': 
      [{'cell_type': 'markdown', 'metadata': {}, 'source': 'Aufgabe 1: Schreiben Sie ein Programm, welches die Zahl 2 zurückgibt.'}, {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': '###Aufgabe 1\n\n# Ihre Lösung hier\nprint(1)'}, 
      {'cell_type': 'markdown', 'metadata': {}, 'source': 'Das Ergebnis ist falsch.'}, 
      {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': '###Aufgabe 2\n\n# Ihre Lösung hier\nprint("Hello")'}, 
      {'cell_type': 'markdown', 'id': 'a720254c', 'metadata': {}, 'source': 'Das Ergebnis ist falsch.'}], 'metadata': {'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 2}

    bei ausgeführter Zelle ist nb wie folgt aufgebaut:
    {'cells': 
      [{'cell_type': 'markdown', 'metadata': {}, 'source': 'Aufgabe 1: Schreiben Sie ein Programm, welches die Zahl 2 zurückgibt.'}, {'cell_type': 'code', 'execution_count': 1, 'metadata': {}, 'outputs': [{'name': 'stdout', 'output_type': 'stream', 'text': '1\n'}], 'source': '###Aufgabe 1\n\n# Ihre Lösung hier\nprint(1)'}, 
      {'cell_type': 'markdown', 'metadata': {}, 'source': 'Das Ergebnis ist falsch.'}, 
      {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': '###Aufgabe 2\n\n# Ihre Lösung hier\nprint("Hello")'}, 
      {'cell_type': 'markdown', 'id': 'a720254c', 'metadata': {}, 'source': 'Das Ergebnis ist falsch.'}], 
      'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3}, 'file_extension': '.py', 'mimetype': 'text/x-python', 'name': 'python', 'nbconvert_exporter': 'python', 'pygments_lexer': 'ipython3', 'version': '3.11.5'}}, 'nbformat': 4, 'nbformat_minor': 2}

    def fuehre_code_aus(code):
        try:
            result = subprocess.run(                        --> durch subprocess.run wird der Code über ein Terminal als separaten
                ["python", "-c", code],                         Prozess ausgeführt
                capture_output=True, text=True, timeout=5
            )     
            return result.stdout.strip()                    --> gibt die Ausgabe des Codes zurück, ohne überflüssige Leerzeichen etc.
        except Exception as e:
            return f"Fehler: {str(e)}"

    #def erhalte_bewertung(code):
        # headers = {"code": code}
        # response = requests.post(URL, headers=headers)

        # result = response.text
        # return result


    def schreibe_bewertung(nb, index, output, erwartet):
        # Da der Output als String herauskommt
        try:
            output = eval(output)
        except:
            pass

        if output == erwartet:
            text = "Das Ergebnis ist korrekt."
        else:
            text = "Das Ergebnis ist falsch."

        if index + 1 < len(nb.cells) and nb.cells[index + 1].cell_type == "markdown":
            nb.cells[index + 1].source = text  
        else:
            markdown_zelle = nbformat.v4.new_markdown_cell(text)
            nb.cells.insert(index + 1, markdown_zelle) 

    def speichere_notebook(notebook_path, nb):
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    for key in solution_per_task:
        if __name__ == "__main__":
            nb, index, code = suche_loesungs_zelle(notebook_datei, key)
                
            if code:
                output = fuehre_code_aus(code)
                schreibe_bewertung(nb, index, output, solution_per_task[key])
                speichere_notebook(notebook_datei, nb)
                print("Bewertung wurde in das Notebook eingefügt.")
            else:
                print("Keine passende Zelle gefunden.")    