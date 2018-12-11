import json
combine_file = open("results.txt", 'w')
combined_list = []

with open("words_list.txt", mode="r") as f:
    for line in f:
        combined_list.append(line.strip())
    f.close()
    for i in range(0, len(combined_list)):
        for j in range(0, len(combined_list)):
            log = combined_list[i]
            pwd = combined_list[j]
            obj = log + " " +pwd
            combine_file.write(obj)
            combine_file.write('\n')
combine_file.close()