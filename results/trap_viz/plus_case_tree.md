# Plus-sign case tree (n=6)

## Head (2,2), first edge right — 180 plus-sign paths realize the root
LEFT: far end 12 -> 6UP: far end 2 -> 1DOWN: far end 26 -> 32 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 6UP: far end 2 -> 1DOWN: far end 26 -> 25 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 6UP: far end 2 -> 1DOWN: far end 26 -> 27 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 32 -> FEASIBLE (15 paths)
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 32    arm outcomes ('+1', '2cycle', '2cycle'): 6
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 32    arm outcomes ('+1', '2cycle', 'plateau-cont'): 7
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 32    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 2
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 32    !! 5 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25 -> FEASIBLE (73 paths)
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    arm outcomes ('+1', '+1', '2cycle'): 16
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    arm outcomes ('+1', '+1', 'plateau-cont'): 8
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    arm outcomes ('+1', '2cycle', '2cycle'): 12
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    arm outcomes ('+1', '2cycle', 'plateau-cont'): 24
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 13
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 25    !! 22 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 12 -> 6UP: far end 2 -> 3DOWN: far end 26 -> 27 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 32 -> FEASIBLE (36 paths)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 32    arm outcomes ('+1', '+1', '2cycle'): 14
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 32    arm outcomes ('+1', '2cycle', '2cycle'): 6
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 32    arm outcomes ('+1', '2cycle', 'plateau-cont'): 16
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 32    !! 5 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 25 -> FEASIBLE (20 paths)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 25    arm outcomes ('+1', '+1', '2cycle'): 6
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 25    arm outcomes ('+1', '2cycle', '2cycle'): 11
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 25    arm outcomes ('+1', '2cycle', 'plateau-cont'): 3
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 25    !! 4 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 27 -> FEASIBLE (36 paths)
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 27    arm outcomes ('+1', '+1', '2cycle'): 12
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 27    arm outcomes ('+1', '2cycle', '2cycle'): 7
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 27    arm outcomes ('+1', '2cycle', 'plateau-cont'): 17
LEFT: far end 12 -> 18UP: far end 2 -> 1DOWN: far end 26 -> 27    !! 7 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 12 -> 18UP: far end 2 -> 3DOWN: far end 26 -> 32 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 18UP: far end 2 -> 3DOWN: far end 26 -> 25 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 12 -> 18UP: far end 2 -> 3DOWN: far end 26 -> 27 -> INFEASIBLE (no Hamiltonian path)
## Head (2,3), first edge right — 430 plus-sign paths realize the root
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33 -> FEASIBLE (51 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', '+1'): 3
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', '2cycle'): 2
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', 'plateau-cont'): 16
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '2cycle', 'plateau-cont'): 17
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 13
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 33    !! 4 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26 -> FEASIBLE (36 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', '+1'): 2
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', 'plateau-cont'): 4
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '2cycle', '2cycle'): 4
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '2cycle', 'plateau-cont'): 23
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 3
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 26    !! 2 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28 -> FEASIBLE (61 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', '+1'): 5
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', 'plateau-cont'): 20
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '2cycle', '2cycle'): 5
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '2cycle', 'plateau-cont'): 16
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 15
LEFT: far end 13 -> 7UP: far end 3 -> 2DOWN: far end 27 -> 28    !! 7 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 33 -> FEASIBLE (12 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', 'plateau-cont'): 2
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 33    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 10
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 26 -> FEASIBLE (18 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', 'plateau-cont'): 2
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 26    arm outcomes ('+1', '2cycle', 'plateau-cont'): 5
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 26    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 11
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 28 -> FEASIBLE (9 paths)
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 28    arm outcomes ('+1', '2cycle', 'plateau-cont'): 9
LEFT: far end 13 -> 7UP: far end 3 -> 4DOWN: far end 27 -> 28    !! 1 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 33 -> FEASIBLE (27 paths)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', '+1'): 1
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', 'plateau-cont'): 14
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 12
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 33    !! 4 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 26 -> FEASIBLE (18 paths)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', '+1'): 2
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', 'plateau-cont'): 2
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 14
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 26    !! 8 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28 -> FEASIBLE (38 paths)
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', '+1'): 3
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', 'plateau-cont'): 12
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '2cycle', 'plateau-cont'): 2
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 21
LEFT: far end 13 -> 19UP: far end 3 -> 2DOWN: far end 27 -> 28    !! 8 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 19UP: far end 3 -> 4DOWN: far end 27 -> 33 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 13 -> 19UP: far end 3 -> 4DOWN: far end 27 -> 26 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 13 -> 19UP: far end 3 -> 4DOWN: far end 27 -> 28 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33 -> FEASIBLE (54 paths)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', '2cycle'): 2
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '+1', 'plateau-cont'): 16
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', '2cycle', 'plateau-cont'): 13
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 19
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('2cycle', 'plateau-cont', 'plateau-cont'): 2
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    arm outcomes ('plateau-cont', 'plateau-cont', 'plateau-cont'): 2
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 33    !! 7 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26 -> FEASIBLE (27 paths)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', '+1'): 1
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', '2cycle'): 1
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '+1', 'plateau-cont'): 2
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', '2cycle', 'plateau-cont'): 15
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 1
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    arm outcomes ('plateau-cont', 'plateau-cont', 'plateau-cont'): 7
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 26    !! 6 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28 -> FEASIBLE (79 paths)
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', '+1'): 2
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', '2cycle'): 4
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '+1', 'plateau-cont'): 20
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', '2cycle', 'plateau-cont'): 15
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('+1', 'plateau-cont', 'plateau-cont'): 22
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('2cycle', 'plateau-cont', 'plateau-cont'): 6
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    arm outcomes ('plateau-cont', 'plateau-cont', 'plateau-cont'): 10
LEFT: far end 13 -> 12UP: far end 3 -> 2DOWN: far end 27 -> 28    !! 17 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 13 -> 12UP: far end 3 -> 4DOWN: far end 27 -> 33 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 13 -> 12UP: far end 3 -> 4DOWN: far end 27 -> 26 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 13 -> 12UP: far end 3 -> 4DOWN: far end 27 -> 28 -> INFEASIBLE (no Hamiltonian path)
## Head (2,4), first edge right — 112 plus-sign paths realize the root
LEFT: far end 14 -> 8UP: far end 4 -> 3DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 8UP: far end 4 -> 3DOWN: far end 28 -> 27 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 8UP: far end 4 -> 3DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 27 -> FEASIBLE (70 paths)
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', '+1'): 50
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', '2cycle'): 16
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', 'plateau-cont'): 4
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 27    !! 15 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 14 -> 8UP: far end 4 -> 5DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 20UP: far end 4 -> 3DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 20UP: far end 4 -> 3DOWN: far end 28 -> 27 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 20UP: far end 4 -> 3DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 27 -> FEASIBLE (6 paths)
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', '+1'): 4
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', '2cycle'): 2
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 27    !! 2 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 14 -> 20UP: far end 4 -> 5DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 13UP: far end 4 -> 3DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 13UP: far end 4 -> 3DOWN: far end 28 -> 27 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 13UP: far end 4 -> 3DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 34 -> INFEASIBLE (no Hamiltonian path)
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 27 -> FEASIBLE (36 paths)
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', '2cycle'): 22
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '+1', 'plateau-cont'): 8
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 27    arm outcomes ('+1', '2cycle', '2cycle'): 6
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 27    !! 9 paths have NO +1 move anywhere (trap candidate)
LEFT: far end 14 -> 13UP: far end 4 -> 5DOWN: far end 28 -> 29 -> INFEASIBLE (no Hamiltonian path)