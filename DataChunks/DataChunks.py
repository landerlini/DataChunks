import ROOT 
import numpy as np 
import pandas as pd 
import root_numpy as rnp 
import root_pandas as rpd

class DataChunks:
  """
    Simple class to extend root_pandas loading a sample via stratification. 
    Given a list of input files, it creates an iterable DataChunks object 
    where at each iteration, the content of all (or up to a certain number) of 
    files concurs. The number of entries sampled from each file is proportional  
    to the number of rows in each file. 

    Example:

    ```
    datachunks = iter ( DataChunks ( 
          [ 'file_with_100_rows.root', 'file_with_900_rows.root' ], 
          chunksize=100 
        )
      )

    for iEpoch in range(1000):
      data = next ( datachunks ) 
    ```

    Loads a chunk of 100 entries of which 10 from `file_with_100_rows.root` and 90 from 
    `file_with_900_rows.root`.
  """
  def __init__ (self, files, chunksize, n_files=100000, key = None, **kwargs):
    """
      Creates a DataChunk object building the sample combining several root files. 

      Arguments
        files - list of strings
          List of file names to be read

        chunksize - int
          Total number of rows to be picked from the various files 

        n_files - int 
          Maximal number of randomly selected files to pick from in a single chunk. 
          Default: 100000 

        key - string or None
          Name of the TTree to be loaded. Can be None (default) is a single TTree
          is defined per TFile. 

        Other arguments are passed to root_numpy.root2array complementing the
        arguments: `file`, `treename`, `start`, `stop` defined by DataChunks. 

    """
    self._files  = list()
    self._n_files = n_files
    self._chunksize = chunksize
    self._ntot = 0 
    self._kwargs = kwargs
    for f in files: 
      key_ = key if key else None 
      if not key_:
        for key_ in rnp.list_trees ( f ) : break 
      root_file = ROOT.TFile.Open ( f ) 
      if not root_file: raise IOError ( "File % could not be opened" % f )
      root_tree = root_file.Get ( key_ ) 
      if not root_file: raise IOError ( "File % could not be opened" % f )
      entries = root_tree.GetEntries() 
      self._files . append ( (f, key_, entries) )
      self._ntot += entries 


  def __iter__ ( self ):
    while True:
      dsets = list()
      files = np.random.permutation(len(self._files))[:self._n_files]
      ntot = sum ( f[2] for f in self._files ) 
      for iFile in files:
        fname, key, maxEntries = self._files [ iFile ] 
        chunksize = int ( float (maxEntries) / ntot * self._chunksize )  
        start = np.random.randint ( 0, max(1, maxEntries - chunksize ) ) 
        stop = start + chunksize 
        dsets . append ( 
            rpd.readwrite.convert_to_dataframe (
                rnp.root2array ( fname, treename = key, start=start, stop=stop, **self._kwargs ) 
              ) 
            )

      yield ( pd.concat ( dsets ) ) 






