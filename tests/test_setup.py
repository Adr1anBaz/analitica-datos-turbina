import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.datos import COLUMNS, resumir_csv, sha256_bytes, verificar_hash
from scripts.descargar_datos import descargar


def csv_example(header=None, row=None):
    """Fixture artificial exclusivamente para pruebas del lector, no para análisis."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(COLUMNS if header is None else header)
    writer.writerow(["1"] * 11 if row is None else row)
    return output.getvalue().encode()


class SetupTests(unittest.TestCase):
    def test_csv_original_sin_preambulo(self):
        self.assertEqual(resumir_csv(csv_example()), {
            "rows": 1, "columns": 11, "missing_cells": 0,
        })

    def test_rechaza_encabezado_incorrecto(self):
        with self.assertRaisesRegex(ValueError, "Encabezado"):
            resumir_csv(csv_example(header=["otra"] + COLUMNS[1:]))

    def test_rechaza_columnas_reordenadas(self):
        with self.assertRaisesRegex(ValueError, "Encabezado"):
            resumir_csv(csv_example(header=list(reversed(COLUMNS))))

    def test_rechaza_ancho_incorrecto(self):
        with self.assertRaisesRegex(ValueError, "ancho"):
            resumir_csv(csv_example(row=["1"] * 10))

    def test_rechaza_faltantes_y_texto(self):
        for value in ("", "na", "texto"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "numérico"):
                resumir_csv(csv_example(row=[value] + ["1"] * 10))

    def test_rechaza_no_finitos(self):
        for value in ("NaN", "inf", "-inf"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "no finito"):
                resumir_csv(csv_example(row=[value] + ["1"] * 10))

    def test_hash_correcto_y_alterado(self):
        expected = sha256_bytes(b"original")
        verificar_hash(b"original", expected, "ejemplo")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            verificar_hash(b"alterado", expected, "ejemplo")

    def test_no_sobrescribe_archivo_existente_alterado(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gt_2011.csv"
            path.write_bytes(b"trabajo local")
            with patch("scripts.descargar_datos.urllib.request.urlopen") as network:
                with self.assertRaisesRegex(ValueError, "SHA-256"):
                    descargar(Path(directory))
                network.assert_not_called()
            self.assertEqual(path.read_bytes(), b"trabajo local")


if __name__ == "__main__":
    unittest.main()
