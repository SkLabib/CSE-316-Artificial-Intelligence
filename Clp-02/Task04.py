text = "apple banana apple orange banana apple"
words = text.split()
WordCount = {}
for word in words:
    if word in WordCount:
        WordCount[word] += 1
    else:
        WordCount[word] = 1

print(WordCount)
