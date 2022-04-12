#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.

maxY(MY) :- node(_,_,MY), MY=#max{Y : node(N,X,Y)}.
#show attr(node,N,pos,@pos(X,MY-Y)) : node(N,X,Y), maxY(MY).
graph(0..level).% :- max_level(level).
#show attr(node, N, color, red) : at(_,N,0,_).
%#show attr(node, N, color, blue) : goal(N).
#show graph/1. #show node/2. #show edge/2.
%#show node(N,L) : node(N,0), graph(L), L>0.
