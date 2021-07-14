# Final Project: Air3D
<i>Make School SPD 1.5</i>

![VideoGameInfo](https://github.com/Kou-kun42/VideoGameInfo/blob/main/videogameinfo.png?raw=true)

### Overview

This is marketplace service that facilitates transactions between owners of 3D printers and users ("renters") who pay these owners to create specified products. Owners can create profiles and list products that they are willing to print and sell, and renters can browse products offered and reach out to owners to negotiate terms for a product. Additionally, renters can also provide detailed descriptions for their own bespoke products that skilled owners could create for them. This service is designed to accelerate the consumer 3D printing revolution by allowing everyone to partake in the joy of 3D printing, even those without knowledge of creating CAD files or working with 3D printers. For a deep dive into the validation for this idea, see (this Medium post)[https://medium.com/@gobindpuniani/air3d-accelerating-the-consumer-3d-printing-revolution-79aca3dd9eb] from one of the cofounders.

### Heroku Deployment

This app is deployed here:
https://air3d.herokuapp.com

Simply click the link above to start using Air3D today!

### Local Deployment

To launch this app on your local environment, clone this repository:

```
git clone https://github.com/Kou-kun42/Air3D.git
```

Then, set up a python virtual environment using:

```
python3 -m venv env
```

and then activate it:

```
source env/bin/activate
```

Next, install all the required packages:

```
pip3 install -r requirements.txt
```

Finally, launch the app:

```
python3 app.py
```
