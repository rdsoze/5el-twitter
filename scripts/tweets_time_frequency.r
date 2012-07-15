tdata <- read.csv(file="/tmp/temp.data.csv",head=FALSE,sep=",")
plot(tdata$V1, type="l", col="red")
lines(tdata$V4, col="green")
