calculate(add, A, B, R) :- R is A + B.
calculate(sub, A, B, R) :- R is A - B.
calculate(mul, A, B, R) :- R is A * B.
calculate(div, A, B, R) :-
    (B =\= 0 ->
        R is A / B ;
        write('Error: Division by zero!'), fail % 'fail' stops the rule and avoids printing a result
    ).
calculate(mod, A, B, R) :-
    (B =\= 0 ->
        R is A mod B ;
        write('Error: Division by zero!'), fail
    ).

menu :-
    nl, write('--- Calculator Menu ---'), nl,
    write('1. Add'), nl,
    write('2. Subtract'), nl,
    write('3. Multiply'), nl,
    write('4. Divide'), nl,
    write('5. Modulus'), nl,
    write('6. Exit'), nl,
    write('Enter Choice: '), read(Choice),
    (Choice == 6 -> write('Exiting...') ; (process(Choice), menu)).

getVal(A, B) :-
    write('Enter 1st number: '), read(A),
    write('Enter 2nd number: '), read(B).

% execute/process with check for successful calculation
process(1) :- getVal(A, B), calculate(add, A, B, R), nl, write('Res = '), write(R).
process(2) :- getVal(A, B), calculate(sub, A, B, R), nl, write('Res = '), write(R).
process(3) :- getVal(A, B), calculate(mul, A, B, R), nl, write('Res = '), write(R).
process(4) :- getVal(A, B), (calculate(div, A, B, R) -> (nl, write('Res = '), write(R)) ; true).
process(5) :- getVal(A, B), (calculate(mod, A, B, R) -> (nl, write('Res = '), write(R)) ; true).
process(_) :- nl, write('Error: Invalid Input! Please enter a number from 1-6.').