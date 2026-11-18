# Team notes

Our shared notebook. Add to it every day. Newest day at the top.

## How we work together (simple rules)

1. **Before you start working:** open the terminal in the project folder and run `git pull`
2. **After you finish:** run
   ```bash
   git add .
   git commit -m "short note about what you did"
   git push
   ```
3. Don't both edit the **same file** at the same time. Tell each other first.
4. Never put real API keys in any file except `.env`.
5. If something breaks, write it in "Problems we hit" below so the other person knows.

## Words we keep using

| Word | Simple meaning |
|---|---|
| Agent / untrusted model | The smart AI doing the chores. We don't fully trust it. |
| Monitor / trusted model | The smaller AI watching the agent and blocking bad actions. |
| Sandbox / container | The locked Docker playroom where the agent works. |
| Main task | The honest chore (e.g. fix a Terraform file). |
| Side task | The secret sneaky goal (e.g. leak the fake key). |
| Safety | How many sneaky attempts we caught. |
| Usefulness | How many honest chores still got done. |
| False positive | Monitor blocked an honest action by mistake. |

---

## Day 1 - Tue Nov 17: Setup + Docker playroom

**Goal:** both of us can run `src/sandbox.py` and see "Step 1 works!"

Checklist:
- [ ] Installed Git, Python, Docker Desktop, VS Code
- [ ] GitHub account ready, repo created (private), partner added
- [ ] Built the Docker image
- [ ] Ran `sandbox.py` and saw "Good: no internet inside the sandbox"
- [ ] Pushed to GitHub

What we learned:
-

Problems we hit:
-

## Day 2 - Wed Nov 18: Agent loop
(to fill in)

## Day 3 - Thu Nov 19: Tasks + LLM monitor
(to fill in)

## Day 4 - Fri Nov 20: Policy-tool monitor + experiments
(to fill in)

## Day 5 - Sat Nov 21: Results + charts
(to fill in)

## Day 6 - Sun Nov 22: Polish + submit
(to fill in)
