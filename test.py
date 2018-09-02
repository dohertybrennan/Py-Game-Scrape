word = "$2.99 to $39.99"
word = word[:5]
word = word.replace("$", "")
word = float(word)
print(type(word))
print(word)