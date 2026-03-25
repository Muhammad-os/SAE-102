#----------------------------------------------Question 1

def create_answers_from_text_file(nom_fichier):
    """
    Lit un fichier texte et renvoie un dictionnaire contenant les réponses
    
    Entrées
    nom_fichier : chemin du fichier à lire
    
    Sortie
    rep : dictionnaire associant le nom de chaque élève à sa liste de notes
    """
    rep = {}
    f = open(nom_fichier)
    lignes = f.readlines()
    f.close()   
    i = 0
    while i < len(lignes):
        cut = lignes[i].split(":")
        rep[cut[0]] = []
        scores = cut[1].split("/")
        j = 0
        while j < len(scores):
            rep[cut[0]].append(int(scores[j]))
            j += 1
        i += 1
    return rep

#----------------------------------------------Question 2

from math import sqrt

def Euclidean_distance(answer1, answer2):
    """
    Calcule la distance euclidienne entre deux listes de réponses
    
    Entrées
    answer1 : première liste de réponses
    answer2 : seconde liste de réponses
    
    Sortie
    La distance euclidienne calculée entre les deux listes
    """
    n = len(answer1)
    dist = 0
    for i in range(n):
        dist += (answer1[i] - answer2[i])**2
    return sqrt(dist)

#----------------------------------------------Question 3

def Euclidean_house(answer, ref):
    """
    Trouve la maison la plus proche d'une réponse donnée en comparant les distances
    
    Entrées
    answer : liste des réponses de l'élève
    ref : liste de dictionnaires contenant les références des maisons
    
    Sortie
    Le nom de la maison dont la distance est la plus faible
    """
    dist_init = Euclidean_distance(ref[0]["answer"], answer)
    house = ref[0]["house"]
    for dico in ref:
        dist_actuelle = Euclidean_distance(dico["answer"], answer)
        # Mise à jour si la distance actuelle est inférieure ou égale à la distance minimale connue
        if dist_actuelle <= dist_init:
            house = dico["house"]
            dist_init = dist_actuelle
    return house

#----------------------------------------------Question 4
from s101 import *
from json import *

def Euclidean_repartition(dico_rep, dico_ref):
    """
    Associe une maison à chaque élève en utilisant la distance euclidienne
    
    Entrées
    dico_rep : dictionnaire des élèves et leurs réponses
    dico_ref : liste des références des maisons
    
    Sortie
    dico_affect : dictionnaire associant chaque élève à sa maison attribuée
    """
    dico_affect = {}
    for nom in dico_rep:
        maison = Euclidean_house(dico_rep[nom], dico_ref)
        dico_affect[nom] = maison
    return dico_affect

f = open("houses_ref.json", "r")
dico_reference = load(f)
f.close()

reponses = create_answers_from_text_file("questionnaire_premiere_annee_10q.txt")

rep_euc = Euclidean_repartition(reponses, dico_reference)

affectation = lecture_reponses("questionnaire_premiere_annee.txt")
rep_classic = repartition(affectation)

s = open("affectation_premiere_annee.json", "r")
rep_magie = load(s)
s.close()

