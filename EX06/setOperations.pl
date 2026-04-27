member(Element, [Element|_]).
    member(Element, [_|Tail]) :- member(Element, Tail).

    subset([], _).
    subset([Head|Tail], List) :- member(Head, List), subset(Tail, List).

    equivalent(List1, List2) :- subset(List1, List2), subset(List2, List1).

    union([], List, List).
    union([Head|Tail], List2, Result) :- member(Head, List2), !, union(Tail, List2, Result).
    union([Head|Tail], List2, [Head|Result]) :- union(Tail, List2, Result).

    intersection([], _, []).
    intersection([Head|Tail], List2, [Head|Result]) :- member(Head, List2), !, intersection(Tail, List2, Result).
    intersection([_|Tail], List2, Result) :- intersection(Tail, List2, Result).

    difference([], _, []).
    difference([Head|Tail], List2, Result) :- member(Head, List2), !, difference(Tail, List2, Result).
    difference([Head|Tail], List2, [Head|Result]) :- difference(Tail, List2, Result).

    cardinality([], 0).
    cardinality([Head|Tail], Count) :- member(Head, Tail), !, cardinality(Tail, Count).
    cardinality([_|Tail], Count) :- cardinality(Tail, RestCount), Count is RestCount + 1.

    menu :-
        nl, write('--- List Operations ---'), nl,
        write('1. Member Check'), nl,
        write('2. Subset Check'), nl,
        write('3. Union'), nl,
        write('4. Intersection'), nl,
        write('5. Difference'), nl,
        write('6. Equivalence'), nl,
        write('7. Cardinality'), nl,
        write('8. Exit'), nl,
        write('Enter Choice: '), read(Choice),
        (Choice == 8 -> write('Goodbye!') ; (execute(Choice), menu)).

    execute(1) :-
        write('Enter Element: '), read(Element), write('Enter List: '), read(List),
        (member(Element, List) -> write('Found!') ; write('Not Found!')), nl.

    execute(2) :-
        write('List 1: '), read(List1), write('List 2: '), read(List2),
        (subset(List1, List2) -> write('L1 is subset of L2') ; write('Not a subset')), nl.

    execute(3) :-
        write('List 1: '), read(List1), write('List 2: '), read(List2),
        union(List1, List2, Result), write('Union: '), write(Result), nl.

    execute(4) :-
        write('List 1: '), read(List1), write('List 2: '), read(List2),
        intersection(List1, List2, Result), write('Intersection: '), write(Result), nl.

    execute(5) :-
        write('List 1: '), read(List1), write('List 2: '), read(List2),
        difference(List1, List2, Result), write('Difference: '), write(Result), nl.

    execute(6) :-
        write('List 1: '), read(List1), write('List 2: '), read(List2),
        (equivalent(List1, List2) -> write('Equivalent') ; write('Not Equivalent')), nl.

    execute(7) :-
        write('Enter List: '), read(List),
        cardinality(List, Count), write('Cardinality: '), write(Count), nl.

    execute(_) :- write('Invalid Choice!'), nl.