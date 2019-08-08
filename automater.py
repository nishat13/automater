# import modules and libraries needed
import pandas as pd
import sys
import re

# global file variable
file_name = 'databook_previous_edition.csv' # list of current books linked to previous editions
database = 'export_book.csv' # all book titles stored in database


# create dataframe
df = pd.read_csv(file_name)
database = pd.read_csv(database)


# return list of books based on partial title
def find_all_titles(partial_title, mode):
    mode = str(mode)
    list = []
    rows = database.loc[database['DATABOOK NAME'].str.contains(str(partial_title))]
    for index, row in rows.iterrows():
        title = str(row['DATABOOK NAME']) # get title in string format
        book_id = row['DATABOOK ID'] # get id
        edition = re.findall('\w+(?=\sEdition)', title)
        if mode == "edition":
            list.append(edition[0])
        elif mode == "title":
            list.append(title)
        elif mode == "book_id":
            list.append(book_id)
        else:
            raise Exception("Invalid Mode")
    return list


# get previous edition of a certain specified title
def getPrevEd(book_title):
    try:
        rindex = df.loc[df['Databook Name'] == str(book_title)].index.values.astype(int)[0]
        edition = df.loc[rindex, 'Previous Databook Name']
        edition = str(edition)
    except Exception as e:
        print(e)
        edition = "NULL"

    return edition


# return list of books with certain cue words that indicate they should not have editions
def getList(cue_word):
    list = []
    cue_word = str(cue_word)
    rows = df.loc[df['Databook ID'] != 0]
    for index, row in rows.iterrows():
        title = str(row['Databook Name']) # get title in string format

        if cue_word in title:
            list.append(title)
    return list


# get all titles in database
def getList():
    list = []
    rows = database.loc[database['DATABOOK ID'] != 0]
    for index, row in rows.iterrows():
        title = str(row['DATABOOK NAME']) # get title in string format
        list.append(title)

    return list


if __name__ == "__main__":

    # get previous edition of single argument
    edition = getPrevEd(sys.argv[1])
    print("PREVIOUS EDITION: " + edition)

    # determine partial title from given title and attempt to match all similar titles
    temp = sys.argv[1]
    length = len(temp.split())
    length = length // 2
    new_string = ""

    for i in range(length):
        if new_string != "":
            new_string = new_string + " " + temp.split()[i]
        else:
            new_string = new_string + temp.split()[i]

    find_all_titles(sys.argv[1], sys.argv[2])
    find_all_titles(sys.argv[1], sys.argv[3])


    # get previous edition of each of the partial title matches
    input = sys.argv[4]# ie: "Airworthiness"
    cuewordlist = find_all_titles(input, "title")

    for i in range(0,len(cuewordlist)):
        edition = getPrevEd(str(cuewordlist[i]))
        if edition != "NULL":
            print("BOOK: " + cuewordlist[i])
            print("-->PREVIOUS EDITION: " + edition)
        else:
            print("(NO EDITION MATCHED):" + cuewordlist[i])










