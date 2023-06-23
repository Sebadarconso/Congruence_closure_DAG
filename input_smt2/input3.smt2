; custom formula, directly translated from one found on the Bradley-Manna textbook
(set-info :status sat)
(declare-sort A 0)                      
(declare-fun f (A) A)                  
(declare-const a A)                   
(assert (and (not (= (f a) a))        
             (= (f (f (f (f (f a))))) a)))
(check-sat)
(exit)