print("Pourcentage d'erreur pour rep_classic : " + str(round(nb_erreurs(rep_classic, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 57.26%
print("Pourcentage d'erreur pour rep_euc : " + str(round(nb_erreurs(rep_euc, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 19.35%

#Le pourcentage d'erreur avec cette nouvelle méthode de répartition est inférieur au pourcentage d'erreurs de la méthode précédente.
#Cette méthode est donc meilleur que celle de la SAÉ S1.01.

#----------------------------------------------Question 5

f = open("houses_multiple_refs.json", "r")
dico_reference_40 = load(f)
f.close()

rep_euc_40 = Euclidean_repartition(reponses, dico_reference_40)

print("Pourcentage d'erreur pour rep_euc_40 : " + str(round(nb_erreurs(rep_euc_40, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 16.13%

#Le pourcentage d'erreur avec ce nouveau dictionnaire de référence est encore plus bas et donc cela nous permet d'être plus précis dans la répartition des élèves.

#----------------------------------------------Question 6

def insertion_position_NN(answer, ref, neighbors):
    """
    Détermine l'indice où insérer un voisin pour garder la liste triée par distance croissante
    
    Entrées
    answer : réponse de l'élève cible
    ref : référence à ajouter
    neighbors : liste actuelle des voisins triée par distance
    
    Sortie
    L'indice d'insertion dans la liste
    """
    dist_ref = Euclidean_distance(answer, ref["answer"])
    i = 0
    while i < len(neighbors):
        ref_neighbor = neighbors[i]
        dist_neighbor = Euclidean_distance(answer, ref_neighbor["answer"])
        # Si le voisin actuel est plus éloigné que la référence on insère ici
        if dist_neighbor > dist_ref:
            return i
        i += 1
    # Si aucune place n'est trouvée avant on ajoute à la fin
    return len(neighbors)

#----------------------------------------------Question 7

def insertion_NN(answer, ref, neighbors, k):
    """
    Insère un voisin dans la liste en respectant l'ordre et la taille maximale k
    
    Entrées
    answer : réponse de l'élève
    ref : référence à ajouter
    neighbors : liste des voisins
    k : nombre maximum de voisins à conserver
    
    Sortie
    La liste des voisins mise à jour
    """
    position_NN = insertion_position_NN(answer, ref, neighbors)
    neighbors.insert(position_NN, ref)
    # Si la liste dépasse k éléments on retire le dernier qui est le plus éloigné
    if len(neighbors) > k:
        neighbors.pop()
    return neighbors
        
#----------------------------------------------Question 8

def NN(answer, ref, k):
    """
    Trouve les k plus proches voisins d'une réponse donnée
    
    Entrées
    answer : réponse de l'élève
    ref : liste de toutes les références
    k : nombre de voisins souhaités
    
    Sortie
    neighbors : liste des k références les plus proches
    """
    neighbors = []
    for dico in ref:
        neighbors = insertion_NN(answer, dico, neighbors, k)
    return neighbors

#----------------------------------------------Question 9

def NN_house(neighbors):
    """
    Détermine la maison finale par majorité parmi les voisins
    
    Entrées
    neighbors : liste des plus proches voisins triée par distance
    
    Sortie
    Le nom de la maison retenue
    """
    compteur = {"Serpentard":0, "Poufsouffle":0, "Serdaigle":0, "Gryffondor":0}
    # Compte les voix pour chaque maison
    for dico in neighbors:
        compteur[dico["house"]] += 1

    maison_max = []
    occ_max = 0
    # Recherche de la maison ayant le plus d'occurrences
    for maison in compteur:
        occurences = compteur[maison]
        if occurences > occ_max:
            occ_max = occurences
            maison_max = [maison]

        elif occurences == occ_max:
            maison_max.append(maison)

    if len(maison_max) == 1:
        return maison_max[0]
    else:
        # En cas d'égalité on choisit la maison du voisin le plus proche géographiquement
        # La liste neighbors étant déjà triée le premier trouvé est le plus proche
        for maison in neighbors:
            if maison["house"] in maison_max:
                return maison["house"]
            
#----------------------------------------------Question 10

def NN_repartition(dico_rep, ref, k):
    """
    Effectue la répartition de tous les élèves en utilisant l'algorithme des k plus proches voisins
    
    Entrées
    dico_rep : dictionnaire des élèves à classer
    ref : dictionnaire de référence
    k : paramètre du nombre de voisins
    
    Sortie
    repartition_NN : dictionnaire associant chaque élève à sa maison
    """
    repartition_NN = {}
    #On parcourt chaque nom dans le dictionnaire
    for nom_eleve in dico_rep:
        #On récupère la réponse associée à ce nom.
        reponse_eleve = dico_rep[nom_eleve]
        #On trouve les k voisins.
        neighbors = NN(reponse_eleve, ref, k)
        #On détermine la maison.
        maison_choisie = NN_house(neighbors)
        #On enregistre le résultat dans le nouveau dictionnaire.
        repartition_NN[nom_eleve] = maison_choisie
            
    return repartition_NN

k1 = (NN_repartition(reponses, dico_reference_40, 1))
k2 = (NN_repartition(reponses, dico_reference_40, 2))
k3 = (NN_repartition(reponses, dico_reference_40, 3))
k4 = (NN_repartition(reponses, dico_reference_40, 4))
k5 = (NN_repartition(reponses, dico_reference_40, 5))

print("Pourcentage d'erreur pour NN_repartition avec k = 1 : " + str(round(nb_erreurs(k1, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 16.12%
print("Pourcentage d'erreur pour NN_repartition avec k = 2 : " + str(round(nb_erreurs(k2, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 16.12%
print("Pourcentage d'erreur pour NN_repartition avec k = 3 : " + str(round(nb_erreurs(k3, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 2.41%
print("Pourcentage d'erreur pour NN_repartition avec k = 4 : " + str(round(nb_erreurs(k4, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 9.68%
print("Pourcentage d'erreur pour NN_repartition avec k = 5 : " + str(round(nb_erreurs(k5, rep_magie)*100/len(rep_magie),2)) +("%")) #Le pourcentage d'erreurs est d'environ 12.10%

#Le pourcentage d'erreur avec cette nouvelle méthode de répartition avec k = 3, k = 4 et k = 5 est inférieur au pourcentage d'erreurs de la méthode précédente.
#Cette méthode avec k = 3 possède le plus faible pourcentage d'erreur. Ainsi, cela est la meilleur méthode de répartition.
