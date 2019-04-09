import ctypes


# Implements the Array ADT using array capabilities of the ctypes module.

class Array:
    '''Represents class Array'''

    def __init__(self, size):
        '''
        Creates an array with size elements.
        :param size: size of the array
        '''
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    def __len__(self):
        '''
        Returns the length of an array
        :return: int
        '''
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        '''
        Gets the content of the index element.
        :param index:index of element to return
        :return: element over the index
        '''
        if index < 0 or index >= len(self):
            raise IndexError
        return self._elements[index]

    def __setitem__(self, index, value):
        '''
        Puts the value in the array element at index position.
        :param index: the index of element
        :param value: the value of element
        :return: None
        '''
        if index < 0 or index >= len(self):
            raise IndexError
        self._elements[index] = value

    def clear(self, value):
        '''
        Clears the array by setting each element to the given value.
        :param value: value to replace
        :return: None
        '''
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        '''
        Returns the array's iterator for traversing the elements.
        :return: ArrayIterator
        '''
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    '''An iterator for the Array ADT.'''

    def __init__(self, the_array):
        '''
        Initialise an ArrayIterator
        :param the_array: Array
        '''
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        '''
        The process of iteration
        :return: ArrayIterator
        '''
        return self

    def __next__(self):
        '''
        Gets the next element
        :return: next element
        '''
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# Implementation of the Array2D ADT using an array of arrays.

class Array2D:
    '''Creates a 2 -D array of size numRows x numCols.'''

    def __init__(self, num_rows, num_cols):
        '''
        Create a 1 -D array to store an array reference for each row.
        :param num_rows: int
        :param num_cols: int
        '''
        self.rows = Array(num_rows)
        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    def num_rows(self):
        '''
        Returns the number of rows in the 2 -D array.
        :return: int
        '''
        return len(self.rows)

    def num_cols(self):
        '''
        Returns the number of columns in the 2 -D array.
        :return: int
        '''
        return len(self.rows[0])

    def clear(self, value):
        '''
        Clears the array by setting every element to the given value.
        :param value:
        :return:
        '''
        for row in self.rows:
            row.clear(value)

    def __getitem__(self, index_tuple):
        '''
        Gets the contents of the element at position [i, j]
        :param index_tuple: tuple
        :return: int
        '''
        if len(index_tuple) == 2:
            raise IndexError("Invalid number of array subscripts.")
        row = index_tuple[0]
        col = index_tuple[1]
        if row < 0 or row > self.num_rows() or col < 0 or col > self.num_cols():
            raise IndexError("Array subscript out of range.")
        array_1d = self.rows[row]
        return array_1d[col]

    def __setitem__(self, index_tuple, value):
        '''
        Sets the contents of the element at position [i,j] to value.
        :param index_tuple: int
        :param value: int
        :return: None
        '''
        if len(index_tuple) > 2:
            raise IndexError("Invalid number of array subscripts.")
        row = index_tuple[0]
        col = index_tuple[1]
        if row < 0 or row > self.num_rows() or col < 0 or col > self.num_cols():
            raise IndexError("Array subscript out of range.")
        array_1d = self.rows[row]
        array_1d[col] = value


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""
    DEFAULT_CAPACITY = 1

    def __init__(self):
        """
        Create an empty array."
        """""
        self._n = 0  # count actual elements
        self._A = self._make_array(DynamicArray.DEFAULT_CAPACITY)  # low-level array

    def __len__(self):
        """
        Return number of elements stored in the array.
        :return: int
        """
        return self._n

    def __getitem__(self, k):
        """
        Return element at index k.
        :param k: int
        :return: value
        """
        if not 0 <= k < self.n:
            raise IndexError('invalid index')
        return self._A[k]  # retrieve from array

    def append(self, obj):
        """
        Add object to end of the array.
        :param obj: value to append
        :return: None
        """
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):  # nonpublic utitity
        """
        Resize internal array to capacity c.
        :param c: int
        :return: None
        """
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array

    def _make_array(self, size):  # nonpublic utitity
        """
        Return new array with capacity c.
        :param c: int
        :return: an array
        """
        return Array(size)  # see ctypes documentation

    def insert(self, k, value):
        """
        Insert value at index k, shifting subsequent values rightward.
        :param k: int
        :param value:value
        :return: None
        """
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """
        Remove first occurrence of value( or  raise ValueError).
        :param value: value
        :return: 0
        """
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item

                return  # exit immediately
        raise ValueError("value not found")  # only reached if no match
