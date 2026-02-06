# Audio Processing Sandbox
A place to write scripts that process my guitar recordings in various ways. Initially, I just wanted to grasp basic ASP concepts, but I'm workshoping some ideas that I think would be useful for a musician.

## Capabilities
- Add effects to a given recording (reverb, delay, echo, chorus, flanger, EQ, filtering, compression, gating, limiting, distortion, remove note onsets)
- Generate a stereo recording from any number of mono audio clips with desired panning angles and relative volumes
- Noise cancellation (performance comparison between adaptive LMS filter, Weiner filter, and a custom DNN)
- Source separation

## Random Project Idea
Given a recording of a song, isolate the guitar. Then, estimate a filter that can take a recording of me playing the riff on the guitar and add the proper effect. I wonder if this could work to change the timbre of the guitar to other intruments.

Specifically, I would apply an LMS filter. A short sample of a sustained note from the song could be treated as the desired output and my guitar could be the input. Maybe I average the filter weights across several sustained notes.

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