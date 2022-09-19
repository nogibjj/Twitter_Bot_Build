# Twitter_Bot_Build
This depository is built as a Twitter bot to search recent Twitter, analyze tweets, sort accounts with specific conditions, and send messages. 

This project has five steps:
1. Build Searching bot to find recently twits with key words
2. Build Analysis function for searching result (Finance related information, social media, NLP)
3. Build a sort function for twits, using Twits information to sort users.
4. Build function for sending direct message for the specific users.
5. Round up project to use cloud service to run the bot automatically.


## 1. Searching Twitter
The first step of this project is searching for tweets containing particular keywords.  And save it as a CSV file into AWS S3.
Before we dive into the code, there are a few things we need to finish the setup:
* Apply for Twitter Developer Account
* Set up AWS S3
 
 ### Twitter Developer Account set up here: 
 https://developer.twitter.com/en/portal/dashboard
 
 Set up the regular developer account since it is fast to approve, but if you need more functions, you can apply Twitter academic research account to get more access to data and operations: https://developer.twitter.com/en/products/twitter-api/academic-research

### The AWS S3 is mainly used for data management and automation.  
You can set up your S3 functions here: https://s3.console.aws.amazon.com/s3/buckets?region=us-east-2



