sentence = str(input("Enter a sentence: "))

words = sentence.split()
count=0
for word in words:
    count += 1
print("Number of words:", count)

char_count = len(sentence)
print("Number of characters:", char_count)

def vowel():
    count = 0
    for i in sentence:
        if i.lower() in 'aeiou':
            count += 1
    print("Number of vowels:", count)

vowel()