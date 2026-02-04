# AI Abstract Generator

Great research requires out-of-box insights. Often, it is important to parse through literature and figure out the problems worth solving. With thousands of papers published each year, it is impossible to keep track of them. Furthermore, scrolling through individual sections of openreview/opencvf takes too much time. Finally, conferences like icml/eccv publish giant books combining all papers. However, most of this is application based and cant help a person from achieving a required level of abstract thought.  

To separate junk papers from good ones, it is therefore necessary to have a 'single' spot with the abstract of all papers in one place. This repo aims to achieve that. It should allow you to go filter research far more quickly. 

For now, i have covered proceedings of cvpr, iccv, neurips, icml, iclr, wacv and eccv for all the years till today. In future, i plan to expand to NLP conferences since both vision and language are essentially sequential problems and contain interconnects in the field, 

For looking at the proceedings, please go the pdf section of appropriate conference. If you are looking to generate abstract collection for any year in the future, any of the relevant files can be run. 

I hope this helps at least one person out there, 


```
python icml.py -> for generating icml abstract. 
python nips.py -> parses neurips.cc for proceedings . 
python openreview-py/openreview.py -> parses openreview for all iclr conferences. 
```
Note: ICLR proceedings contain all submissions including accepted/rejected papers. As @andrej karpathy says, it is important to expose oneself to both good and 'bad' research :-) 

In case of doubts, email: rajatmodi62@gmail.com
Thanks and wishing you a successful career,

Credits:
Beautifulsoup for crawling, and the amazing folks at openreview for api. 


### from now, i have started making list of notable papers 

criteria is my own, pushes are welcome. we are interested in bigger story, not stupid increments over benchmarks. 

nips 25

- Memory Mosaics at scale
- Analog In-memory Training on General Non-ideal Resistive Elements: The Impact of Response Functions
Large Language Diffusion Models
Learning long range dependencies through time reversal symmetry breaking
Mean Flows for One-step Generative Modeling
Error Forcing in Recurrent Neural Networks
Controlling Thinking Speed in Reasoning Models
Rotary Masked Autoencoders are Versatile Learners
Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation
Harnessing the Universal Geometry of Embeddings
Chirality in Action: Time-Aware Video Representation Learning by Latent Straightening
Find your Needle: Small Object Image Retrieval via
Multi-Object Attention Optimization: somewhat interesting but not that groundbreaking
Cameras as Relative Positional Encoding
Generative Graph Pattern Machine
70% Size, 100% Accuracy: Lossless LLM Compression for Efficient GPU Inference via Dynamic-Length Float (DFloat11)
start from 117
Object-centric Binding in Contrastive
Language-Image Pretrainin
start from 124 
