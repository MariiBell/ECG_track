from Interface import Interface

import socket
import matplotlib.pyplot as plt
import numpy as np
import time
from keras.models import load_model
import pandas as pd
import os
from scipy import signal
import joblib

class ECG_track(Interface):
    def __init__(self,
                 path_to_res, 
                 path_to_model, path_to_scaler, threshold = 0.05,
                 fs = 250, cutoff_l = 0.5, cutoff_h = 40, order = 3,
                 message = b"it's me", sig_len = 5
                 ):
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
        self._create_dir_for_res(path_to_res)
        self._create_filter(fs, cutoff_l, cutoff_h, order)
        self.sig_len  = int(sig_len*fs)
        self._init_nn(path_to_model, path_to_scaler, threshold)
        self._init_plot()
        self._init_client(message)

    
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
        if not('results' in os.listdir(path_to_res)):
            os.mkdir(os.path.join(path_to_res, 'results'))
            f = open(os.path.join(path_to_res, 'results','num.txt'), 'x')
            f.write('0')
            self.exp_i = 0
            f.close()
        elif not('num.txt' in os.listdir(os.path.join(path_to_res, 'results'))):
            f = open(os.path.join(path_to_res, 'results','num.txt'), 'x')
            f.write('0')
            self.exp_i = 0
            f.close()
        else:
            f = open(os.path.join(path_to_res, 'results','num.txt'), 'r')
            self.exp_i = int(f.read().strip().split("\n")[-1])+1
            f.close()
            f = open(os.path.join(path_to_res, 'results','num.txt'), 'w')
            f.write(str(self.exp_i))
            f.close()
        self.path_to_res = path_to_res
        
            
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
        nyq = 0.5 * fs
        self.b, self.a = signal.butter(order, (cutoff_l / nyq, cutoff_h / nyq), btype='bandpass', analog=False)

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
        self.model = load_model(path_to_model)
        self.scaler = joblib.load(path_to_scaler)
        self.threshold = threshold

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
        plt.close('all')
        plt.figure(figsize=(16,6))        
        plt.ion()

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
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(('0.0.0.0', 5006))
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while True:
            print("Waiting for data...")
            data, adr = self.client.recvfrom(1024)
            print(f'Данные от {adr}: {data}')
            if data == message:
                time.sleep(0.5)
                self.right_adr = adr
                self.client.sendto(message , (adr))
                break

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
        plt.plot(data_for_plot['Time'], data_for_plot['Target1'], label='Target1', color='blue', linewidth=1)
        plt.scatter(data_for_plot['Time'][data_for_plot[scored_['Anomaly']==True]['Target1'].index],data_for_plot[scored_['Anomaly']==True]['Target1'],label='anomal',marker='.', color='red')
        plt.legend(loc='lower left')
        plt.xlabel("Time (s)")
        plt.ylabel("ECGI (mV)")
        plt.title('ECG Test Data', fontsize=16)
        plt.show()
        plt.pause(0.01)
        plt.cla()
    
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
        data_for_pred = np.hstack([np.array([data]).T, np.array([data]).T])
        data_for_pred = self.scaler.transform(data_for_pred)
        data_for_pred = np.resize(data_for_pred, (self.sig_len,1,2))
        pred = self.model.predict(data_for_pred)
        pred = pred.reshape(pred.shape[0], pred.shape[2])
        pred = pd.DataFrame(pred, columns=['Target1','Target2'])
        pred.index = range(self.sig_len)

        scored_ = pd.DataFrame(index=pred.index)       
        scored_['Loss_mae'] = np.mean(np.abs(pred-data_for_pred.reshape(data_for_pred.shape[0], data_for_pred.shape[2])), axis = 1) 
        scored_['Threshold'] = self.threshold
        scored_['Anomaly'] = scored_['Loss_mae'] > scored_['Threshold']
        return pred, scored_

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
        data = [] 
        time1 = []
        with open(os.path.join(self.path_to_res, 'results',f'signal_{self.exp_i}.txt'), 'a')  as file_for_sig:
            with open(os.path.join(self.path_to_res, 'results',f'anomaly_{self.exp_i}.txt'), 'a') as file_for_pred:
                while True:

                    data_, adr = self.client.recvfrom(1024)
                    data_ = list(data_.split())

                    if adr == self.right_adr:
                        data.append(int(data_[0])/65535*1100*3.2/100)     
                        time1.append(int(data_[1])*(10**(-9)))            
                    
                        if len(data)==self.sig_len:

                            data = signal.filtfilt(self.b, self.a, data)
                            

                            pred, scored_ = self._predict(data)

                            data_for_plot = pd.DataFrame(np.hstack([np.array([time1]).T, np.array([data]).T]), columns = ['Time', 'Target1'])
                            data_for_plot.index = pred.index                

                            file_for_sig.write(data_for_plot.to_string(header=False,index=False)+'\n')
                            file_for_pred.write(scored_.to_string(header=False,index=False)+'\n')

                            self._visualize(data_for_plot, scored_)

                            data = []
                            time1 = []