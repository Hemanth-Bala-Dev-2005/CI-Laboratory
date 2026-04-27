male(gangadhar). male(motilal). male(jawaharlal). male(feroze).
male(rajiv). male(sanjay). male(rahul). male(varun).

female(indrani). female(swarup_rani). female(kamala). female(indira).
female(sonia). female(maneka). female(priyanka). female(vijaya_lakshmi).

parent(gangadhar, motilal). parent(indrani, motilal).
parent(motilal, jawaharlal). parent(swarup_rani, jawaharlal).
parent(motilal, vijaya_lakshmi). parent(swarup_rani, vijaya_lakshmi).
parent(jawaharlal, indira). parent(kamala, indira).
parent(feroze, rajiv). parent(indira, rajiv).
parent(feroze, sanjay). parent(indira, sanjay).
parent(rajiv, rahul). parent(sonia, rahul).
parent(rajiv, priyanka). parent(sonia, priyanka).
parent(sanjay, varun). parent(maneka, varun).

married(gangadhar, indrani).
married(motilal, swarup_rani).
married(jawaharlal, kamala).
married(feroze, indira).
married(rajiv, sonia).
married(sanjay, maneka).

father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).

spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).
wife(X, Y) :- female(X), spouse(X, Y).
husband(X, Y) :- male(X), spouse(X, Y).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
brother(X, Y) :- male(X), sibling(X, Y).
sister(X, Y) :- female(X), sibling(X, Y).

son(X, Y) :- male(X), parent(Y, X).
daughter(X, Y) :- female(X), parent(Y, X).

grandpa(X, Y) :- male(X), parent(X, Z), parent(Z, Y).
grandma(X, Y) :- female(X), parent(X, Z), parent(Z, Y).

uncle(X, Y) :- male(X), sibling(X, Z), parent(Z, Y).
uncle(X, Y) :- male(X), spouse(X, Z), sibling(Z, P), parent(P, Y).

aunt(X, Y) :- female(X), sibling(X, Z), parent(Z, Y).
aunt(X, Y) :- female(X), spouse(X, Z), sibling(Z, P), parent(P, Y).

nephew(X, Y) :- male(X), (sibling(Y, Z) ; (spouse(Y, S), sibling(S, Z))), parent(Z, X).
niece(X, Y) :- female(X), (sibling(Y, Z) ; (spouse(Y, S), sibling(S, Z))), parent(Z, X).

cousin(X, Y) :- parent(P1, X), parent(P2, Y), sibling(P1, P2).



get_relationship(X, Y, father) :- father(X, Y).
get_relationship(X, Y, mother) :- mother(X, Y).
get_relationship(X, Y, son) :- son(X, Y).
get_relationship(X, Y, daughter) :- daughter(X, Y).
get_relationship(X, Y, brother) :- brother(X, Y).
get_relationship(X, Y, sister) :- sister(X, Y).
get_relationship(X, Y, husband) :- husband(X, Y).
get_relationship(X, Y, wife) :- wife(X, Y).
get_relationship(X, Y, grandfather) :- grandpa(X, Y).
get_relationship(X, Y, grandmother) :- grandma(X, Y).
get_relationship(X, Y, grandson) :- male(X), parent(Z, X), parent(Y, Z).
get_relationship(X, Y, granddaughter) :- female(X), parent(Z, X), parent(Y, Z).
get_relationship(X, Y, uncle) :- uncle(X, Y).
get_relationship(X, Y, aunt) :- aunt(X, Y).
get_relationship(X, Y, nephew) :- nephew(X, Y).
get_relationship(X, Y, niece) :- niece(X, Y).
get_relationship(X, Y, cousin) :- cousin(X, Y).


relation(X, Y, R) :- get_relationship(X, Y, R), !.
relation(_, _, 'no relation found').