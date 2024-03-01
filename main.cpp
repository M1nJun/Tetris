CUT-STRING(L, i, j, l, r)
    if l == r
        return (0, [])
    minCost = ∞
    for k = i to j
        if l + r + CUT-STRING(L, i, k, l, L[k]).cost + CUT-STRING(L, k, j, L[k], j).cost < minCost
            minCost = r - l + CUT-STRING(L, i, k, l, L[k]).cost + CUT-STRING(L, k + 1, j, L[k], j).cost
            minSeq = L[k] + CUT-STRING(L, i, k, l, L[k]) + CUT-STRING(L, i, k + 1, l, L[k])
    return (minCost, minSeq)