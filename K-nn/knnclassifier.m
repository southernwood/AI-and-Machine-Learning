function preds = knnclassifier(xTr,yTr,xTe,k);
% function preds=knnclassifier(xTr,yTr,xTe,k);
%
% k-nn classifier 
%
% Input:
% xTr = dxn input matrix with n column-vectors of dimensionality d
% xTe = dxm input matrix with n column-vectors of dimensionality d
% k = number of nearest neighbors to be found
%
% Output:
%
% preds = predicted labels, ie preds(i) is the predicted label of xTe(:,i)
%


% output random result as default (you can erase this code)
[d,n]=size(xTe);
[d,ntr]=size(xTr);
if k>ntr,k=ntr;end;

%currently assigning random predictions

%% fill in code here
[indices, ~] = findknn(xTr,xTe,k);
preds = zeros(1, n);
for i = 1 : n
    labels = yTr(indices(:,i)');
    a = sort(histcounts(labels),'descend');
    [~, size_a] = size(a);
    if size_a > 1 && a(1) == a(2)
        preds(i) = knnclassifier(xTr,yTr,xTe(:,i),k-1);
    else
        preds(i) = mode(labels);
    end
end

end