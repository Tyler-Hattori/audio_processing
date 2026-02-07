# Audio Processing Sandbox
A place to store my Jupyter notebooks that process my guitar recordings in various ways. Initially, I just wanted to grasp basic ASP concepts, but I'm workshoping some ideas that I think would be useful for a musician. I've converted some of the Jupyter notebooks into scripts that can be run from a terminal.

## Capabilities
- Mono to stereo conversion for a moving source, including frequency dependent path loss, doppler effect, and rudimentary considerations for the low pass filter from the geometry of the ear
- Adaptive noise cancellation using NLMS filtering, mimicking filtering done in modern headphones without secondary path considerations.
- Sustained note extraction from a given audio file. The criteria for classifying a note as sustained includes the slope and magnitude of RMS energy over time and the stability of the estimated pitch by YIN.
- Timbre replication given a reference recording, the same recording with some change in timbre, and a separate recording on which the filter is applied. Implemented with mean FFT ratios of sustained notes.

## In Progress, Not Shown
- Source separation using Non-negative Matrix Factorization with constraints on sparsity and harmonicity
- Custom tunable amp model GUI with an initial nonlinearity (tanh) for distortion, EQ bandpass filters, a cut-and-paste filter to get a desired timbre, an output nonlinearity for compression, and added reverb (echo and decay).

## Random Project Idea
Given a recording of a song, isolate the guitar. Then, estimate a filter that can take my guitar recording and add the proper effect. This would entail estimating any distortion with an initial nonlinearity (tanh), applying a linear filter, estimating any compression with another nonlinearity, and replicating any reverb by identifying early refractions and decay time. These are differentiable functions, so a model could be learned. A remedy for the lack of training data from a short clip could be to have a priori assumptions on the linear filter from basic timbre transfer and reasonably initialized values for the nonlinearities in modifying a typical amplifier. This model, while not being as thorough as a deep neural net, would be easily interpretable. I think this is important for my own intuition, and because I could make a relatively simple GUI that can tune the hyperparamters directly.

## Prerequisites
Anaconda.

## Installation
Create and activate a conda environment. Run the following:

```
conda install python
```
```
conda install setuptools
```
```
pip install -e .
```
To verify the package was installed, run
```
pip list
```
and check if **guitar_processing** is listed.

## Usage
Run any of the scripts in /guitar_processing/scripts or read through and run a workbook