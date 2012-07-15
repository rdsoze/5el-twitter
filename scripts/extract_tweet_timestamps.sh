python temporalData.py > /tmp/tweet_time.txt

 cut -d" " -f1,2,3,4 /tmp/tweet_time.txt | cut -d":" -f1,2 | awk 'BEGIN{OFS=FS=""}{$(NF)=""}1' | uniq -c  | awk '{ print $1","$2","$3","$4}'  > /tmp/temp.data.csv
