#!/usr/bin/env python3
#@author: Deniz Sert
#@version: Saturday 2/15/20, Friday 2/21/20

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for lab 2 will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).

def load_a_pickle(self):
    '''
    Loads a pickle file (yum!)
    '''
    filename = 'resources/names.pickle'
    with open(filename, 'rb') as f:
        self.data = pickle.load(f)

def actor_from_id(actor_id):
    '''
    Takes in an actor_id, returns the actor's name
    '''
    with open('resources/names.pickle', 'rb') as f: #open pickle file
        names = pickle.load(f)
    for key in names:
        if names[key] == actor_id:
            return key
    return("Actor not in dataset")

def id_from_actor(actor_name):
    '''
    Takes in an actor's name, returns the actor's ID
    '''
    with open('resources/names.pickle', 'rb') as f:
        names = pickle.load(f)
    if actor_name in names: #loop thru pickle data
        return names[actor_name]
    return("Actor not in dataset")

def movie_from_id(id_name):
    '''
    Takes in movie ID; returns the movie name.
    '''
    with open('resources/movies.pickle', 'rb') as f:
        movies = pickle.load(f)
    for key in movies: #loop thru pickle data
        if movies[key] == id_name:
            return key
    return("Movie not in dataset")

def id_from_movie(movie_name):
    '''
    Takes in an movie's name, returns the movie's ID
    '''
    with open('resources/movies.pickle', 'rb') as f:
        movies = pickle.load(f)
    if movie_name in movies: #loop thru pickle file
        return movies[movie_name]
    return("Actor not in dataset")



def acted_together(data, actor_id_1, actor_id_2):
    #return True if both id's are in the Dataset Values
    for tup in data:
        if actor_id_1 in tup and actor_id_2 in tup:
            return True
    return False


def actors_with_bacon_number(data, n):
    '''
    Takes in a pickle data file and the number of bacon iterations; returns actors with that data set
    '''
    #initializes dictionaries and sets
    actor_web = create_actor_dictionary(data)
    nodes_from_bacon = {0: {4724}}
    given_bacon = {4724}

    #returns Bacon's actors
    if n == 1:
        return actor_web[4724]

    iteration = 0
    while iteration < n: #rerun general algorithm until n has been reached
        for previous_actor in nodes_from_bacon[iteration]: #loop representing layers
            for actor in actor_web[previous_actor]: #loop through previous actor's neighbors
                if actor not in given_bacon: #assign a bacon number to neighbors
                    given_bacon.add(actor)
                    nodes_from_bacon.setdefault(iteration+1, set()).add(actor)

        iteration += 1
        if iteration not in nodes_from_bacon: #if nodes_from_bacon[iteration] does not exist, return an empty set
            return set()
    return nodes_from_bacon[n]


def bacon_path(data, actor_id):
    '''
    Creates a path from Bacon to input Actor.
    '''
    return actor_to_actor_path(data, 4724, actor_id)

def create_actor_dictionary(data):
    '''
    Organizes pickle data to a dictionary mapping actor_1: {set of actors who acted with actor_1}
    '''
    actor_web = {4724: set()}
    # build actor dictionary
    for tup in data:
        actor_web.setdefault(tup[0], set()).add(tup[1])
        actor_web.setdefault(tup[1], set()).add(tup[0])
    return actor_web

def create_movie_dictionary(data):
    '''
    Organizes pickle data to a dictionary mapping each movie: {set of actors in movie}
    '''
    movie_web = {}
    for tup in data: #loop thru tuples in the pickle file (actor1, actor2, movieID)
        for i in range(2):
            movie_web.setdefault(tup[2], set()).add(tup[i])
    return movie_web


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    '''
    Creates a path from Bacon to input Actor.
    '''
    def is_actor(a2):
        return actor_id_2 == a2

    return actor_path(data, actor_id_1, is_actor)

def movie_path(data, actor_id_1, actor_id_2):
    '''
    This function takes in 2 actors; returns a sequence of movies to watch that connects the actors.
    '''
    actor_path = actor_to_actor_path(data, actor_id_1, actor_id_2)
    actors_to_movies = {}
    movie_list = []

    for tup in data: #organize data into a dictionary
        actors_to_movies[frozenset((tup[0], tup[1]))] = tup[2]


    for i in range(len(actor_path)-1): #loop thru actors in actor_to_actor path and pair each one to a movie
        movie_list.append(actors_to_movies.get((frozenset((actor_path[i], actor_path[i+1])))))

    return movie_list



