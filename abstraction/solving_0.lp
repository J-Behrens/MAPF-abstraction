time(0..horizon).
level(level).

% Starting positions:
at(R,C2,0,0) :- init(object(robot,R),value(at,(X,Y))), node(C,X,Y), n_is_in_c(C2,C,0).

% New positions on highest level:
1{at(R,C2,L,T+1) : edge((C,C2),L); at(R,C,L,T+1)}1 :- at(R,C,L,T), level(L), time(T+1).

% Not on a position the robot wasn't on on the level above
:- at(R,C,L,_), not at(R,C2,L+1,_), n_is_in_c(C,C2,L+1).

% Keep order of higher levels:
%:- at(R,N,0,T), at(R,N2,0,T2), at(R,C,1,T3), at(R,C2,1,T4), c_is_in_c(C,N,1), c_is_in_c(C2,N2,1), T>T2, T3<T4.

% Robot cannot be at more than one position per timestep:
:- at(R,N,0,T), at(R,N2,0,T), N!=N2.

% Goal:
goal(N) :- init(object(order,O),value(line,(A,_))), init(object(product,A),value(on,(S,_))), init(object(shelf,S),value(at,(X,Y))), node(N,X,Y).
at_goal(N,0) :- goal(N), n_is_in_c(C,N,0), at(R,C,0,horizon), init(object(robot,R),_).
%at_goal(N,0) :- goal(N), n_is_in_c(C,N,0), at(R,C,0,_), init(object(robot,R),_).
:- goal(N), not at_goal(N,0).

% Vertex collision:
:- { at(R,C,0,T) : init(object(robot,R),_) }  > 1, node(C,0), time(T).
 
% Edge collision:
:- at(R,C,0,T), at(R2,C2,0,T), at(R,C2,0,T+1), at(R2,C,0,T+1), time(T).

% Crossing collision:
:- at(R,N,0,T), at(R,N2,0,T+1),  at(R2,N3,0,T),  at(R2,N4,0,T+1), time(T),
   node(N,X,Y), node(N2,X+1,Y+1), node(N3,X+1,Y), node(N4,X,Y+1).

:- at(R,N,0,T),     at(R,N2,0,T+1), at(R2,N3,0,T),  at(R2,N4,0,T+1), time(T),
   node(N,X+1,Y+1), node(N2,X,Y),    node(N3,X,Y+1), node(N4,X+1,Y).
   
:- at(R,N,0,T), at(R,N2,0,T+1), at(R2,N3,0,T),  at(R2,N4,0,T+1), time(T),
   node(N,X,Y), node(N2,X+1,Y+1),    node(N3,X,Y+1),   node(N4,X+1,Y).
   
:- at(R,N,0,T), at(R,N2,0,T+1), at(R2,N3,0,T),  at(R2,N4,0,T+1), time(T),
   node(N,X+1,Y+1), node(N2,X,Y),    node(N3,X+1,Y),   node(N4,X,Y+1).

#show at/4.
