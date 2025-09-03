
from typing import List

class Solution:
    def fairCandySwap(self, aliceSizes: List[int], bobSizes: List[int]) -> List[int]:
        aliceSizes.sort()
        bobSizes.sort()
        if sum(aliceSizes) > sum(bobSizes):
            candidates = [x for x in aliceSizes if x > max(bobSizes)]
            print(candidates)
            for i in bobSizes:
                for j in candidates:
                    if sum(aliceSizes) - j + i == sum(bobSizes) + j - i:
                        return [j, i]
        else:
            candidates = [x for x in bobSizes if x > max(aliceSizes)]
            print(candidates)
            for i in aliceSizes:
                for j in candidates:
                    print(i, j)
                    if sum(aliceSizes) + j - i == sum(bobSizes) - j + i:
                        return [i, j]
    

aliceSizes = [8,73,2,86,32]
bobSizes = [56,5,67,100,31]
print(Solution().fairCandySwap(aliceSizes, bobSizes))