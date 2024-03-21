"""
Fichiers d'exemples pour la problématique de l'APP6 (S2)
(c) Julien Rossignol & JB Michaud Université de Sherbrooke
v 1.1 Hiver 2024

"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

import helpers as hp


###############################################################################
def exampleRacines():
    """
    Calcule et affiche les pôles et zéros d'une FT arbitraire

    :return:
    """
    b1 = [1, 0, 0]  # définition des facteurs du polynome numérateur
    a1 = [1, 1, 0.5]  # définition des facteurs du polynome dénominateur

    # méthode plus manuelle
    z1 = np.roots(b1)
    # pour éventuellement faire l'inverse de l'opération roots, i.e. passer d'une
    # liste de racines aux coefficients du polynôme, voir np.poly
    p1 = np.roots(a1)
    print(f'Racine exemple 1 Zéros:{z1}, Pôles:{p1}')  # affichage du resultat dans la console texte
    # appel d'une fonction pour affichage graphique, voir autre fichier helpers.py
    hp.pzmap1(z1, p1, 'Example de racines 1')

    # méthode utilisant scipy
    (z2, p2, k2) = signal.tf2zpk(b1, a1)  # passage à la représentation zok (liste de racines + "gain")
    print(f'Racine exemple 2 Zéros : {z2}, Pôles: {p2}, Gain: {k2}')
    hp.pzmap1(z2, p2, 'Example de racines 2')


###############################################################################
def exampleBode():
    """
    Calcule et affiche le lieu de bode d'une FT arbitraire

    :return:
    """
    b1 = [1, 0, 0]  # définition du numérateur de la fonction de transfert
    a1 = [1, 1, 0.5]  # définition du dénominateur de la fonction de transfert

    # méthode 1 avec bode
    tf1 = signal.TransferFunction(b1, a1)  # définit la fonction de transfert
    # calcul le diagrame de Bode, la magnitude en dB et la phase en degrés la fréquence en rad/s
    w1, mag1, phlin1 = signal.bode(tf1, np.logspace(-1.5, 1, 200))  # on pourrait aussi laisser la fonction générer les w
    # fonction d'affichage
    hp.bode1(w1, mag1, phlin1, 'Example 1')


###############################################################################
def exampleButterworth():
    """
    Exemple de génération et affichage pour la FT d'un filtre de butterworth d'ordre 4

    :return:
    """

    order = 4
    wn = 1   # frequence de coupure = 1 rad/s
    # définit un filtre passe bas butterworth =>  b1 numerateur, a1 dénominateur
    b1, a1 = signal.butter(order, wn, 'low', analog=True)
    print(f'Butterworth Numérateur {b1}, Dénominateur {a1}')  # affiche les coefficients correspondants au filtre
    print(f'Racine butterworth Zéros:{np.roots(b1)}, Pôles:{np.roots(a1)}')  # affichage du resultat dans la console texte


    # Réponse en fréquence
    mag1, ph1, w1, fig, ax = hp.bodeplot(b1, a1, 'Butterworth Example')

    # Délai de groupe
    delay = - np.diff(ph1) / np.diff(w1)    # calcul
    hp.grpdel1(w1, delay, 'Exemple butterworth')    # affichage

    # Exemple 1 réponse temporelle 3 cos
    t1 = np.linspace(0, 10, 5000, endpoint=False)
    # génération de 3 sinusoîdes
    u1 = (np.cos(2 * np.pi * 0.4 * t1) + 0.6 * np.cos(2 * np.pi * 4 * t1) +
          0.5 * np.cos(2 * np.pi * 8 * t1))
    # simulation temporelle du système
    tout1, yout1, xout1 = signal.lsim((b1, a1), u1, t1)
    hp.timeplt1(t1, u1, tout1, yout1, 'filtrage de 3 sinus')   # affichage

    # Exemple 2 réponse à l'échelon à la mitaine mitaine
    t2 = np.linspace(0, 10, 5000, endpoint=False)
    u2 = np.ones_like(t2)
    tout2, yout2, xout2 = signal.lsim((b1, a1), u2, t2)
    hp.timeplt1(t2, u2, tout2, yout2, 'échelon avec lsim')

    # Exemple 3 réponse à l'échelon via scipy.signal
    tout3, yout3 = signal.step((b1, a1))
    t3m = np.amax(tout3)
    stept3 = t3m/len(tout3)
    hp.timeplt1(np.arange(0, t3m, stept3), np.ones_like(tout3),
                tout3, yout3, 'échelon avec signal.step')


###############################################################################
def probleme1():
    """
    Framework pour le problème 1 du laboratoire

    :return:
    """
    #Question A
    
    ##FT1
    #Entrez les poles, les zeros et le gain de la FT #1
    z1 = [3]
    p1 = [-3]
    k1 = 1
    num1 = [1, -3]
    denum1 = [1, 3]
    #Ajouter le code pour obtenir la représentation de la fonction de transfert sous forme de polynome. Indice: Regarder la fonction scipy.signal.zpk2tf


    #Ajouter le code pour generer la carte des poles et zeros et le lieu de Bode
    #utiliser les fonctions dans helpers.py
    hp.pzmap1(z1 ,p1 ,"de H1")
    # hp.bodeplot(num1, denum1,"VA CHIER")
    poly1 = signal.zpk2tf(z1, p1, k1) # on obtient le polynome de la fonction de transfert harmonique H(s) sous forme de liste (a l'index 0, on a le num et a l'index 1 le denum)
    w1, mag1, phase1 = signal.bode(poly1) # on obtient la fréquence (rad/s), le gain (dB) et la phase (deg)
    hp.bode1(w1, mag1, phase1,"H1")
    
    ##FT2
    #Entrez les poles, les zeros et le gain de la FT #2
    z2 = [3+5j, 3-5j]
    p2 = [-3+5j, -3-5j]
    k2 = 1
    num2 = [1,-6, 34]
    denum2 = [1, 6, 34]
    
    #Ajouter le code pour obtenir la représentation de la fonction de transfert sous forme de polynome
    hp.pzmap1(z2, p2, "H2")
    # hp.bodeplot(num2, denum2, "VA CHIER2")
    poly2 = signal.zpk2tf(z2, p2, k2)
    w2, mag2, phase2 = signal.bode(poly2)
    hp.bode1(w2, mag2, phase2,"H2")
    
    #Ajouter le code pour generer la carte des poles et zeros et le lieu de Bode
    #utiliser les fonctions dans helpers.py


    tupleND1 = (poly1[0], poly1[1]) # tuple avec num, dénum
    tupleND2 = (poly2[0], poly2[1])
    #Question B
    
    #Analysez bien les lignes suivantes pour comprendre leur fonctionnement
    # définit les entrées pour la simulation temporelle, i.e. quelques sinusoîdes de fréquence différentes
    t = np.linspace(0, 10, 5000)  # 5000 points de 0 à 10s
    w = [0, 1, 4, 15, 50]   # valeurs des fréquences désirées, rad/s
    # génère une constante si w = 0 sinon un sinus
    # np.ones_like génère un tableau de même forme et longeur que t rempli de 1
    # si w[i]==0, on met 1 dans le tableau, sinon on met np.sin(w[i] * t) dans le tableau
    u = [np.ones_like(t) if w[i] == 0 else np.sin(w[i] * t) for i in range(len(w))] # liste

    # exemple réponse temporelle pour plusieurs entrées sinusoidales définies ci-dessus
    # initialise les listes qui vont contenir l'information retournée par lsim
    tout = []
    yout1 = []
    yout2 = []
    # itère sur les fréquences désirées
    for i in range(len(w)):
        #Commentez la ligne ci-dessous et decommentez les lignes commentees de la boucle for en completant les argument des appels a lsim
        temp = [t,u[i]] 
        
        temp = signal.lsim(tupleND1,u[i],t)  # temp = [t, y, x], voir l'aide de lsim
        tout.append(temp[0])
        yout1.append(temp[1])
        
        temp = signal.lsim(tupleND2,u[i],t)  # répète pour l'autre FT
        yout2.append(temp[1])
        
    #Affichage des simulations
    hp.timepltmulti1(t, u, w, tout, yout1, 'H1')
    hp.timepltmulti1(t, u, w, tout, yout2, 'H2')

    #Question C 
    #Comment mettre les filtres en serie/parrallele? Reflechisser a deux approches possibles, l'une utilisant lsim et l'autre utilisant les fonctions paratf et seriestf de la librairie helper
    #Ensuite, vous pouvez utiliser le meme genre de boucle que ci-dessous pour generer les reponses aux differentes frequences

    z3, p3, k3 = hp.paratf(z1, p1, k1, z2, p2, k2)
    z4, p4, k4 = hp.seriestf(z1, p1, k1, z2, p2, k2)
    tupleZPK3 = (z3, p3,k3)
    tupleZPK4 = (z4, p4, k4)
    tout_2 = []
    yout1_2 = []
    yout2_2 = []
    for i in range(len(w)):
        # Commentez la ligne ci-dessous et decommentez les lignes commentees de la boucle for en completant les argument des appels a lsim
        temp_2 = [t, u[i]]

        temp_2 = signal.lsim(tupleZPK3, u[i], t)  # temp = [t, y, x], voir l'aide de lsim
        tout_2.append(temp_2[0])
        yout1_2.append(temp_2[1])

        temp_2 = signal.lsim(tupleZPK4, u[i], t)  # répète pour l'autre FT
        yout2_2.append(temp_2[1])
    hp.timepltmulti1(t, u, w, tout_2, yout1_2, 'H1+H2')
    hp.timepltmulti1(t, u, w, tout_2, yout2_2, 'H1*H2')
    #Question D
    #Inspirez-vous de la question a pour afficher la carte des poles et zeros et le lieu de Bode de ces filtres, afficher aussi le delais de groupe en utilisant hp.grpdel1 en vous inspirant de la fonction exempleButterworth
    # ---------------H1+H2-------------------- #
    hp.pzmap1(z3, p3, "H1+H2")
    # hp.bodeplot(num1, denum1,"VA CHIER")
    poly3 = signal.zpk2tf(z3, p3, k3)
    w3, mag3, phase3 = signal.bode(poly3)
    mag3, ph3, w3, fig1, ax1 = hp.bodeplot(poly3[0], poly3[1],"H1+H2")
    # ---------------H1*H2-------------------- #
    hp.pzmap1(z4, p4, "H1*H2")
    # hp.bodeplot(num2, denum2, "VA CHIER2")
    poly4 = signal.zpk2tf(z4, p4, k4)
    w4, mag4, phase4 = signal.bode(poly4)
    mag4, ph4, w4, fig2, ax2 = hp.bodeplot(poly4[0],poly4[1], "H1*H2")
    # -------------Délais de groupe---------------#
    delay1 = - np.diff(ph3) / np.diff(w3)
    hp.grpdel1(w3, delay1, 'H1+H2')
    delay2 = - np.diff(ph4) / np.diff(w4)
    hp.grpdel1(w4, delay2, 'H1*H2')

###############################################################################
def probleme2():
    """
    Framework pour le problème 2

    :return:
    """
    
    #Question A
    
    #Frequence de coupure des filtres, a ajuster
    wc = 2 * np.pi * 5000      # fréquence de coupure rad/s

    #Generez les filtres butterworth avec la fonction signal.butter, sous quel forme est la sortie (polynome ou pole-zero-gain)?
    #Transformer la sortie de signal.butter dans l'autre representation (vous pouvez vous inspirer de la question A du probleme 1)

    # z1, p1, k1 = signal.butter(2, wc, btype='lowpass', analog=True)
    b1, a1 = signal.butter(2, wc, btype='lowpass', analog=True)
    # z2, p2, k2 = signal.butter(2, wc, btype='highpass', analog=True)
    b2, a2 = signal.butter(2, wc, btype='highpass', analog=True)
    #Affichage des polynomes
    print(f'Passe-bas Numérateur {b1}, Dénominateur {a1}')  # affiche les coefficients correspondants au filtre
    print(f'Passe-haut Numérateur {b2}, Dénominateur {a2}')  # affiche les coefficients correspondants au filtre
    z1, p1, k1 = signal.tf2zpk(b1, a1)
    z2, p2, k2 = signal.tf2zpk(b2, a2)

    #Questions B et C

    #Génère une onde carrée, ajuster la frequence
    fsquare = 1000  # Hz
    t, step = np.linspace(0, .01, 5000, retstep=True)
    u1 = signal.square(2 * np.pi * fsquare * t, 0.5)

    #Gain de chacune des bandes, ajuster au besoin
    # lowk = k1
    # highk = k2
    lowk = 1
    highk = 1

    # w = [0, 1, 4, 15, 50]  # valeurs des fréquences désirées, rad/s
    # génère une constante si w = 0 sinon un sinus

    z3, p3, k3 = hp.paratf(z1, p1, k1*lowk, z2, p2, k2*highk)
    tupleZPK3 = (z3, p3, k3)
    # exemple réponse temporelle pour plusieurs entrées sinusoidales définies ci-dessus
    # initialise les listes qui vont contenir l'information retournée par lsim
    tout, yout1, xout1 = signal.lsim((z1, p1, k1), u1, t)
    tout, yout2, xout2 = signal.lsim((z2, p2, k2), u1, t)
    tout, yout3, xout3 = signal.lsim(tupleZPK3, u1, t)

    hp.timepltmulti2(t, u1,tout,[yout1,yout2,yout3],"Égaliseur lowk = 1, highk = 1",['H1', 'H2', 'HÉgalisateur'])
    # itère sur les fréquences désirées

    #En vous inspirant de la question C du probleme 1, mettre ces deux filtres en parallele, afficher le lieu de bode et le délai de groupe

    #Simuler la sortie de chacun des filtres (passe-haut, passe-bas et les deux en parallele) avec la fonction lsim
    
    
    #Question D
    
    # génère une entrée sinusoïdale à la même fréquence que l'onde carrée
    fsin = fsquare
    u2 = np.sin(2*np.pi*fsin*t)

    # redéfinit les gains de bande
    lowk = 0.1
    highk = 1
    tout, yout4, xout4 = signal.lsim((z1, p1, k1), u2, t)
    yout4 = yout4*lowk
    tout, yout5, xout5 = signal.lsim((z2, p2, k2), u2, t)
    yout5 = yout5 * highk


    z4, p4, k4 = hp.paratf(z1, p1, k1 * lowk, z2, p2, k2 * highk)
    tupleZPK4 = (z4, p4, k4)
    tout, yout6, xout6 = signal.lsim(tupleZPK4, u2, t)
    hp.timepltmulti2(t, u2, tout, [yout4, yout5, yout6], "Égaliseur lowk = 0.1, high = 1", ['H1', 'H2', 'HÉgalisateur'])

    #Simuler la sortie de chacun des filtres (passe-haut, passe-bas et les deux en parallele) avec la fonction lsim et l'entre u2
    
    #Question E
    #Inspirer vous du probleme 1 pour afficher le lieu de bode et le delais de groupe des filtres conçus
    # hp.bodeplot(num1, denum1,"VA CHIER")
    poly4 = signal.zpk2tf(z3, p3, k3)
    w3, mag3, phase3 = signal.bode(poly4)
    mag4, ph4, w4, fig, ax = hp.bodeplot(poly4[0], poly4[1], "lowk = 1, highk=1")
    delay = - np.diff(ph4) / np.diff(w4)
    hp.grpdel1(w4, delay, "lowk = 1, highk=1")
    
###############################################################################
def main():
    # décommentez la ou les lignes correspondant aux fonctions que vous voulez exécuter
    # exampleRacines()
    # exampleBode()
    # exampleButterworth()
    probleme1()
    probleme2()
    plt.show()


#####################################
# Manière standardisée d'exécuter ce que vous désirez lorsque vous "exécutez" le fichier
# permet d'importer les fonctions définies ici comme un module dans un autre fichier .py
# voir par exemple le fichier helper.py qui n'exécutera jamais rien tout seul
# et dont les fonctions sont importées ici à titre de support pour ce qu'on essaie de faire
# pour l'instant ne rien modifier ci-dessous
if __name__ == '__main__':
    main()
