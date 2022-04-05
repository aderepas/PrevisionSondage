import matplotlib.pyplot as plt
from scipy import stats

# Nom des candidats
candidats_name = ["N.Arthaud","P.Poutou","F.Roussel","J.Mélenchon","A.Hidalgo","Y.Jadot","E.Macron","V.Pécresse","J.Lasalle","N.Dupont-Aignan","M.LePen","E.Zemmour"]
# Colors for each candidates
colors = ["darkred","firebrick","red","crimson","pink","lawngreen","gold","deepskyblue","cyan","royalblue","darkblue","dimgray"]

candidats = []
minidate = 999
filename = "data.txt"
with open(filename,'r') as f:
    line = " "
    while line != "":
        line = f.readline().replace("%","")
        lst = line.split("\t")
        if len(lst) == 15:
            date = lst[1].split("-")
            if date[0].isdigit():
                date = (int(date[0])+int(date[1].split(" ")[0]) +  (62 if date[1].split(" ")[1] == "avril" else 0))/2

            else:
                date = (int(date[0].split(" ")[0])+31+int( "".join(filter(str.isdigit,date[1].split(" ")[1]))))/2 
            minidate = min(minidate,date)
            pourcentage = [*map(lambda x: x.replace(",","."),lst[-12:])]
            candidats += [[date,[*map(float,pourcentage)]]]


for i in range(len(candidats)):
    candidats[i][0] = candidats[i][0] - minidate

rep = " "
while rep not in 'GC':
    rep = input("Voulez vous voir une avancée globale/L'avancée pour chaque candidats ?[G/C]\n>>>").upper()

y = [candidats[j][0]for j in range(len(candidats))]
somme_days = sum(y)/len(y) # Average of the days


resultat_sondage = []
if rep == "G": # Général
    for i in range(12):
        y = [candidats[j][1][i] for j in range(len(candidats))]
        x = [candidats[j][0]for j in range(len(candidats))]

        slope, intercept, _, _, _ = stats.linregress(x,y)

        def regression(x):
            return slope * x + intercept

        resultat_sondage += [sum(y) / len(y) + slope * (14 - somme_days)]
        mapped = [*map(regression,x)]

        # Graph
        plt.plot(x, mapped, color = colors[i], label = candidats_name[i])
        plt.scatter(x, y, marker = 'o', color = colors[i])
        plt.legend()
    plt.grid(linewidth = 0.2)
    plt.show()
else: # Foreach Candidates
    for i in range(12):
        y = [candidats[j][1][i] for j in range(len(candidats))]
        x = [candidats[j][0]for j in range(len(candidats))]

        slope, intercept, _, _, _ = stats.linregress(x,y)

        def regression(x):
            return slope*x + intercept
        
        resultat_sondage += [sum(y) / len(y) + slope * (14 - somme_days)]
        mapped = [ *map(regression , x) ]

        # Graph
        plt.plot(x, mapped,color = "gray")
        plt.title(candidats_name[i])
        plt.scatter(x, y, marker = 'o', color = colors[i])
        plt.grid(linewidth = 0.2)
        plt.show()


def normalize(a): # For real polls
    somme = sum(resultat_sondage)
    return a/(somme/100)

resultat_sondage = [ *map(normalize , resultat_sondage) ]

for i in range(12):
    print(f"\n{candidats_name[i]}:\nScore présumé: {round(resultat_sondage[i],2)}%")
