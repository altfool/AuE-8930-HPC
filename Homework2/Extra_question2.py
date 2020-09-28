# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeKLists(self, lists: [ListNode]) -> ListNode:
        lists_len = len(lists)
        if lists_len == 0:
            return None
        if lists_len == 1:
            return lists[0]
        if lists_len == 2:
            return self.merge2Lists(lists[0], lists[1])
        # when >= 3 listNodes
        return self.merge2Lists(self.mergeKLists(lists[:lists_len//2]), self.mergeKLists(lists[lists_len//2:]))

    def merge2Lists(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        merge 2 linked list
        """
        if not l1:
            return l2
        if not l2:
            return l1
        header = ListNode()
        tmpHead = header
        while l1 and l2:
            if l1.val < l2.val:
                tmpHead.next = ListNode(l1.val)
                tmpHead = tmpHead.next
                l1 = l1.next
            else:
                tmpHead.next = ListNode(l2.val)
                tmpHead = tmpHead.next
                l2 = l2.next
        if l1:
            while l1:
                tmpHead.next = ListNode(l1.val)
                tmpHead = tmpHead.next
                l1 = l1.next
        if l2:
            while l2:
                tmpHead.next = ListNode(l2.val)
                tmpHead = tmpHead.next
                l2 = l2.next
        return header.next

    def convertList2Node(self, lists: [list]) -> [ListNode]:
        mylist = []
        for lt in lists:
            mySubListNodeHeader = ListNode()
            tmpHead = mySubListNodeHeader
            for val in lt:
                tmpHead.next = ListNode(val)
                tmpHead = tmpHead.next
            mylist.append(mySubListNodeHeader.next)
        return mylist

    def printList(self, myListNode: ListNode):
        """
        print a linked list
        """
        if not myListNode:
            print("List is empty")
        print(myListNode.val, end="")
        myListNode = myListNode.next
        while myListNode:
            print(" -> {}".format(myListNode.val), end="")
            myListNode = myListNode.next

    def printListNode(self, myListNode: [ListNode]):
        print("[")
        for ln in myListNode:
            self.printList(ln)
            print("")
        print("]")

# test
mySol = Solution()
lists = [[1,4,5],[1,3,4],[2,6]]
print(lists)
mylistofNodes = mySol.convertList2Node(lists)
print(" list of linked-node list: ")
mySol.printListNode(mylistofNodes)
mergedListNode = mySol.mergeKLists(mylistofNodes)
print("merged linked list: ")
mySol.printList(mergedListNode)
