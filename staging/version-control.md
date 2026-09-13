---
---
https://ericsink.com/vcbe/html/history_of_version_control.html
https://www.computer.org/csdl/journal/ts/2025/03/10821013/23d1xvEsT6M

## Problem (even today with version control)
I want to build a extension that allows you to save states of apps you care about. For example I would like to save the set of subscriptions from YouTube as of a specific date so that I can rollback to it or look at it whenever I want in the future. the idea is to minimize the cleaning and maintainance that needs to happen when you change the state of an application. For example deleting a subscription on youtube should be revertible by looking at a previous state that had that subscription. The idea is sort of a github for external applications rather than files.
What if you could embed in the current state the past states as well? So instead of saving the history you only ever save one state, but it inherently contains all the history and everything that happens it gets recorded

## What is version history
We have the power to decide what to keep a record of, and what to let go. This is a much more involved decision process than it might seem at first especially when it's not some boss at your company that is dictating this choice. For example, am I recording the kilograms of food I have eaten every day: if I don't I will never be able to take this decision back and record the past information again, but if I do I might end up wasting 10 minutes of my life every day.
This question becomes even harder to answer, at least for me, when the present conflicts with the past. For example, if I am keeping a record 

## Paper 
Let's say I am a butcher in Europe in medieval times. And let's say I wanted to update the price of my premiere meat: steak. I am just opening my shop around the town of Torrecchiara, Italy and it's January 1st of 1055 A.C. 
Other butchers around the city sell it for around 15 shillings per kilogram. So I decide to slightly undercut them by selling for 14. I buy a board to put outside my shop and write in big characters "$14" (Imagine $ is the symbol of shilling in 1055 Italy). Given I have a competitive price a lot of people start buying from me so I can soon afford to increase the price without losing customers. So on January 15th I increase to 16 shilling per kilogram. I go to my board outside, erase the "$14", and write "$16". And then again to 17 two weeks after and then again 18 a month after. However, that summer a really bad virus arrives that kills many of the cows and I am forced to bring my prices up to 35. I reggrettedly have to come every morning very early to change the price in the board outside before any customer arrives.  
As the year comes to an end, I start to put aside the money to give to the prince for taxes, but I have a problem: the prince is asking me to pay him based on the original price of the meat. But I only ever recorded the total prices of the sales, and I certainly don't want to assume that all those prices were based on the $35 of the last price hike. I would like to have the list of prices for each day of the year so that I could tell what the tax to pay is for each sale, but that's not something I recorded. I have lost some history, I need to do better for next year. For this year, I will just flee the city and not pay taxes. Who pays taxes in Italy anyways... 
It's the new year, and now I have a better system: I will keep a log of the prices each day, in a separate paper, and update the board outside with only the actual price for the day. Great, the version history of my prices is saved.

## Blockchain


## Git

## Perforce
