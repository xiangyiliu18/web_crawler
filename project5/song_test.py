leet_speak_name = input()
leet_speak_file = open("leet_speak_file.txt", "w")


def leet_speak(words_list):
    with open(words_list, 'r') as f:
        for line in f:
            line = line.replace('a', '4').replace('A', '4')
            line = line.replace('e', '3').replace('E', '3')
            line = line.replace('l', '1').replace('L', '1')
            line = line.replace('t', '7').replace('T', '7')
            line = line.replace('o', '0').replace('O', '0')
            leet_speak_file.write(line)
        f.close()
    leet_speak_file.close()


leet_speak(leet_speak_name)

# lowercase_uppercase = input()
# lower_upper = open("lower_upper.txt", "w")
#
#
# def lower_upper_permutation(words_list):
#     with open(words_list, 'r') as f:
#         for line in f:
#             temp = list(capitalization_permutations(line))
#             for item in temp:
#                 lower_upper.write("%s" % item)
#         f.close()
#     lower_upper.close()
#
#
# def capitalization_permutations(s):
#     """Generates the different ways of capitalizing the letters in
#     the string s."""
#
#     # >>> list(capitalization_permutations('abc'))
#     # ['ABC', 'aBC', 'AbC', 'abC', 'ABc', 'aBc', 'Abc', 'abc']
#     # >>> list(capitalization_permutations(''))
#     # ['']
#     # >>> list(capitalization_permutations('X*Y'))
#     # ['X*Y', 'x*Y', 'X*y', 'x*y']
#
#     if s == '':
#         yield ''
#         return
#     for rest in capitalization_permutations(s[1:]):
#         yield s[0].upper() + rest
#         if s[0].upper() != s[0].lower():
#             yield s[0].lower() + rest
#
#
# lower_upper_permutation(lowercase_uppercase)


# words_list = input()
# file = open("reversed_words.txt", "w")
#
#
# def reverse_chars(words_list):
#     with open(words_list, 'r') as f:
#         for line in f:
#             file.write(reverse(line))
#             # print(reverse(line))
#         f.close()
#     file.close()
#
#
# # Function to reverse a string
# def reverse(string):
#     string = string[::-1]
#     return string
#
#
# reverse_chars(words_list)