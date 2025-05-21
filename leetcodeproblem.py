from statistics import multimode

from numpy.ma.core import negative


# class Solution(object):
#     def divide(self, dividend, divisor):
#         maxi = 2**31 - 1
#         mini = -2**31
#         if dividend == mini and divisor == -1:
#             return maxi
#         print(dividend<0)
#         print(divisor<0)
#         negative = (dividend<0) != (divisor<0)
#         dividend, divisor = abs(dividend), abs(divisor)
#
#         quotient = 0
#         while dividend>=divisor:
#             temp, multiple = divisor, 1
#             while dividend >=(temp << 1):
#                 temp <<= 1
#                 multiple <<=1
#             dividend-=temp
#             quotient+=multiple
#         print(negative)
#         return -quotient if negative else quotient
# obj = Solution()
# print(obj.divide(15,-3))

class Solution(object):
    def countPrimes(self, n):
        if n < 2:
            return 0

        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n, i):
                    is_prime[j] = False

        return sum(is_prime)

#
# obj = Solution()
# print(obj.countPrimes(10))
class Solution1(object):
    def patterns(self, nums):
        for i in range(nums):
            for j in range(i):
                print("* ", end='')
            print('')
    def patterns1(self, nums):
        for i in range(nums,0,-1):
            for j in range(1,i+1):
                print(j,end='')
            print('')


    def patterns2(self,n):
        for i in range(n):
            for j in range(n-i-1):
                print(' ', end = '')
            for j in range((i*2)+1):
                print("*", end= '')
            for j in range(n-i-1):
                print(' ', end='')
            print('')

    def patterns3(self, n):
        for i in range(n,0,-1):
            for j in range(n,i,-1):
                print(' ', end='')
            for j in range(i*2-1):
                print('*', end='')
            for j in range(n,i,-1):
                print(' ', end='')

            print('')

    def patterns4(self, n):
        for i in range(1,(2*n)):
            temp = i
            if i>n:
                temp = (2*n)-i
            for j in range(temp):
                print('*',end='')
            print('')

    def patterns5(self, nums):
        start = 1
        for i in range(1,nums+1):
            if i%2!=0:
                start = 1
            else:
                start = 0
            for j in range(i):
                print(start, end='')
                start = 1-start
            print('')

    def patterns6(self, nums):
        for i in range(nums):
            for j in range(i+1):
                print(j+1, end= '')
            for j in range((2*nums)-(2*i)-2):
                print(' ', end = '')
            for j in range(i+1, 0, -1):
                print(j, end = '')


            print('')


obj = Solution1()
# obj.patterns(5)
# obj.patterns1(5)
# obj.patterns2(5)
# obj.patterns3(5)
# obj.patterns4(5)
# obj.patterns5(5)
# obj.patterns6(4)


class Mathematics():
    def counter(self,n):
        counter = 0
        while n>0:
            n= int(n/10)
            counter+=1

        print(counter)
    def reversenumber(self, n):
        temp = 0
        while n>0:
            temp=(temp*10)+ (n%10)
            n=int(n/10)

        print(temp)




obj = Mathematics()
# obj.counter(323445)
obj.reversenumber(342350000)
num = {
    "title": "Final Exam",
    "description": "Math exam assignment",
    "due_date": "2025-06-01T12:00:00Z",
    "assigned_class": 9,
    "questions": [5,8,9]
}