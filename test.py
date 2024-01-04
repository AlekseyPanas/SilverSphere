import timeit
import math
import heapq


def time_seq_loops():
    def hi():
        for i in range(200):
            math.factorial(150)

    def bye():
        for i in range(300):
            math.factorial(150)


    def test():
        for i in range(4000):
            hi()
            bye()


    def test2():
        for i in range(4000):
            hi()
        for i in range(4000):
            bye()


    t = timeit.timeit("test()", globals={"test": test}, number=1)
    print(t)

    t = timeit.timeit("test2()", globals={"test2": test2}, number=1)
    print(t)


def heaptest():
    x = []
    heapq.heappush(x, (1,"hi"))
    heapq.heappush(x, (2, "hii"))
    heapq.heappush(x, (3, "hiii"))
    heapq.heappush(x, (4, "hiiii"))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))


if __name__ == "__main__":
    heaptest()
