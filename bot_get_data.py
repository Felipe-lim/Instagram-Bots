"""

This program was made with the objective of getting some informations from profiles on Instagram.
It gets informations such as followers, following, number of likes and comments,
avarage number of likes and comments per publication and avarage number of comments and likes
in the last 10 publications.

"""

from instabot import Bot
import numpy as np
import pandas as pd
from time import sleep


bot = Bot()
#declaring accounts to be accessed
ext_users = ['list of counts you want to extract information']
#list with accounts ids
ext_ids = []


#login
bot.login(username="your_username", password="yout_password")

#filling the list with ids from accounts
n=0
for x in ext_users:
    ext_ids.append(bot.get_user_id_from_username(ext_users[n]))
    n += 1


#gdata = general data
gdata = [] 

#Loading followers, following, avg likes from last 10, general avg likes and number of likes. Also all that to comments

n=0
for x in ext_ids:

    #getting followers and following
    nfollowing = bot.get_user_following(ext_ids[n])
    nfollower = bot.get_user_followers(ext_ids[n])

    #gets the id of all publications on the profile
    extmedia = bot.get_total_user_medias(ext_ids[n])

    #gets number of pubs in each profile
    nmce = len(extmedia)
    

    cont=0
    n2 = 0
    nlikes = 0
    nlikes10 = 0
    ncomments = 0
    ncomments10 = 0


    #gets the like and comment data
    for x in extmedia: 

        #likes
        likes = bot.get_media_likers(extmedia[n2])
        #print('\n likes', '\n', extmedia[n2], likes,'\n')
        nlikes += len(likes)

        #comenarios
        comments = bot.get_media_commenters(extmedia[n2])
        #print('\n comentarios', '\n', extmedia[n2], comments,'\n')
        ncomments += len(comments)
        
        #avg of last 10
        if n2 < 10:
            nlikes10 += len(likes)
            ncomments10 += len(comments)
            cont +=1
        n2 +=1

    #avarage likes and comments
    like_avg = nlikes//(nmce)
    like10_avg = nlikes10 // cont

    comment_avg = ncomments // (nmce)
    comment10_avg = ncomments10 // cont

    #adding all the data to a list
    gdata.append(len(nfollowing))
    gdata.append(len(nfollower))
    gdata.append(nmce)

    gdata.append(like10_avg)
    gdata.append(like_avg)
    gdata.append(nlikes)

    gdata.append(comment10_avg)
    gdata.append(comment_avg)
    gdata.append(ncomments)

    n += 1



#making a table
data = np.array(gdata).reshape(len(ext_ids), 9 )
columns = ['following', 'followers', 'np', 'avgl10', 'avgl', 'nl', 'avgc10', 'avgc', 'nc']

#np = number of pubs
#avgl10 = avarage of likes from last 10 pubs
#avgl = avarage of likes
#nl = number of likes on profile
# avgc10 = avarage of comments from last 10 pubs
# avgc = avarage of comments
# nc = number of comments on profile


main_table = pd.DataFrame(data=data, index=ext_users,columns=columns)

print('\n\n', main_table)
