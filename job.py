'''Programming Evaluation Rules:
-   Find the 2nd highest and 2nd lowest for the series of number that I message you over the Google meeting.
-	You have 20 minutes to complete your 1st coding test.
-   You cannot use any programming built-in functions.
-	You cannot get any help online or locally.
-	You cannot hardcode any values in your programming.
-	It is a programming logic test, you can use Arrays, variables, loops, conditions.
-   if you like, you can use Copy/Pen.'''

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0,n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr
    
def secondLargest(arr):
    largest = arr[len(arr)-1]
    for i in range(len(arr)-2, 0, -1):
        if arr[i] < largest:
            return arr[i]
    
    
def secondLowest(arr):
    lowest = arr[0]
    
    for i in range(1,len(arr)):
        if arr[i]>lowest:
            return arr[i]
    


# num  = [105,110,320,1001,503,203,505,101,503,110,101,320,203,505,105,110,320,101,503]
# num = bubble_sort(num)
# print("array",num)
# secondLargest = secondLargest(num)
# print("\nSecond Largest",secondLargest)
# secondLowest = secondLowest(num)
# print("\nSecond Lowest",secondLowest)




def fourthLargest(arr):
    largest = arr[len(arr)-1]
    count = 0
    for i in range(len(arr)-2, -1, -1):
        if arr[i] < largest:
            count += 1
            if count == 3:
                return arr[i]
    
    return None

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        mergeSort(left)
        mergeSort(right)

        i = j = k = 0

        # Merge the sorted halves
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # Copy any remaining elements of left[]
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        # Copy any remaining elements of right[]
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


# arr = [38, 27, 43, 3, 9, 82, 10]
# mergeSort(arr)
# print(arr)  # Output should be: [3, 9, 10, 27, 38, 43, 82]



class Solution():
    def nSumRecursion(self, n):
        if n == 1:
            return n
        
        return n + self.nSumRecursion(n-1)







obj = Solution()
print(obj.nSumRecursion(3))

