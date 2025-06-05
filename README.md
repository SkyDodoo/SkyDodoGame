
# 🐦 SkyDodo

SkyDodo is a charming vertical platformer inspired by **Doodle Jump**, built using **Python** and **Pygame**.  
You play as an animated dodo bird that jumps from platform to platform as the world scrolls underneath.

## Team:
Heiß Annabell,
Lösch Laetitia, Ermel Alisa,
Glushenkova Mariia

## Repository:
The source code and assets for SkyDodo are maintained in our repository:
https://git-iit.fh-joanneum.at/itm24-bootcamp/skydodo
---

### 🎮 Features

- 🐤 Animated Dodo character (sprite sheet based)
- 🪵 Dynamic platforms that scroll and recycle
- 🌄 Parallax background layers for a polished look
- 💥 Gravity, collision detection, and smooth movement
- 📦 Modular structure: `player.py`, `platform.py`, `main.py`, `start.py`

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://gitlab.com/yourusername/skydodo.git
cd skydodo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the game
python main.py

### 📦 Folder Structure

```

SkyDodo/
├── assets/
│   ├── dodo\_sprite\_sheet.png
│   ├── background\_0.png
│   ├── background\_1.png
│   └── ...
├── main.py
├── player.py
├── platform.py
├── start.py
├── requirements.txt
└── README.md

````

---

### 🔧 Requirements

- Python 3.8 or newer
- Pygame 2.x+

Install dependencies:

```bash
pip install -r requirements.txt
````

---

### 🚀 Run the Game

```bash
python main.py
```

---

## Project Description
SkyDodo is designed as a smooth and engaging vertical scroller featuring:
### 🐤 Player Character:
* Sprite Animation: Uses sprite sheets with multiple animation states (idle, flying, eating) and cycles frames based on player actions.

* Movement & Physics: Handles horizontal movement and jumping with gravity applied for realistic vertical motion.

* Animation Control: Updates animation frames using a timer and flips the sprite depending on movement direction.

* Rendering & Collision: Draws the player on screen and provides a collision rectangle for interactions.
### Platforms:
* Procedural Generation & Recycling: Platforms spawn randomly with spacing checks to avoid overlaps, and are recycled when off-screen to create endless gameplay.

* Collision & Spacing Logic: Ensures fair distances between platforms vertically and horizontally.

* Visuals: Different images for static and moving platforms, with special ground rendering.

* Scrolling Effect: Platforms move down to simulate player ascent.

* Efficient Updates: Only moving platforms update positions each frame for performance.
Scrolling platforms that recycle as the player ascends.
* Visuals: Parallax background layers.
Mechanics: Gravity, collision detection, and player movement.

### 💥 Enemies:
* Spawns a specified number of enemies at random positions on the screen.

* Collision Avoidance: Ensures enemies don’t spawn inside or too close to platforms or other enemies, respecting minimum distances.

* Screen Boundaries: Enemies are spawned within the visible game area.

* Attempts Limit: Tries up to 1000 times to find valid spawn locations before stopping. Output: Returns a list of spawned enemy instances.

### 🏠 Start Screen
Displays the game’s start menu with background animation, UI buttons, and privacy info.

* Background: Animated sky and moving clouds create a dynamic backdrop.

* Player: Shows a flying player sprite looping across the screen as decoration.

### ▶️ Pause Menu
Created with a blocking pause screen loop using Pygame. It renders a translucent overlay on the game screen to visually indicate the paused state. The menu displays a title and two interactive buttons: Resume and Quit.
### 🧠 Planned Features

* [ ] Game over screen with restart option
* [ ] Score counter based on height
* [ ] Power-ups (e.g. wings, springs)
* [ ] Sounds and background music
* [ ] Falling enemies

---

### 🙌 Contributing

1. Fork this repository
2. Create your branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add cool feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

---

### 📃 License

MIT License © 2025
Made with 💙 by the SkyDodo Team

````

---

## ✅ 2. `requirements.txt`

```txt
pygame>=2.0.0
````

---

## ✅ 3. GitHub Repo Starter

To set it up:

1. Go to [GitLab](https://git-iit.fh-joanneum.at/itm24-bootcamp/) → New repository → Name it `SkyDodo`
2. Push from terminal:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/SkyDodo.git
git push -u origin main
```
