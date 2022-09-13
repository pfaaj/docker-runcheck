
<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pfaaj/docker-runcheck">
    <img src="images/logo.png" alt="Logo" width="400" height="400">
  </a>

  <h3 align="center">Docker runcheck</h3>

  <p align="center">
    Check available binaries in the used images before running an expensive and long docker build.
    <br />
    <a href="https://github.com/pfaaj/docker-runcheck"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/pfaaj/docker-runcheck/issues">Report Bug</a>
    ·
    <a href="https://github.com/pfaaj/docker-runcheck/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

+ Run docker-runcheck to validate your Dockerfile before attempting time-intensive docker builds. 

+ docker-runcheck contructs one or more containers (based on the mentioned images), without running any of them. We list the available binaries and if any run commands are detected that are not supported by the available binaries, an error will be returned.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started


We need the docker sdk and the dockerfile library
 
  ```sh
  pip install -r requirements.txt 
  ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
### Usage

You can run docker-runcheck with:

  ```sh
  python docker-runcheck.py
  ```

![](images/runcheck.gif)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- ROADMAP -->
## Roadmap

- [] List all available binaries
- [] List all mentioned binaries
- [] Check whether mentioned binaries are available


See the [open issues](https://github.com/pfaaj/docker-runcheck/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- For apt stuff, package info

git clone https://salsa.debian.org/apt-team/python-apt
cd python-apt
sudo apt install libapt-pkg-dev
python setup.py build

or alternatively https://help.launchpad.net/API/launchpadlib

or https://sources.debian.org/doc/api/ -> examples 
https://sources.debian.org/api/info/package/davfs2/1.5.2-1/ 
https://sources.debian.org/api/src/cowsay/3.03+dfsg1-4/cows/
-->

<!-- CONTRIBUTING 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- LICENSE -->
## License

Distributed under the MIT License. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Paulo Aragao - paulo.aragao.dev@gmail.com

Project Link: [https://github.com/pfaaj/docker-runcheck/](https://github.com/pfaaj/docker-runcheck)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS 
## Acknowledgments


<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/pfaaj/docker-runcheck.svg?style=for-the-badge
[contributors-url]: https://github.com/pfaaj/docker-runcheck/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pfaaj/docker-runcheck.svg?style=for-the-badge
[forks-url]: https://github.com/pfaaj/docker-runcheck/network/members
[stars-shield]: https://img.shields.io/github/stars/pfaaj/docker-runcheck.svg?style=for-the-badge
[stars-url]: https://github.com/pfaaj/docker-runcheck/stargazers
[issues-shield]: https://img.shields.io/github/issues/pfaaj/docker-runcheck.svg?style=for-the-badge
[issues-url]: https://github.com/pfaaj/docker-runcheck/issues
[license-shield]: https://img.shields.io/github/license/pfaaj/docker-runcheck.svg?style=for-the-badge
[license-url]: https://github.com/pfaaj/docker-runcheck/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/paulo-aragao
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
