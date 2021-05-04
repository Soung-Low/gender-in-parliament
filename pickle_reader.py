import pickle 

def read_pickle_file(file):
    pickle_data = pickle.load(open(file, 'rb'))
    return pickle_data