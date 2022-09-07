

with open("groupsList.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
for line in lines:
    line = line.strip()
    if line == "" or line.startswith("#"):
        continue
    groups = line.split(",")
    group_name = groups[0]

    print(line)
