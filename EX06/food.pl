food(apples).
food(chickens).
alive(ajay).
eats(ajay, peanuts).

killed(X) :- \+ alive(X).

food(X) :- eats(Y, X), \+ killed(Y).

likes(ravi, X) :- food(X).

eats(rita, X) :- eats(ajay, X).