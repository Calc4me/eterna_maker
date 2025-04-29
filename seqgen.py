import random
seq = []
for i in range(random.randint(100,500)):
    seq.append(random.choice(["A", "U", "G", "C"]))
print("".join(seq))