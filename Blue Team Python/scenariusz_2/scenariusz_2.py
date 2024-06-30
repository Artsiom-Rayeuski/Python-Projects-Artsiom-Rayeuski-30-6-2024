import os
import re
import xml.etree.ElementTree as ET
import Evtx.Evtx as evtx
import subprocess

def evtx_to_xml(evtx_path, xml_path):
    try:
        # Przetwórz plik EVTX do formatu XML za pomocą python-evtx
        with evtx.Evtx(evtx_path) as log:
            records = [record.xml() for record in log.records()]

        with open(xml_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xml_file.write('<Events>\n')
            xml_file.write('\n'.join(records))
            xml_file.write('\n</Events>\n')

        #print(f"Plik EVTX został pomyślnie przetworzony do formatu XML: {xml_path}")
    except Exception as e:
        print(f"Błąd podczas przetwarzania pliku EVTX: {e}")


def re_analysis_xml(xml_path, regex):
    try:
        # Wczytaj dane z pliku XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        xml_data = ET.tostring(root, encoding='utf-8').decode('utf-8')

        # Użyj wyrażenia regularnego na danych
        matches = re.finditer(regex, xml_data)
        return [match.group(0) for match in matches]
    except Exception as e:
        print(f"Wystąpił błąd podczas analizy pliku XML: {e}")
        return []

def re_analysis_text(data, regex):
    # Użyj wyrażenia regularnego z modułu re na danych
    matches = re.finditer(regex, data)
    return [match.group(0) for match in matches]

def re_analysis(file_path, regex):
    # Sprawdź czy plik jest w formacie EVTX
    if file_path.lower().endswith('.evtx'):
        try:
            xml_path = file_path.replace('.evtx', '.xml')
            evtx_to_xml(file_path, xml_path)
            result = re_analysis_xml(xml_path, regex)
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania pliku EVTX: {e}")
        finally:
            # Spróbuj usunąć plik XML (jeśli istnieje)
            if 'xml_path' in locals() and os.path.exists(xml_path):
                os.remove(xml_path)
    else:
        # Użyj wyrażenia regularnego z modułu re na pliku tekstowym
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        result = re_analysis_text(data, regex)

    print(f"Wyniki analizy pliku {file_path} za pomoc modułu Python re:")
    print(result)



def grep_analysis(file_path, regex):
    try:
        # Sprawdź czy plik jest w formacie EVTX
        if file_path.lower().endswith('.evtx'):
            # Zamień EVTX na XML
            xml_path = file_path.replace('.evtx', '.xml')
            evtx_to_xml(file_path, xml_path)
            # Użyj grep do analizy pliku z użyciem wyrażenia regularnego
            result = subprocess.run(['grep', regex, xml_path], capture_output=True, text=True)
            print(f"Wyniki analizy pliku {file_path} za pomocą grep:")
            print(result.stdout)
        else:
            # Użyj grep do analizy pliku tekstowego z użyciem wyrażenia regularnego
            result = subprocess.run(['grep', regex, file_path], capture_output=True, text=True)
            print(f"Wyniki analizy pliku {file_path} za pomocą grep:")
            print(result.stdout)
    except Exception as e:
        print(f"Wystąpił błąd podczas analizy pliku {file_path}: {e}")


def offline_file_analysis(file_path, regex, use_grep=True):
    try:
        if use_grep:
            grep_analysis(file_path, regex)
        else:
            re_analysis(file_path, regex)
    except Exception as e:
        print(f"Wystąpił błąd podczas analizy pliku {file_path}: {e}")

if __name__ == '__main__':
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = path_to_folder + "/files/sample.evtx"
    offline_file_analysis(file_path, r'SourceIp', False)