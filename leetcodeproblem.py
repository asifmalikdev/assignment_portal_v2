from statistics import multimode

from numpy.ma.core import negative


class Solution(object):
    def divide(self, dividend, divisor):
        maxi = 2**31 - 1
        mini = -2**31
        if dividend == mini and divisor == -1:
            return maxi
        print(dividend<0)
        print(divisor<0)
        negative = (dividend<0) != (divisor<0)
        dividend, divisor = abs(dividend), abs(divisor)

        quotient = 0
        while dividend>=divisor:
            temp, multiple = divisor, 1
            while dividend >=(temp << 1):
                temp <<= 1
                multiple <<=1
            dividend-=temp
            quotient+=multiple
        print(negative)
        return -quotient if negative else quotient
obj = Solution()
print(obj.divide(15,-3))


