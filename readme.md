# Face authenticator

A face authenticator system with life proof verification using cloud points.

# Features

## Face recognition and life proof verification
### Life proof failed in tests with printed and smartphone photos.

<img align="center" style="margin-left:20px;" width="250" src="docs/test1.png">
<img align="center" style="margin-left:20px;" width="250" src="docs/test2.png">
<img align="center" style="margin-left:20px;" width="251" src="docs/test3.png">

### Life proof sucess in a test with a real person.

<img align="center" style="margin-left:20px;" width="321" src="docs/test5.png">
<img align="center" style="margin-left:20px;" width="400" src="docs/test4.png">

# Our cloud point generator

We used a mechanical pencil with a PCB board to make holes in a sheet of aluminum foil. Then, we fixed the punched aluminum foil in a cardboard box with adhesive tape. As light source we used a  smartphone flashlight.



<img align="center" style="margin-bottom: 15px;" src="docs/hardware3.png">
<img align="center" style="margin-left: 90px;" width="200" src="docs/hardware1.png">
<img align="center" style="margin-left: 100px;" width="366" src="docs/hardware2.png">

\* It's also possible to use infrared led with a camera without IR filter.

# Getting Started
## Prerequisites

```
sudo apt install cmake
sudo apt install g++
sudo apt install python3-dev
```

```
pip install -r requirements.txt
```
\* Developed on Python 3.6.9 
## Run
```
python main.py
```    

# Developers
* [Augusto Ribeiro Castro](https://github.com/GuttinRibeiro)
* Gustavo Alvim Gava
* [Mateus Rocha de Medeiros](https://github.com/mateus-rm) 
* [Matheus Carvalho Nali](https://github.com/MatheusNali)