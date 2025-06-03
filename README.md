
# 🐦 SkyDodo

SkyDodo is a charming vertical platformer inspired by **Doodle Jump**, built using **Python** and **Pygame**.  
You play as an animated dodo bird that jumps from platform to platform as the world scrolls underneath.

## Team:
Heiß Annabell,
Lösch Laetitia, Ermel Alisa,
Glushenkova Mariia
---

### 🎮 Features

- 🐤 Animated Dodo character (sprite sheet based)
- 🪵 Dynamic platforms that scroll and recycle
- 🌄 Parallax background layers for a polished look
- 💥 Gravity, collision detection, and smooth movement
- 📦 Modular structure: `player.py`, `platform.py`, `main.py`, `start.py`

---

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
