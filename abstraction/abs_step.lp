%max_level(level).
level(level).

% Nodes:
node(N,L)   :- clique(N,      L), level(L).
node(N,L)   :- clique(N,_,    L), level(L).
node(N,L)   :- clique(N,_,_,  L), level(L).
node(N,L)   :- clique(N,_,_,_,L), level(L).

% Keeping track of which node/clique is contained in which clique:
c_is_in_c(N,N ,L) :-   node(N,         L), level(L).
c_is_in_c(N,N2,L) :- clique(N,N2,      L), level(L).
c_is_in_c(N,N2,L) :- clique(N,N2,_ ,   L), level(L).
c_is_in_c(N,N2,L) :- clique(N,N2,_ ,_ ,L), level(L).
c_is_in_c(N,N3,L) :- clique(N,_ ,N3,   L), level(L).
c_is_in_c(N,N3,L) :- clique(N,_ ,N3,_ ,L), level(L).
c_is_in_c(N,N4,L) :- clique(N,_ ,_ ,N4,L), level(L).
n_is_in_c(C,N ,L) :- c_is_in_c(C,C2,L), n_is_in_c(C2,N,L-1), level(L).

% Nodes can not be contained in more than one clique:
:- 1!={c_is_in_c(_,C,L)}, node(C,L-1), level(L).
:- 1<{clique(N,L); clique(N,_,L); clique(N,_,_,L); clique(N,_,_,_,L)}, node(N,L-1), level(L).	% Special case because ID of first node in clique is also used as cliques ID

% Clique generation:
{clique(N,         L);
 clique(N,N2,      L) : edge((N,N2),L-1);
 clique(N,N2,N3,   L) : edge((N,N2),L-1), edge((N,N3),L-1), edge((N2,N3),L-1);
 clique(N,N2,N3,N4,L) : edge((N,N2),L-1), edge((N,N3),L-1), edge((N2,N3),L-1), edge((N,N4),L-1), edge((N2,N4),L-1), edge((N3,N4),L-1)
}1 :- node(N,L-1), level(L).

% Edges:
edge((C,C2),L) :- edge((N ,N2),0), n_is_in_c(C,N,L), n_is_in_c(C2,N2,L), C<C2, level(L).
edge((N,N2),L) :- edge((N2,N ),L), level(L).

% Optimization:
#heuristic clique(N,         L). [4,false]
%#heuristic clique(N,N2,      L). [3,false]
%#heuristic clique(N,N2,N3,   L). [2,false]
%#heuristic clique(N,N2,N3,N4,L). [1,false]

#show node/2. #show edge/2.
#show node/3.
#show n_is_in_c/3.
#show c_is_in_c/3.

%#show goal/1.
%#show at/4.
%#show n_is_in_c/3.
%#show clique/2. #show clique/3. #show clique/4. #show clique/5.
