
# 🐦 SkyDodo

SkyDodo is a charming vertical platformer inspired by **Doodle Jump**, built using **Python** and **Pygame**.  
You play as an animated dodo bird that jumps from platform to platform as the world scrolls underneath.

---

## 👥 Team

- Heiß Annabell  
- Lösch Laetitia  
- Ermel Alisa  
- Glushenkova Mariia

---

## 🖼️ Screenshots

| ![](./assets/images/screenshots/Screenshot%202025-06-05%20at%2011.54.46.png) | *Landing Page* |
|------------------------------------------------------------------------------|----------------|
| ![](./assets/images/screenshots/Screenshot%202025-06-05%20at%2011.54.52.png) | *Policy Statement* |
| ![](./assets/images/screenshots/Screenshot%202025-06-05%20at%2011.55.08.png) | *Game Over* |
| ![](./assets/images/screenshots/Screenshot%202025-06-05%20at%2011.55.14.png) | *Gameplay* |
| ![](./assets/images/screenshots/Screenshot%202025-06-05%20at%2011.55.36.png) | *Pause Menu* |

---

## 📁 Repository

- [GitHub](https://github.com/SkyDodoo/SkyDodoGame)
- [GitLab (FH JOANNEUM)](https://git-iit.fh-joanneum.at/itm24-bootcamp/skydodo)

---

## 🎮 Features

- 🐤 Animated Dodo character (sprite sheet-based)
- 🪵 Dynamic, recycling platforms
- 🌄 Parallax background layers
- 💥 Gravity, collisions, smooth player movement
- 📦 Modular architecture: `player.py`, `platform.py`, `main.py`, `start.py`

---

## 🧪 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/skydodo.git
cd skydodo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the game
python main.py
````

---

### 📂 Folder Structure

```
SkyDodo/
├── assets/
│   ├── dodo_sprite_sheet.png
│   ├── background_0.png
│   ├── background_1.png
│   └── ...
├── main.py
├── player.py
├── platform.py
├── start.py
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

* Python 3.8 or newer
* Pygame 2.x+

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Project Description

### 🐤 Player Character

* **Sprite Animation**: Uses sprite sheets with idle, flying, and eating states
* **Movement & Physics**: Gravity-based jumping and horizontal movement
* **Animation Control**: Frame-based updates and sprite flipping
* **Collision Detection**: With bounding rectangles for platforms and enemies

### 🪵 Platforms

* Procedural generation with spacing logic
* Recycling off-screen platforms for endless gameplay
* Distinct textures for static and special platforms
* Efficient update loop for moving elements only

### 💥 Enemies

* Spawned with collision and boundary checks
* Avoids overlapping with platforms
* Limited retry logic to prevent infinite loops

### 🏠 Start Screen

* Dynamic background
* Animated flying Dodo
* Policy statement button and stylish menu

### ⏸️ Pause Menu

* Semi-transparent overlay
* Interactive "Resume" and "Quit" buttons

---

## 🧪 Planned Features

* [ ] Game over screen with restart option
* [ ] Score counter (height-based)
* [ ] Power-ups (wings, springs)
* [ ] Background music and sounds
* [ ] Additional enemy types (falling, flying)

---

## 🛠️ Documented Bugfixing & Problem-Solving

We faced numerous challenges throughout development — from Git merge conflicts and sync issues to debugging platform collision logic and player physics.
Fixes included:

* UI responsiveness and layout issues
* Broken score display
* Scroll speed adjustments
* Player death detection
* Log-based debugging and testing sessions
  The team collaboratively resolved these with a shared mindset of experimentation and continuous improvement.

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch: `git checkout -b new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to your fork: `git push origin new-feature`
5. Submit a pull request 🎉

---

## 📃 License

MIT License © 2025
Made with 💙 by the SkyDodo Team

---

## 📦 `requirements.txt`

```txt
pygame>=2.0.0
```

---

## 🚀 GitHub Repo Starter Setup

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/SkyDodo.git
git push -u origin main
```