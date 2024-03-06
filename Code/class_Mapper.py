class ClassMapper:
    def __init__(self):
        self.class_mapping = {
            0: '1000gen14back', 1: '1000gen14front', 2: '1000gen15back', 3: '1000gen15front', 
            4: '1000gen16back', 5: '1000gen16front', 6: '1000gen17back', 7: '1000gen17front', 
            8: '100gen11back', 9: '100gen11front', 10: '100gen12back', 11: '100gen12front', 
            12: '100gen14back', 13: '100gen14front', 14: '100gen15back', 15: '100gen15front', 
            16: '100gen16back', 17: '100gen16front', 18: '100gen17back', 19: '100gen17front', 
            20: '10gen11back', 21: '10gen11front', 22: '10gen12back', 23: '10gen12front', 
            24: '20gen11back', 25: '20gen11front', 26: '20gen12back', 27: '20gen12front', 
            28: '20gen15back', 29: '20gen15front', 30: '20gen16back', 31: '20gen16front', 
            32: '20gen17back', 33: '20gen17front', 34: '500gen11back', 35: '500gen11front', 
            36: '500gen13back', 37: '500gen13front', 38: '500gen14back', 39: '500gen14front', 
            40: '500gen15back', 41: '500gen15front', 42: '500gen16back', 43: '500gen16front', 
            44: '500gen17back', 45: '500gen17front', 46: '50gen13back', 47: '50gen13front', 
            48: '50gen15back', 49: '50gen15front', 50: '50gen16back', 51: '50gen16front', 
            52: '50gen17back', 53: '50gen17front', 54: '5gen11back', 55: '5gen11front', 
            56: 'memo_2530back', 57: 'memo_2530front', 58: 'memo_2539_50back', 
            59: 'memo_2539_50front', 60: 'memo_2547back', 61: 'memo_2547front', 
            62: 'memo_2549back', 63: 'memo_2549front', 64: 'memo_2550back', 
            65: 'memo_2550front', 66: 'memo_2553back', 67: 'memo_2554back', 
            68: 'memo_2554front', 69: 'memo_2555_100back', 70: 'memo_2555_80back', 
            71: 'memo_2555_80front', 72: 'memo_2558back', 73: 'memo_2559_500back', 
            74: 'memo_2559_70back', 75: 'memo_2559_70front', 76: 'memo_2562_1000back', 
            77: 'memo_2562_1000front', 78: 'memo_2562_100back', 79: 'memo_2562_100front'
        }

    def map_classes(self, class_ids):
        mapped_class_ids = [self.class_mapping.get(class_ids)]
        return mapped_class_ids[0] if mapped_class_ids else None
