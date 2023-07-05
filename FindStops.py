#!/usr/bin/env python

import logging
import sys
import pathlib

import click
import ROOT

logging.basicConfig(
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

log = logging.getLogger(__name__)


@click.command
@click.argument("input", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("--tree", default="Events", help="Name of ROOT TTree")
@click.option("-d", "--debug", is_flag=True)
@click.option(
    "-o",
    "--output",
    default="FindStops.root",
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
)
def main(input: pathlib.Path, tree: str, debug: bool, output: pathlib.Path) -> None:
    if debug:
        log.setLevel(logging.DEBUG)

    log.info("Find STops to Neutralino")
    # ROOT.EnableImplicitMT()

    # load C++ routines
    log.debug("Loading C++ ...")
    ROOT.gInterpreter.AddIncludePath(str(pathlib.Path(__file__).parent))
    ROOT.gROOT.ProcessLine('#include "FindStops_inc.hxx"')
    ROOT.gROOT.ProcessLine('#include "PrintGenPart_inc.hxx"')

    log.debug("Opening %s", input)
    chain = ROOT.TChain(tree)
    nr_files = 0
    if input.is_dir():
        for file in input.glob("**/*.root"):
            chain.Add(f"root://eos.grid.vbc.ac.at/{file}")
            nr_files += 1
    else:
        chain.Add(f"root://eos.grid.vbc.ac.at/{input}")
        nr_files += 1
    log.info("Number of file: %d", nr_files)
    log.info("Number of events: %d", chain.GetEntries())

    df = ROOT.RDataFrame(chain)

    df = (
        df.Define(
            "STop_mask",
            "FindSTopToLSP(GenPart_genPartIdxMother,GenPart_pdgId)",
        )
        .Define("STop_pt", "GenPart_pt[STop_mask]")
        .Define("STop_eta", "GenPart_eta[STop_mask]")
        .Define("STop_phi", "GenPart_phi[STop_mask]")
        .Define("STop_mass", "GenPart_mass[STop_mask]")
        .Define("STop_vx", "GenPart_vx[STop_mask]")
        .Define("STop_vy", "GenPart_vy[STop_mask]")
        .Define("STop_vz", "GenPart_vz[STop_mask]")
        .Define(
            "STop_dlen",
            "STopDecayLen(STop_vx, STop_vy, STop_vz, GenPart_vx[0], GenPart_vy[0], GenPart_vz[0])",
        )
        .Define("STop_tau", "STopDecayTau(STop_pt, STop_eta, STop_mass, STop_dlen)")
    )

    df = (
        df.Define(
            "STop_svIdx", "STopMatchSV(STop_vx, STop_vy, STop_vz, SV_x, SV_y, SV_z)"
        )
        .Define("STop_nr_match", "Sum(STop_svIdx >= 0)")
        .Define("STop_nr", "STop_pt.size()")
        .Define("STop_dlen_match", "STop_dlen[STop_svIdx >= 0]")
        .Define("STop_sv_x", "Take(SV_x, STop_svIdx)")
        .Define("STop_sv_y", "Take(SV_y, STop_svIdx)")
        .Define("STop_sv_z", "Take(SV_z, STop_svIdx)")
    )
    # df.Display(["STop_nr_match"]).Print()

    # df = df.Filter("STop_nr_match > 0")

    # df = df.Range(0, 3)
    # df.Display(
    #     [
    #         "STop_svIdx",
    #         "STop_vx",
    #         "STop_vy",
    #         "STop_vz",
    #         "STop_dlen",
    #         "STop_sv_x",
    #         "STop_sv_y",
    #         "STop_sv_z",
    #     ]
    # ).Print()
    # ROOT.ForeachPrintGenPart(df)
    # sys.exit()

    histos = [
        df.Histo1D(("STop_pt", "P_{T}", 100, 0.0, 1000.0), "STop_pt"),
        df.Histo1D(("STop_eta", "#eta", 100, -5.0, 5.0), "STop_eta"),
        df.Histo1D(("STop_phi", "#phi", 100, -3.14156, 3.14156), "STop_phi"),
        df.Histo1D(("STop_dlen", "Decay length", 100, 0.0, 30.0), "STop_dlen"),
        df.Histo1D(("STop_tau", "Lifetime", 100, 0.0, 1e-9), "STop_tau"),
        df.Histo1D(("STop_nr_match", "Matched to SV", 5, -1.5, 3.5), "STop_nr_match"),
        df.Histo1D(("STop_nr", "Nr STop per event", 5, -1.5, 3.5), "STop_nr"),
        df.Histo1D(
            ("STop_dlen_match", "Decay length for matched Stop", 100, 0.0, 30.0),
            "STop_dlen_match",
        ),
    ]

    log.info("Writing %s", str(output))
    out = ROOT.TFile.Open(str(output), "RECREATE")
    for h in histos:
        h.Write()
    out.Close()


if __name__ == "__main__":
    main()
