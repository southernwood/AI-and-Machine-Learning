A = [35, 41, 21, 20, 17, 55, 12];
B = [33, 15, 18, 4, 51, 17, 46];
All = [35, 41, 21, 20, 17, 55, 12, 33, 15, 18, 4, 51, 17, 46];
flag = 1;
while flag == 1
    u_a = mean(A);
    sigma_a = std(A);
    u_b = mean(B);
    sigma_b = std(B);
    A_next = [];
    B_next = [];
    flag = 0;
    for i = A
        pa = normpdf(i,u_a, sigma_a);
        pb = normpdf(i,u_b, sigma_b);
        if pb > pa
            B_next = [B_next, i];
            flag = 1;
        else
            A_next = [A_next, i];
        end
    end
    for i = B
        pa = normpdf(i,u_a, sigma_a);
        pb = normpdf(i,u_b, sigma_b);
        if pa > pb
            A_next = [A_next, i];
            flag = 1;
        else
            B_next = [B_next, i];
        end
    end
    A = A_next;
    B = B_next;
end
    

