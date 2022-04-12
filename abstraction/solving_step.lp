level(level).
time(0..horizon).

% Starting position:
at(R,C2,L,0) :- init(object(robot,R),value(at,(X,Y))), node(C,X,Y), n_is_in_c(C2,C,L), level(L).

% New positions:
1{at(R,C2,L,T+1) : edge((C,C2),L); at(R,C,L,T+1)}1 :- at(R,C,L,T), level(L), time(T+1).

% Not on a position the robot wasn't on on the level above
:- at(R,C,L,_), not at(R,C2,L+1,_), c_is_in_c(C,C2,L+1).

% Keep order of higher levels:
%:- at(R,N,L,T), at(R,N2,L,T2), at(R,C,L+1,T3), at(R,C2,L+1,T4), c_is_in_c(C,N,L+1), c_is_in_c(C2,N2,L+1), T>T2, T3<T4, level(L).

% Goal:
goal(N) :- init(object(order,O),value(line,(A,_))), init(object(product,A),value(on,(S,_))), init(object(shelf,S),value(at,(X,Y))), node(N,X,Y).
at_goal(N,L) :- goal(N), n_is_in_c(C,N,L), at(R,C,L,horizon), init(object(robot,R),_), level(L).
:- goal(N), not at_goal(N,L), level(L).

#show at/4.
#show goal/1.

% maybe constraints with capacities and number of incoming edges / nodes inside clique
