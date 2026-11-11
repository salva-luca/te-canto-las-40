# Medallero de la votación (23 votos, cerrada el 11/11/2026). Conteo en votos/votacion.csv.
# Los empates por el 2º puesto (show, dúo o grupo, coreografía) los definió Salva.
# (categoria, [(nombre, detalle) para oro, plata, bronce])
VOTANTES = 23
MEDALLERO = [
("Mejor cantante", [
    ("Ale", "Freddie Mercury"),
    ("Maru", "Madonna"),
    ("Agus", ""),
]),
("Mejor show", [
    ("Sweet Dreams", "Crista"),
    ("Fuego de noche", "Nati, Ale, Salva y Martín"),
    ("Total Eclipse of the Heart", "Full band"),
]),
("Mejor personificación", [
    ("Crista", "Annie Lennox"),
    ("Ale", "Freddie Mercury"),
    ("Maru", "Madonna"),
]),
("Mejor dúo o grupo", [
    ("Bachata rosa", "Maru y Salva"),
    ("Fuego de noche", "Nati, Ale, Salva y Martín"),
    ("Like a Prayer", "Maru y Agus"),
]),
("Mejor coreografía", [
    ("Like a Prayer", "Maru y Agus"),
    ("You Shook Me All Night Long", "Ale y Salva"),
    ("Sweet Dreams", "Crista"),
]),
]

# Las figuras de la noche: suma de votos de cada persona en todas las categorías,
# pesando más los votos propios que los compartidos. (nombre, look, texto)
FIGURAS = [
("Maru", "Madonna", "La cumpleañera arrasó: fue la más votada de la noche, se llevó dos oros y es la que más temas cantó. Reina de su propia fiesta."),
("Ale", "Freddie Mercury", "Mejor cantante y con medalla en las cinco categorías. Nadie fue tan constante como su Freddie."),
("Crista", "Annie Lennox", "Imbatible en solitario: con Sweet Dreams ganó Mejor show y con su Annie Lennox, Mejor personificación."),
]
