# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        add 2 linked list
        """
        l1num = self.convertList2Num(l1)    # convert list 1 to num 1
        l2num = self.convertList2Num(l2)    # convert list 2 to num 2
        fsum = l1num + l2num
        return self.convertNum2List(fsum)   # convert sum to list

    def convertNum2List(self, num: int) -> ListNode:
        """
        convert a number to linked List
        """
        header = ListNode()
        tmpHead = header
        while num:
            tmpHead.next = ListNode(num % 10)
            num = num // 10
            tmpHead = tmpHead.next
        return header.next

    def convertList2Num(self, l1: ListNode) -> int:
        lnum = 0
        diglvl = 1
        while l1:
            lnum += l1.val * diglvl
            l1 = l1.next
            diglvl *= 10
        return lnum

    def printList(self, myListNode):
        """
        print a linked list
        """
        if not myListNode:
            print("List is empty")
        print(myListNode.val, end="")
        myListNode = myListNode.next
        while myListNode:
            print("-> {}".format(myListNode.val), end="")
            myListNode = myListNode.next

    def test(self, n1, n2):
        """
        used for testing
        """
        print("\ntesting...")
        print("input 1: {}\t".format(n1), end="")
        self.printList(self.convertNum2List(n1))
        print("\ninput 2: {}\t".format(n2), end="")
        self.printList(self.convertNum2List(n2))
        print("\nsum  is: {}\t".format(n1+n2), end="")
        self.printList(self.addTwoNumbers(self.convertNum2List(n1), self.convertNum2List(n2)))

# test
mySol = Solution()
mySol.test(1234, 2345)
mySol.test(135, 7463897)



