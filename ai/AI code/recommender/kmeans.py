from sklearn.cluster import KMeans
import glob
import os
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
tqdm.pandas()
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import warnings
warnings.filterwarnings('ignore')

def main():
  # collect the file names
  num = 0
  file_names = []
  folder_path = '.../text_data/'
  txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
  for file_name in txt_files:
    print(os.path.basename(file_name))
    file_names.append(os.path.basename(file_name))
    num += 1

  # kmeans with clusters = 13
  num_clusters = 13
  kmeans = KMeans(n_clusters=num_clusters)
  kmeans.fit(X)
  labels = kmeans.fit_predict(X)

  # print the result with file name
  for i, file_name in enumerate(file_names):
    print(f"{file_name} belongs to cluster: {labels[i]}")

if __name__ == "__main__":
    main()

