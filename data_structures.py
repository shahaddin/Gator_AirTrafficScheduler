#Shahaddin Gafarov. UFID: 3053-9258
#COP 5536 Project 1: Gator Air Traffic Slot Scheduler
#data_structures.py: holds the necessary data structures for the code to function properly


#I imported math for the floor function
import math

#some variables of the flight_class might be optional/secondary
from typing import Optional


#the binary min heap implementation
#https://www.geeksforgeeks.org/python/min-heap-in-python/
#https://www.educative.io/blog/data-structure-heaps-guide
class binaryminheap:
    #initialize an empty heap
    def __init__(self):
        self.heap = []
    
    #insert function, which needs a number to insert(and self which holds the heap)
    def insert(self, number):
        #how many elements we got in the heap
        l = len(self.heap)

        #add the number to the heap at its end
        self.heap.append(number)

        #we start from l at the newly added node, and go up correcting the structure until we reach the root
        #which means we have succesfully corrected the structure after the insert
        while(l>0):
            #since it is stored in array format, the parents alwasy residens in n-1/2-th node.
            #and if n is odd then the parent will be the whole number part
            parent = math.floor((l-1) / 2)
            #if the child is indeed smalelr than the parent, it gets swapped,
            #thus maintaining the min-heap property
            if(self.heap[l]<self.heap[parent]):
                temp = self.heap[l]
                self.heap[l] = self.heap[parent]
                self.heap[parent] = temp
                l = parent
            #if not, we dont need to reach the root, as none of the subsequent elements will be bigger either
            else:
                break
    
    #not needed since we will only delete the minimum
    def delete(self, number):
        pass

    #access the minimum element of the heap, which is at the root per min heap properties
    def getmin(self):
        #if the heap has no elements, return false
        if(len(self.heap) == 0):
            return False
        #if it does have any elements, we only need to look ath the root regardless
        else:
            minimum = self.heap[0]
            return minimum
    
    #deletes the min element, or the root in other words of the min heap
    def deletemin(self):

        #same as getmin, there needs to be at least 1 element to delete minimum
        if(len(self.heap)<1):
            print("Trying to remove from empty heap")
            return False
        #if there is at least one element in the heap:
        else:
            #I did not use deletemin returning the deleted minimum number as a functionality,
            # but it was useful to have for testing purposes
            minimum = self.heap[0]
            #switching the root with the last element of the heap(by copying)
            self.heap[0] = self.heap[len(self.heap)-1]
            #delete the original last element
            xxx = self.heap.pop()
            
            #the index of the new last node
            last_node = len(self.heap)
            i = 0 

            #correct the shape of the min heap on a forever going loop
            #start from the new root, and ensure that the property gets handled all the way to the end, or until the point that
            #the node is bigger than its children
            while(1):
                #the smaller of the 3 nodes is supposed to be the parent, small_node is more like a temp for i, as a future trigger signal if anything happens
                small_node = i
                #derived from the earlier logic, of n-1/2th,
                #which converts into n *2 +1 or(+2) for getting the children given the parent node
                left_child = (2*small_node) + 1
                right_child = (2* small_node) + 2

                #if the parent is smaller, point to the left child
                if(left_child < last_node):
                    if(self.heap[left_child]<self.heap[small_node]):
                        small_node = left_child
                #if the parent is smaller,  point to the right child
                if(right_child < last_node):
                    if(self.heap[right_child]<self.heap[small_node]):
                        small_node = right_child                 

                #if none of the if cases above is triggered, that means parent is at least smaller or equal to its children
                #which means the min heap property is satisfied and no need to check further down
                if(small_node == i):
                    break
                else:
                #if a new pointer on the either of the 2 if cases happen, then swap the parent node and the child node
                    temp3 = self.heap[i]
                    self.heap[i] = self.heap[small_node]
                    self.heap[small_node] = temp3
                    #update i to the child node(where the originally root-swapped node now resides)
                    i = small_node
                    continue
            
            #since we wont use deletemin for getting the minimum elemnt info return True could have also been used
            #return True
            #I kept it as return minimum for bonus functionality
            return minimum

    #not needed for this project
    def heapify(self):
        pass