def actor_path(data, actor_id_1, goal_test_function):
    '''
    Creates a path from Bacon to input Actor, given a specific goal to sort.
    '''

    if goal_test_function(actor_id_1): #check if inputted actor is the destination node
        return [actor_id_1]
    # intitialize agenda(list) actor_web (actor: set of neighbor actors), actor_parents (child: parent)
    visited = set()
    agenda = [actor_id_1]
    actor_parents = {}
    actor_web = create_actor_dictionary(data)
    destination_actor = None

    while agenda:  # keep looping while agenda has items in it
        current_node = agenda.pop(0)
        visited.add(current_node)
        if goal_test_function(current_node):  # checks if the input goal has been reached
            destination_actor = current_node
            break
        else:
            for neighbor_node in actor_web[current_node]:  # checking neighbors of current node
                if neighbor_node not in visited:
                    agenda.append(neighbor_node)  # add to agenda
                    actor_parents.setdefault(neighbor_node,
                                             current_node)  # if the dictionary key does not exist, map it to current node. do not touch if there is already a key
                    visited.add(current_node)  # adds both the current and its child nodes to visited set
                    visited.add(neighbor_node)

    # check for no path
    if destination_actor not in actor_parents:
        return None

    # generates path starting with destination node
    value = destination_actor
    path = [destination_actor]
    while value != actor_id_1:  # appends nodes to path until reaching Bacon
        path.append(actor_parents[value])
        value = actor_parents[value]
    path.reverse()  # return a list that starts with Bacon
    return path


def actors_connecting_films(data, film1, film2):
    '''
    Takes in 2 films; returns a list of actors connecting the two films.
    '''
    movie_web = create_movie_dictionary(data) #creates movie dict mapping movie: {set of actors}
    film2_actors = movie_web[film2]
    paths_list = []


    for starting_actor in movie_web[film1]: #loop thru set of actors in the first movie's database
        paths_list.append(actor_path(data, starting_actor, lambda p: p in film2_actors)) #returns a list of connected actors

    sorted_paths_list = sorted(paths_list, key=len) #sort the list of lists based off the length of each element
    shortest_list = sorted_paths_list.pop(0)
    return shortest_list

