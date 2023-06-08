
# Mechanical Iris Web App
Full-stack web application that designs mechanical Irises. 

#### User Interface:
<p align="center">
  <img src="https://github.com/slehmann1/MechanicalIris/blob/main/SupportingInformation/Interface.gif?raw=true" alt="Interface Overview"/>
</p>

#### CAD Equivalent:
<p align="center">
  <img src="https://github.com/slehmann1/MechanicalIris/blob/main/SupportingInformation/Solidworks.gif?raw=true" alt="CAD Equivalent"/>
</p>

#### Final 3D-Printed Mechanical Iris:
<p align="center">
  <img src="https://github.com/slehmann1/MechanicalIris/blob/main/SupportingInformation/3DPrinted.gif?raw=true" alt="3D Printed Iris"/>
</p>


### Featureset Overview
Mechanical irises can be parameterized by the number of blades, their minimum and maximum aperture size, and both blade and pin sizes. Final iris designs are visualized and can be exported as DXF files for later modification in CAD programs like SolidWorks, Fusion 360 or CATIA. 

Geometry for the irises is determined by finding solutions to a series of non-linear equations; these equations are derived from [closed-loop equations from kinematic analysis](https://ocw.metu.edu.tr/pluginfile.php/3961/mod_resource/content/12/ch3/3-4.htm). 

### Architecture
This is a RESTful application, where all equations for iris designs are solved in the backend as well as generation of DXFs. 

#### Backend
Relies on Django REST framework, numpy, scipy, pytest, matplotlib, and ezDXF. 

#### Frontend
Uses React, TypeScript, JQuery, and Bootstrap. 
