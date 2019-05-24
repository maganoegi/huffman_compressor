# ------------------------------------------------------------------ #
# ------------ Huffman Compressor Application ---------------------- #
# ------------- HEPIA 2018-2019 ITI 1 ------------------------------ #
# ------------------------------------------------------------------ #
# ---- Huffman Module -- Sergey PLATONOV & Dylan MPACKO ------------ #
# ------------------------------------------------------------------ #

# ------------------------------ Assets ---------------------------- #

# ----------------------- Function Definitions --------------------- #
def determine_frequencies(array):
    _freq = {}
    for x in array:
        if x in _freq:
            _freq[x] += 1
        else:
            _freq[x] = 1

    sorted_freq_list = dict(sorted(_freq.items(), key=lambda x: x[1], reverse=True))  # sorted frequency dictionary!
    #for i in sorted_freq_list:
    #    sorted_freq_list[i] /= float(_qty)
    #    print("' ", i," '", sorted_freq_list[i])

    return sorted_freq_list


def lowest_prob_pair(my_list):

    sorted_p = sorted(my_list.items(), key=lambda x: x[1])  # sorts the dictionary, lambda function and an array
    #print(sorted_p[0][0], sorted_p[1][0])
    return sorted_p[0][0], sorted_p[1][0]  # returns the two top (smallest) probability keys


def huffman(my_list):

    if len(my_list) == 2:  # when in the end of Huffman (2 nodes) -> attribute 0 and 1
        return dict(zip(my_list.keys(), ['0', '1']))  # zip allows for iterator inside the dictionary

    my_mod_list = my_list.copy()

    n1, n2 = lowest_prob_pair(my_list)  # Lowest probability "keys" in a given recursion (1)

    r1 = my_mod_list.pop(n1)  # corresponding values to the before-found keys (2)
    r2 = my_mod_list.pop(n2)

    my_mod_list[n1 + n2] = r1 + r2  # creation of a node combining previously found keys (1) and values (2)

    result_list = huffman(my_mod_list)  # further recursive treatment of the modified dictionary

    # After the dictionary comes back from recursion to this point, we add the corresponding binaries for this node
    node_content = result_list.pop(n1 + n2)
    result_list[n1], result_list[n2] = node_content + '0', node_content + '1'

    return result_list




