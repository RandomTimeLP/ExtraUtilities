import requests

def check_package_existence(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(f"Fehler beim Abrufen der Informationen zu {package_name}. Statuscode: {response.status_code}")

def find_similar_packages(package_name):
    similar_packages = []
    url = f"https://pypi.org/simple/{package_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        lines = content.splitlines()
        for line in lines:
            if package_name.lower() in line.lower() and line.strip() != package_name:
                similar_packages.append(line.strip())
    return similar_packages

# Beispielverwendung
package_name = "extrautils"
if check_package_existence(package_name):
    print(f"Das Paket {package_name} existiert bereits auf PyPI.")
    similar_packages = find_similar_packages(package_name)
    if similar_packages:
        print(f"Möglicherweise ähnliche Pakete: {', '.join(similar_packages)}")
else:
    print(f"Das Paket {package_name} existiert noch nicht auf PyPI.")