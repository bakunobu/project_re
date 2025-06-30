
from typing import List

def missingNumber(nums: List[int]) -> int:
    nums.sort()
    if len (nums) == 0:
        return 0
    elif len(nums) == 1:
        if nums[0] == 0:
            return 1
        else:
            return 0
    lb = 0
    rb = len(nums)
    while lb < rb:
        i = (lb + rb) // 2
        print('...',i)
        if i == len(nums) - 1:
            if nums[i] == i:
                return i+1
            else:
                return i
            
        if nums[i] == i:
            if nums[i + 1] == i + 1:
                lb = i
            else:
                return i + 1
        elif nums[i] > i:
            print('here')
            if i == 0:
                return 0
            else:
                if num[i-1] == i - 1:
                    if i == 1:
                        return 1
                    return i
                else:
                    rb = i
                    
print(missingNumber([0, 2]))
 