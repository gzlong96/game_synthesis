import numpy as np

def gen_button_n_light2():
    with open('b_n_l_2.txt', 'w') as log:
        for state in [[True, False], [False, True], [False, False]]:
            for act in [1,2]:
                new_state = [True, True]
                if act==1:
                    new_state[0] = not state[0]
                    new_state[1] = state[1]
                else:
                    new_state[0] = state[1]
                    new_state[1] = state[0]
                log.write(str(state) + '\t' + str(act) + '\t' + str(new_state) + '\n')

gen_button_n_light2()