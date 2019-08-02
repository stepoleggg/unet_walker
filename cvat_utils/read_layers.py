with open("layers.txt", "r") as f:
    arr = (f.read()).split("\n")

d = {}
for i,v in enumerate(arr):
    d.update({v:len(arr)-1-i})