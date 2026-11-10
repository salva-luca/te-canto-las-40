# Registro de la noche del karaoke (09/11/2026), tal como lo anotó Salva, con los títulos prolijos.
# (tema, quienes). "Full band" = cantó todo el mundo; no suma en el ranking individual.
FULL = "Full band"
NOCHE = [
("Like a Prayer", ["Maru", "Agus"]),
("Crazy Little Thing Called Love", ["Ale"]),
("Un amor (Lali)", ["Felipe"]),
("Porque yo te amo (Sandro)", ["Agus"]),
("Todo sigue igual", ["Martín", "Sofi"], "Los dos pitis"),
("Sweet Dreams", ["Crista"]),
("Hay que venir al sur", ["Maca"]),
("You Shook Me All Night Long", ["Ale", "Salva"]),
("Maldita noche", ["Agus"]),
("Bachata rosa", ["Maru", "Salva"]),
("Lo mejor del amor", ["Agus", "Martín"]),
("Dejaría todo", ["Ale", "Salva"]),
("Just a Girl", ["Crista", "Lu"]),
("No podrás", ["Crista", "Salva", "Agus"]),
("Por qué te vas", ["Ayma", "Guille", "Julie", "Simona"]),
("No te creas tan importante", ["Maru", "Nati", "Mili"]),
("Crazy in Love", ["Maca", "Crista"]),
("Imán", ["Maru", "Sofi"]),
("Tiny Dancer", ["Iara", "Javi", "Fede Max"]),
("Fuiste", ["Salva", "Lu", "Maca"]),
("Satisfaction", ["Iara", "Ale", "Fede Max"]),
("Toxic", ["Maca", "Crista", "Lu"]),
("Fuego de noche", ["Nati", "Ale", "Salva", "Martín"]),
("Isla", ["Ayerbe", "Sofi"]),
("Gangsta's Paradise", ["Lu", "Maru", "Javi"]),
("Kiss from a Rose", ["Maru", "Lu", "Javi"]),
("Al siguiente nivel", ["Maca", "Santi", "Sofi"]),
("Dos días en la vida", [FULL]),
("Por amarte así", ["Ale", "Nati", "Salva"]),
("Estoy aquí", ["Maru", "Crista", "Nati"]),
("Piel morena", ["Maca", "Crista"]),
("Total Eclipse of the Heart", [FULL]),
("La incondicional", [FULL]),
("Amor (Cristian Castro)", [FULL]),
("Obsesionario en la mayor", ["Gigi", "Pato", "Manu", "Martín"]),
("Ain't Over 'til It's Over", ["Iara", "Maru"]),
("Sin disfraz", ["Lu", "Salva", "Maru"]),
("Pronta entrega", ["Agus", "Martín"]),
("It Must Have Been Love", [FULL]),
("Una calle nos separa", ["Agus", "Martín", "Nati"]),
("Canción de despedida", [FULL]),
]
NO_PERSONAS = {FULL}  # aparece en el registro pero no es una persona del ranking


def quienes(fila):
    nombres = fila[1]
    if len(fila) > 2:
        return f"{fila[2]} (" + " y ".join(nombres) + ")"
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " y " + nombres[-1]


def ranking():
    cuenta = {}
    for fila in NOCHE:
        for n in fila[1]:
            if n not in NO_PERSONAS:
                cuenta[n] = cuenta.get(n, 0) + 1
    return sorted(cuenta.items(), key=lambda x: (-x[1], x[0]))


def personas():
    return sorted({n for f in NOCHE for n in f[1] if n not in NO_PERSONAS})


if __name__ == "__main__":
    for n, c in ranking():
        print(c, n)
    print(len(NOCHE), "temas,", sum(1 for f in NOCHE if f[1] == [FULL]), "full band,", len(personas()), "personas")
