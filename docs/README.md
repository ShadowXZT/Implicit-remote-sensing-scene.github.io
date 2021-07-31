Implicit Neural Representations for Large-scale Remote Sensing Scene

Problem statement:
Assume that we have got a 3D city model, which can be reconstructed by MVS from multiple satellite images. Given the 3D model and street-view images at several locations, we aim to render novel views at other locations continuously.


Data description:
1.	Top view satellite image. The red dot indicates the location for capturing the street view images.
2.	The corresponding 3D city model (mesh and texture), with pixel-wise segmentation annotations. Georeferenced to the top-view image and street view images.
3.	The corresponding street view images at coordinate (6063,4597) of the 3D model. The filenames of these images indicate the camera poses (location, pitch, fov and heading). 
4.	The corresponding 360 street view image
5.	Illustration of an initial idea on novel street view synthesis.




In Data_sample/panos.txt:

        Pano_ID,              Lat,               Lon,          Y in 3D model,     X in 3D model
  
        AXD-LhS8HF3v1XajBnV2nA, 60.1644797333783, 24.92898345052589, 4400.232103129849,  6056.963851299137

Pano_ID can be used to download the street view image;
Lat and Lon can be used to download the Street view image or the top-view satellite image
X and Y can be used to locate in the 3D mesh model and render the synthetic image


Mesh_render.py is a sample code for rendering the synthetic image. Using the street view API, we can get the corresponding real image.

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
