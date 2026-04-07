
class Utils:    
    ORGANIZATIONS = {
        1: "PEGI",
        2: "ESRB",
        3: "CERO",
        4: "USK",
        5: "GRAC",
        6: "CLASS_IND",
        7: "ACB",
    }

    RATING_CATEGORIES = {
        # PEGI
        1: "Three",
        2: "Seven",
        3: "12",
        4: "16",
        5: "18",
        6: "Eighteen",  # ejemplo según IGDB
        # ESRB
        8: "E",
        9: "E10",
        10: "T",
        11: "M",
        12: "AO",
        13: "Mature",   # etc
        # CERO
        14: "CERO_A",
        15: "CERO_B",
        16: "CERO_C",
        17: "CERO_D",
        18: "CERO_Z",
        # USK
        20: "USK_0",
        21: "USK_6",
        22: "USK_12",
        23: "USK_16",
        24: "USK_18",
        25: "USK_18+", 
        # GRAC
        28: "GRAC_Eight",
        29: "GRAC_Twelve",
        30: "GRAC_Sixteen",
        31: "GRAC_Eighteen",
        # CLASS_IND
        32: "CLASS_IND_18",
        # ACB
        33: "ACB_R18",
        34: "ACB_Mature",
        35: "ACB_Restricted",
        37: "ACB_Adults",
    }