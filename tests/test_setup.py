import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.datos import resumir_csv, sha256_bytes, verificar_hash
from scripts.descargar_datos import descargar


def csv_example(label="pos", width=171):
    output = io.StringIO()
    output.write("Comentario de procedencia\n\n")
    writer = csv.writer(output)
    writer.writerow(["class"] + [f"x{i}" for i in range(170)])
    writer.writerow([label] + ["na"] * (width - 1))
    return output.getvalue().encode()


class SetupTests(unittest.TestCase):
    def test_csv_con_preambulo(self):
        self.assertEqual(resumir_csv(csv_example()), {
            "rows": 1, "columns": 171, "classes": {"pos": 1}, "missing_cells": 170,
        })

    def test_csv_sin_encabezado(self):
        with self.assertRaisesRegex(ValueError, "encabezado"):
            resumir_csv(b"no es un dataset\n")

    def test_rechaza_ancho_incorrecto(self):
        with self.assertRaisesRegex(ValueError, "ancho"):
            resumir_csv(csv_example(width=170))

    def test_rechaza_etiqueta_incorrecta(self):
        with self.assertRaisesRegex(ValueError, "Etiqueta"):
            resumir_csv(csv_example(label="unknown"))

    def test_hash_correcto_y_alterado(self):
        expected = sha256_bytes(b"original")
        verificar_hash(b"original", expected, "ejemplo")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            verificar_hash(b"alterado", expected, "ejemplo")

    def test_no_sobrescribe_archivo_existente_alterado(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aps_failure_training_set.csv"
            path.write_bytes(b"trabajo local")
            with patch("scripts.descargar_datos.urllib.request.urlopen") as network:
                with self.assertRaisesRegex(ValueError, "SHA-256"):
                    descargar(Path(directory))
                network.assert_not_called()
            self.assertEqual(path.read_bytes(), b"trabajo local")


if __name__ == "__main__":
    unittest.main()
