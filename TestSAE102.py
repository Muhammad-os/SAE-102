import SAE102_Muhammad_Côme as sae102 
import os

#---------------------------------------------- Test Question 1 : create_answers_from_text_file

def test_create_answers_from_text_file():
    # Création d'un fichier temporaire pour le test
    nom_fichier = "test_temp_eleves.txt"
    f = open(nom_fichier, "w")
    f.write("Harry Potter:1/2/3/4\nHermione Granger:10/10/10/10")
    f.close()
    
    # Exécution de la fonction
    resultat = sae102.create_answers_from_text_file(nom_fichier)
    
    # Vérification
    attendu = {
        "Harry Potter": [1, 2, 3, 4],
        "Hermione Granger": [10, 10, 10, 10]
    }
    
    assert resultat == attendu
    print("Test de la fonction create_answers_from_text_file: ok")
    
    # Nettoyage du fichier temporaire même si le test échoue
    if os.path.exists(nom_fichier):
        os.remove(nom_fichier)

# Test Question 2 : Euclidean_distance

def test_Euclidean_distance():
    # Test avec distance nulle
    assert sae102.Euclidean_distance([1, 2, 3], [1, 2, 3]) == 0.0
    
    assert sae102.Euclidean_distance([0, 0], [3, 4]) == 5.0
    
    print("Test de la fonction Euclidean_distance: ok")

#---------------------------------------------- Test Question 3 : Euclidean_house (1-NN)

def test_Euclidean_house():
    # Création de références simplifiées
    refs = [
        {"house": "MaisonA", "answer": [0, 0]},
        {"house": "MaisonB", "answer": [10, 10]}
    ]
    
    # Cas 1 : Point proche de MaisonA ([1,1] est plus proche de [0,0])
    assert sae102.Euclidean_house([1, 1], refs) == "MaisonA"
    
    # Cas 2 : Point proche de MaisonB ([9,9] est plus proche de [10,10])
    assert sae102.Euclidean_house([9, 9], refs) == "MaisonB"
    
    print("Test de la fonction Euclidean_house: ok")

#---------------------------------------------- Test Question 4 : Euclidean_repartition

def test_Euclidean_repartition():
    refs = [
        {"house": "MaisonA", "answer": [0, 0]},
        {"house": "MaisonB", "answer": [10, 10]}
    ]
    
    eleves = {
        "Eleve1": [1, 1], # Doit aller en MaisonA
        "Eleve2": [9, 9]  # Doit aller en MaisonB
    }
    
    resultat = sae102.Euclidean_repartition(eleves, refs)
    
    assert resultat["Eleve1"] == "MaisonA"
    assert resultat["Eleve2"] == "MaisonB"
    
    print("Test de la fonction Euclidean_repartition: ok")

#---------------------------------------------- Test Question 6 : insertion_position_NN

def test_insertion_position_NN():
    target = [0]
    # Liste de voisins triée par distance croissante : 
    # Voisin1 (dist 2), Voisin2 (dist 10)
    neighbors = [
        {"house": "V1", "answer": [2]}, 
        {"house": "V2", "answer": [10]}
    ]
    
    # Cas 1 : Candidat plus proche que tout le monde (dist 1) -> Indice 0
    cand1 = {"house": "C1", "answer": [1]}
    assert sae102.insertion_position_NN(target, cand1, neighbors) == 0
    
    # Cas 2 : Candidat au milieu (dist 5) -> Indice 1
    cand2 = {"house": "C2", "answer": [5]}
    assert sae102.insertion_position_NN(target, cand2, neighbors) == 1
    
    # Cas 3 : Candidat plus loin (dist 20) -> Indice 2 (fin)
    cand3 = {"house": "C3", "answer": [20]}
    assert sae102.insertion_position_NN(target, cand3, neighbors) == 2
    
    print("Test de la fonction insertion_position_NN: ok")

#---------------------------------------------- Test Question 7 : insertion_NN

