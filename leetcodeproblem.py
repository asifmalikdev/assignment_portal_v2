class Solution(object):
    def strStr(self, haystack, needle):
        if needle=="":
            return 0
        for i in range((len(haystack)-len(needle))+1):
            if haystack[i:(i+len(needle))]==needle:
                return i
        return -1




obj = Solution()
print(obj.strStr("asdfasdf", 'df'))
print(obj.strStr("asdfasdf", 'asdfg'))
print(obj.strStr("assdfasdf", 'asdf'))