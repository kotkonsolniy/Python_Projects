import pickle

class FibonacciIterator:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result


fib_iter = FibonacciIterator(10) # create итератор


serialized_iter = pickle.dumps(fib_iter)


deserialized_iter = pickle.loads(serialized_iter)


for num in deserialized_iter:
    print(num)