from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def __init__(self,
                 path_to_res, 
                 path_to_model, path_to_scaler, threshold = 0.1,
                 fs = 250, cutoff_l = 0.5, cutoff_h = 40, order = 3,
                 message = b"it's me",):
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

        Returns
        -------
        None 
        '''
        pass
        
    @abstractmethod
    def _create_dir_for_res(self, path_to_res):

        '''
        Creation of the folder with results:
            signal_n.txt - a file with two columns (1st - Time in sec, 2nd - filtered ECGI in mV )

        Parameters
        ----------
        path_to_res : str
            The directory to create a folder with the results.
        Returns
        -------
        None 
        '''
        pass  
            
    @abstractmethod
    def _create_filter(self, fs, cutoff_l, cutoff_h, order):
        '''
        Creation of the bandpass filter.

        Parameters
        ----------
        path_to_model : str
            The path to the model.
        path_to_scaler : str
            The path to the scaler.
        threshold : float
            Threshold for anomaly prediction.
        
        Returns
        -------
        None 
        '''
        pass

    @abstractmethod
    def _init_nn(self, path_to_model, path_to_scaler, threshold):
        '''
        Neural network initialization.

        Parameters
        ----------
        fs : int
            Sampling frequency of the input signal.
        cutoff_l : float
            Lower cutoff frequency of the bandpass filter.
        cutoff_h : float
            Higher cutoff frequency of the bandpass filter.
        order : int
            Bandpass filter order.
        
        Returns
        -------
        None 
        '''
        pass
      
    @abstractmethod
    def _init_plot(self):
        '''
        Figure for plotting initialization.

        Parameters
        ----------
        None
        
        Returns
        -------
        None 
        '''
        pass
        
    @abstractmethod
    def _init_client(self, message):
        '''
        Client initialization.

        Parameters
        ----------
        message : binary
            Message to link client and server.
        
        Returns
        -------
        None 
        '''
        pass
        
    @abstractmethod
    def _visualize(self, data_for_plot, scored_):
        '''
        Data visualization.

        Parameters
        ----------
        data_for_plot : pandas dataframe
            Input signal with columns ['Time', 'Target1'].
        scored_ : pandas dataframe
            Dataframe with anomaly detection with columns ['Loss_mae', 'Threshold', 'Anomaly'].
            'Anomaly' - True/False
        
        Returns
        -------
        None 
        '''

    @abstractmethod
    def _predict(self, data):
        '''
        Neural network forward pass + anomaly detection.

        Parameters
        ----------
        data : list
            A part of thr input signal of a given size to be processed.
        
        Returns
        -------
        pred : pandas dataframe
            Neural network prediction.
        scored_ : pandas dataframe
            Dataframe with anomaly detection with columns ['Loss_mae', 'Threshold', 'Anomaly'].
            'Anomaly' - True/False
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