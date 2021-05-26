

class SuffixArray:
    END_CHAR = "$"

    def __init__(self, string:str):
        self.string = string + self.END_CHAR
        self.length = len(self.string)
        self.suffix_array = [i for i in range(self.length)]
        self.index_array = [None for _ in range(self.length)]
        self.rank_array = [i for i in range(self.length)]
        self.temp_array = [1 for _ in range(self.length)]


    def __str__(self):
        return str(self.suffix_array)


    def construct(self):
        # first sort the suffixes based on first two characters

        self.suffix_array.sort(key= lambda x: self.string[x:x + 2])
        self.rank_array = [ord(char) for char in self.string]

        # sort suffix array using prefix doubling
        k=1
        while 2*k <= self.length:
            flag = False
            print(self.suffix_array)
            print([self.rank_array[i] for i in self.suffix_array])
            print("---", k)
            for i in range(self.length-1):
                if self.rank_array[self.suffix_array[i]] < self.rank_array[self.suffix_array[i+1]]:
                    self.temp_array[self.suffix_array[i+1]] = self.temp_array[self.suffix_array[i]] + 1
                elif self.rank_array[self.suffix_array[i]] > self.rank_array[self.suffix_array[i+1]]:
                    self.temp_array[self.suffix_array[i + 1]] = self.temp_array[self.suffix_array[i]]
                    self.temp_array[self.suffix_array[i]] += 1
                else:
                    # print(self.suffix_array[i], self.rank_array[self.suffix_array[i]+k])
                    # print(self.suffix_array[i+1], self.rank_array[self.suffix_array[i+1] + k])
                    # print()
                    if self.rank_array[self.suffix_array[i]+k] < self.rank_array[self.suffix_array[i+1]+k]:
                        self.temp_array[self.suffix_array[i + 1]] = self.temp_array[self.suffix_array[i]] + 1
                    elif self.rank_array[self.suffix_array[i]+k] > self.rank_array[self.suffix_array[i+1]+k]:
                        self.temp_array[self.suffix_array[i + 1]] = self.temp_array[self.suffix_array[i]]
                        self.temp_array[self.suffix_array[i]] += 1
                        flag = True
                    else:
                        self.temp_array[self.suffix_array[i+1]] = self.temp_array[self.suffix_array[i]]
                print("--", [self.temp_array[i] for i in self.suffix_array])

            self.rank_array = self.temp_array[::]
            # self.temp_array = [1 for _ in range(self.length)]
            temp_arr = [[] for i in range(max(self.rank_array))]
            for i in range(self.length):
                temp_arr[self.rank_array[i]-1].append(i)
            temp_suffix_array = []
            for i in range(len(temp_arr)):
                temp_suffix_array.extend(temp_arr[i])
            self.suffix_array = temp_suffix_array[::]

            k = 2**k

if __name__=="__main__":
    input_str = "MISSISSIPPI"
    sa = SuffixArray(input_str)
    sa.construct()
    print(sa)