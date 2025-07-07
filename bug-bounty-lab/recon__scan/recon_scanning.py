import os
import json
import csv
from datetime import datetime

# Target da scansionare
target = "www.gazzetta.it"

# Funzione per eseguire Nmap e restituire i risultati
def run_nmap(target):
    nmap_results = {}
    try:
        # Esegui il port scanning con Nmap
        nmap_output = os.popen(f"nmap -p- --open {target}").read()
        nmap_results["port_scan"] = nmap_output

        # Esegui il vuln scanning con Nmap
        vuln_output = os.popen(f"nmap --script=vuln {target}").read()
        nmap_results["vuln_scan"] = vuln_output

    except Exception as e:
        nmap_results["error"] = str(e)
    
    return nmap_results

# Funzione per eseguire Nikto e restituire i risultati
def run_nikto(target):
    nikto_results = {}
    try:
        # Esegui il Web Scanning con Nikto
        nikto_output = os.popen(f"nikto -h {target}").read()
        nikto_results["nikto_scan"] = nikto_output
    except Exception as e:
        nikto_results["error"] = str(e)
    
    return nikto_results

# Funzione per esportare i risultati in JSON
def export_to_json(results, filename="scan_report.json"):
    try:
        with open(filename, 'w') as json_file:
            json.dump(results, json_file, indent=4)
        print(f"Report salvato in {filename}")
    except Exception as e:
        print(f"Errore durante il salvataggio in JSON: {e}")

# Funzione per esportare i risultati in CSV
def export_to_csv(results, filename="scan_report.csv"):
    try:
        # Prepara i dati per CSV
        header = ["tool", "scan_type", "output"]
        rows = []
        for tool, scans in results.items():
            if isinstance(scans, dict):
                for scan_type, output in scans.items():
                    rows.append([tool, scan_type, output])

        # Scrivi i risultati su CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Report salvato in {filename}")
    except Exception as e:
        print(f"Errore durante il salvataggio in CSV: {e}")

# Funzione per creare un report di scansione
def create_report(target, results):
    report_name = f"recon_report_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(report_name, 'w') as report_file:
            report_file.write(f"Reconnaissance Report for {target}\n")
            report_file.write(f"Generated on: {datetime.now()}\n\n")

            for tool, scans in results.items():
                report_file.write(f"Tool: {tool}\n")
                if isinstance(scans, dict):
                    for scan_type, output in scans.items():
                        report_file.write(f"  {scan_type}:\n")
                        report_file.write(f"    {output}\n")
            print(f"Report salvato in {report_name}")
    except Exception as e:
        print(f"Errore durante il salvataggio del report: {e}")

# Funzione principale che esegue le scansioni e salva i risultati
def main(target):
    results = {}

    # Esegui le scansioni Nmap e Nikto
    print(f"Avviando la scansione di {target}...")
    results["Nmap"] = run_nmap(target)
    results["Nikto"] = run_nikto(target)

    # Esporta i risultati in JSON e CSV
    export_to_json(results)
    export_to_csv(results)

    # Crea un report completo
    create_report(target, results)

# Esegui il programma
if __name__ == "__main__":
    main(target)
