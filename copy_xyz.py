#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XYZ Clipboard Plugin for MoleditPy
Shows the current 3D structure as XYZ coordinates and copies them to the clipboard
"""

import logging

PLUGIN_NAME = "Copy XYZ"
PLUGIN_VERSION = "2026.11.01"
PLUGIN_SUPPORTED_MOLEDITPY_VERSION = ">=5.0.0, <6.0.0"
PLUGIN_AUTHOR = "borisiori"
PLUGIN_LICENSE = "LGPL-3.0-or-later"
PLUGIN_DESCRIPTION = "Show the current 3D structure as XYZ coordinates in a dialog and copy them to the clipboard"
PLUGIN_DEPENDENCIES = ["rdkit", "PySide6-Essentials"]
PLUGIN_TAGS = ["File", "Visualization"]
PLUGIN_CONTEXT = None


def initialize(context):
    """Initialize the XYZ clipboard plugin."""
    global PLUGIN_CONTEXT
    PLUGIN_CONTEXT = context
    context.add_export_action(
        "Copy XYZ Coordinates...", lambda: copy_xyz_to_clipboard(context)
    )


def generate_atom_lines(mol):
    """Build the atom coordinate lines for a molecule, matching the core XYZ exporter format."""
    conf = mol.GetConformer()

    # Atom lines: keep dummy-atom symbols carried over from loaded XYZ files
    xyz_lines = []
    for i in range(mol.GetNumAtoms()):
        pos = conf.GetAtomPosition(i)
        atom = mol.GetAtomWithIdx(i)
        symbol = atom.GetSymbol()
        if atom.GetAtomicNum() == 0 and atom.HasProp("xyz_original_symbol"):
            symbol = atom.GetProp("xyz_original_symbol")
        xyz_lines.append(
            f"  {symbol:<5}{pos.x:>15.8f}{pos.y:>15.8f}{pos.z:>15.8f}"
        )

    return "\n".join(xyz_lines) + "\n"


def get_charge_and_multiplicity(mol):
    """Read charge and multiplicity using the same rules as the core XYZ exporter."""
    from rdkit import Chem
    from rdkit.Chem import Descriptors

    # Charge: prefer the value kept from the loaded XYZ file, else formal charge
    charge = 0
    if mol.HasProp("_xyz_charge"):
        charge = mol.GetIntProp("_xyz_charge")
    else:
        try:
            charge = Chem.GetFormalCharge(mol)
        except (RuntimeError, ValueError, AttributeError) as e:
            logging.warning("Could not compute formal charge: %s", e)

    # Multiplicity: radical electrons + 1, same rule as the core exporter
    multiplicity = 1
    try:
        multiplicity = Descriptors.NumRadicalElectrons(mol) + 1
    except (RuntimeError, ValueError, AttributeError) as e:
        logging.warning("Could not compute multiplicity: %s", e)

    return charge, multiplicity


def copy_xyz_to_clipboard(context):
    """Show the XYZ coordinates in a dialog and place them on the clipboard."""
    from PySide6.QtGui import QGuiApplication, QFont
    from PySide6.QtWidgets import (
        QDialog,
        QHBoxLayout,
        QLabel,
        QMessageBox,
        QPlainTextEdit,
        QPushButton,
        QVBoxLayout,
    )

    # Get the main window and current molecule
    mw = context.get_main_window()
    mol = context.current_molecule

    # Check if there's a molecule to export
    if not mol or mol.GetNumAtoms() == 0:
        QMessageBox.warning(
            mw,
            "No Molecule",
            "No molecule loaded. Please create or load a molecule first.",
        )
        return

    # Check if the molecule has 3D coordinates
    if mol.GetNumConformers() == 0:
        QMessageBox.warning(
            mw,
            "No 3D Structure",
            "The molecule has no 3D coordinates. Please generate a 3D structure first.",
        )
        return

    try:
        xyz_text = generate_atom_lines(mol)
        charge, multiplicity = get_charge_and_multiplicity(mol)
    except Exception as e:
        QMessageBox.critical(mw, "Copy Failed", f"Failed to build XYZ text:\n{e}")
        return

    # Copy to the clipboard right away so a single Ctrl+V is enough
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(xyz_text)

    # --- Preview dialog (charge/multiplicity shown in the title, not the text) ---
    dlg = QDialog(mw)
    dlg.setWindowTitle(
        f"{PLUGIN_NAME} - {mol.GetNumAtoms()} atoms, "
        f"chrg {charge}, mult {multiplicity} (copied to clipboard)"
    )
    dlg.resize(560, 420)

    layout = QVBoxLayout(dlg)

    hint = QLabel(
        "The coordinates below are already on the clipboard.\n"
        "The text is selected, so Ctrl+C copies it again at any time."
    )
    layout.addWidget(hint)

    # Read-only monospace view with the whole text pre-selected
    text_edit = QPlainTextEdit(xyz_text)
    text_edit.setReadOnly(True)
    text_edit.setFont(QFont("Courier New", 10))
    text_edit.selectAll()
    layout.addWidget(text_edit)

    btn_row = QHBoxLayout()
    btn_row.addStretch()

    copy_btn = QPushButton("Copy to Clipboard")
    copy_btn.setDefault(True)

    close_btn = QPushButton("Close")

    def _copy_and_confirm():
        clipboard.setText(xyz_text)
        copy_btn.setText("Copied!")
        if PLUGIN_CONTEXT is not None:
            PLUGIN_CONTEXT.show_status_message(
                "XYZ coordinates copied to clipboard", 3000
            )

    copy_btn.clicked.connect(_copy_and_confirm)
    close_btn.clicked.connect(dlg.accept)
    btn_row.addWidget(copy_btn)
    btn_row.addWidget(close_btn)
    layout.addLayout(btn_row)

    dlg.show()
    if PLUGIN_CONTEXT is not None:
        PLUGIN_CONTEXT.show_status_message(
            "XYZ coordinates copied to clipboard", 3000
        )


def run(mw):
    if not hasattr(mw, "plugin_manager"):
        return

    context = PLUGIN_CONTEXT
    if not context:
        return

    copy_xyz_to_clipboard(context)
