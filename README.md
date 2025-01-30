# The EPQ project main directory
# Folders and Files Description
| Folders / Files | description |
| --- | --- |
| 📁 `music_recognition_main` | Folder that includes the main algorithm |
| 📁 `music_recognition_web_portal` | Folder that includes the interaction part (the website that serves the algorithm) |
| 📁 `Report` | The Final Report Source |
| 📁 `Presentation` | The Final Presentation Source |
| 📁 ~~`database`~~ | ~~The database folder~~ |
| 📁 ~~`songs`~~ | ~~The songs source folder + test set~~ |
| 🗄️ `requirements.txt` | packages and dependency required |
| 🗄️ `requirements_with_gui.txt` | packages and dependency required with graphical interface |
| 🗄️ `Dockerfile` | Containerized build instructions using docker |
| 🗄️ `docker-compose.yml` | Containerized build instructions using docker |

*Note: The* ~~crossed out~~ *folders are not included because it requires manual download*
# Instructions for building the software 
With docker and git install type in command line:
`git clone --recurse-submodules -j8 https://github.com/seabass6969/EPQ`
`sudo docker compose up -d --force-recreate --build`
