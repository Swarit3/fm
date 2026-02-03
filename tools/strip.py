import sys,os

lfl = open(sys.argv[1]).read().split('\n')
out = []
wrt = ''

for ln in lfl:
    oln = ''
    for w in ln:
        if w == '#':
            break
        oln += w
    out.append(oln)

for ln in out:
    if ln != '':
        wrt += ln + '\n'

if os.path.exists(sys.argv[2]):
    print("Refusing to overwrite. Can be risky, y'know.")
else:
    open(sys.argv[2], "w").write(wrt)
    print("Success")
