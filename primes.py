def is_prime(i,n):
    return (lambda i,n : (True if (i >= n) else  (False if ((n % i) == 0) else is_prime((i + 1),n)) if (i <  n) else  None))(i,n)

print(is_prime(2,9))