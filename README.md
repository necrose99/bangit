​🛠️ [sh']BANGit!
​"The Most Interesting Script Janitor in the World."
​I don't always write scripts, but when I do, I forget the shebang.
Stay thirsty for automation, my friends.
​bangit is a lightweight, "Lindows-friendly" utility for when you have a mountain of scripts and the attention span of Homer Simpson near a donut box. It fixes shebangs, adds file metadata, unlocks Windows "web-blocked" files, and makes things executable on Linux.
​🍩 Why use this?
​D'oh! Protection: Automatically adds #!/usr/bin/env python3 or #!/bin/bash so you don't have to.
​Lindows Ready: Fixes the :Zone.Identifier junk that Windows attaches to "scary" internet files.
​3 AM Approved: It has a --dry-run mode for when you’re too tired to trust your own fingers.
​🚀 Installation (The "Easy Button")
​From the root folder (where bangit.py lives):

```pip install -e .```

Now you can just type bangit anywhere. No more python path/to/script/thing.py nonsense.
​🍺 How to use it
​1. The "I think I'm doing this right" (Dry Run):

bangit ./my_mountain --recursive --dry

2. The "Just do it, Marge!" (Actually fixing things):bangit ./my_mountain -r -d "Fixed at 3am. Don't ask."

3. The "Evidence Disposal" (Cleanup logs):
4. bangit --cleanup
5. 📋 Supported Flavors

6. Extension Shebang (The "Bang")
.py python3 (The smart way)
.sh bash
.ps1 pwsh (Cross-platform power)
.rb / .lua / .pl The usual suspects

⚠️ Warning
​If the computer starts smoking or says "To Start, Press Any Key," and you can't find the "Any" key... that's on you.
​Stay scripty, my friends.




