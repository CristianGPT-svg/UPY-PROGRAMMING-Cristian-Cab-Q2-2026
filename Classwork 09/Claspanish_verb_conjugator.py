# INPUT
verb = input("Ingrese verbo: ")

# PROCESS
pronouns = ['yo', 'tu', 'el', 'nosotros', 'vosotros', 'ellos']

endings = {
    'ar': ['o', 'as', 'a', 'amos', 'ais', 'an'],
    'er': ['o', 'es', 'e', 'emos', 'eis', 'en'],
    'ir': ['o', 'es', 'e', 'imos', 'is', 'en']
}

stem = verb[:-2]
verb_ending = verb[-2:]
conjugations = endings[verb_ending]

# OUTPUT
for i in range(len(pronouns)):
    print(pronouns[i] + " " + stem + conjugations[i])
