from arrays import Array


class Encoder:
    '''
    This is a class for Encoder representation
    '''

    def __init__(self, message):
        '''
        Initialises an Encoder class
        :param message:str
        '''
        self.message = message

    @staticmethod
    def _encode_letter(letter):
        '''
        Encodes a letter
        :param letter: str
        :return: tuple
        '''
        return (ord(letter) // 16), (ord(letter) % 16)

    def convert(self):
        '''
        Returns the array of angles on which a camera should turn.
        :return:Array
        '''
        lst_indexes = []
        for el in self.message:
            lst_indexes.append(self._encode_letter(el))
        print("lst", lst_indexes)
        ar = Array(len(self.message) * 2)
        index = 0
        sum = 0
        for el in self.message:
            ar[index] = self._encode_letter(el)[0] * 22.5 - sum
            sum += ar[index]
            ar[index + 1] = 22.5 * self._encode_letter(el)[1] - sum
            sum += ar[index + 1]
            index += 2
        return ar


class Decoder:
    '''This class represents a Decoder'''

    def __init__(self, array):
        '''
        Initialises a Decoder
        :param array: Array
        '''
        self.array = array

    @staticmethod
    def _decode_letter(digit):
        '''
        Decodes a letter
        :param digit: list
        :return: letter
        '''
        return chr(digit[0] * 16 + digit[1])

    def decode(self):
        '''
        Decodes a message
        :return:str
        '''
        angle = 0
        text = ""
        nums = []
        for i in range(0, len(self.array), 2):
            tup = [None, None]
            angle += self.array[i]
            tup[0] = int(angle // 22.5)
            angle += self.array[i + 1]
            tup[1] = int(angle // 22.5)
            nums.append(tup)
        for num in nums:
            text += self._decode_letter(num)
        return text


e = Encoder("Hello from Earth")
convertor = e.convert()
final_nums = []
for index in range(len(convertor)):
    final_nums.append(convertor.__getitem__(index))
print(final_nums)
d = Decoder(
    [90.0, 90.0, -45.0, -22.5, 22.5, 135.0, -135.0, 135.0, -135.0, 202.5, -292.5, -45.0, 135.0, 0.0, 22.5, -112.5, 90.0,
     202.5, -202.5, 157.5, -247.5, -45.0, 90.0, 22.5, 22.5, -112.5, 135.0, -112.5, 112.5, -67.5, 45.0, 45.0])
print(d.decode())
