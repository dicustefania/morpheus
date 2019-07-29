# morpheus

Summer Python project for senior undergraduate students (2019-2020) @ ETTI, UPB.

### Project milestones:

0. Set up a work environment ("[**Project setup**](https://github.com/SRBNM/morpheus/tree/master#project-setup)" section) and get the hang of the work procedure ("[**Work procedure**](https://github.com/SRBNM/morpheus/tree/master#work-procedure)" section).

1. Build a database of clean singing and authentic [growl](https://youtu.be/4VQUZLWVo88?t=585) singing voice recordings (**CAGsDB**).

2. Implement the voice morphing algorithm (**VMA**) proposed in \[1\].

3. From the authentic and morphed growl recordings, extract the features (**Features**) used for classification, according to 3 proposed feature sets.

4. Develop a SVM classifier (**Baseline**) to distinguish between authentic and morphed growl.

5. Develop a deep feedforward neural network classifier (**DNN**) to distinguish between authentic and morphed growl.

[\[1\] J. Bonada and M. Blaauw, "Generation of growl-type voice qualities by spectral morphing," in Proc. of the 2013 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Vancouver, Canada, pp. 6910-6914, May 2013](https://ieeexplore.ieee.org/abstract/document/6639001)

### Project details:

1. **CAGsDB**:
   - The final database will contain 3 singing voice classes: Clean and Growled_A (_authentic_) + Growled_M (_morphed_).
   - For each of the first two classes, 2 singers (the same for both classes) must be used.
   - For each singer, 50 sustained vocalizations ("_Aaahs_ and _Ooohs_") must be recorded (the same for both singers).
   - This results in 2x2x50 = 200 recordings.
   - All files must be single-channel (_mono_), recorded at 16 kHz sampling rate, using PCM format (_.wav_), and be around 1-2 seconds long. For example, [Audacity](https://www.audacityteam.org/download) can be used as the recording software.
   - Each audio file should be saved using the following naming convention: **CCSVV.wav**, where **CC** is the class identifier ('CC' or 'GA'), **SS** is the singer ID number ('1' or '2') and **VV** is the vocalization ID number ('01' ... '50'); e.g: _CC123.wav_ -- Clean singing by the 1st singer, 23rd vocalization.
   - For each singer, an Excel file (_.xlsx_) must be created, in which to log additional information: singer gender, age, and musical training (especially concerning growling vocals).
   - After applying the voice morphing algorithm, the processed audio data will be saved in files following the same naming convention, but with the 'GM' class identifier.

2. **VMA**:
   - A general outline of the algorithm is given below. Please refer to the original paper for details.
     1. For the first **GA** recording, [read](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.read.html) it from the disk and extract a (_at least 1 second_) long segment containing only the vocalization (**_morph sample_**).
     2. Add [zero-padding](https://docs.scipy.org/doc/numpy/reference/generated/numpy.pad.html) (using [appropriately many](https://ccrma.stanford.edu/~jos/sasp/Bias_Parabolic_Peak_Interpolation.html) samples).
     3. Compute the [FFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.fft.html) (using [appropriately many](https://electronica.curs.pub.ro/2018/pluginfile.php/35936/mod_folder/content/0/Cap6_PDS-D_Burileanu-2019.pdf?forcedownload=1) samples).
     4. Find the [peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) of the magnitude spectrum.
     5. Implement and use [quadratic (_parabolic_) interpolation](https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html) to estimate the fundamental frequency (FF) and the magnitudes of the FF and of the harmonics.
     6. Implement and use [linear interpolation](https://ccrma.stanford.edu/~jos/pasp/Linear_Interpolation.html) to estimate the [phases](https://ccrma.stanford.edu/~jos/sasp/Phase_Interpolation_Peak.html) of the FF and of the harmonics from the phase spectrum.
     7. Read from the disk the first **CC** recording and divide it into 25 ms long frames, using Hamming windowing (**_input voice_**).
     8. Repeat steps (b)-(f) for a frame obtained in step (g).
     9. [Resample](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.resample_poly.html) the segment from step (a) with the factor given by the ratio between the FF of the _input voice_ and that of the _morph sample_. For the FIR filter, use a Hamming window, an order of 80, and the [appropriate cut-off frequency](https://electronica.curs.pub.ro/2018/pluginfile.php/31072/mod_folder/content/0/Cap_4-TaPDS_Ian_2019.pdf?forcedownload=1).
     10. Calculate the mapping indices, using equation (1) from [1].
     11. Calculate the frequency shifts, using equation (3) from [1].
     12. Calculate the gains as the ratios between the magnitudes of the _input voice_ harmonics and those of the _morph sample_ harmonics.
     13. Calculate the phase corrections as the ratios between the phases of the _input_ voice harmonics and those of the _morph sample_ harmonics.
     14. Apply the harmonic mapping and filtering, using equation (2) from [1].
     15. Apply spectral mixing, using [linear interpolation](https://ccrma.stanford.edu/~jos/pasp/Linear_Interpolation.html), between the _input voice_ frame spectrum and the spectrum obtained in step (n).
     16. Compute the [IFFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.ifft.html) of the spectrum obtained in step (o). This is the current frame of the newly synthesized morphed growl recording.
     17. Repeat steps (h)-(p) for the next frame obtained in step (g).
     18. Concatenate all the frames obtained in step (q). This is the newly synthesized morphed growl recording. [Write](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html) it to disk as a _.wav_ file.
     19. Repeat steps (a)-(f) for the next recording in the **GA** class, and steps (g)-(r) for the next one in the **CC** class. **Always make sure to use the corresponding CC and GA recordings!** You should now have 100 **GM** class recordings.

3. **Features**:
   - For each audio recording in the **GA** and **GM** classes (200 instances), the following processing steps will be applied:
     - pre-processing:
       - framing: 25 ms duration, 10 ms steps
     - frame-wise feature extraction:
       - MFCCs: 26 filters between 80 Hz and 8 kHz, 13 coefficients, 512 FFT points, Hamming windowing function
       - delta coefficients: +/- 1 frame
       - delta-delta coefficients: +/- 1 frame
     - sentence-wise feature extraction:
       - averaging (_mean_) the frame-wise features over the entire sentence
   - Using the sentence-wise features, the following 3 datasets will be created:
     - Set_1: MFCCs
     - Set_2: MFCCs and delta coefficients
     - Set_3: MFCCs, delta coefficients and delta-delta coefficients
   - Each feature in each dataset will be normalized using the [z-score transform](https://en.wikipedia.org/wiki/Standard_score#Calculation) over the 200 samples of the two classes.
   - The final datasets will be saved to disk in Excel (_.xlsx_) format, using [Pandas](https://xlsxwriter.readthedocs.io/working_with_pandas.html).

4. **Baseline**:
   - The baseline system will consist of a [SVM](https://scikit-learn.org/stable/modules/svm.html) classifier.
   - Implementation will be done using the scikit-learn [SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) class.
   - Two hyperparameters will be adjusted during validation:
     - the kernel function: linear vs. RBF (radial basis function)
     - the C parameter (regularization parameter)
   - All other parameters will be used with their default values.
   - In separate trials, experiments will be done using each of the 3 feature datasets previously described.
   
5. **DNN**:
   - The proposed system will be a deep feedforward (dense) neural network using multilayer perceptrons ([MLP](https://keras.io/layers/core/)).
   - Implementation will be done using the Keras [Sequential](https://keras.io/models/sequential/) model.
   - (**_details to follow_**).
   - In separate trials, experiments will be done using each of the 3 feature datasets previously described.

6. Other notes:
   - The train/dev/test split will be 40%/30%/30%.
   - The metrics used for performance assessment and comparison will be:
     - accuracy
     - precision and avg. precision
     - recall and avg. recall
     - F1-measure and avg. F1-measure
   - In addition, the following graphical results are required:
     - confusion matrices
     - validation error vs. epoch
     - validation accuracy vs. epoch
   - In the final stage, a **4-page** paper (using the [IEEE Word template](https://www.ieee.org/content/dam/ieee-org/ieee/web/org/conferences/Conference-template-A4.doc)) will be written to clearly, convincingly, and eloquently present the project and how it relates to the wider scope of voice morphing and machine learning research.
   - Structure:
     * Abstract
     * S1. Introduction
     * S2. System Architecture
     * S3. Implementation Details
     * S3.1. The Clean And Growled Singing Database (CAGsDB)
     * S3.2. Feature Extraction
     * S3.3. Implementation Details
     * S4. Experimental Setup and Results
     * S4.1. Experimental Setup Details
     * S4.2. Experimental Results
     * S5. Conclusions
     * References

### Project setup:

0. Make sure your operating system architecture is **64-bit**!

1. Install [Anaconda for Python 3](https://www.anaconda.com/distribution/).

2. (_If using Windows, launch Anaconda Prompt as Admin._) Set up a new virtual environment, named _morpheus_:
```
conda create -n morpheus python=3.6 tensorflow keras scikit-learn pandas xlsxwriter matplotlib graphviz spyder
conda info --envs
```

3. Activate the _morpheus_ environment:
```
conda activate morpheus
conda info --envs
```

4. Install the [python_speech_features](https://python-speech-features.readthedocs.io/en/latest/) package:
```
pip install python-speech-features
conda list
```

5. Register a [GitHub account](https://github.com).

6. Fork (_copy_) the **original** [_morpheus_ repository](https://github.com/SRBNM/morpheus) by clicking on the **Fork** button in the top right corner.

7. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

8. (_If using Windows, launch Git Bash._) Configure _git_ (_Hint: you can always use the_ **git --help** _command_):
```
git config --global user.email "<email_address>"
(e.g: <email_address> = smihalache@gmail.com   <--- use the same email as for your GitHub account)
git config --global user.name "<name>"
(e.g: <name> = SRBNM   <--- use the same name as for your GitHub account)
```

9. Navigate to your desired work folder path (_Hint: you can always use the_ **ls -a** _command to list all files in the current directory_):
```
cd <path>
(e.g: path = "/c/summer_project/")
```

10. Clone (_download_) the **forked** _morpheus_ repository (_your copy_) and add a remote (_alias_) to the **original** one (_Hint:_ **morpheus** _is the name of the remote of the_ **original** _repository and_ **origin** _is the name of the remote of_ **your** _repository_):
```
git clone https://github.com/<username>/morpheus.git
(e.g: <username> = GreuceanuSfarmafalci   <--- your GitHub account username)
git remote add morpheus https://github.com/SRBNM/morpheus.git
git remote -v
```

11. Switch to your repository directory (_Hint: Notice the_ **(master)** _marker_):
```
cd morpheus
```

12. Launch Spyder from the Anaconda virtual environment (_morpheus_):
```
spyder &
```

13. From the **Project** menu, select **New Project...**. Select **Existing directory** and browse for the _path_ used at step 11 (e.g: "_C:\summer_project\morpheus_"). Create a new file and save it with the **.py** extension (e.g: **main.py**).

14. Update your **remote** fork with all **local** changes:
```
git checkout master
git add --all
git commit -m "<short_description>"
(e.g: <short_description> = first update   <--- to explain what is being changed)
git push origin master
```

### Work procedure

1. Update your **local** fork from the **original** repository:
```
cd <path>/morpheus
git pull morpheus master
```

2. Activate the Anaconda _morpheus_ virtual environment and launch Spyder.
```
conda activate morpheus
spyder &
```

3. After finishing coding, update your **remote** fork with all **local** changes.
```
git checkout master
git add --all
git commit -m "<short_description>"
git push origin master
```

### Software and code resources:

- Anaconda3 (with Spyder IDE)
- GitHub
- TensorFlow
- NumPy
- SciPy
- SciKit Learn
- Pandas
- Xlsxwriter
- Matplotlib
- h5py
- Graphviz
- Keras
- python_speech_features