#the max pairing heap implementation
class maxpairingheap:
    
    #defining the properties of the node in a sub-class
    class pairingheapnode:
        #every node is supposed to have a key for priority, and number is the actual contnent inside
        #additionally there is a pointer to the child
        #and 2 pointers left and right(first node's left pointer points to the parent)
        def __init__(self, number, key):
            self.number = number
            self.key = key
            #self.child, self.left, self.right = None?
            self.child, self.left, self.right = None, None, None

    #create an empty max pairing heap(mph for short)
    def __init__(self):
        self.mph = None

    #insert operation, needs the actual value of the node and the priority(key)
    def insert(self, number, key):
        #create a node with the given properties
        node = maxpairingheap.pairingheapnode(number, key)
        #do a meld operation with the heap and the newly created node
        self.mph = self.meld(self.mph, node)
        
        #returns the node if needed, but won;t be used necessarily anywhere
        return node
        #return self.mph

    #gets the maximum value which is stored at the root
    def getmax(self):
        #if heap is empty return False
        if(self.mph == None):
            # print("empty max pairing heap(getmax)")
            return False
        else:
        #if the heap is not empty, return the root(value and the key), which self.mph points to
            return self.mph.number, self.mph.key
    
    #deletes the max value(root) instead of fetching it like getmax()
    def deletemax(self):
        #again, if no elements, then there is nothing to remove thus false
        if(self.mph == None):
            # print("empty max pairing heap(deletemax)")
            return False
        else:
            #root variable for pointing to the root
            root = self.mph
            # root_key = root.key
            # root_number = root.number
            
            #root_first_child points to the child of the root
            root_first_child = root.child

            #if there is some child of the root, then two_pass can happen to merge the reamining child of the root
            if(root_first_child!=None):
                #now that the first child doesntrr have a parent, its left pointer will point to null
                root_first_child.left = None
                #and we will do the two_pass scheme for the first child and the remaining children there
                self.mph = self.two_pass(root_first_child)
                return True
            
            #if the root doesnt have any child, then after root gets deleted no elements will be left
            else:
                # print("no elements left")
                self.mph = None
                return True


    #Assignment Description was: Update priority (pairing heap: increase-key if priority increases; erase+insert if decreases).
    #Which I guess means there is no decreasekey() wanted in pairing heap, just do erase and an insert in order
    #the increasekey() function:
    def increasekey(self, node, key_updated):
        #I update the key here
        node.key = key_updated

        #if the node is the root or if it's already severed(as an independent max peairing heap)
        #then it has no parent
        if node is self.mph:
            parent = None
        elif node.left == None:
            parent = None
        #if we are at the leftmost node, we have instant access to the parent
        elif node.left.child == node:
            parent = node.left
        #if it is some middle child node, then we need to go all the way to the left until we find the parent
        else:
            leftmostfinder = node.left
            while leftmostfinder.left != None and leftmostfinder.left.child != leftmostfinder:
                leftmostfinder = leftmostfinder.left
            parent = leftmostfinder.left

        #if there was no parent found, or the parent was already bigger that the updated key
        #then there is nothing to change as everything is still in the same relative structure
        if(parent == None or node.key <= parent.key):
            return 
        
        #if there is a structural change happening, then we sever that node(and the entire thing down below)
        #to be melded with the remaining heap as two separate maxpariingheaps
        else:
            #sever the node
            self.severnode(node)
            #meld them together as one max pairing heap
            self.mph = self.meld(self.mph, node)
            #nothing to return needed, maybe True for signaling a succesusful operation as a helper
            return



    # #old increasekey(), although it is working it is not technically correct
    # def increasekey(self, node, key_updated):
    #     #updated the key of the node
    #     node.key = key_updated
    #     #if the update doesnt change the relative structure of the heap or if the node is the root(again the first condition)
    #     #then nothing to do:
    #     if(node.left == None or node.key <=node.left.key or node is self.mph):
    #         return
    #     #if there is a structural change happening, then we sever that node(and the entire thing down below)
    #     #to be melded with the remaining heap as two separate maxpariingheaps
    #     else:
    #         #sever the node
    #         self.severnode(node)
    #         #meld them together as one max pairing heap
    #         self.mph = self.meld(self.mph, node)
    #         #nothing to return needed, maybe True for signaling a succesusful operation as a helper
    #         return
        
    #meld function for melding 2 max pairing heaps, taking them as inputs
    def meld(self, primary, secondary):
        #if either one of them is empty, a quick primary=(existing_node) will suffice
        if(primary==None):
            primary = secondary
        elif(secondary==None):
            primary = primary

        #if both nodes do have existing elements:
        else:
            #the name "primary" is assigned to be the one with bigger key between the two
            if(primary.key < secondary.key):
                temp4 = primary
                primary = secondary
                secondary = temp4
            
            #secondary.left will point to the parent since it is the root(technically leftmost child of its own league)
            #and will become the leftmost node among primary node's children
            secondary.left = primary
            #rest(original children) from primary node's will be to the right of the secondary node
            secondary.right = primary.child

            #if the primary does have a child then the childs left would be the secondary instead of primary
            #and now primary's child will point to secondary node
            if(primary.child!=None):
                primary.child.left = secondary
                primary.child = secondary
            #if it doesnt have a child, then there is no primary.child.left happening since primary.child is nothing
            else:
                primary.child = secondary

        #return the primary, which will be the melded-together version of both nodes
        return primary

        
    #the two pass scheme, merging all the children nodes into one node, whcih needs the first child as input
    def two_pass(self, root_first_child):

        #if there is no firs child, then None will be the final merge result(as there should be no siblings as well)
        if(root_first_child == None):
            return root_first_child
        #if the child has no siblings, the child itself will be the result of the merge
        elif(root_first_child.right == None):
            #root_first_child.left = None?
            return root_first_child
        #if there is >1 children:
        else:
            #merge pass will hold the melds
            merge_pass = []
            #goes on until there is no sibling's left, signaling all nodes being melded together
            while(root_first_child != None):
                
                #pointers to current node and its right sibling
                current_node = root_first_child
                current_sibling = root_first_child.right

                #if there is a right sibling, next_node is right sibling's right sibling
                if(current_sibling != None):
                    next_node = current_sibling.right
                    #root_first_child = next_node
                #if there is no right sibling, next node points to None
                else:
                    next_node = None

                #currentt node gets severed from parent(which got deleted) and its right sibling as independent node(root)
                current_node.left = current_node.right = None

                #and if there is no sibling then that root alone itself is the sole element of merge_pass
                #which might be a little redundant becasuse of the checks that are happening outside of the while loop
                #but just in case
                if(current_sibling == None):
                    merge_pass.append(current_node)
                    root_first_child = None
                    break
                else:
                #if there is a sibling sever taht too and establish as independent node-root
                    current_sibling.left, current_sibling.right = None, None

                    #Old fix, not working really at the moment
                    #next_node = current_sibling.right
                    #root_first_child= next_node
                    #current_node.left = current_node.right = None
                    #current_sibling.left = current_sibling.right = None

                    #and merge pass is updated with the melded version of the current_node and its sibling
                    merge_pass.append(self.meld(current_node, current_sibling))
                    #then we resttart the process with the third node(first node's right sibling's right sibling)
                    root_first_child = next_node


        #the final tree is at the last element of merge pass
        final_tree = merge_pass[len(merge_pass)-1]
        
        #then the final tree gets melded with the nodes behind it, per two-pass scheme requirements
        i=1
        while(i<=len(merge_pass)-1):
            final_tree = self.meld(final_tree, merge_pass[len(merge_pass)-1-i])
            i += 1
        
        #final_tree's last form will be the lone node and the result of the two-pass scheme
        return final_tree
    
    #severs the node
    def severnode(self, node):
        #if root, nothing to be severed
        if(node is self.mph):
            # if(node.right != None):
            #     node.right.left = None
            # node.right = node.left = None
            return

        #if not the root:
        else:
            #if the node is the most-left child(one more left is the parent)
            if(node.left.child == node):
                #then the nodes first_child property gets passed to its sibling to the right
                node.left.child = node.right
                #if the sibling has a right sibling, then it's left should point to the parent
                if(node.right != None):
                    node.right.left = node.left
                
                #and after the right sibling and parent realtionship is established, we can safely sever the connection to those two
                node.right = node.left = None
                return

            #if the node is not the leftmost child
            if(node.left.child != node):
                #the right sibling of it's left sibling gets to be the right sibling of this node(l->this node->r turns into l->r)
                node.left.right = node.right
                #if the node does have right sibling, then that right sibling will also get connected to the left sibling as doubly linked list
                if(node.right != None):
                    node.right.left = node.left 
                #then we can safely sever the connection now that the other two siblings are linked to each others
                node.right = node.left = None      
                return        
    
    #I don't use decreasekey operation as explained above Increasekey() comment, but I kept it regardless(I also havent tested the logic I have written thsi was more of a prototype)
    # def decreasekey(self, node, key_updated):
    #     #x points to the firstchild of the node
    #     x = node.child
    #     checker = 1
    #     while(x != None):
    #         if(key_updated<x.key):
    #             checker = 0
    #         x = x.right

    #     node.key = key_updated

    #     if(checker == 1 or node.child == None):
    #         # print("no restructuring needed!")
    #         return

    #     else:
    #         self.severnode(node)
    #         root_first_child = node.child
    #         root_first_child.left = None
    #         node.child = None

    #         isroot = 0
    #         if(self.mph is node):
    #             isroot = 1

    #         meld_subtree = self.meld(self.two_pass(root_first_child), node)
            
    #         if(isroot == 0):
    #             meld_subtree = self.meld(meld_subtree, self.mph)
            
    #         self.mph = meld_subtree
    #         return


#the class that defines properties of a flight
#https://docs.python.org/3/library/typing.html
class flight_class:
    #the flight id, airline id, submit time, priority and duration ahs to be given at all times
    flight_id : int
    airline_id : int
    submit_time : int
    priority : int
    duration : int

    #but the status, runway_id,start_time,end_time may not be given at the start and gets defined mid-logic
    status : Optional[str] = None
    runway_id : Optional[int] = None
    start_time : Optional[int] = None
    end_time : Optional[int] = None

    #selfnote:
    #ssh shahaddingafarov@thunder.cise.ufl.edu
    