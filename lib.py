import re
import math

def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def dataCleaner(dataDict):
    # change '\n \r \t' to ' '
    for key in  dataDict:
        dataDict[key] = re.sub(r"[\n\r\t]", " ", dataDict[key])
    
    # remove emojies
    for key in dataDict:
        dataDict[key] = remove_emoji(dataDict[key])

    # correction
    for key in dataDict:
        dataDict[key] = re.sub(r"[.?!@#$%^&*()+\-=\<>:;'\"|~`_{}\[\]\\/]", " ", dataDict[key])
        dataDict[key] = re.sub("[؟×÷«»,،]", " ", dataDict[key])
        dataDict[key] = dataDict[key].replace("ـ", "")
        dataDict[key] = re.sub("\u200c+", " ", dataDict[key])
        dataDict[key] = re.sub(r"^\s+", "", dataDict[key])
        dataDict[key] = re.sub(r"\s+$", "", dataDict[key])
        dataDict[key] = re.sub(r"\s+", " ", dataDict[key])

    # remove stopwords
    with open("stopwords.txt", encoding='utf8') as file:
        for word in file.readlines():
            for key in  dataDict:
                dataList = dataDict[key].split(" ")
                if str.strip(word) in dataList:
                    while True:
                        try:
                            dataList.remove(str.strip(word))
                        except ValueError:
                            break
                    dataDict[key] = " ".join(dataList)
                    print("stopwords..." + str.strip(word) + "..." + key)

    # remove void items
    pop_queue = []
    for key in dataDict:
        if re.sub("\\s+", "", dataDict[key]) == "":
            pop_queue.append(key)
    for key in pop_queue:
        dataDict.pop(key)
    

    return dataDict

def tf(term, documentText):
    count = 0
    total = 0

    for word in documentText.split(" "):
        if word == term:
            count += 1
        total += 1

    return count / total

def df(term, documentDict):
    count = 0

    for key in documentDict:
        if term in documentDict[key]:
            count += 1
    
    return count


def idf(doc_count, term_df):
    return math.log10(doc_count / term_df)