class Solution:
    def findMaxContigSubarray(self, nums: list) -> int:
        max_global = max_tmp = nums[0]
        idx = 1
        while idx < len(nums):
            max_tmp = max(max_tmp+nums[idx], nums[idx])
            if max_tmp > max_global:
                max_global = max_tmp
            idx += 1
        return max_global

# test
mySol = Solution()
nums = [-2,1,-3,4,-1,2,1,-5,4]
print("nums: {} has larget sum {}".format(nums, mySol.findMaxContigSubarray(nums)))
nums = [2,0,1,-5,3,-1,2,3,-3,2]
print("nums: {} has larget sum {}".format(nums, mySol.findMaxContigSubarray(nums)))
