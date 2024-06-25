from ECG_track import ECG_track

ecg_track = ECG_track(path_to_res = '.' , 
                 path_to_model ='./model/ecg_model.h5', path_to_scaler = "./model/chfdb_chf01_275.txt"
                 )


ecg_track.track()




