# Pearson correlation coefficient reduction (PCCR) for pigments and dyes analysis
Python Implementation of our dimensionnality reduction method for hyperspectral imaging based on Pearson correlation coefficient.

## Prerequise

Install the list below : 
- csv
- numpy
- matplotlib
- sklearn
- mpl_scatter_density
- spectral
- cv2
- scipy   
- pandas

## First part: Generation of the set of characteristic spectra

The set generation can be made 'with creation_spectra_base.py'.

Some parameters like the filepath, the name of your hyperspectral image, the labels
 of each of the spectra or even the name of the database have to be mentionned at the beginning 
The set of characterstic spectra is saved as a dictionnary.


## Second part: Dye Recognition
This notebook is used to illustrate the results we get with the Aubusson tapestry. 
After indicating your parameters at the beginning, run it in order to get an interactive visualisation of the PCA
obtained on the PCCR values. 
On the bottom left, you can see which of the pixels are on the cluster you click on.
On the bottom righ, the mean spectrum is visible.

## Second part: Pigments comparison
This notebook is used to illustrate the results we get with the Iznik tiles comparison. 
All the pipeline is visible here and 3 different visualisations are presented : 
- a PCA
- a confusion matrix
- a dendrogram from agglomerative clustering process
 The folders in */data* can be used for testing.
You can compare the results you obtain with our results. 

Contact informations 
-------
- Corentin Cou <corentin.cou@institutoptique.fr>


License
-------
 
[CeCILL-B](LICENSE.txt)