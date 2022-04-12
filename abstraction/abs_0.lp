direction((X,Y)) :- X=-1..1, Y=-1..1, |X|+|Y|=1..2.

node(N,X,Y) :- init(object(node,N),value(at,(X,Y))).
node(N,0)   :- node(N,_,_).

n_is_in_c(N,N,0) :- node(N,0).

edge((N,N2),0) :- direction((DX,DY)), node(N,X,Y), node(N2,X2,Y2), (X,Y)=(X2-DX,Y2-DY), (X2,Y2)=(X+DX,Y+DY).

#show edge/2.
#show node/2. #show node/3.
#show n_is_in_c/3.
