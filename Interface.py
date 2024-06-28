from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def __init__(self,
                 path_to_res, 
                 path_to_model, path_to_scaler, threshold = 0.1,
                 fs = 250, cutoff_l = 0.5, cutoff_h = 40, order = 3,
                 message = b"it's me", sig_len = 5):
        '''
        Creation the folder with results.
        Filter initialization.
        Neural network initialization.
        Figure for plotting initialization.
        Client initialization.

        Parameters
        ----------
        path_to_res : str
            The  directory to create a folder with the results.
        path_to_model : str
            The path to the model.
        path_to_scaler : str
            The path to the scaler.
        threshold : float
            Threshold for anomaly prediction.
        fs : int
            Sampling frequency of the input signal.
        cutoff_l : float
            Lower cutoff frequency of the bandpass filter.
        cutoff_h : float
            Higher cutoff frequency of the bandpass filter.
        order : int
            Bandpass filter order.
        message : binary
            Message to link client and server.
        sig_len : float
            Signal length for plot and process in sec.

        Returns
        -------
        None 
        '''
        pass
        

    
    @abstractmethod
    def track(self):
        '''
        Signal read + detect anomaly + viasualize + save to file.

        Parameters
        ----------
        None
        
        Returns
        -------
        None 
        '''
        pass