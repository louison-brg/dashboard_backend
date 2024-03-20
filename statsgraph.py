weeks = []
for week in range(0, 53):
    weeks.append(week)

#print(amountSubs)

d = "M 2.5490196078431 48.4375 L 7.4509803921569 48.4375 L 12.352941176471 48.4375 L 17.254901960784 46.875 L 22.156862745098 48.4375 L 27.058823529412 48.4375 L 31.960784313725 46.875 L 36.862745098039 43.75 L 41.764705882353 40.625 L 46.666666666667 32.8125 L 51.56862745098 40.625 L 56.470588235294 43.75 L 61.372549019608 43.75 L 66.274509803922 42.1875 L 71.176470588235 43.75 L 76.078431372549 40.625 L 80.980392156863 32.8125 L 85.882352941176 37.5 L 90.78431372549 37.5 L 95.686274509804 43.75 L 100.58823529412 34.375 L 105.49019607843 34.375 L 110.39215686275 34.375 L 115.29411764706 50 L 120.19607843137 34.375 L 125.09803921569 18.75 L 130 18.75 L 134.90196078431 3.125 L 139.80392156863 18.75 L 144.70588235294 18.75 L 149.60784313725 34.375 L 154.50980392157 34.375 L 159.41176470588 18.75 L 164.3429038282 34.375 L 169.24486461251 18.75 L 174.14682539683 18.75 L 179.04878618114 3.125 L 183.95074696545 18.75 L 188.85270774977 3.125 L 193.75466853408 18.75 L 198.65662931839 18.75 L 203.55859010271 3.125 L 208.46055088702 3.125 L 213.36251167134 34.375 L 218.26447245565 18.75 L 223.16643323996 3.125 L 228.06839402428 18.75 L 232.97035480859 18.75 L 237.8723155929 18.75 L 242.77427637722 18.75 L 247.67623716153 34.375 L 252.54901960784 18.75 L 257.45098039216 3.125"
d = d.split(' ')
d.pop(0)
amountSubs = []
for elem in d:
    if elem != "L":
        amountSubs.append(float(elem))

for i in range(len(amountSubs) - 1, -1, -1):
    if i % 2 == 0:
        amountSubs.pop(i)

#print(coordinates)

hachage= {}
for i in range(0, 33):
    hachage[50 - i * 1.5625] = 0 + 10000 * i

#print(subs_dict)

for i in range(len(amountSubs)):
    amountSubs[i] = hachage[amountSubs[i]]

print("Liste d'abonnés après remplacement par les valeurs du dictionnaire 'subs_dict':", amountSubs)


import matplotlib.pyplot as plt
# Tracer le graphique
plt.plot(weeks, amountSubs, marker='o', linestyle='-')

# Ajouter des étiquettes aux axes et un titre
plt.xlabel('Semaines')
plt.ylabel('Abonnés')
plt.title("Évolution du nombre d'abonnés du créateur")

# Afficher le graphique
plt.grid(True)
plt.show()

#<g class="highcharts-label highcharts-tooltip highcharts-color-undefined" data-z-index="8" filter="url(#highcharts-drop-shadow-undefined)" transform="translate(16,16)" style="cursor: default; pointer-events: none;" opacity="1"><path fill="#ffffff" class="highcharts-label-box highcharts-tooltip-box" d="M 3 0 L 164 0 A 3 3 0 0 1 167 3 L 167 34 A 3 3 0 0 1 164 37 L 89 37 L 83 43 L 77 37 L 3 37 A 3 3 0 0 1 0 34 L 0 3 A 3 3 0 0 1 3 0 Z" stroke-width="0" stroke="#c84329"></path><text x="8" data-z-index="1" y="15" style="color: rgb(51, 51, 51); font-size: 0.8em; fill: rgb(51, 51, 51);"><tspan style="font-size: 5pt;">Oct  4, 2023 - Oct 10, 2023</tspan><tspan class="highcharts-br" dy="12" x="8">​</tspan><tspan style="color: rgb(204, 35, 35); fill: rgb(204, 35, 35);">●</tspan> MrBeast: <tspan style="font-weight: bold;">7,000,000 Subscribers</tspan></text></g>