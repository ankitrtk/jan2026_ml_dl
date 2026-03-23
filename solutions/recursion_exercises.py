def string_permutations(letters):
    result = ['']

    for c in letters:
        new_result = []

        for word in result:
            for i in range(len(word) + 1):
                new_result.append(word[:i] + c + word[i:])
        result = new_result
    return len(result), result


# print(string_permutations('abcd'))


class LineModel:  # y = mx + c
    def fit(data):
        x1, y1 = data[0]

        x2, y2 = data[1]

        self.m =

        self.c =


    def predict(x_new):
        # return x_new*m + c

        return ....
