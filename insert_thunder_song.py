import csv

def insert_thunder_song():
    with open('/home/work/work/song/30W.csv', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            print row[0]
            print row[1]
            print row[2]
            print row[3]

#def insert_thunder_song():
    #with open('/home/work/work/song/o2o-140.csv', 'r') as f:
        #reader = csv.reader(f)
        #for row in reader:
            #print row[0]
            #print row[1]
            #print row[2]
            #print row[3]

def main():
    insert_thunder_song()

if __name__ == "__main__":
    main()
