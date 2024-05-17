# Class Enroller

#### Get your chromedriver based on your operating system. <a>href="https://googlechromelabs.github.io/chrome-for-testing/" Here </a>


<h1 align="center">
  <br>
  <a href="https://github.com/Abhinav-ranish/ASU-Selenium-ClassEnroller"><img src="https://raw.githubusercontent.com/Abhinav-ranish/ASU-Autologin/main/asu.ico" alt="ASU" width="200"></a>
  <br>
  Class Enroller - ASU
  <br>
</h1>

<h4 align="center">An automated class enroller for Arizona State University. Build with selenium (python) <a href="https://www.python.org/" target="_blank">Python</a>.</h4>

<p align="center">
  <a href="https://www.paypal.me/aranish911">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

[![screenshot](https://img.youtube.com/vi/SxLpP7ES3-o/0.jpg)](https://youtu.be/SxLpP7ES3-o)

## Key Features
* Cross-compatible (Mac, Unix, Windows)
* Scrape Data from classsearch.asu.edu.
* Checks Availability of classes -> saves the class as open and if Twilio is uncommented out sends a call to desired number
* Duo Push (Passcode) - Will need a new OTP every re-run. To Bypass this you will have to turn off 2fa. (Or Look into Session Cache Stuff)
* Autologins to your asu and enrolls you into the class.
* If you wanna use it for Linux/Mac Autologin script is in /autologin/autoopener.py change the executable from .... .exe to python autologin//autoopener.py
* Visit [AutoLogin](https://github.com/Abhinav-ranish/ASU-Autologin) for more documentation

## How to Use
To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Abhinav-ranish/ASU-ClassEnroller

# Go into the repository
$ cd ASU-ClassEnroller

# Set up a virtual environment
$ python -m venv env

# Install dependencies
$ pip install selenium twilio

# Add your Twilio Config (Only if you want Call notification aswell)
$ vim scraper.py 

# Add your ASU authentication details 
$ vim autoopenner.py

# Run the app
$ python scraper.py
```

> **Note**
> You will require a new Duo OTP every time you re-run.  &nbsp;&middot;&nbsp;
> All your credentials should be entered in autoopener.py  &nbsp;&middot;&nbsp;



## For Enquiries @ aranish@asu.edu 

## Download

Download the pre-build installer found in [Releases](https://github.com/Abhinav-ranish/Selenium-ClassEnroller/releases)


## Credits

This software uses the following open-source packages:

- [Selenium](https://www.selenium.dev/documentation/)
- [Python](https://www.python.org/downloads/)

## Related

[Auto Login](https://github.com/Abhinav-ranish/ASU-Autologin) - Python selenium script for auto-login ASU

## Support

<a href="https://paypal.me/aranish911" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


## License

MIT
Old files/ Class scraper has multiple class functionality but i haven't fixed the auto enroller for that.

---

> LinkdIn [abhinav_ranish](https://www.linkedin.com/in/abhinavranish/) &nbsp;&middot;&nbsp;
> GitHub [@abhinav-ranish](https://github.com/abhinav-ranish) &nbsp;&middot;&nbsp;
> Instagram [@abhinav.ranish](https://instagram.com/abhinav.ranish)



## Youtube Video - Outdated (Only has scraper)
[![Alt text](https://img.youtube.com/vi/Rb7f3m1Acos/0.jpg)](https://youtu.be/Rb7f3m1Acos)
