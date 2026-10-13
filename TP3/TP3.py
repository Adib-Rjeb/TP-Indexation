import re
import math
from collections import defaultdict, Counter

STOPWORDS = set("""
a an and are as at be by for from has he in is it its of on that the to was were will with
""".split())

def stem(word):
    """Stemming anglais volontairement simple pour l'expérience model/models."""
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

def preprocess(text, use_stemming=False):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS]
    if use_stemming:
        tokens = [stem(t) for t in tokens]
    return tokens

def construire_index_enrichi(documents, use_stemming=False):
    index = defaultdict(lambda: {"df": 0, "postings": {}})
    for doc_id, text in documents.items():
        tf = Counter(preprocess(text, use_stemming))
        for term, freq in tf.items():
            index[term]["postings"][doc_id] = {"tf": freq}
    for term, data in index.items():
        data["df"] = len(data["postings"])
    return dict(index)

def calculer_idf(terme, index_inverse, N):
    df = index_inverse.get(terme, {}).get("df", 0)
    return math.log10(N / df) if df else 0.0

def poids_tfidf(terme, doc_id, index_inverse, N):
    posting = index_inverse.get(terme, {}).get("postings", {}).get(doc_id)
    if not posting:
        return 0.0
    tf = posting["tf"]
    return (1 + math.log10(tf)) * calculer_idf(terme, index_inverse, N)

def document_vector(doc_id, vocabulary, index_inverse, N):
    return [poids_tfidf(term, doc_id, index_inverse, N) for term in vocabulary]

def query_vector(query, vocabulary, index_inverse, N, use_stemming=False):
    tf = Counter(preprocess(query, use_stemming))
    return [
        (1 + math.log10(tf[t])) * calculer_idf(t, index_inverse, N)
        if t in tf and t in index_inverse else 0.0
        for t in vocabulary
    ]

def cosine_similarity(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a*a for a in v1))
    n2 = math.sqrt(sum(b*b for b in v2))
    return dot / (n1*n2) if n1 and n2 else 0.0

def search(query, documents, index_inverse, vocabulary, N, k=5, use_stemming=False):
    qv = query_vector(query, vocabulary, index_inverse, N, use_stemming)
    results = []
    for doc_id in documents:
        score = cosine_similarity(qv, document_vector(doc_id, vocabulary, index_inverse, N))
        if score > 0:
            results.append((doc_id, score))
    return sorted(results, key=lambda x: (-x[1], x[0]))[:k]

def recherche_booleenne_and(query, documents, index_inverse, use_stemming=False):
    terms = list(dict.fromkeys(preprocess(query, use_stemming)))
    if not terms:
        return []
    if any(t not in index_inverse for t in terms):
        return []
    sets = [
        set(index_inverse[t]["postings"].keys())
        for t in terms
    ]
    matches = set.intersection(*sets)
    return [doc_id for doc_id in documents if doc_id in matches]

