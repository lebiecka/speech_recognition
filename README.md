# speech_recognition
Simple speech recognition system can be implemented using DTW and MFCC. System is able to recognize 13 polish words pronuanced by different speakers
 
# MFCC - Mel-Frequency Cepstral Coefficients
<br>
<div>MFCC algoritm is used for feature extraction.</div>
<br>
<div>MFCCs are the coefficients which represents short-term power spectrum of a data according to MEL scale of frequency,  
which is based on human hearing perception.</div>
# DTW - Dynamic Time Wrapping
<br>
<div>For classify objects DTW - Dynamic Time Wrapping was used.</div>
<br>
<div>DWT algorithm measures similarity between two signals with different signal length.<div>
<div>Classifier measures distance between testing signal and every signal in training set and assigns object to the class of signal, where the least distance was found.</div>

Set of words:
GARAZ, MUZYKE, NASTROJ, OTWORZ, PODNIES, ROLETY, SWIATLO, TELEWIZOR, WLACZ, WYLACZ, ZAMKNIJ, ZAPAL, ZROB

*Script division_into_single_word.ipynb can be used to obtain set of single words from the whole recording. 


First install librosa and dtw. For both the latest stable release in available on PyPI by typing: <br />
  pip install librosa <br />
  pip install dtw  <br />
  
Sources:
https://www.researchgate.net/publication/260762671_Speech_recognition_using_MFCC_and_DTW
