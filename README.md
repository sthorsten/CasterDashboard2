# R6 Caster Dashboard

![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/sthorsten/CasterDashboard2?include_prereleases&sort=semver)
![Docker](https://github.com/sthorsten/CasterDashboard2/workflows/Docker/badge.svg)
[![License](https://img.shields.io/github/license/sthorsten/CasterDashboard2)](LICENSE.md)


## ⚠️ Important Note
I am currently in the process of cleaning up some important parts of the code, updating dependencies, removing old code parts and changing the structure around a bit.

**Please be aware that this may break things!**

Once this process is complete, I will move to the first beta release, which should be more stable overall and easier to install and update (an updated guide on this will follow).


## 📝 Description

This is the repository for the new Rainbow Six Siege Caster Dashboard.
The dashboard aims to help Casters with production by providing easy-to-use and modular Overlays and control via a web dashboard.


## Features

### Matches
- Create, view, edit, share and manage matches
- Map Picks & Bans
- Operator Bans
- Round History (BombSpot, WinTeam, Opening Frag Team, Notes, Live Statistics)   

### Data Management
- Create, view and edit Teams (and their logos)
- No need to add teams every time you want to cast or produce a match

### League Administration

- Manage your league
- Add and edit sponsors
- Grant or revoke other users access to your league

### Statistics

- Map pick, ban and win rates
- BombSpot pick and win rates
- Filter for a specific league, season or team

### Overlays
- Show viewers match related data with the Start, InGame, Maps, Round overlays and more
- Show your social media tags, create polls and more*
- Leagues can easily get custom overlay styles


## 🚀 Installation

***This section is outdated and will be updated with the first beta release!***

The dashboard is available via multiple [Docker Images](https://github.com/sthorsten?tab=packages&repo_name=CasterDashboard2).

To install the complete dashboard on your machine, download the [docker-compose.yml](docker-compose.yml) file and edit the required parts marked by comments.

Start the stack by running `docker-compose up -d` in the directory you put the [docker-compose.yml](docker-compose.yml) in.

> **Note:** The parameter `-d` is optional and starts the stack in detached mode.

Alternatively you can use any docker management software, such as [Portainer](https://www.portainer.io/). 

Once the stack is running, you can  access the dashboard's admin page via `<yourdomain.example>/admin` and login with the default username `admin` and password `caster_dashboard_2`.

> **Note:** I recommend creating users manually from there and disable the default admin user!


## 🔨 Development setup

This project can be easily setup by using [Visual Studio Code](https://code.visualstudio.com/) as an IDE and utilizing [Docker](https://www.docker.com/) and VSCode's [Remote Containers](https://code.visualstudio.com/docs/remote/containers).

1. Make sure you have [Docker (Desktop)](https://docs.docker.com/engine/install/) and all necessary dependcies (such as WSL2 on Windows) installed.

2. Clone this repo via https `git clone https://github.com/sthorsten/CasterDashboard2.git` or ssh `git clone git@github.com:sthorsten/CasterDashboard2.git`

3. Open the `backend` and `frontend` folders seperately in VSCode. The first startup can take a while!

4. Copy the example environment files `.env.devcontainer` to `.env`

5. Install the required dependencies by running `poetry install` for the `backend` and `yarn install` for the frontend.

6. Make sure the included VSCode extensions are enabled in your workspace.

7. That's it. Happy coding ❤️


## 🖼️ Screenshots

*Coming soon...*


## Contributing

- If you want to help me develop the dashboard, create issues, comment, like and share the project. ❤️
- Ideas for new features, mean comments about what a mess my code is and other things are most welcome 😉
- If you know your way around in code, feel free to submit a pull request! 💾
- You can also get in touch with me via one of my social media channels 💬


### Translations

> **Note:** Translations are on hold for now.


## 🗒️ Changelog

Current Version: 2.1.0-alpha

**Note:** This release is not ready for production yet!

See the full [Changelog](CHANGELOG.md) for further information.