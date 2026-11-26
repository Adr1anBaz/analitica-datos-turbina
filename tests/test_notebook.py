"""Ejecuta la exploración desde cero para detectar dependencias del estado del kernel."""

import unittest

import nbformat
from nbclient import NotebookClient

from scripts.datos import ROOT, verificar_directorio


class NotebookTests(unittest.TestCase):
    def test_ejecucion_limpia_desde_notebooks(self):
        notebook = nbformat.read(ROOT / "notebooks/01_carga_y_variables.ipynb", as_version=4)
        nbformat.validate(notebook)
        notebook.cells.append(nbformat.v4.new_code_cell("""
assert df.shape == (36733, 12)
assert df_entrenamiento.shape == (15039, 12)
assert set(df_entrenamiento['anio']) == {2011, 2012}
assert df['anio'].value_counts().to_dict() == {
    2011: 7411, 2012: 7628, 2013: 7152, 2014: 7158, 2015: 7384
}
assert df.isna().sum().sum() == 0
assert matriz_correlacion.shape == (10, 10)
assert 'anio' not in matriz_correlacion.columns
assert 'CO' not in matriz_correlacion.columns
assert abs(matriz_correlacion.loc['AT', 'NOX'] - (-0.600006)) < 0.000001
for year in range(2011, 2016):
    original = pd.read_csv(ruta_datos / f'gt_{year}.csv')
    unido = df.loc[df['anio'] == year].drop(columns='anio').reset_index(drop=True)
    pd.testing.assert_frame_equal(unido, original)
"""))
        NotebookClient(
            notebook,
            timeout=120,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT / "notebooks")}},
        ).execute()
        self.assertTrue(verificar_directorio())


if __name__ == "__main__":
    unittest.main()
