import pandas as pd
import openpyxl
from os import PathLike
from numpy import array_split

class Backend:
    df:pd.DataFrame
    cols:list[str]
    pools:list[pd.DataFrame]
    def __init__(self,path:str|PathLike):
        self.df = pd.read_excel(path)
        
        self.cols = ["Name","Firstname","Age","Weight","Club"]
    
    def run(self):
        pools = self.group_by_weight()
        
        self.pools = pools
        
        return pools

    def group_by_weight(self, min_size=4, max_size=6, threshold=2.0, break_threshold=5.0):
        """
        Groups rows by similar weight values.
        
        - If weights stay's within `threshold`, keep extending (up to max_size)
        - If weight exceeds `break_threshold`, start a new (even for 1-2 rows)
        """
        df = self.df[self.cols].sort_values('Weight').reset_index(drop=True)
        groups = []
        i = 0
        while i < len(df):
            start_weight = df.loc[i, 'Weight']
            j = i + 1

            # Continue extending the group
            while j < len(df):
                diff = df.loc[j, 'Weight'] - df.loc[j - 1, 'Weight']

                # Break if a large jump occurs
                if diff > break_threshold:
                    break
                
                # Stop extending if group gets large or weights diverge
                if (df.loc[j, 'Weight'] - start_weight) > threshold and (j - i) >= min_size:
                    break
                
                # Stop max size
                if (j - i) >= max_size:
                    break

                j += 1

            groups.append(df.iloc[i:j])
            i = j

        return groups

if __name__ == "__main__":
    b = Backend("test_in.xlsx")
    
    b.df.columns = b.cols+["n","n"]
    
    b.run()