"""# write a file using pickle

with open("filename.pickle", "wb") as f:
    pickle.dumb(file,f)

# read a file using pickle

pickle_in = with open("filename.pickle", "rb") as f:
    file = pickle.load(pickle_in)

# using pickle to save a model that has a certain accuracy

best = 0
for __ in range (#however many times you wanna train)

    #paste the code to run net here

    if acc > best
        best = acc
        with open("filename.pickle", "wb") as f:
            pickle.dumb(file, f)

"""