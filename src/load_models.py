import pickle

def load_lstm():
    pickle_in_lstm = open("./Models/LSTM_MODEL.pkl", "rb")
    model_lstm = pickle.load(pickle_in_lstm)
    return model_lstm



