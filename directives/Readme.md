category,delay,initial,dropPercentage,dropAmount,timeInterval,maxOfferPercentage
#this directive file describes how to give offers on each item in a specific category
#category: the matching ebay category. writing "default" here will create one that applies to each item if it doesn't have a directive in here
#delay: this is an integer number that states a number of days to wait before starting to send offers out to buyers
#initial: this is a decimal number that states the start of the percentage off to send to buyers once the delay period has passed
#these two are better used exclusevly but it is not impossible to use both at the same time
#dropPercentage: this is a decimal number that is multiplied by the number of timeIntervals that have passed after the delay period and then added to the percentage off.
#dropAmount: this is a decimal number that is subtracted from the offer amount for each timeIntervals that have passed after the inital percentage has been taken off.
#timeInterval: this is an integer number of days. it will be used by taking the number of days since the delay period and then dividing that figure by timeInterval and then rounding down.
#maxOfferPercentage: this is a decimal number which limits offers to only take up to this percentage off

#here is an example default offer directive
#it waits 2 weeks before sending out 5% offers (the minimum allowable by eBay) and then increases 
# the percentage off by a half percentage every week.
# by day 30 this particular directive sends out 6% off offers
default,14,5,0.5,0,7,0.50