# if __name__ == '__main__':
# # additional code here will be run only when lab.py is invoked directly
# # (not when imported from test.py), so this is a good place to put code
# # used, for example, to generate the results for the online questions.
# # print(load_a_pickle(self))
#
#     # with open('resources/small.pickle', 'rb') as f:
#     #     smalldb = pickle.load(f)
#     #
# #******NAMES PICKLE*********
#     # with open('resources/names.pickle', 'rb') as f:
#     #     names = pickle.load(f)
#     #
#     # print(names['Danielle Hoover'])
#     #
#     # for key in names:
#     #     if names[key] == 101219:
#     #         print(key)
#
# #*********TINY TESTS*********
#     # with open('resources/tiny.pickle', 'rb') as f:
#     #     tinydb = pickle.load(f)
#     #
#     # print(tinydb)
#
# #******SMALL PICKLE TEST***********
#     # with open('resources/small.pickle', 'rb') as f:
#     #     smalldb = pickle.load(f)
#
#      # print(smalldb)
#
#     # # print(names)
#     # #********REX LINN AND GEENA DAVIS CHECKER**********
#     # actor_1 = id_from_actor("Rex Linn")
#     # actor_2 = id_from_actor("Geena Davis")
#     # res = acted_together(smalldb, actor_1, actor_2)
#     # if res:
#     #     print("Yes, " + str(actor_from_id(actor_1)) + " and " + str(actor_from_id(actor_2)) + " have acted together")
#     # else:
#     #     print("No, " + str(actor_from_id(actor_1))+ " and " + str(actor_from_id(actor_2)) + " haven't acted together")
#     #
#     # #************CHRIS HOGAN AND TONY SHALHOUB CHECKER************
#     # actor_1 = id_from_actor("Chris Hogan")
#     # actor_2 = id_from_actor("Tony Shalhoub")
#     # res = acted_together(smalldb, actor_1, actor_2)
#     # if res:
#     #     print("Yes, " + str(actor_from_id(actor_1)) + " and " + str(actor_from_id(actor_2)) + " have acted together")
#     # else:
#     #     print("No, " + str(actor_from_id(actor_1))+ " and " + str(actor_from_id(actor_2)) + " haven't acted together")
#
# #********BACON NUMBER*********
# # with open('resources/tiny.pickle', 'rb') as f:
# #     tinydb = pickle.load(f)
# # print(tinydb)
#
# #******BACON NUMBER 1**********
# # actor_set = actors_w_bacon_num_1(tinydb)
# # print(actor_set)
# # print(tinydb)
# # for actor_id in actor_set:
# #     actor_id = actor_from_id(actor_id)
# # print(actor_set)
#
# # actor_set = {}
# # #**********BACON NUMBER 0***********
# # print(actors_with_bacon_number(tinydb, 3))
# # print("Database of actors: ", tinydb)
# # print("\n\nActors with Bacon number 0: ", actor_set)
# #
# # #**********BACON NUMBER 3************
# # actor_set = actors_with_bacon_number(tinydb, 3)
# # # print("Database of actors: ", tinydb)
# # print("\n\nActors with Bacon number 3: ", actor_set)
# #
# # #**********BACON NUMBER 2***********
# # actor_set = actors_with_bacon_number(tinydb, 2)
# # print("Database of actors: ", tinydb)
# # print("\n\nActors with Bacon number 2: ", actor_set)
# #
# # #**********BACON NUMBER 3************
# # actor_set = actors_with_bacon_number(tinydb, 3)
# # print("Database of actors: ", tinydb)
# # print("\n\nActors with Bacon number 3: ", actor_set)
#
#
# #********LARGE PICKLE TEST***********
# # with open('resources/large.pickle', 'rb') as f:
# #     largedb = pickle.load(f)
# #
# # # print(largedb)
# #
# # large_bacon = actors_with_bacon_number(largedb, 6)
# # print(large_bacon)
# #
# # actor_names = set()
# # for actor in large_bacon:
# #     actor_names.add(actor_from_id(actor))
# #
# # print(actor_names)
#
#
# #**********BACON PATHS TEST (Dijkstra's)************
# # print(bacon_path(largedb, 1204))
#
#
# # actor_2 = id_from_actor("Betty Gray")
# # id_list = bacon_path(largedb, actor_2)
# # # print(bacon_path(largedb, actor_2))
# #
# # name_list = [actor_from_id(actor) for actor in id_list]
# # print(name_list)
#
#
# #**********ACTOR TO ACTOR TEST**************
# # print(actor_to_actor_path(tinydb, 1532, 1640))
#
# # actor_1 = id_from_actor("Dennis Cadena")
# # actor_2 = id_from_actor("Natalie Portman")
# # id_list = actor_to_actor_path(largedb, actor_1, actor_2)
# #
# # name_list = [actor_from_id(actor) for actor in id_list]
# # print(name_list)
#
# #*********MOVIE PATH TEST*********
#     # with open('resources/movies.pickle', 'rb') as f:
#     #     moviedb = pickle.load(f)
#     # actor_id_1 = id_from_actor("Michael Sheen")
#     # actor_id_2 = id_from_actor("Vjeran Tin Turk")
#     # movie_path = movie_path(largedb, actor_id_1, actor_id_2)
#     #
#     # movie_names = [movie_from_id(movie) for movie in movie_path]
#     # print(movie_names)
#
#     #********ACTOR PATH TEST***********
#     # actor_id_1 = 975260
#     # goal_test_function = lambda p: False
#     # print(actor_path(largedb, actor_id_1, goal_test_function))
#     # # print(create_actor_dictionary(tinydb))
#
#     #**********ACTORS CONNECTING MOVIES TEST**********
#     # movie_1 =
#     # actors_connecting_films(largedb, film1, film2)
#     # print(largedb)
#     # print(create_movie_dictionary(largedb))
#     #
#     # starting_actor = 4724
#     # film2_actors = {1640}
#     # print(actor_path(largedb, starting_actor, lambda p: p in film2_actors))
#
#     # movie_id_1 = id_from_movie('Frost/Nixon')
#     # movie_id_2 = id_from_movie('7 Hours Later')
#     #
#     # actor_id_list = actors_connecting_films(largedb, movie_id_1, movie_id_2)
#     #
#     # actor_name_list = [actor_from_id(actor) for actor in actor_id_list]
#     #
#     # print(actor_name_list)
#
