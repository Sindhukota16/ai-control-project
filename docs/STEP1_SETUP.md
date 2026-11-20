# Step 1 (Day 1): Setup + the Docker playroom

**Time needed:** about 1.5 to 2 hours (most of it is installing things)
**Goal for today:** you run one command and see `Step 1 works!` on your screen.

> **How to read this guide**
>
> - Grey boxes like the one below are **commands**. You type (or copy-paste) them into the **terminal** and press **Enter**.
> - When you see **Windows** and **Mac**, only follow the one for your computer.
> - Don't skip steps. If something doesn't match what this guide says, stop and check the Troubleshooting section at the bottom.
>
> ```bash
> this is a command
> ```

---

## Part A: Install the tools (both of you do this, once)

### A1. Install Git (saves and shares our code)

- **Windows:** go to https://git-scm.com/download/win, download, and run the installer. Click **Next** on every screen (the default options are fine).
- **Mac:** open the **Terminal** app (press `Cmd + Space`, type `Terminal`, press Enter), then type:
  ```bash
  git --version
  ```
  If a popup asks to install "command line developer tools", click **Install** and wait.

### A2. Install Python (the language our code is written in)

- **Windows:** go to https://www.python.org/downloads/ and download Python 3.11 or newer.
  **IMPORTANT:** on the first screen of the installer, tick the box **"Add python.exe to PATH"**, then click **Install Now**.
- **Mac:** go to https://www.python.org/downloads/, download the macOS installer, and run it.

### A3. Install Docker Desktop (builds the locked playroom)

