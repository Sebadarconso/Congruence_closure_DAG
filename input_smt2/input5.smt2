(set-info :smt-lib-version 2.6)
(set-logic QF_UF)
(set-info :source |Benchmarks from the paper: "Extending Sledgehammer with SMT Solvers" by Jasmin Blanchette, Sascha Bohme, and Lawrence C. Paulson, CADE 2011.  Translated to SMT2 by Andrew Reynolds and Morgan Deters.|)
(set-info :category "industrial")
(set-info :status unsat)
(declare-sort S1 0)
(declare-sort S2 0)
(declare-sort S3 0)
(declare-sort S4 0)
(declare-sort S5 0)
(declare-sort S6 0)
(declare-sort S7 0)
(declare-fun f1 () S1)
(declare-fun f2 () S1)
(declare-fun f3 (S2 S3 S4 S5 S6) S1)
(declare-fun f4 () S2)
(declare-fun f5 () S3)
(declare-fun f6 () S4)
(declare-fun f7 () S5)
(declare-fun f8 (S7) S6)
(declare-fun f9 () S7)
(declare-fun f10 () S6)
(assert (and (not (= f1 f2)) (not (= (f3 f4 f5 f6 f7 (f8 f9)) f1)) (= (f3 f4 f5 f6 f7 f10) f1) (= f10 (f8 f9)) (= (f3 f4 f5 f6 f7 f10) f1)))
(check-sat)
(exit)