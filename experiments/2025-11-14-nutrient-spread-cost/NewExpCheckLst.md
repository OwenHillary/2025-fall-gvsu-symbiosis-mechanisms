
Checklist for making a new exp 

Step 1:

    Copy a prevoius EXP         :   +
    Rename                      :   +

    Delte old data in new file  :   +

Step 2:  (Changing scripts) 

    Gen-Slurm:
        Set new Parameters      :   +
    
    Run-Slurm:
        Change EXP_Slug!!!      :   +
        Update SEED!!!          :   +
    
Step 3: (Adding to git, we dont need to add thing 12 times)

    git add exp_name            : +
    git commit -m "Stuff"       : +
    git push owen owen          : +

Step 4: (HPC side)

    git pull owen owen          : +
    add symbulation to  config  : +

Step 5: (Analysis)

    Aggergate:
        edit time series feild  : +

    R:
        change EXP_SLUR         : +
        edit factors            : +


