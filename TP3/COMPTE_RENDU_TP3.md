# Compte rendu — TP3 :

# Exercice 1

Le corpus contient 25 documents portant sur la recherche d’information, les index inversés, les modèles booléens et vectoriels, TF-IDF, BM25 et les embeddings.

Un corpus de documents proches thématiquement est plus intéressant, car plusieurs documents peuvent partager des termes. Le moteur doit donc distinguer les documents les plus pertinents grâce aux poids TF-IDF et à la similarité cosinus, plutôt que de trouver un résultat évident.

# Exercice 2 
Exemples issus de 'documents.tsv' :

| Document | Texte original | Tokens après suppression des stopwords |
|----------|----------------|----------------------------------------|
| D1 | Information retrieval systems use inverted indexes for efficient search | information, retrieval, systems, use, inverted, indexes, efficient, search |
| D2 | The vector space model represents documents and queries as vectors | vector, space, model, represents, documents, queries, vectors |
| D3 | Boolean retrieval uses AND OR and NOT operators | boolean, retrieval, uses, or, not, operators |

Le pipeline met le texte en minuscules, découpe le texte en tokens, puis supprime les mots vides. Le stemming est désactivé dans cette première expérience.

Il faut appliquer le même prétraitement aux documents et aux requêtes pour que les termes soient représentés de manière cohérente et puissent être comparés dans le même vocabulaire.

# Exercice 3

L’index associe chaque terme aux documents qui le contiennent. Chaque entrée contient 'df' et une liste 'postings' avec le 'tf' du terme dans chaque document.

Extrait de l’index généré :

| Terme | DF | Postings |
|-------|----|----------|
| 'bm25' | 2 | D6(tf=1), D16(tf=1) |
| 'boolean' | 2 | D3(tf=1), D13(tf=1) |
| 'between' | 2 | D14(tf=1), D18(tf=1) |

TF est le nombre d’occurrences d’un terme dans un document. DF est le nombre de documents différents qui contiennent ce terme.

# Exercice 4

Avec \(N=25\) documents et \(IDF(t)=\log_{10}(N/DF(t))\) :

| Terme | DF | IDF |
|-------|----|-----|
| information | 4 | 0,7959 |
| retrieval | 10 | 0,3979 |
| vector | 3 | 0,9208 |
| boolean | 2 | 1,0969 |

- DF maximal : 'retrieval', avec DF = 10.
- DF minimal : les termes présents dans un seul document, avec DF = 1.
- IDF maximal : les termes de DF = 1, avec IDF = 1,3979.

Un terme rare reçoit un IDF élevé, car il permet de mieux distinguer les documents dans lesquels il apparaît. Un terme très fréquent apporte moins d’information pour différencier les documents.

# Exercice 5

Pour le document D8, les poids calculés et triés par ordre décroissant sont :

| Terme | TF | DF | IDF | TF-IDF |
|-------|----|----|-----|--------|
| represents | 1 | 2 | 1,0969 | 1,0969 |
| using | 1 | 2 | 1,0969 | 1,0969 |
| embeddings | 1 | 3 | 0,9208 | 0,9208 |
| dense | 1 | 4 | 0,7959 | 0,7959 |
| queries | 1 | 5 | 0,6990 | 0,6990 |
| documents | 1 | 9 | 0,4437 | 0,4437 |
| retrieval | 1 | 10 | 0,3979 | 0,3979 |

Dans D8, tous ces termes ont TF = 1. Leurs poids TF-IDF diffèrent donc en fonction de leur IDF : les termes les plus rares obtiennent les poids les plus élevés. Ainsi, les termes ayant le plus grand TF ne sont pas toujours ceux qui ont le plus grand TF-IDF.

# Exercice 6

Le vocabulaire contient 107 termes.

| Document | Nombre de composantes | Composantes nulles |
|----------|-----------------------|--------------------|
| D1 | 107 | 99 |
| D2 | 107 | 100 |
| D3 | 107 | 101 |

Les vecteurs sont creux, car chaque document ne contient qu’une petite partie des termes du vocabulaire global. Les autres composantes sont égales à zéro.

# Exercice 7

Pour la requête 'information retrieval model', les poids non nuls sont :

| Terme | Poids |
|-------|-------|
| information | 0,7959 |
| retrieval | 0,3979 |
| model | 0,9208 |

Un terme absent du vocabulaire de la collection ne possède pas de composante correspondante dans le vecteur. Il est donc ignoré par cette représentation et ne contribue pas au score.

# Exercice 8

Pour la requête 'information retrieval model', les premiers scores obtenus sont :

| Document | Score cosinus |
|----------|---------------|
| D2 | 0,2705 |
| D7 | 0,2434 |
| D6 | 0,2418 |

Un score proche de 1 indique une forte similarité entre les vecteurs. Un score proche de 0 indique une faible similarité. Si l’un des vecteurs a une norme nulle, la fonction retourne 0 pour éviter une division par zéro.

# Exercice 9 

