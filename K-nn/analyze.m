function output=analyze(kind,truth,preds)	
% function output=analyze(kind,truth,preds)		
%
% Analyses the accuracy of a prediction
% Input:
% kind='acc' classification error
% kind='abs' absolute loss
% (other values of 'kind' will follow later)
% 
[~, n] = size(truth);
switch kind
	case 'abs'
		% compute the absolute difference between truth and predictions
		%fill in the code here
        output = sum(abs(truth - preds))/n;
		
	case 'acc' 
		%% fill in code here
error = 0;
for i = 1 : n
    if truth(i) ~= preds(i)
         error = error + 1;
    end
end
output = (n - error)/n;
                
end;

