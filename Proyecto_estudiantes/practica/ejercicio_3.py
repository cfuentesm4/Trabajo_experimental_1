inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)

print(sorted(ambas))
print(sorted(solo_mate))
print(total)