# Requête 1 : 'information retrieval model'

| Rang | Document | Score |
|------|----------|-------|
| 1 | D2 | 0,2705 |
| 2 | D7 | 0,2434 |
| 3 | D6 | 0,2418 |
| 4 | D14 | 0,2404 |
| 5 | D1 | 0,2395 |

D2 arrive en tête grâce au terme 'model'. D7 contient 'information', 'retrieval' et la forme plurielle 'models', mais sans stemming, 'models' ne correspond pas à 'model'. D6 est pertinent grâce à 'information retrieval'.

# Requête 2 : 'TF IDF ranking'

| Rang | Document | Score |
|---|---|---|
| 1 | D4 | 0,4575 |
| 2 | D15 | 0,4524 |
| 3 | D16 | 0,3136 |
| 4 | D6 | 0,1623 |
| 5 | D20 | 0,1374 |

D4 et D15 correspondent directement à TF-IDF. D16 arrive troisième, car il traite de l’amélioration de TF-IDF par BM25 et du classement.

### Requête 3 : 'dense retrieval embeddings'

| Rang | Document | Score |
|---|---|---|
| 1 | D8 | 0,5887 |
| 2 | D9 | 0,2356 |
| 3 | D18 | 0,2098 |
| 4 | D24 | 0,1934 |
| 5 | D17 | 0,1908 |

D8 contient les trois termes de la requête et obtient le meilleur score. D9 et D18 partagent le terme 'embeddings'. D24 et D17 traitent aussi de méthodes de recherche dense ou hybride.

### Requête 4 : 'boolean query documents'

| Rang | Document | Score |
|---|---|---|
| 1 | D13 | 0,4539 |
| 2 | D3 | 0,2825 |
| 3 | D21 | 0,1667 |
| 4 | D25 | 0,1532 |
| 5 | D8 | 0,0604 |

D13 est en tête grâce à son contenu sur le modèle booléen et les documents. D3 correspond au terme 'boolean' et à la recherche booléenne. D21 partage le terme 'query' avec la requête. Le classement repose sur les termes effectivement partagés après le prétraitement.

### Requête 5 : 'search engines inverted indexes'

| Rang | Document | Score |
|---|---|---|
| 1 | D10 | 0,5365 |
| 2 | D20 | 0,4847 |
| 3 | D1 | 0,3998 |
| 4 | D11 | 0,3025 |
| 5 | D5 | 0,2102 |

D10 contient les termes de la requête et obtient le meilleur score. D20 associe les moteurs de recherche aux index inversés. D1 traite également des index inversés et de la recherche efficace.

Les résultats montrent que le classement dépend des termes partagés et de leur poids TF-IDF. Les formes différentes d’un même mot ne sont pas automatiquement rapprochées sans normalisation morphologique.

# Exercice 10 

Requête utilisée : 'information retrieval model'.

| Mesure | Sans stemming | Avec stemming |
|---|---|---|
| Score de D2 (forme 'model') | 0,2705 | 0,2027 |
| Score de D7 (forme 'models') | 0,2434 | 0,4879 |
| Rang de D2 | 1 | 5 |
| Rang de D7 | 2 | 1 |

Avec stemming, 'models' est ramené à 'model'. D7 correspond alors aux trois termes de la requête et passe au premier rang. Les scores changent aussi parce que l’index et les statistiques DF/IDF sont recalculés après normalisation. Cette expérience montre que le prétraitement peut modifier le classement final.

Le stemming utilisé ici est volontairement simple ; il peut produire des formes imparfaites et ne remplace pas un lemmatiseur complet.

# Exercice 11

Requête : 'information retrieval model'.

| Critère | Booléen AND | Vectoriel TF-IDF |
|---|---|---|
| Documents retrouvés | Aucun document ne contient les trois formes exactes | D2, D7, D6, D14, D1 en tête |
| Correspondance partielle | Non : tous les termes sont exigés | Oui : un document peut être classé s’il partage certains termes |
| Score de pertinence | Pas de score dans cette implémentation | Score cosinus entre 0 et 1 |
| Classement | Pas de classement par score | Classement par score décroissant |

Un document contenant seulement deux des trois termes peut être rejeté par AND, mais retrouvé par TF-IDF avec un score positif. La recherche booléenne impose une correspondance stricte, tandis que la recherche vectorielle permet une correspondance partielle.

# Exercice 12

Le programme charge les 25 documents, construit l’index une seule fois au démarrage, affiche la taille du vocabulaire (107 termes) et permet de lancer plusieurs requêtes avec un Top-3, Top-5 ou Top-10.

TF-IDF présente certaines limites : il repose principalement sur la correspondance lexicale, ne comprend pas le sens des mots, ne rapproche pas automatiquement les variantes morphologiques et ne prend pas directement en compte la longueur des documents. BM25 peut améliorer le classement en tenant compte de la fréquence du terme, de sa rareté et de la longueur des documents, avec une saturation de la fréquence.

