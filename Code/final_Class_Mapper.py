class Final_Class:
    def __init__(self):
        # Mapping class IDs to custom labels
        self.class_mapping = {
            0: '1000Gen14', 1: '1000Gen14', 2: '1000Gen15', 3: '1000Gen15', 
            4: '1000Gen16', 5: '1000Gen16', 6: '1000Gen17', 7: '1000Gen17', 
            8: '100Gen11', 9: '100Gen11', 10: '100Gen12', 11: '100Gen12', 
            12: '100Gen14', 13: '100Gen14', 14: '100Gen15', 15: '100Gen15', 
            16: '100Gen16', 17: '100Gen16', 18: '100Gen17', 19: '100Gen17', 
            20: '10Gen11', 21: '10Gen11', 22: '10Gen12', 23: '10Gen12', 
            24: '20Gen11', 25: '20Gen11', 26: '20Gen12', 27: '20Gen12', 
            28: '20Gen15', 29: '20Gen15', 30: '20Gen16', 31: '20Gen16', 
            32: '20Gen17', 33: '20Gen17', 34: '500Gen11', 35: '500Gen11', 
            36: '500Gen13', 37: '500Gen13', 38: '500Gen14', 39: '500Gen14', 
            40: '500Gen15', 41: '500Gen15', 42: '500Gen16', 43: '500Gen16', 
            44: '500Gen17', 45: '500Gen17', 46: '50Gen13', 47: '50Gen13', 
            48: '50Gen15', 49: '50Gen15', 50: '50Gen16', 51: '50Gen16', 
            52: '50Gen17', 53: '50Gen17', 54: '5Gen11', 55: '5Gen11', 
            56: 'memo_2530', 57: 'memo_2530', 58: 'memo_2539_50', 
            59: 'memo_2539_50', 60: 'memo_2547', 61: 'memo_2547', 
            62: 'memo_2549', 63: 'memo_2549', 64: 'memo_2550', 
            65: 'memo_2550', 66: 'memo_2553', 67: 'memo_2554', 
            68: 'memo_2554', 69: 'memo_2555_100', 70: 'memo_2555_80', 
            71: 'memo_2555_80', 72: 'memo_2558', 73: 'memo_2559_500', 
            74: 'memo_2559_70', 75: 'memo_2559_70', 76: 'memo_2562_1000', 
            77: 'memo_2562_1000', 78: 'memo_2562_100', 79: 'memo_2562_100'
        }

    def map_classes(self, class_ids):
        mapped_class_ids = [self.class_mapping.get(class_ids)]
        return mapped_class_ids[0] if mapped_class_ids else None
