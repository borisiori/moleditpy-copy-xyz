# Copy XYZ – MoleditPy Plugin

A lightweight plugin for [MoleditPy](https://github.com/HiroYokoyama/python_molecular_editor) that allows users to preview and copy molecular XYZ coordinates directly to the system clipboard.

Designed to simplify the transfer of molecular geometries to computational chemistry software such as ORCA.

## Features

- **Instant clipboard copying:** Copy molecular coordinates without creating or saving an XYZ file.
- **Coordinate preview:** Display the current molecular geometry in a convenient, read-only dialog.
- **High precision:** Export Cartesian coordinates with eight decimal places.
- **Charge and multiplicity:** Display molecular charge and estimated spin multiplicity in the dialog title.
- **Original atom symbols:** Preserve custom atom symbols from imported XYZ files when available.
- **Error handling:** Detect missing molecules or unavailable 3D coordinates.
- **MoleditPy integration:** Access the plugin directly from the application's Export menu.

## Requirements

- MoleditPy >= 5.0.0, < 6.0.0
- Python 3
- RDKit
- PySide6-Essentials

The plugin uses MoleditPy's existing plugin API and requires no external command-line tools.

## Installation

### Manual installation

1. Download [`copy_xyz.py`](https://github.com/borisiori/moleditpy-copy-xyz/blob/main/copy_xyz.py).
2. Copy the file into your MoleditPy plugins directory.
3. Restart MoleditPy.
4. Access **Copy XYZ Coordinates...** from the Export menu.

The plugin may also become available through MoleditPy's official Plugin Installer if accepted into its plugin registry.

## Usage

1. Open or create a molecule in MoleditPy.
2. Ensure that the molecule contains 3D coordinates.
3. Open the **Export** menu.
4. Select **Copy XYZ Coordinates...**.
5. The coordinates are automatically copied to the clipboard.
6. A dialog displays the coordinates for inspection or copying again.

Paste the coordinates directly into a molecular modeling program, text editor, or quantum chemistry input file.

## Example Output

```text
  O         0.00000000     0.00000000     0.11730000
  H         0.00000000     0.75720000    -0.46920000
  H         0.00000000    -0.75720000    -0.46920000
```

The plugin copies only the atomic symbols and Cartesian coordinates, without an XYZ atom-count header or comment line.

For ORCA calculations, users can paste the coordinates into an appropriate `* xyz charge multiplicity` block.

**Note:** The displayed spin multiplicity is estimated from RDKit radical-electron information and may not represent every electronic state. Users should verify charge and multiplicity independently before quantum chemistry calculations.

## Compatibility

Developed for MoleditPy 5.x using the official plugin context API.

## Version

**2026.11.01** — Initial release.

## Author

**borisiori**

GitHub: https://github.com/borisiori

## License

GNU Lesser General Public License v3.0 or later (LGPL-3.0-or-later).

See the `LICENSE` file for the complete license terms, once added to the repository.

## Acknowledgments

Thanks to HiroYokoyama for developing and maintaining MoleditPy and its extensible plugin ecosystem.
