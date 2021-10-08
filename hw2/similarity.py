import math as math
import sys
import time as time

if len(sys.argv) < 3:
    print("Usage:")
    print("$ python3 similarity.py <data_file> <output_file> \
    [user_thresh (default = 5)]")
    sys.exit()

data_file = sys.argv[1]
output_file = sys.argv[2]

if len(sys.argv) <4:
    user_thresh = 5
else:
    user_thresh = int(sys.argv[3])

ref_file = open(data_file, "r")
output = open(output_file, "w")

time0 = time.time()

#the dictionary that we will use in this code
movie_data = {}

#two pieces of information that we will need
#in the final print
nb_lines = 0
user_database = set()

for line in ref_file:
    nb_lines +=1
    user_id = int(line.split()[0])
    user_database.add(user_id)
    movie_id = int(line.split()[1])
    rate = int(line.split()[2])
    if movie_id in movie_data:
        movie_data[movie_id][user_id]=rate
    else:
        movie_data[movie_id]={}
        movie_data[movie_id][user_id]=rate

ref_file.close()

def get_common_users(movie_data,m1,m2):
    '''this function enables us to get the common users
    that ranked movie m1 and movie m2'''
    return set(movie_data[m1]) & set(movie_data[m2])

def average_rating(movie_data,m1):
    '''this function returns the average rating of
    movie m1'''
    ave = 0
    for k in movie_data[m1].values():
        ave += int(k)
    ave = ave / len(movie_data[m1])
    return(ave)

def similarity(movie_data,m1,m2,user_thresh):

    '''This function calculates the cosine similarity
    between movies m1 and m2.
    It doesn't calculate the similarities if the movies
    have less than user_thresh common users.
    If the denominator equals 0, it considers that the
    movies have no relation.'''

    com_users = get_common_users(movie_data,m1,m2)
    if len(com_users) <=user_thresh:
        return "None",0

    av_m1 = average_rating(movie_data,m1)
    av_m2 = average_rating(movie_data,m2)

    up_part = 0
    low_part_m1 = 0
    low_part_m2 = 0

    for user in com_users:
        rating_m1 = movie_data[m1][user]
        rating_m2 = movie_data[m2][user]
        up_part += (rating_m1-av_m1)*(rating_m2-av_m2)
        low_part_m1 += (rating_m1-av_m1)**2
        low_part_m2 += (rating_m2-av_m2)**2

    if low_part_m1 == 0 or low_part_m2 == 0:
        return 0,len(com_users)

    similarity = up_part/math.sqrt(low_part_m1*low_part_m2)

    return round(similarity,2),len(com_users)

def get_similar_movie(movie_data,m1):
    '''This function finds the most similar movie for
    movie m1. It also returns the value of the cosine
    similarity between these 2 movies (this value is
    initiated at -2 to be sure that it will be lower
    than every value computed).'''

    similar_movie = "None"
    similarity_value = - 2
    nb_com_users = 0

    for m2 in movie_data.keys():
        if m2 != m1:
            similar,com_users = similarity(movie_data,m1,m2,user_thresh)
            if similar != "None":
                if similar > similarity_value:
                    similar_movie = m2
                    similarity_value = similar
                    nb_com_users = com_users

    return similar_movie,similarity_value,nb_com_users

most_similar = {}

for m1 in movie_data.keys():
    simi_data = get_similar_movie(movie_data,m1)
    most_similar[m1]=simi_data

list_movies = set(most_similar)

for m1 in list_movies:
    m1_data = most_similar[m1]
    if m1_data[0] == "None":
        output.write("{}\n".format(m1))
    else:
        m1_output = "{} ({},{},{})\n"\
    .format(m1,m1_data[0],m1_data[1],m1_data[2])
    output.write(m1_output)

output.close()

total_time=round(time.time()-time0,3)

print("Input MovieLens file: {}".format(data_file))
print("Output file for similarity data: {}".format(output_file))
print("Minimum number of common users: {}".format(user_thresh))
len_users = len(user_database)
len_movies = len(movie_data.keys())
print("Read {} lines with total of {} movies and {} users"\
.format(nb_lines,len_movies,len_users))
print("Computed similarities in {} seconds".format(total_time))

