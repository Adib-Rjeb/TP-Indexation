import re
from collections import defaultdict
import math

# Exercice 1 :

# Chargement des documents depuis documents.tsv
def charger_documents(chemin):   
    documents = {}
    with open(chemin, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            # Séparation par tabulation
            doc_id, contenu = ligne.split("\t", 1)
            documents[doc_id] = contenu
    return documents

# Test :
docs = charger_documents("TP2\documents.tsv")
for doc_id, contenu in docs.items():
    print(f"{doc_id} → {contenu}")

# Exercice 2 :

def tokeniser(texte):

    #On récupère les mots (lettres accentuées incluses)
    texte = texte.lower()
    return re.findall(r"[a-zàâäéèêëîïôöùûüç0-9]+", texte)


def construire_index_inverse(documents):

    #retourne un dictionnaire : mot -> liste triée d'identifiants de documents.
    #Les identifiants sont les numéros extraits (D1 -> 1, D2 -> 2, ...)
    #pour permettre la comparaison numérique dans l'intersection.
    
    index = defaultdict(set)
    for doc_id, contenu in documents.items():
        num = int(re.sub(r"\D", "", doc_id))
        for mot in tokeniser(contenu):
            index[mot].add(num)
    return {mot: sorted(docs) for mot, docs in index.items()}


# Test :
index_inverse = construire_index_inverse(docs)
print("=== Index inversé complet ===")
for mot, liste in sorted(index_inverse.items()):
    print(f"{mot} → {liste}")

# Exercice 3 :

def intersection(list1, list2):
    i, j = 0, 0
    result = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return result

# Test :
terme1 = input("Entrez le premier terme : ")
terme2 = input("Entrez le deuxième terme : ")

docs1 = index_inverse.get(terme1, [])
docs2 = index_inverse.get(terme2, [])

print(f"Intersection : {intersection(docs1, docs2)}")

# Exercice 4 :

def construire_skip(liste, taille_skip=None):
    """
    Construit les skip pointers d'une liste triée.
    Retourne une liste de tuples (index_source, index_destination).
    Par défaut : saut de √n éléments.
    """
    n = len(liste)
    if n == 0:
        return []
    if taille_skip is None:
        taille_skip = max(1, int(math.sqrt(n)))
    skips = []
    i = 0
    while i + taille_skip < n:
        skips.append((i, i + taille_skip))
        i += taille_skip
    return skips

def intersection_avec_skip(list1, list2, skips1, skips2):
    
    i, j = 0, 0
    result = []

    # Dictionnaires pour retrouver un saut depuis un index
    dict_skip1 = {src: dst for src, dst in skips1}
    dict_skip2 = {src: dst for src, dst in skips2}

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1

        elif list1[i] < list2[j]:
            if i in dict_skip1 and list1[dict_skip1[i]] <= list2[j]:
                i = dict_skip1[i]
            else:
                i += 1

        else:
            if j in dict_skip2 and list2[dict_skip2[j]] <= list1[i]:
                j = dict_skip2[j]
            else:
                j += 1

    return result

#Test :

skips1 = construire_skip(docs1)
skips2 = construire_skip(docs2)

print(f"Skips 1 : {skips1}")
print(f"Skips 2 : {skips2}")

resultat_skip = intersection_avec_skip(docs1, docs2, skips1, skips2)
print(f"Intersection avec skip : {resultat_skip}")