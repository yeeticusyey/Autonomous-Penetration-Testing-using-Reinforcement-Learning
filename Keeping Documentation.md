# README-Phy

Made some modifications to the repo since I saw it empty, hope you don't mind. Let me know if you have any questions or errors setting things up

-- Phyllis 



I've added CyberBattleSim as a submodule, so we'll be using it more as a library as compared to modifying CyberBattleSim itself. All modifications should be done in the /Modifications folder.



## Downloading the Repo

Note that since CBS is submodules, when you clone this repo you should use:

```
git clone https://github.com/yeeticusyey/Autonomous-Penetration-Testing-using-Reinforcement-Learning.git --recursive
```

Else, the CyberBattleSim folder will be empty. If you have already cloned it and it's currently empty, use the command `git submodule update --init `



## Installing Jupyter Notebooks

This is needed to run your simulations and view them graphically

```bash
sudo apt-get install python3-pip
pip3 install jupter
jupyter notebook
```



## Installing CyberBattleSim

```bash
cd CyberBattleSim
./init.sh
```





## Keeping Documentation

You should have two main documents in this repo. 

1) README.md

   - Put your user guide. Make sure installation and usage instructions are included. 

2) CHANGELOG.md

   - This is mainly for housekeeping purposes so everyone can track progress and goals

   - There's no strict guide for format as long as it's easy to read, but if you're not sure how to format it, you and look here for inspiration: https://keepachangelog.com/en/1.0.0/

     

## Using the Demo

I've added a demo file for how I've added features outside CyberBattleSim. 



| Current File         | CBS Equivalent                       | Purpose                                                      |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| my_ctf.py            | cyberbattle/samples/toyctf.toyctf.py | Place your modified environment here manually to play around and test things out |
| cyberbattle_myctf.py | cyberbattle/_env/cyberbattle_env.py  | Defines the cyberbattle environment so you can call it from OpenAI gym in runme.ipynb |
| runme.ipynb          | notebooks/toyctf-random.ipynb        | Run your final simulation here                               |

In the progress of adding more features, you might need to add more files to the current ones that use modified functions from CBS. So learning how I've taken and modified these files for use outside CyberBattleSim might be helpful.

