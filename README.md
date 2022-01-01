<div id="top"></div>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/richmoolah/stuck-fish">
    <img src="misc/fish.jpg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">stuck-fish</h3>

  <p align="center">
    a simple chess interface and engine
    <br />
    <a href="https://github.com/richmoolah/stuck-fish"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/richmoolah/stuck-fish">View Demo</a>
    ·
    <a href="https://github.com/richmoolah/stuck-fish/issues">Report Bug</a>
    ·
    <a href="https://github.com/richmoolah/stuck-fish/issues">Request Feature</a>
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

[![Product Name Screen Shot][product-screenshot]](misc/stuck-fish.gif)

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With



* [python3](https://www.python.org/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)
* [python-chess](https://python-chess.readthedocs.io/en/latest/)
* [sqlite3](https://www.sqlite.org/index.html)
* [numpy](https://numpy.org/)
* [scikitlearn](https://scikit-learn.org/stable/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Install python3
   ```sh
   sudo apt-get update
   sudo apt-get install python3
   ```   

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/richmoolah/stuck-fish.git
   ```

2. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```

3. Run stuckfish.py
    ```sh
    python3 stuckfish.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Stuck-fish is a simple chess interface that ships with a stuck-fish bot that you can play against. When the application is started, you can simply select whether you want to play against another player or against
the stuck-fish bot.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Playable interface
- [x] First iteration of stuck-fish bot (heuristics-based)
- [ ] Update engine to store played games
    - [ ] Update engine to analyze games and tweak play

See the [open issues](https://github.com/richmoolah/stuck-fish/issues) for tracked issues.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Currently stuck-fish is a personal project used for learning but if you would like to contribute to it, please reach out at the contact below!

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Richard Xu - richardxu@uchicago.edu

Project Link: [https://github.com/richmoolah/stuck-fish](https://github.com/richmoolah/stuck-fish)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Thanks to python-chess for creating a FEN engine that I could use to visualize stuck-fish!

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/richmoolah/stuck-fish.svg?style=for-the-badge
[contributors-url]: https://github.com/richmoolah/stuck-fish/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/richmoolah/stuck-fish.svg?style=for-the-badge
[forks-url]: https://github.com/richmoolah/stuck-fish/network/members
[stars-shield]: https://img.shields.io/github/stars/richmoolah/stuck-fish.svg?style=for-the-badge
[stars-url]: https://github.com/richmoolah/stuck-fish/stargazers
[issues-shield]: https://img.shields.io/github/issues/richmoolah/stuck-fish.svg?style=for-the-badge
[issues-url]: https://github.com/richmoolah/stuck-fish/issues
[license-shield]: https://img.shields.io/github/license/richmoolah/stuck-fish.svg?style=for-the-badge
[license-url]: https://github.com/richmoolah/stuck-fish/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/richardxu5
[product-screenshot]: misc/stuck-fish.gif
