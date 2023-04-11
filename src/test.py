from algorithm.algorithm import getMinimumSpanningTree, expandMST
test = [
    [0,10,0,30,100],
    [10,0,50,0,0],
    [0,50,0,20,10],
    [30,0,20,0,60],
    [100,0,10,60,0]
]

hasil = getMinimumSpanningTree(test)
print(hasil)
hasil = expandMST(hasil)
print(hasil)