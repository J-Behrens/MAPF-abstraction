position((X,Y)) :- init(object(node,_),value(at,(X,Y))).

%%% initial instance %%%
node(N,X,Y) :- init(object(node,N),value(at,(X,Y))).
node(N,0)   :- node(N,_,_).

direction((X,Y)) :- X=-1..1, Y=-1..1, |X|+|Y|=1.
edge((N,N2),0) :- direction((DX,DY)), node(N,X,Y), node(N2,X2,Y2), (X,Y)=(X2-DX,Y2-DY), (X2,Y2)=(X+DX,Y+DY).

%%% abstraction %%%

% crossings
node(N,1) :- 3	{position((X',Y')) : X'=X-1..X+1, Y'=Y-1..Y+1, |X-X'|+|Y-Y'|=1} 4, node(N,X,Y).

% corners
node(N,1) :-	{position((X',Y )) : X'=X-1..X+1, Y'=Y-1..Y+1, |X'-X|=1, |Y'-Y|=1}=1, node(N,X,Y),
		{position((X ,Y')) : X'=X-1..X+1, Y'=Y-1..Y+1, |X'-X|=1, |Y'-Y|=1}=1.

node(N,X,Y,1) :- node(N,1), node(N,X,Y).

% edges		   
edge((N,N'),1) :- X<X', node(N,X,Y,1), node(N',X',Y,1), X!=X', position((X'',Y)) : X''=X..X'; not node(_,X'',Y,1) : X''=X..X', X''!=X, X''!=X'.
edge((N,N'),1) :- Y<Y', node(N,X,Y,1), node(N',X,Y',1), Y!=Y', position((X,Y'')) : Y''=Y..Y'; not node(_,X,Y'',1) : Y''=Y..Y', Y''!=Y, Y''!=Y'.
edge((N',N),1) :- edge((N,N'),1).
