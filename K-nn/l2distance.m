function D=l2distance(X,Z)
% function D=l2distance(X,Z)
%	
% Computes the Euclidean distance matrix. 
% Syntax:
% D=l2distance(X,Z)
% Input:
% X: dxn data matrix with n vectors (columns) of dimensionality d
% Z: dxm data matrix with m vectors (columns) of dimensionality d
%
% Output:
% Matrix D of size nxm 
% D(i,j) is the Euclidean distance of X(:,i) and Z(:,j)
%
% call with only one input:
% l2distance(X)=l2distance(X,X)
%

if (nargin==1) % case when there is only one input (X)
	%% fill in code here
S = sum(X.*X, 1);
G = X'*S; 
D = sqrt(abs(repmat(S',[1 size(S,2)]) + repmat(S,[size(S,2) 1]) - 2*G));

else  % case when there are two inputs (X,Z)
	%% fill in code here

S = sum(X.*X, 1);
R  =sum(Z.*Z,1); 
G = X'*Z; 
D = sqrt(abs(repmat(S',[1 size(R,2)]) + repmat(R,[size(S,2) 1]) - 2*G));
end;
%



