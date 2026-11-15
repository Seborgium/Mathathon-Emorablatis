from delta import all_flat_bases
fb = all_flat_bases()
for k in ['m0','m1']:
    E,L = fb[k]
    print(k, "column support L =", L)
    for row in E:
        print("   ", row)
