import unittest

class HashTable:
    """
    A class to represent a basic HashTable

    Attributes/Fields
    -----------------
    size : int
        size of hashtable instance representing total capacity
    slots: list
        list object to store keys after hashing - at location: hash(key)
    data: list
        list object to store data after hashing - at location: hash(key)

    Methods
    -------
    put(key, data)
    hashfunction(key, size)
    rehash(oldhash, size)
    get(key)
    __getitem__(key)
    __setitem__(key,data)
    __delitem__(key)
    __len__(self)
    __contains__(key)

    Unittests
    ---------
    testKeysAfterPuts
    testDataAfterPuts
    testDataAfterDelete
    testKeysAfterDelete
    testDataAfterDeleteCollision
    testKeysAfterDeleteCollision
    testLength
    testContainsTrue
    testContainsFalse
    testResize
    testOverfillRefillData
    testOverfillRefillKeys
    """

    def __init__(self, size):
        """ innit method which takes in size and stores key(slots) and data """
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size


    def put(self,key,data):
        """ Allows you to put keys and data into the hashtable using modulo division. This function will also rehash if
        a key becomes the same value as another key after the modulo division. It will take the oldhash and add one to
        move it into the next available slot. If the same key is used it will just replace the data already in under
        that key. If the amount of slots filled in the table is two less than the whole size of the table, the table
        resizes and adds 5 so the new table is 19 and a prime number. It then rehashes the keys and data
         in the previous table into the new larger table. """

        hashvalue = self.hashfunction(key, len(self.slots))

        if len(self) == self.size-2:

            oldData = self.data
            oldKeys = self.slots

            self.size = self.size * 2 + 5

            self.slots = [None] * self.size
            self.data = [None] * self.size

            while len(oldKeys) != 0:
                if oldKeys[0] == None:
                    oldData.remove(oldData[0])
                    oldKeys.remove(oldKeys[0])
                else:
                    self.put(oldKeys[0], oldData[0])
                    oldData.remove(oldData[0])
                    oldKeys.remove(oldKeys[0])

        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))
                while self.slots[nextslot] != None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot, len(self.slots))

                if self.slots[nextslot] == None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data

    def hashfunction(self, key, size):
        """ hashfunction which takes the key and modulo divides it by the size """
        return key % size

    def rehash(self, oldhash, size):
        """ rehash is used to handle collisions by adding 1 then modulo dividing the old hash """
        return (oldhash + 1) % size


    def get(self,key):
        """ The get function is used by taking a key and returning the data associated with it """
        startslot = self.hashfunction(key,len(self.slots))

        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and not found and not stop:
             if self.slots[position] == key:
                 found = True
                 data = self.data[position]
             else:
                 position=self.rehash(position,len(self.slots))
                 if position == startslot:
                     stop = True
        return data

    def __getitem__(self,key):
        """ This overrides the get item function to get the key """
        return self.get(key)

    def __setitem__(self,key,data):
        """ This overrides the setitem function to set the key and data when using the put function """
        self.put(key,data)

    def __delitem__(self, key):
        """ Using code from the put function, this function overrides the delete method by first checking that if a
        slot's hashvalue is equal to none that the data is also equal to none. It then goes through to find if the
        hashvalue is equal to the key that data and slots are switched to none. The next block goes through and
        rehashes in case of a collision. The last if/else makes sure that nextslot gets switched to none after the
        rehash. """
        hashvalue = self.hashfunction(key, len(self.slots))

        if self.slots[hashvalue] == None:
            self.data[hashvalue] = None
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = None
                self.slots[hashvalue] = None
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))
                while self.slots[nextslot] != None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot, len(self.slots))

                if self.slots[nextslot] == None:
                    self.data[nextslot] = None
                else:
                    self.data[nextslot] = None
                    self.slots[nextslot] = None

    def __len__(self):
        """ This length function interates through self.slots and returns a 1 for each time self.slots is not equal
        to none. The function is wrapped in a sum function that adds all the 1's together and returns the total
        slots that are filled. """
        return sum([1 for x in self.slots if x != None])

    def __contains__(self, key):
        """ This function simply checks if the key is in the self.slots """
        return key in self.slots


