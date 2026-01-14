The idea of this test is to use some sucessfull parameters from the previous run, but this time mess more with the sym parameters.

The Varabiles in this test were:
    NUTRIENT_INTERACTION_MULTIPLIER | 4x, 8x
    NUTRIENT_STEAL_PROP | .8, 1.0

    Host/Sym Min Cycles | 100/10, 100/25, 160/40

The results here are interesting as we still get desent amount of NOR but notabliy for the runs with shorter Host min cycles the averge complexity reached is lower when NSP is only .8.  Another key note here is the multiply of seems to have little effect on host complexity, this is likly due to the sym being able to reach repo cost within the alotted time frame with the lowest mult.