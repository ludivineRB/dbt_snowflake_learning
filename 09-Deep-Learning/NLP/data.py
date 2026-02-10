import json
import random
from typing import List, Dict, Tuple

CAPITALS_DATA = {
    "France": "Paris",
    "Allemagne": "Berlin",
    "Espagne": "Madrid",
    "Italie": "Rome",
    "Royaume-Uni": "Londres",
    "Portugal": "Lisbonne",
    "Pays-Bas": "Amsterdam",
    "Belgique": "Bruxelles",
    "Suisse": "Berne",
    "Autriche": "Vienne",
    "Pologne": "Varsovie",
    "Grèce": "Athènes",
    "Suède": "Stockholm",
    "Norvège": "Oslo",
    "Danemark": "Copenhague",
    "Finlande": "Helsinki",
    "Russie": "Moscou",
    "Ukraine": "Kiev",
    "Roumanie": "Bucarest",
    "Bulgarie": "Sofia",
    "Hongrie": "Budapest",
    "République tchèque": "Prague",
    "Slovaquie": "Bratislava",
    "Croatie": "Zagreb",
    "Serbie": "Belgrade",
    "Irlande": "Dublin",
    "Islande": "Reykjavik",
    "Luxembourg": "Luxembourg",
    "Malte": "La Valette",
    "Chypre": "Nicosie",
    "États-Unis": "Washington",
    "Canada": "Ottawa",
    "Mexique": "Mexico",
    "Brésil": "Brasilia",
    "Argentine": "Buenos Aires",
    "Chili": "Santiago",
    "Pérou": "Lima",
    "Colombie": "Bogota",
    "Venezuela": "Caracas",
    "Uruguay": "Montevideo",
    "Paraguay": "Asunción",
    "Bolivie": "La Paz",
    "Équateur": "Quito",
    "Cuba": "La Havane",
    "Jamaïque": "Kingston",
    "Chine": "Pékin",
    "Japon": "Tokyo",
    "Inde": "New Delhi",
    "Corée du Sud": "Séoul",
    "Indonésie": "Jakarta",
    "Thaïlande": "Bangkok",
    "Vietnam": "Hanoï",
    "Philippines": "Manille",
    "Malaisie": "Kuala Lumpur",
    "Singapour": "Singapour",
    "Pakistan": "Islamabad",
    "Bangladesh": "Dacca",
    "Turquie": "Ankara",
    "Iran": "Téhéran",
    "Irak": "Bagdad",
    "Arabie saoudite": "Riyad",
    "Égypte": "Le Caire",
    "Israël": "Jérusalem",
    "Liban": "Beyrouth",
    "Jordanie": "Amman",
    "Syrie": "Damas",
    "Émirats arabes unis": "Abou Dabi",
    "Qatar": "Doha",
    "Koweït": "Koweït",
    "Australie": "Canberra",
    "Nouvelle-Zélande": "Wellington",
    "Afrique du Sud": "Pretoria",
    "Nigeria": "Abuja",
    "Kenya": "Nairobi",
    "Éthiopie": "Addis-Abeba",
    "Ghana": "Accra",
    "Maroc": "Rabat",
    "Algérie": "Alger",
    "Tunisie": "Tunis",
    "Libye": "Tripoli",
    "Sénégal": "Dakar",
    "Côte d'Ivoire": "Yamoussoukro",
    "Cameroun": "Yaoundé",
    "Zimbabwe": "Harare",
    "Tanzanie": "Dodoma",
    "Ouganda": "Kampala"
}

def create_training_data(test_split: float = 0.2) -> Tuple[List[Dict], List[Dict]]:
    """
    Crée les données d'entraînement et de test pour le modèle avec augmentation de données.
    
    Args:
        test_split: Proportion des données à utiliser pour le test
        
    Returns:
        Tuple contenant les données d'entraînement et de test
    """
    all_data = []
    
    # Variantes de questions pour augmenter les données
    question_templates = [
        "Quelle est la capitale de {country} ?",
        "Quelle est la capitale du {country} ?",
        "Quelle est la capitale de la {country} ?",
        "Quelle ville est la capitale de {country} ?",
        "Quelle ville est la capitale du {country} ?",
        "Quelle ville est la capitale de la {country} ?",
        "Quel est le siège du gouvernement de {country} ?",
        "Quel est le siège du gouvernement du {country} ?",
        "Quel est le siège du gouvernement de la {country} ?",
        "Dans quelle ville se trouve le gouvernement de {country} ?",
        "Dans quelle ville se trouve le gouvernement du {country} ?",
        "Dans quelle ville se trouve le gouvernement de la {country} ?",
        "Où se situe la capitale de {country} ?",
        "Où se situe la capitale du {country} ?",
        "Où se situe la capitale de la {country} ?",
        "Pouvez-vous me dire la capitale de {country} ?",
        "Pouvez-vous me dire la capitale du {country} ?",
        "Pouvez-vous me dire la capitale de la {country} ?",
        "Connaissez-vous la capitale de {country} ?",
        "Connaissez-vous la capitale du {country} ?",
        "Connaissez-vous la capitale de la {country} ?",
        "Capital de {country} ?",
        "Capital du {country} ?",
        "Capital de la {country} ?",
        "Capitale {country}",
        "{country} capitale ?",
        "{country} - capitale ?"
    ]
    
    for country, capital in CAPITALS_DATA.items():
        # Ajouter toutes les variantes pour chaque pays
        for template in question_templates:
            try:
                question = template.format(country=country)
                all_data.append({
                    "text": question,
                    "label": capital,
                    "country": country
                })
            except:
                # Si le template ne fonctionne pas (ex: article manquant), passer
                continue
    
    random.shuffle(all_data)
    
    split_idx = int(len(all_data) * (1 - test_split))
    train_data = all_data[:split_idx]
    test_data = all_data[split_idx:]
    
    return train_data, test_data

def get_all_capitals() -> List[str]:
    """Retourne la liste de toutes les capitales."""
    return list(set(CAPITALS_DATA.values()))

def save_data(train_data: List[Dict], test_data: List[Dict]):
    """Sauvegarde les données dans des fichiers JSON."""
    with open('train_data.json', 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    
    with open('test_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    train_data, test_data = create_training_data()
    save_data(train_data, test_data)
    print(f"Données créées: {len(train_data)} exemples d'entraînement, {len(test_data)} exemples de test")