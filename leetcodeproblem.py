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




# obj = Mathematics()
# obj.counter(323445)
# obj.reversenumber(342350000)
num = {
    "title": "Final Exam",
    "description": "Math exam assignment",
    "due_date": "2025-06-01T12:00:00Z",
    "assigned_class": 9,
    "questions": [5,8,9]
}
class Solution():
    def convert(self, s, n):
        if n ==  s:
            return s

        new_list = ""
        for i in range(0, len(s), 2*n - 2):
            new_list += s[i]

        for row in range(1,n-1):
            i = row
            while i < len(s):
                new_list = new_list+s[i]
                diag = i + (2*n - 2 - 2*row)
                if diag < len(s):
                    new_list = new_list+s[diag]
                i = i+ (2*n)-2
        for i in range(n - 1, len(s), 2 * n - 2):
            new_list += s[i]

        return new_list



    def lengthOfLastWord(self, s):
        index=0
        s=s.strip()
        print(s)
        for i in range(len(s)-1,-1,-1):
            if s[i] == " ":
                print("inside if",index)
                break

            else:
                index+=1
        print(index)







obj = Solution()
# obj.convert("paypalishiring", 3)
obj.lengthOfLastWord("hwllo wolrd you are gone world ")

#
# import sys
# import array
# import random
#
# # Create a large number of integers
# num_elements = 1_000_000
# int_list = [random.randint(0, 100) for _ in range(num_elements)]
# int_array = array.array('i', int_list)
#
# # Get memory size of list and array
# list_size = sys.getsizeof(int_list) + sum(sys.getsizeof(i) for i in int_list)
# array_size = sys.getsizeof(int_array)
#
# print(f"List memory usage: {list_size / (1024*1024):.2f} MB")
# print(f"Array memory usage: {array_size / (1024*1024):.2f} MB")
# my_array = array.array('i', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#  21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
#  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
#  61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
#  81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
# )
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#  21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
#  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
#  61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
#  81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
# #
# # print("list per index size", sys.getsizeof(my_list))
# # print("array per index size", sys.getsizeof(my_array))
# #
