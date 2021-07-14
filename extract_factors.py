import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from textwrap import wrap
import matplotlib as mpl
from cycler import cycler

raw_df = pd.read_csv("mentalisLeltar\\Csocsó-mentális-leltár-válaszok.csv", sep=";", index_col=1)
if raw_df.shape[1] != 32:
    raise Exception("Number of columns isn't 32, please check input file")

wants_feedback = raw_df[pd.notnull(raw_df.index)]
jeligek = list(wants_feedback.index)
jeligek = [re.sub(r"\W", r"_", jelige) for jelige in jeligek]

wants_feedback_answers = wants_feedback.iloc[:,[1,2,3,4,5,6,7,8,9,12,13,14,15,16,19,20,21,22,23,24]]
if wants_feedback_answers.shape[1] != 20:
    raise Exception("NUmber of columns isn't 20, something went wrong")

wants_feedback_answers.to_csv("wants_feedback_answers.csv", sep=";", header=False, index=False)

with open("wants_feedback_answers.csv", encoding="utf-8") as f:
    feedback = ""
    for line in f:
        feedback_line = ""
        line_split = re.split(r";", line.strip("\n"))
        for answer in line_split:
            if re.match(r"\d", answer):
                answer = re.sub(r"(\d)\..+", r"\1", answer)
            else:
                answer = re.sub(r".+", r"np.nan", answer)
            feedback_line += answer + ";"
        
        feedback += feedback_line[:-1] + "\n"

with open("feedback_data.csv", "w", encoding="utf-8") as f:
    f.write(feedback)

feedback_data = np.genfromtxt("feedback_data.csv", delimiter=";")

x = ["Előkészületek", "Kontroll", "Koncentráció", "Csapatmunka", "Alkalmazkodás", "Meccsek kiértékelése"]
y = np.empty(6)
y_mu = np.empty(6)
faktorok = [[0,1,16], [2,3,4,8,9,10,11,12], [3,5,6,7,10], [14,15], [1,12,13,15,17], [17,18,19]]

plt.style.use("dark_background")
fig = plt.figure(dpi=300)
ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.75])
ax1.set_axis_off()
ax1_text = "Előkészületek: használod-e a  meccs előtti rutinjaid, tudatosan zónába tudsz-e kerülni  meccsek előtt\n\nKontroll: szabályozod-e a meccs előtt/közben felmerülő érzelmeket , pozitív gondolatokat erősíted-e\n\nKoncentráció: ki tudod-e zárni a tőled független akár belső akár külső zavaró tényezőket\n\nCsapatmunka: csapatösszhang fenttartására törekszel-e/ kommunikálsz a csapattársaddal játék közben\n\nAlkalmazkodás: ellenfél gyengeségeit felismered, ez alapján építed és alkalmazod a stratégiád\n\nMeccsek kiértékelése: figyelsz-e a meccsek utólagos elemzésére,  pozitív elemek és fejlesztendő területek összgyűjtésére"
ax1_list = ax1_text.split(sep="\n\n")
ax1_list = ["\n".join(wrap(ax1_line, 35)) for ax1_line in ax1_list]
ax1_text = "\n\n\n".join(ax1_list)
ax1.text(x=0, y=1, s="SKILLEK", size="medium", ha="left", va="bottom")
ax1.text(x=0, y=0.95, s=ax1_text, size="x-small", ha="left", va="top")

ax2 = fig.add_axes([0.4, 0.3, 0.55, 0.5])

for faktor in range(6):
    y_mu[faktor] = np.nanmean(feedback_data[:,faktorok[faktor]])


for ember in range(len(jeligek)):
    for faktor in range(6):
        y[faktor] = np.nanmean(feedback_data[ember,faktorok[faktor]])
    
    rects = ax2.bar(x, y)
    ax2.bar_label(rects, labels=np.round(y,1), label_type="edge")
    fig.suptitle(t=re.sub(r"_", r" ", jeligek[ember].strip("_").upper()), x=0.05, y=0.95, ha="left", va="top", size="large")
    ax2.set_ylim(1, 5, 1)
    ax2.set_yticks([1.0, 2.0, 3.0, 4.0, 5.0], minor=False)
    ax2.set_title("Eredmények\n", style="italic", color="paleturquoise", va="bottom")
    ax2.set_frame_on(False)
    ax2.grid(b=True, axis="y", linewidth=1, alpha=0.25)
    ax2.tick_params(length=0)
    ax2.tick_params(axis="x", labelsize="small", rotation=50)
    ax2.text(x=2.5, y=-1.2, s="1=nem kell fejleszteni    5=biztos fejlesztésre szorul", size="small", ha="center")
    ax2.bar(x, y_mu, alpha=0.35, color="grey")

    plt.savefig("mentalisLeltar\\diagramok\\" + jeligek[ember].strip("_") + ".png")
    
    ax2.clear()


plt.clf()
plt.close()