def load_documents(path="documents.tsv"):
    docs = {}
    from pathlib import Path

    fichier = Path(__file__).resolve().parent / path

    with open(fichier, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            doc_id, text = line.split("\t", 1)
            docs[doc_id] = text
    return docs

def afficher_pretraitement(documents):
    print("\nEXERCICE 2 - PRETRAITEMENT")
    for doc_id in list(documents)[:3]:
        text = documents[doc_id]
        lower_tokens = re.findall(r"[a-z0-9]+", text.lower())
        filtered = [t for t in lower_tokens if t not in STOPWORDS]
        print(f"{doc_id}: original={text}")
        print(f"  tokens={lower_tokens}")
        print(f"  sans stopwords={filtered}")
        print(f"  termes indexes={preprocess(text)}")

def afficher_index(index):
    print("\nEXERCICE 3 - EXTRAIT DE L'INDEX (10 termes)")
    for term in sorted(index)[:10]:
        postings = ", ".join(f"{d}(tf={p['tf']})" for d,p in sorted(index[term]["postings"].items()))
        print(f"{term:20} DF={index[term]['df']:2} POSTINGS: {postings}")

def afficher_df_idf(index, N):
    print("\nEXERCICE 4 - DF / IDF")
    for term in ("information", "retrieval", "vector", "boolean"):
        if term in index:
            print(f"{term:15} DF={index[term]['df']:2} IDF={calculer_idf(term,index,N):.4f}")
    max_df = max(v["df"] for v in index.values())
    min_df = min(v["df"] for v in index.values())
    max_idf = max(calculer_idf(t,index,N) for t in index)
    print("DF maximal:", ", ".join(t for t,v in index.items() if v["df"] == max_df), "=", max_df)
    print("DF minimal:", ", ".join(t for t,v in index.items() if v["df"] == min_df), "=", min_df)
    print("IDF maximal:", ", ".join(t for t in index if abs(calculer_idf(t,index,N)-max_idf)<1e-12), f"= {max_idf:.4f}")

def afficher_tfidf(index, documents, N, doc_id="D8"):
    print(f"\nEXERCICE 5 - POIDS TF-IDF DE {doc_id}")
    rows=[]
    for term, data in index.items():
        p=data["postings"].get(doc_id)
        if p:
            rows.append((term,p["tf"],data["df"],calculer_idf(term,index,N),poids_tfidf(term,doc_id,index,N)))
    for term,tf,df,idf,w in sorted(rows,key=lambda x:(-x[4],x[0])):
        print(f"{term:15} TF={tf:2} DF={df:2} IDF={idf:.4f} TF-IDF={w:.4f}")

def afficher_vecteurs(documents, index, vocab, N):
    print("\nEXERCICE 6 - VECTEURS")
    for doc_id in ("D1","D2","D3"):
        v=document_vector(doc_id,vocab,index,N)
        nonzero=[(t,w) for t,w in zip(vocab,v) if w]
        print(f"{doc_id}: {len(v)} composantes, {sum(x==0 for x in v)} nulles; non nulles={nonzero}")

def afficher_requete(query, index, vocab, N):
    print("\nEXERCICE 7 - VECTEUR REQUETE")
    qv=query_vector(query,vocab,index,N)
    print("Requête:",query)
    print("Poids non nuls:",[(t,round(w,4)) for t,w in zip(vocab,qv) if w])

def afficher_recherche(query, documents, index, vocab, N, k=5):
    print(f"\nRequête: {query}")
    print(f"{'Rang':<5}{'DocID':<8}{'Score':<10}Document")
    for rank,(doc_id,score) in enumerate(search(query,documents,index,vocab,N,k),1):
        print(f"{rank:<5}{doc_id:<8}{score:.4f}    {documents[doc_id]}")

def experimenter_stemming(documents, query="information retrieval model"):
    print("\nEXERCICE 10 - SANS / AVEC STEMMING")
    N=len(documents)
    for enabled,label in ((False,"sans"),(True,"avec")):
        idx=construire_index_enrichi(documents,enabled)
        vocab=sorted(idx)
        results=search(query,documents,idx,vocab,N,k=N,use_stemming=enabled)
        ranks={d:i for i,(d,s) in enumerate(results,1)}
        scores=dict(results)
        print(label, "stemming:")
        for doc_id in ("D2","D7"):
            print(f"  {doc_id}: score={scores.get(doc_id,0):.4f}, rang={ranks.get(doc_id,'non classé')}")

def experimenter_and(documents, index, vocab, N, query="information retrieval model"):
    print("\nEXERCICE 11 - BOOLÉEN AND VS TF-IDF")
    boolean=recherche_booleenne_and(query,documents,index)
    vectoriel=search(query,documents,index,vocab,N,k=5)
    print("Requête:",query)
    print("AND:", boolean if boolean else "aucun document")
    print("TF-IDF Top-5:", [(d,round(s,4)) for d,s in vectoriel])

def figl_search_engine():
    documents=load_documents()
    N=len(documents)
    index=construire_index_enrichi(documents)
    vocabulary=sorted(index)
    print("FIGL SEARCH ENGINE V2")
    print("Documents indexed:",N)
    print("Vocabulary size:",len(vocabulary))
    while True:
        query=input("\nQuery (exit pour quitter) > ")
        if query.lower() in ("exit","quit"):
            break
        try:
            k=int(input("Top-k ? (3/5/10) "))
            if k not in (3,5,10):
                print("Choisir 3, 5 ou 10.")
                continue
        except ValueError:
            print("Veuillez saisir un nombre.")
            continue
        afficher_recherche(query,documents,index,vocabulary,N,k)

def run_report_examples():
    documents=load_documents()
    N=len(documents)
    index=construire_index_enrichi(documents)
    vocab=sorted(index)
    print("Nombre de documents:",N)
    print("Taille du vocabulaire:",len(vocab))
    afficher_pretraitement(documents)
    afficher_index(index)
    afficher_df_idf(index,N)
    afficher_tfidf(index,documents,N,"D8")
    afficher_vecteurs(documents,index,vocab,N)
    afficher_requete("information retrieval model",index,vocab,N)
    print("\nEXERCICE 8 - SCORES COSINUS")
    afficher_recherche("information retrieval model",documents,index,vocab,N,k=N)
    print("\nEXERCICE 9 - CINQ REQUETES (TOP-5)")
    queries=[
        "information retrieval model",
        "TF IDF ranking",
        "dense retrieval embeddings",
        "boolean query documents",
        "search engines inverted indexes"
    ]
    for q in queries:
        afficher_recherche(q,documents,index,vocab,N,5)
    experimenter_stemming(documents)
    experimenter_and(documents,index,vocab,N)
    print("\nEXERCICE 12 - LANCER python TP3.py pour le mode interactif.")

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="--rapport":
        run_report_examples()
    else:
        figl_search_engine()
