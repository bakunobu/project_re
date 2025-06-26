def minMaxDifference(num: int) -> int:
    nums = []
    while num:
        el = num % 10
        num //=10
        nums.append(el)
    nums = nums[::-1]
    to_replace_max = None
    to_replace_min = None
    max_num = 0
    min_num = 0
    total = 0
    for i, el in enumerate(nums):
        if to_replace_max is None and el != 9:
            to_replace_max = el
        if to_replace_min is None and el != 0:
            to_replace_min = el
        if el == to_replace_max:
            max_num += 9 * (10**(len(nums)-1-i))
        else:
            max_num += el * (10**(len(nums)-1-i))
        if el == to_replace_min:
            min_num += 0 * (10**(len(nums)-1-i))
        else:
            min_num += el * (10**(len(nums)-1-i))
    return(max_num - min_num)
        # if el == to_replace_max:
        #     result = (9 - el) * (10**(len(nums)-1-i))
        #     total += result
        # if el == to_replace_min:
        #     result = el * (10**(len(nums)-1-i))
        #     total += result

    # return total
  
    
print(minMaxDifference(90693669))