def test_insertion_NN():
    target = [0]
    k = 2
    neighbors = []
    
    # 1. Ajout d'un élément
    # Distance = 10
    cand1 = {"house": "Loin", "answer": [10]} 
    neighbors = sae102.insertion_NN(target, cand1, neighbors, k)
    assert len(neighbors) == 1
    assert neighbors[0]["house"] == "Loin"
    
    # 2. Ajout d'un élément plus proche
    # Distance = 2
    cand2 = {"house": "Proche", "answer": [2]}
    neighbors = sae102.insertion_NN(target, cand2, neighbors, k)
    assert len(neighbors) == 2
    assert neighbors[0]["house"] == "Proche" # Doit être premier
    
    # 3. Ajout d'un élément très proche alors que la liste est pleine (k=2)
    cand3 = {"house": "TresProche", "answer": [1]}
    neighbors = sae102.insertion_NN(target, cand3, neighbors, k)
    
    assert len(neighbors) == 2
    assert neighbors[0]["house"] == "TresProche"
    assert neighbors[1]["house"] == "Proche"
    # Vérifie que "Loin" n'est plus là
    noms = [n["house"] for n in neighbors]
    assert "Loin" not in noms
    
    print("Test de la fonction insertion_NN: ok")

#---------------------------------------------- Test Question 8 : NN

def test_NN():
    # On cherche les 2 plus proches voisins de 5
    target = [5]
    refs = [
        {"house": "A", "answer": [1]},  # dist 4
        {"house": "B", "answer": [6]},  # dist 1 (Le plus proche)
        {"house": "C", "answer": [100]}, # dist 95
        {"house": "D", "answer": [4]}   # dist 1 (2e plus proche)
    ]
    k = 2
    
    resultat = sae102.NN(target, refs, k)
    
    # On attend B et D
    assert len(resultat) == 2
    noms_resultat = [r["house"] for r in resultat]
    assert "B" in noms_resultat
    assert "D" in noms_resultat
    assert "C" not in noms_resultat
    
    print("Test de la fonction NN: ok")

#---------------------------------------------- Test Question 9 : NN_house (Vote)

def test_NN_house():
    # Cas 1 : Majorité claire
    # 2 Gryffondor vs 1 Serpentard -> Gryffondor doit gagner
    voisins_maj = [
        {"house": "Gryffondor"}, 
        {"house": "Gryffondor"}, 
        {"house": "Serpentard"}
    ]
    assert sae102.NN_house(voisins_maj) == "Gryffondor"
    
    # Cas 2 : Égalité
    # Règle : En cas d'égalité, on prend la maison du voisin le plus proche géographiquement.
    # La liste 'neighbors' est supposée déjà triée par distance croissante.
    # Donc on regarde le premier élément de la liste qui appartient à une des maisons ex-aequo.
    voisins_egalite = [
        {"house": "Serdaigle"}, # C'est le plus proche (index 0)
        {"house": "Poufsouffle"}, 
        {"house": "Poufsouffle"}, 
        {"house": "Serdaigle"}
    ]
    # Ici 2 Serdaigle, 2 Poufsouffle. Le tout premier voisin (le plus proche) est Serdaigle.
    assert sae102.NN_house(voisins_egalite) == "Serdaigle"
    
    print("Test de la fonction NN_house: ok")

#---------------------------------------------- Test Question 10 : NN_repartition

def test_NN_repartition():
    # Données simplifiées avec des vrais noms de maisons
    refs = [
        {"house": "Gryffondor", "answer": [10]}, # Profil "10"
        {"house": "Serpentard", "answer": [0]}    # Profil "0"
    ]
    eleves = {
        "Drago": [1],  # Proche de 0 -> Serpentard
        "Harry": [9]   # Proche de 10 -> Gryffondor
    }
    k = 1
    
    resultat = sae102.NN_repartition(eleves, refs, k)
    
    assert resultat["Drago"] == "Serpentard"
    assert resultat["Harry"] == "Gryffondor"
    
    print("Test de la fonction NN_repartition: ok")

# Lancement de tous les tests

test_create_answers_from_text_file()
test_Euclidean_distance()
test_Euclidean_house()
test_Euclidean_repartition()
test_insertion_position_NN()
test_insertion_NN()
test_NN()
test_NN_house()
test_NN_repartition()
