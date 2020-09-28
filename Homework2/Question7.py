# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        if root.left == None and root.right == None:
            # leaf node
            if root.val == sum:
                return True
            else:
                return False
        else:
            return self.hasPathSum(root.left, sum-root.val) or self.hasPathSum(root.right, sum-root.val)

mySol = Solution()
# test case 1
print("test case 1:")
print("                          5                           ")
print("                        /    \                        ")
print("                      4        8                      ")
print("                    /        /    \                   ")
print("                  11        13     4                  ")
print("                 /  \         \                       ")
print("                7    2         1                      ")
a5=TreeNode(5); a4=TreeNode(4); a8=TreeNode(8); a11=TreeNode(11); a13=TreeNode(13); a4_2=TreeNode(4); a7=TreeNode(7); a2=TreeNode(2); a1=TreeNode(1);
a5.left = a4; a5.right = a8; a4.left = a11; a8.left = a13; a8.right = a4_2; a11.left = a7; a11.right = a2; a13.right = a1;
checksum = 22; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(a5, checksum)))
checksum = 17; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(a5, checksum)))
checksum = 24; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(a5, checksum)))

# test case 2
print("test case 2:")
print("                          9                           ")
print("                        /    \                        ")
print("                      11      15                      ")
print("                    /   \    /   \                    ")
print("                   7     1  0     3                   ")
print("                           /                          ")
print("                          2                           ")
b9=TreeNode(9); b11=TreeNode(11); b15=TreeNode(15); b7=TreeNode(7); b1=TreeNode(1); b0=TreeNode(0); b3=TreeNode(3); b2=TreeNode(2);
b9.left = b11; b9.right = b15; b11.left = b7; b11.right = b1; b15.left = b0; b15.right = b3; b0.left = b2;
checksum = 24; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(b9, checksum)))
checksum = 21; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(b9, checksum)))
checksum = 26; print("has path of sum {}: {}".format(checksum, mySol.hasPathSum(b9, checksum)))