class TestHashTable(unittest.TestCase):
    """ Extend unittest.TestCase and add methods to test HashTable """

    def testKeysAfterPuts(self):
        """ Check that hashtable keys are as expected for simple case """
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        expected = [21, 27, None, None, 11, None, 6]
        self.assertEqual(h.slots, expected)

    def testDataAfterPuts(self):
        """ Check that hashtable data is as expected for simple case """
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        expected = ['bird', 'horse', None, None, 'dog', None, 'cat']
        self.assertEqual(h.data, expected)

    def testDataAfterDelete(self):
        """check that the data is deleted after deleting h[11]"""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        del h[11]
        expected = ['bird', 'horse', None, None, None, None, 'cat']
        self.assertEqual(h.data, expected)

    def testKeysAfterDelete(self):
        """Check that the key is deleted from the slots after deleting h[11] """
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        del h[11]
        expected = [21, 27, None, None, None, None, 6]
        self.assertEqual(h.slots, expected)

    def testDataAfterDeleteCollision(self):
        """Check that the data is deleted after forcing a collisions between h[18] and h[11]."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        h[18] = 'cobra'
        del h[18]
        expected = ['bird', 'horse', None, None, 'dog', None, 'cat']
        self.assertEqual(h.data, expected)

    def testKeysAfterDeleteCollision(self):
        """Check that the key is deleted after forcing a collisions between h[18] and h[11]."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        h[18] = 'cobra'
        del h[18]
        expected = [21, 27, None, None, 11, None, 6]
        self.assertEqual(h.slots, expected)

    def testLength(self):
        """Test that the length function is working to find number of filled slots."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        expected = 4
        self.assertEqual(len(h), expected)

    def testContainsTrue(self):
        """Test that the contains function is working by seeing if 27 is in the hashtable."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        expected = True
        self.assertEqual(27 in h, expected)

    def testContainsFalse(self):
        """Test that the contains function is working by checking for a number that wasn't added to the table."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        expected = False
        self.assertEqual(88 in h, expected)

    def testResize(self):
        """This function tests that the size of the hashtable doubles and adds 5 to get prime number 19
         when there are less than two slots available."""
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        h[18] = 'cobra'
        h[98] = 'sandwich'
        expected = 19
        self.assertEqual(h.size, expected)

    def testOverfillRefillData(self):
        """ This function tests that the size of the hashtable doubles and adds 5 to get prime number 19
         when there are less than two slots available then moves the data from the old hashtable and
         rehashes the values into the new larger table. """
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        h[18] = 'cobra'
        h[98] = 'sandwich'
        h[33] = 'telephone'
        h[56] = 'ghost'
        expected = ['sandwich', 'ghost', 'bird', None, None, None, 'cat', None, 'horse', None, None, 'dog', None, None,
                    'telephone', None, None, None, 'cobra']
        self.assertEqual(h.data, expected)

    def testOverfillRefillKeys(self):
        """ This function tests that the size of the hashtable doubles and adds 5 to get prime number 19
         when there are less than two slots available then moves the keys from the old hashtable and
         rehashes the values into the new larger table. """
        h = HashTable(7)
        h[6] = 'cat'
        h[11] = 'dog'
        h[21] = 'bird'
        h[27] = 'horse'
        h[18] = 'cobra'
        h[98] = 'sandwich'
        h[33] = 'telephone'
        h[56] = 'ghost'
        expected = [98, 56, 21, None, None, None, 6, None, 27, None, None, 11, None, None,
                    33, None, None, None, 18]
        self.assertEqual(h.slots, expected)


# main()
def main():
    """ Main function used to show examples and run test_hashtable tests """
    h = HashTable(7)
    h[6] = 'cat'
    h[11] = 'dog'
    h[21] = 'bird'
    h[27] = 'horse'
    print("-"*10, "keys and values", "-"*10)
    print(h.slots)
    print(h.data)
    print(len(h))
    print(h.size)

    # check that data was stored correctly
    print("-"*10, "data check", "-"*10)
    if h.data == ['bird', 'horse', None, None, 'dog', None, 'cat']:
        print("    + HashTable 'put' all items in correctly")
    else:
        print("    - items NOT 'put' in correctly")

    # check that 'in' operator works correctly
    print("-"*10, "in operator", "-"*10)
    if 27 in h:
        print("    + 'in' operator correctly implemented")
    else:
        print("    - 'in' operator NOT working")

    del h[11]
    # check that len() function is implemented and works
    print("-" * 10, "len() function", "-" * 10)
    if len(h) == 3:
        print("    + 'len' function works properly")
    else:
        print("    - 'len' function NOT working")

    # "in" operator (returns a boolean)
    print("-" * 10, "len() after deletion", "-" * 10)
    if 11 not in h:
        print("    + 'in' operator works correctly after 11 was removed")
    else:
        print("    - 'in' operator OR 'del' NOT working")

    # check that data was also removed
    print("-" * 10, "data after deletion", "-" * 10)
    if h.data == ['bird', 'horse', None, None, None, None, 'cat']:
        print("    + data is correct after deletion")
    else:
        print("    - data not correctly removed after deletion")


def unittest_main():
    """Run's unnitest's main which runs all of the class TestHashTable's methods """
    print("-"*25, "running unit tests", "-"*25)
    unittest.main()


if __name__ == '__main__':
    main()
    unittest_main()
    test = TestHashTable
