# morpheus

Summer Python project for senior undergraduate students (2019-2020) @ ETTI, UPB.

### Project milestones:

0. Set up a work environment ("[**Project setup**](https://github.com/SRBNM/morpheus/tree/master#project-setup)" section).

1. Build a database of normal speech and (authentic) growled speech (_NAG_).

2. Implement the voice morphing algorithm (_VMA_) proposed in \[1\].

3. Develop a SVM classifier (_Baseline_), to distinguish between authentic and morphed growls.

4. Develop a deep feedforward neural network classifier (_DNN_), to distinguish between authentic and morphed growls.

[\[1\] J. Bonada and M. Blaauw, "Generation of growl-type voice qualities by spectral morphing," in Proc. of the 2013 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Vancouver, Canada, pp. 6910-6914, May 2013](https://ieeexplore.ieee.org/abstract/document/6639001)

### Project details:

1. NAG:
   - The final database will contain 3 speech classes: Normal and Growled_A (authentic) + Growled_M (morphed).
   - For the first two classes, at least 10 speakers must be used.
   - For each speaker, at least 10 utterances must be recorded.
   - All files must be recorded at 16 kHz sampling rate, using PCM format, and must be at least 3 seconds long.
   - Additional information to log: speaker id#, gender, age, and musical training (especially concerning growling vocals).

2. VMA:
   - Complete implementation (**_details to follow_**).

3. Baseline:
   - The baseline system will consist of a [SVM](https://scikit-learn.org/stable/modules/svm.html) classifier (**_details to follow_**).
   - In separate trials, it will be trained and tested using the following extracted feature sets:
     * MFCC
     * MFCC and delta coefficients
     * MFCC, delta coefficients, and delta-delta coefficients.

4. DNN:
   - The proposed system will be a deep feedforward (dense) neural network using multilayer perceptrons ([MLP](https://keras.io/layers/core/)) (**_details to follow_**).
   - The extracted features will be the same as in the three baseline sets (in separate trials).

5. Other notes:
   - The train/dev/test split will be 40%/30%/30%.
   - The metrics used for performance assessment and comparison will be: Accuracy, Precision and Avg. Precision, Recall and Avg. Recall, F1-measure and Avg. F1-measure.
   - In addition, the following graphical results are required: confusion matrices, and validation error and accuracy evolution in time.
   - In the final stage, a **4-page** paper (using the [IEEE Word template](https://www.ieee.org/content/dam/ieee-org/ieee/web/org/conferences/Conference-template-A4.doc)) will be written to clearly, convincingly, and eloquently present the project and how it relates to the wider scope of voice morphing and machine learning research.
   - Structure:
     * Abstract
     * S1. Introduction
     * S2. Proposed System Architecture
     * S3. Implementation Details
     * S3.1. The NAG Database
     * S3.2. Extracted Features
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
conda create -n morpheus python=3.6 tensorflow keras scikit-learn pandas matplotlib graphviz spyder
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

5. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

6. (_If using Windows, launch Git Bash._) After registering a GitHub account online, configure _git_ (_Hint: you can always use the_ **git --help** _command_):
```
git config --global user.email "<email_address>"
(e.g: <email_address> = smihalache@gmail.com   <--- use your main email address)
git config --global user.name "<name>"
(e.g: <name> = SRBNM   <--- use the same name as for your GitHub account)
```

7. Navigate to your desired work folder path (_Hint: you can always use the_ **ls -a** _command to list all files in the current directory_):
```
cd <path>
(e.g: cd "/c/summer_project/")
```

8. Clone the _morpheus_ repository:
```
git clone https://github.com/SRBNM/morpheus.git
```

9. Switch to the repository directory (_Hint: Notice the_ **(master)** _marker_):
```
cd morpheus
```

10. (Update your master clone and) Create, checkout (switch to) and push (upload) your own branch (_Hint:_ **origin** _is the name of the remote \[alias\] of the repository_):
```
git pull
git branch <new_branch_name>
git checkout <new_branch_name>
git push origin <new_branch_name>
(<new_branch_name> = stefaniad | alexg | narcisag | anam | mariann   <--- use the corresponding name for your branch)
```

11. 

### Software and code resources:

- Anaconda3 (with Spyder IDE).
- TensorFlow
- NumPy
- SciPy
- SciKit Learn
- Pandas
- Matplotlib
- h5py
- Graphviz
- Keras
- python_speech_features
