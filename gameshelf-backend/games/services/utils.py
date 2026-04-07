
class Utils:
    RATING_CATEGORIES = {
        1: 'Three', 2: 'Seven', 3: '12', 4: '16', 5: '18', 6: 'Eighteen',
        8: 'E', 9: 'E10', 10: 'T', 11: 'M', 12: 'AO', 13: 'Mature',
        14: 'CERO_A', 15: 'CERO_B', 16: 'CERO_C', 17: 'CERO_D', 18: 'CERO_Z',
        20: 'USK_0', 21: 'USK_6', 22: 'USK_12', 23: 'USK_16', 24: 'USK_18', 25: 'USK_18+',
        28: 'GRAC_Eight', 29: 'GRAC_Twelve', 30: 'GRAC_Sixteen', 31: 'GRAC_Eighteen',
        32: 'CLASS_IND_18',
        33: 'ACB_R18', 34: 'ACB_Mature', 35: 'ACB_Restricted', 37: 'ACB_Adults',
    }

    MATURE_THRESHOLDS = {
        'PEGI': ['Eighteen'],
        'ESRB': ['M', 'AO'],
        'CERO': ['CERO_Z'],
        'USK': ['USK_18'],
        'GRAC': ['GRAC_Eighteen'],
        'CLASS_IND': ['CLASS_IND_18'],
        'ACB': ['ACB_R18'],
    }

    REGION_RATINGS = {
        1: 'PEGI',        # europe
        2: 'ESRB',        # north_america
        3: 'PEGI',        # australia
        4: 'PEGI',        # new_zealand
        5: 'CERO',        # japan
        6: 'GRAC',        # china
        7: 'GRAC',        # asia
        8: 'IARC',          # worldwide
        9: 'GRAC',        # korea
        10: 'GRAC',       # brazil
    }