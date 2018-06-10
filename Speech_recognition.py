{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Speech Recognition system using MFCC and DTW algorithms.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'pywt'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-6-cad70484ab1e>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     15\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     16\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrandom\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 17\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mpywt\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     18\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mdtw\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mdtw\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'pywt'"
     ]
    }
   ],
   "source": [
    "import scipy.io.wavfile as wavfile \n",
    "import matplotlib.pyplot as plt\n",
    "import re\n",
    "import os\n",
    "import numpy as np\n",
    "import math\n",
    "from scipy.io import wavfile\n",
    "from scipy import signal\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import normalize\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn import metrics\n",
    "from python_speech_features import mfcc\n",
    "from python_speech_features import delta\n",
    "from pydub import AudioSegment\n",
    "import logging\n",
    "import random\n",
    "import pywt\n",
    "from dtw import dtw"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'data' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-3-1762d12881c3>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     47\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     48\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 49\u001b[0;31m \u001b[0;32mfor\u001b[0m \u001b[0md\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mdata\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     50\u001b[0m     \u001b[0msignal\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mfs\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mget_signal_from_file\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0md\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'signal_path'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     51\u001b[0m     \u001b[0md\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"fs\"\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mfs\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mNameError\u001b[0m: name 'data' is not defined"
     ]
    }
   ],
   "source": [
    "# Constants\n",
    "\n",
    "WIN_LENGTH = 0.025 \n",
    "WIN_STEP =0.01\n",
    "NUM_CEP=13\n",
    "\n",
    "# Methods for prepare data to futher processing and classification\n",
    "\n",
    "def match_signal_file_with_label_track_file():\n",
    "    signal_and_label_track_pairs = list()\n",
    "    for _file in os.listdir(\"data/\"):\n",
    "        if(_file.endswith(\".wav\")):\n",
    "            signal_and_label_track_pairs.append({\"signal_path\": _file, \"label\": os.path.splitext(_file)[0]+\".txt\"})\n",
    "    return signal_and_label_track_pairs\n",
    "\n",
    "def get_signal_from_file(signal_file_name):\n",
    "    fs, signal = wavfile.read(signal_file_name) \n",
    "    if (signal.ndim>1):\n",
    "        signal = signal[:,0]\n",
    "    return signal, fs\n",
    "\n",
    "def show_signal(signal, label):\n",
    "    plt.plot(signal)\n",
    "    plt.xlabel(label)\n",
    "    plt.show()   \n",
    "    \n",
    "def parse_track_file(label_track_file_name):\n",
    "    label_track_file = open(label_track_file_name)\n",
    "    label_track_file_line = label_track_file.readlines()\n",
    "    label_track_list = list(); \n",
    "    for line in label_track_file_line :\n",
    "        label_item = re.split(r'\\s+', line);\n",
    "        label_track_list.append({\"timestamp_start\":float(label_item[0].replace(\",\", \".\"))*1000, \n",
    "                               \"timestamp_end\":float(label_item[1].replace(\",\", \".\"))*1000, \n",
    "                               \"label\": label_item[2]})\n",
    "    return label_track_list #[\"timestamp_start\":0, \"timestamp_end\": 1234, \"label\": \"GARAZ\", \"label_id\"=}]\n",
    "\n",
    "    \n",
    "# Extract raw data signal from particular file and assign it to its item\n",
    "# Dataset dictionary structure:\n",
    "# dataset = \n",
    "#     {'signal_path': 'data_output/OTWORZ_258118_3.wav', \n",
    "#     'label': 'OTWORZ', \n",
    "#     'gender': 'K', \n",
    "#     'fs': 44100, \n",
    "#     'signal': array([48, 24, 38, ...,  0, 14,  6]}\n",
    "\n",
    "\n",
    "for d in data:\n",
    "    signal, fs = get_signal_from_file(d['signal_path'])\n",
    "    d[\"fs\"] = fs\n",
    "    d[\"signal\"] = signal\n",
    "    \n",
    "print(\"It was created %s new .wav files, where each signal represents one word.\" % len(data))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# MFFC - Mel-Frequency Cepstral Coefficients"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 258,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Example of MFFC result image\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "def get_MFCC(signal, samplerate):\n",
    "    # Mute warnings\n",
    "    logging.getLogger().setLevel(logging.ERROR)\n",
    "    mfcc_features = mfcc(signal, samplerate, winlen=WIN_LENGTH, winstep=WIN_STEP, numcep=NUM_CEP, winfunc=np.hamming)\n",
    "    # Unmute warnings\n",
    "    logging.getLogger().setLevel(logging.NOTSET)\n",
    "    return mfcc_features\n",
    "\n",
    "# Prepare dataset for train and test. \n",
    "dataset = list()\n",
    "for d in data:\n",
    "    # For classification was used only initial 13x20 coefficients \n",
    "    dataset_features = np.reshape(((get_MFCC(d[\"signal\"], d[\"fs\"]))[:20]), (-1))\n",
    "    dataset.append([dataset_features, d['label']])\n",
    "            \n",
    "# Example of MFFC spectrum image\n",
    "print(\"Example of MFFC result image\")\n",
    "mffc_example = get_MFCC(data[0][\"signal\"], data[0][\"fs\"])\n",
    "plt.xlabel(\"frames\")\n",
    "plt.ylabel(\"frequency\")\n",
    "plt.title(data[0][\"label\"])\n",
    "plt.imshow(mffc_example.T)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 255,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Prepare datasets for classification\n",
    "def get_datasets(dataset, N): \n",
    "    random.shuffle(dataset)\n",
    "\n",
    "    x,y = zip(*dataset)\n",
    "    x = list(x)\n",
    "    y = list(y)\n",
    "\n",
    "    train_x = x[0:N]\n",
    "    train_y = y[0:N]\n",
    "    test_x =  x[N:len(dataset)]\n",
    "    test_y =  y[N:len(dataset)]\n",
    "\n",
    "#   Standardize features\n",
    "    scaler = StandardScaler()\n",
    "    scaler.fit(train_x)\n",
    "    train_x = [s.reshape(-1,20) for s in np.array(scaler.transform(train_x))]  \n",
    "    test_x = [s.reshape(-1,20) for s in np.array(scaler.transform(test_x))]\n",
    "        \n",
    "    return train_x, train_y, test_x, test_y"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# DTW - Dynamic Time Wrapping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 256,
   "metadata": {},
   "outputs": [],
   "source": [
    "def cross_validation(train_x, train_y, test_x, test_y): \n",
    "    predict = ['' for x in range(len(test_y))]\n",
    "\n",
    "    for test_iter, test in enumerate(test_x):\n",
    "        dist_min = math.inf\n",
    "        for train_iter, train in enumerate(train_x):\n",
    "            dist, _, _, _ = dtw(test, train, dist=lambda test, train: np.linalg.norm(test - train, ord=1))\n",
    "            if dist_min > dist: \n",
    "                dist_min = dist\n",
    "                predict[test_iter] = train_y[train_iter]\n",
    "    return predict\n",
    "\n",
    "train_x, train_y, test_x, test_y = get_datasets(dataset_train, 500) \n",
    "predicted = cross_validation(train_x, train_y, test_x, test_y) \n",
    "expected = test_y"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Classification report"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 257,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification report: \n",
      "\n",
      "             precision    recall  f1-score   support\n",
      "\n",
      "      GARAZ       0.78      0.64      0.70        11\n",
      "     MUZYKE       0.93      0.74      0.82        19\n",
      "    NASTROJ       0.31      0.80      0.44         5\n",
      "     OTWORZ       0.80      0.67      0.73         6\n",
      "    PODNIES       0.89      0.89      0.89         9\n",
      "     ROLETY       0.86      0.50      0.63        12\n",
      "    SWIATLO       0.89      1.00      0.94         8\n",
      "  TELEWIZOR       0.71      0.71      0.71        14\n",
      "      WLACZ       0.67      0.75      0.71         8\n",
      "     WYLACZ       0.54      0.64      0.58        11\n",
      "    ZAMKNIJ       0.40      0.33      0.36         6\n",
      "      ZAPAL       0.56      0.62      0.59         8\n",
      "       ZROB       0.71      0.71      0.71         7\n",
      "\n",
      "avg / total       0.73      0.69      0.70       124\n",
      "\n",
      "\n",
      "Accuracy classification score: 69.35%\n",
      "Precision classification score: 73.49%\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "print(\"Classification report: \\n\\n%s\\n\"\n",
    "      % (metrics.classification_report(expected, predicted)))\n",
    "mat = metrics.confusion_matrix(expected, predicted)\n",
    "label_names = list(set(expected))\n",
    "plt.figure()\n",
    "plt.imshow(mat, interpolation='nearest', cmap='Blues')\n",
    "plt.title('normalized confusion matrix')\n",
    "plt.colorbar()\n",
    "plt.ylabel('True label')\n",
    "plt.xlabel('Predicted label')\n",
    "tick_marks = np.arange(len(label_names))\n",
    "plt.xticks(tick_marks, label_names, rotation=90)\n",
    "plt.yticks(tick_marks, label_names)\n",
    "plt.tight_layout()\n",
    "\n",
    "accuracy = metrics.accuracy_score(expected, predicted)\n",
    "print('Accuracy classification score: {0:.2f}%'.format(100*accuracy))\n",
    "precision = metrics.precision_score(expected, predicted, average='weighted')\n",
    "print('Precision classification score: {0:.2f}%'.format(100*precision))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
