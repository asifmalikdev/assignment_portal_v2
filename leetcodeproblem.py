class Solution(object):
    def isMatch(self, s, p):
        if "." and "*" in p:
            for i in s:
                if i in p:
                    return True

        if '*' in p:
            pass


        else:
            if s == p:
                return True
            else:
                return False
            False
obj = Solution()
print(obj.isMatch('asd', '*fsdf'))