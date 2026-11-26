"""Verifica la estructura, ejecución completa, figuras embebidas y ausencia de fuga en Proyecto_Final_Turbina_Colab.ipynb."""

import unittest
import nbformat

from scripts.datos import ROOT, verificar_directorio


class ProyectoColabNotebookTests(unittest.TestCase):
    def test_notebook_colab_ejecutado_y_con_figuras(self):
        nb_path = ROOT / "notebooks" / "Proyecto_Final_Turbina_Colab.ipynb"
        self.assertTrue(nb_path.is_file(), "Falta notebooks/Proyecto_Final_Turbina_Colab.ipynb")

        nb = nbformat.read(nb_path, as_version=4)
        nbformat.validate(nb)

        code_cells = [c for c in nb.cells if c.cell_type == "code"]
        self.assertGreaterEqual(len(code_cells), 10)

        # Todas las celdas de código deben haber sido ejecutadas sin errores
        png_count = 0
        texto_total = []
        for idx, cell in enumerate(code_cells):
            self.assertIsNotNone(cell.get("execution_count"), f"Celda de código {idx} sin ejecutar")
            for out in cell.get("outputs", []):
                self.assertNotEqual(out.get("output_type"), "error", f"Error en celda {idx}: {out.get('evalue')}")
                data = out.get("data", {})
                if "image/png" in data:
                    png_count += 1
                if "text/plain" in data:
                    texto_total.append("".join(data["text/plain"]))
                if out.get("output_type") == "stream":
                    texto_total.append("".join(out.get("text", [])))

        # Debe contener al menos 10 figuras generadas y el mensaje final de pruebas aprobadas
        self.assertGreaterEqual(png_count, 10, f"Se esperaban >=10 figuras PNG, se encontraron {png_count}")
        salida_unida = "\n".join(texto_total)
        self.assertIn("TODAS LAS PRUEBAS DE INTEGRIDAD, ANTI-FUGA Y CORDURA FÍSICA PASARON EXITOSAMENTE.", salida_unida)

        # Los cinco CSV originales deben permanecer intactos tras la ejecución
        self.assertTrue(verificar_directorio())


if __name__ == "__main__":
    unittest.main()
