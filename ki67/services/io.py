import logging
from pathlib import Path
from typing import Dict, Union

import numpy as np
import pandas as pd
from skimage import io


class DataIO:
    """Unified slide data exporter/importer"""

    class Image:
        """Images IO"""

        def __init__(self, prefix: Union[str, Path], slide: str):
            self.logger = logging.getLogger(f'ki67.Exporter.Image:{slide}')
            self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)

        def filepath(self, name: str) -> Path:
            return self.prefix / f'{name}.png'

        def save(self, name: str, img: np.ndarray) -> Path:
            filepath = self.filepath(name)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            io.imsave(str(filepath), img)
            self.logger.info(f'Saved {filepath}')
            return filepath

        def load(self, name: str) -> np.ndarray:
            filepath = self.filepath(name)
            img = io.imread(str(filepath))
            self.logger.info(f'Loaded {filepath}')
            return img

    class Array:
        """Numpy Array IO"""

        def __init__(self, prefix: Union[str, Path], slide: str):
            self.logger = logging.getLogger(f'ki67.Exporter.Array:{slide}')
            self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)

        def filepath(self, name: str) -> Path:
            return self.prefix / f'{name}.npz'

        def save(self, name: str, array: np.ndarray) -> Path:
            filepath = self.filepath(name)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(str(filepath), arr=array)
            self.logger.info(f'Saved {filepath}')
            return filepath

        def load(self, name: str) -> np.ndarray:
            filepath = self.filepath(name)
            array = np.loads(str(filepath))['arr']
            self.logger.info(f'Loaded {filepath}')
            return array

    class MultiArray:
        """Multiple Numpy Arrays IO"""

        def __init__(self, prefix: Union[str, Path], slide: str):
            name = f'ki67.Exporter.MultiArray:{slide}'
            self.logger = logging.getLogger(name)
            self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)

        def filepath(self, name: str) -> Path:
            return self.prefix / f'{name}.npz'

        def save(self, name: str, **arrays: Dict[str, np.ndarray]) -> Path:
            filepath = self.filepath(name)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(str(filepath), **arrays)
            self.logger.info(f'Saved {filepath}')
            return filepath

        def load(self, name: str) -> Dict[str, np.ndarray]:
            filepath = self.filepath(name)
            arrays = np.loads(str(filepath))
            self.logger.info(f'Loaded {filepath}')
            return arrays

    class DataFrame:
        """Pandas Dataframe IO"""

        def __init__(self, prefix: Union[str, Path], slide: str):
            self.logger = logging.getLogger(f'ki67.Exporter.DataFrame:{slide}')
            self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)

        def filepath(self, name: str) -> Path:
            return self.prefix / f'{name}.gz.parquet'

        def save(self, name: str, df: pd.DataFrame, *, index=True) -> Path:
            filepath = self.filepath(name)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(str(filepath), compression='gzip', index=index)
            self.logger.info(f'Saved {filepath}')
            return filepath

        def load(self, name: str) -> pd.DataFrame:
            filepath = self.filepath(name)
            df = pd.read_parquet(str(filepath))
            self.logger.info(f'Loaded {filepath}')
            return df

    class TFRecord:
        """Tensorflow Records IO"""

        def __init__(self, prefix: Union[str, Path]):
            self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)

        def filepath(self, name: str) -> Path:
            return self.prefix / f'{name}.tfrecords'

    def __init__(self, prefix: Union[str, Path], slidename: str):
        """
        Parameters
        ----------
        prefix : Union[str, Path]
            the root directory, where all files should be placed
            (e.g. experiment run)
        slidename : str
            name of the reference slide, which will also a parent directory
        """

        self.prefix = prefix if isinstance(prefix, Path) else Path(prefix)
        self.prefix = self.prefix / slidename

        self.image = self.Image(self.prefix, slidename)
        self.array = self.Array(self.prefix, slidename)
        self.multiarray = self.MultiArray(self.prefix, slidename)
        self.dataframe = self.DataFrame(self.prefix, slidename)
        self.tfrecord = self.TFRecord(self.prefix)