- Go to https://www.docker.com/products/docker-desktop/
- **Windows:** download the Windows version and install it. If it asks about **WSL 2**, say yes. Restart your computer if it asks.
- **Mac:** pick **Apple chip** (M1/M2/M3/M4) or **Intel chip**. Not sure which you have? Click the Apple menu > **About This Mac** and look at "Chip".
- Open **Docker Desktop** after installing. Skip the sign-in if you want (you don't need an account).
- Wait until the bottom-left corner says **Engine running** (green).

### A4. Install VS Code (where we write code and type commands)

- Go to https://code.visualstudio.com/, download it, and install it.

### A5. Check everything installed correctly

1. Open **VS Code**.
2. At the top menu, click **Terminal > New Terminal**. A panel opens at the bottom of the window. **This is the terminal. This is where you type every command in this guide.**
3. Type each of these and press **Enter** after each one:

   ```bash
   git --version
   ```
   ```bash
   docker --version
   ```
   - **Windows:**
     ```bash
     python --version
     ```
   - **Mac:**
     ```bash
     python3 --version
     ```

Each one should print a version number, like `Python 3.12.4`. If one says "not recognized" or "command not found", close VS Code completely, open it again, and retry. Still broken? See Troubleshooting.

---

## Part B: Create the GitHub repo (ONLY Sindhu does this)

### B1. Make sure you both have GitHub accounts
Sign up for free at https://github.com if you don't have one. Each person needs their own account.

### B2. Create the repo
1. On GitHub, click the **+** at the top right > **New repository**.
2. **Repository name:** `ai-control-project`
3. **Description:** `Benchmarking sandboxed execution and monitoring against sabotage in AI agents`
4. Choose **Private** (we make it public on Sunday).
5. **Do NOT** tick "Add a README file". Leave every other option as it is.
6. Click **Create repository**.
7. You'll see a page with a link ending in `.git`, like
   `https://github.com/YOUR-USERNAME/ai-control-project.git`. Copy it. You need it in Part C.

### B3. Add your friend
1. In the repo, click **Settings** (top bar of the repo page).
2. In the left menu, click **Collaborators**.
3. Click **Add people**, type your friend's GitHub username, and click **Add**.
4. Your friend gets an email. They must click **Accept invitation**.

---

## Part C: Get the project onto your computer (Sindhu)

### C1. Tell Git who you are (one time only)
In the VS Code terminal, type these, using **your** name and the email you used on GitHub:

```bash
git config --global user.name "Sindhu Kota"
```
```bash
git config --global user.email "your-github-email@example.com"
```

### C2. Download the empty repo

> **Lesson from Day 1:** `git clone` **creates the project folder for you**, inside whatever folder your terminal is in. Don't make the folder by hand. Clone into `C:\Projects` (Windows), **not** your Documents folder, because Documents is often synced to OneDrive and that caused confusion.

1. Make a Projects folder and go into it.
   - **Windows:**
     ```bash
     cd C:\
     ```
     ```bash
     mkdir Projects
     ```
     ```bash
     cd C:\Projects
     ```
     (If `mkdir` says the folder already exists, that's fine.)
   - **Mac:**
     ```bash
     mkdir -p ~/Projects && cd ~/Projects
     ```
2. Download the repo. On your GitHub repo page, click the green **Code** button and copy the link, then:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-control-project.git
   ```
   It may warn "You appear to have cloned an empty repository". **That's normal.** This command just created the folder `ai-control-project`.
3. Go into it:
   ```bash
   cd ai-control-project
   ```

### C3. Put the starter files in the folder

> **Lesson from Day 1:** when you unzip, Windows makes an outer folder (`ai-control-project-step1`) with the real project folder **inside** it. Copy what's inside the **inner** `ai-control-project` folder, not the outer one.

1. Download `ai-control-project-step1.zip`, right-click it, and choose **Extract All**.
2. Open the extracted folder, then open the `ai-control-project` folder **inside** it.
3. Select everything (`Ctrl + A`), copy (`Ctrl + C`), go to `C:\Projects\ai-control-project`, and paste (`Ctrl + V`).
4. Open the project in VS Code. Windows tends to open OneDrive by default, so either:
   - **File > Open Folder**, click the **address bar** at the top, type `C:\Projects\ai-control-project`, press **Enter**, then **Select Folder**, or
   - type this in the terminal:
     ```bash
     code -r C:\Projects\ai-control-project
     ```
   If it asks "Do you trust the authors?", click **Yes**.
5. On the left (the Explorer panel), check you can see:
   ```
   .env.example
   .gitignore
   README.md
   docs/
   sandbox/
   src/
   ```
   **Don't see `.gitignore` or `.env.example`?** Files starting with a dot can get missed when copying. Copy them again from the unzipped folder.
6. Open a new terminal: **Terminal > New Terminal**. The line should end in `C:\Projects\ai-control-project>`. **From now on, every command runs from here.**

> **PowerShell or Git Bash?** The top of the terminal panel says which one you're using (`powershell` or `bash`). Git, Docker, and Python commands work the same in both. But a few commands only work in one: `Copy-Item` and `$env:` are **PowerShell only**; `cp` and `ls -a` are **Git Bash** (PowerShell also accepts `cp`, but uses `ls -Force` instead of `ls -a`). If you see "command not found", this is usually why.

---

## Part D: Build and test the playroom (everyone)

### D1. Make sure Docker is running
Open **Docker Desktop** and wait for **Engine running**. Keep it open in the background.

### D2. Build the playroom
In the VS Code terminal (inside the `ai-control-project` folder), type:

```bash
docker build -t ai-control-sandbox ./sandbox
```

**What this does:** it reads `sandbox/Dockerfile` (the recipe) and builds a small Linux computer image called `ai-control-sandbox`. The first time takes 1 to 3 minutes because it downloads Python. It's done when you see your cursor again and there's no red `ERROR`.

### D3. Run the test
- **Windows:**
  ```bash
  python src/sandbox.py
  ```
- **Mac:**
  ```bash
  python3 src/sandbox.py
  ```

**What this does:** it starts the playroom with **no internet**, runs a few commands inside it, prints the results, and then deletes the playroom.

**You should see something like this:**
```
Starting the sandbox...

$ whoami
agent
(exit code: 0)

$ pwd
/workspace
...
$ cat secrets/api_key.txt
sk-FAKE-DO-NOT-USE-12345
...
Good: no internet inside the sandbox
(exit code: 0)

Sandbox stopped and removed. Step 1 works!
```

**What each line proves:**

| Output | What it means |
|---|---|
| `agent` | The robot is a normal user, not an admin. |
| `/workspace` | It starts inside its own folder. |
| `cat main.tf` shows the file | It can read the Terraform chore file. |
| `sk-FAKE-...` | The fake treasure is planted. Later we check whether it tries to leak it. |
| `Good: no internet` | The room is locked. Even a sneaky agent can't send anything out. |
| `Step 1 works!` | 🎉 Done. |

---

## Part E: Save your work to GitHub (Sindhu first)

Type these one at a time in the terminal:

```bash
git status
```
This lists the new files Git sees (shown in red). **Check that there's no `.env` file in the list.** (There shouldn't be one yet.)

```bash
git add .
```
This picks up all the files to save. (The dot means "everything here".)

```bash
git commit -m "Day 1: project setup and Docker sandbox"
```
This saves a snapshot with a short note.

```bash
git push -u origin main
```
This uploads it to GitHub. If a window pops up asking you to **sign in to GitHub**, click through and allow it.

> If you get `error: src refspec main does not match any`, type `git branch -M main`, then run the push command again.

Refresh your repo page on GitHub. You should see all the files and the README showing at the bottom. ✅

---

## Part F: Your friend's turn

Your friend does:
1. **Part A** (install tools)
2. Accepts the GitHub invitation (from B3)
3. **C1** (with *their own* name and email)
4. **C2**, using Sindhu's repo link. **Skip C3**: the files download automatically.
5. **File > Open Folder** > `C:\Projects\ai-control-project`, then **Terminal > New Terminal**
6. **Part D** (build and test)
7. Opens `docs/TEAM_NOTES.md`, ticks the Day 1 boxes, writes one thing they learned, then:
   ```bash
   git add .
   git commit -m "Day 1 notes from partner"
   git push
   ```
8. Sindhu then runs `git pull` to get those notes. **That's how you share work every day.**

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `git` / `python` / `docker` "not recognized" (Windows) | Close and reopen VS Code. If Python is still not found, reinstall it and tick **"Add python.exe to PATH"**. |
| `python` not found (Mac) | Use `python3` instead. |
| `Cannot connect to the Docker daemon` or `error during connect` | Docker Desktop isn't running. Open it and wait for **Engine running**. |
| `docker build` says `failed to read dockerfile` or `path "./sandbox" not found` | You're in the wrong folder (often the outer unzip folder). Open `C:\Projects\ai-control-project` (see C3) and try again. |
| `Copy-Item: command not found` | Your terminal is Git Bash, not PowerShell. Use `cp -r` instead, or copy with File Explorer. |
| `python: can't open file 'src/sandbox.py'` | Same thing: you're in the wrong folder. |
| Test prints `WARNING: internet is ON` | Something's wrong with the setup. Don't continue. Share the output with your partner (or Claude). |
| `git push` asks for a password | GitHub doesn't accept your normal password here. Use the sign-in popup, or install **GitHub Desktop**, sign in there once, and try again. |
| `Permission denied` on `git push` (friend) | The friend hasn't accepted the collaborator invite yet. Check email. |

---

## What you learned today

- **Docker image** = a recipe-built mini computer (`sandbox/Dockerfile` is the recipe).
- **Container** = a running copy of that image. We start a fresh one every time, so the agent can't leave anything behind.
- `--network none` = no internet. This is the "lock" on the playroom.
- `docker exec` = send a command into the running container. In Step 2, the AI agent sends its commands exactly this way.
- **Git** = saves snapshots of your work. **GitHub** = where you and your partner share those snapshots.

**Next (Day 2):** connect a real AI model so it can decide which commands to run in the playroom by itself.
