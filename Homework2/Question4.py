class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        lf = rh = 0
        max_len = 0
        myset = set()
        while rh < len(s):
            if s[rh] not in myset:
                myset.add(s[rh])
                max_len = max(max_len, rh-lf+1)
            else:
                while s[lf] != s[rh]:
                    myset.remove(s[lf])
                    lf += 1
                lf += 1
            rh += 1
        return max_len

mySol = Solution()
print(mySol.lengthOfLongestSubstring("abcabcbb"))
print(mySol.lengthOfLongestSubstring("abeshdsaelsk"))
