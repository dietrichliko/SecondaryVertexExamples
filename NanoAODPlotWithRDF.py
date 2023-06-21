#!/usr/bin/env python

import logging
import pathlib

import click
import ROOT

logging.basicConfig(
    format="%(asctime)s - %(levelname)8s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

log = logging.getLogger(__name__)

# ReNanoAOD
# DEFAULT_INPUT = (
#     "/scratch-cbe/users/dietrich.liko/cache/user"
#     "/prhussai/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8"
#     "/crab_RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1_privateUL16nanoAPVv9/211124_194033/"
# )
DEFAULT_INPUT = (
    "/scratch-cbe/users/dietrich.liko/cache/mc"
    "/RunIISummer20UL16NanoAODAPVv9/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM"
    "/106X_mcRun2_asymptotic_preVFP_v11-v1"
)
DEFAULT_OUTPUT = "NanoAODPlotWithRDF.root"


@click.command
@click.option(
    "-i",
    "--input",
    default=DEFAULT_INPUT,
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    help="Input directory",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    default=DEFAULT_OUTPUT,
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    show_default=True,
)
@click.option(
    "--root-mt/--no-root-mt",
    default=True,
    help="Enable ROOT multithreading",
    show_default=True,
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug output",
    show_default=True,
)
@click.option(
    "--print-cols",
    is_flag=True,
    default=False,
    help="Print columns names",
    show_default=True,
)
def main(
    input: pathlib.Path,
    output: pathlib.Path,
    debug: bool,
    root_mt: bool,
    print_cols: bool,
):
    """Secondary vertex plots."""
    log.info("NanoAODPlotWithRDF")
    if root_mt:
        log.debug("Enable ROOT multithreading")
        ROOT.EnableImplicitMT()

    chain = ROOT.TChain("Events")
    nr_files = 0
    for file in input.glob("**/*.root"):
        chain.Add(str(file))
        nr_files += 1
    log.info("Found %d files", nr_files)

    df = ROOT.RDataFrame(chain)

    if print_cols:
        for name in df.GetColumnNames():
            print(f"{name} : {df.GetColumnType(name)}")

    # Filter events
    df_main = df.Filter("MET_pt>5")

    df = df.Define("SV_chi2_over_ndof", "SV_chi2/SV_ndof")

    histos = [
        df_main.Histo1D(("MET_pt", "MET", 100, 0.0, 1000.0), "MET_pt"),
        # df_main.Histo1D(("HT", "HT", 100, 0.0, 1000.0), "HT"),
        df.Histo1D(
            ("SV_ntracks", "Number of Secondary Vertex tracks", 20, -0.5, 19.5),
            "SV_ntracks",
        ),
        df.Histo1D(
            ("SV_charge", "Secondary Vertex charge", 21, -10.5, 10.5), "SV_charge"
        ),
        df.Histo1D(("SV_pt", "Secondary Vertex p_{t}", 100, 0.0, 500.0), "SV_pt"),
        df.Histo1D(("SV_mass", "Secondary Vertex p_{t}", 100, 0.0, 50.0), "SV_mass"),
        df.Histo1D(("SV_eta", "Secondary Vertex #eta", 100, -3.0, 3.0), "SV_eta"),
        df.Histo1D(("SV_phi", "Secondary Vertex #eta", 100, -3.0, 3.0), "SV_phi"),
        df.Histo1D(
            ("SV_dxy", "Secondary Vertex #Delta_{xy}", 100, -1.0, 10.0), "SV_dxy"
        ),
        df.Histo1D(
            ("SV_dlen", "Secondary Vertex decay length", 100, -1.0, 10.0), "SV_dlen"
        ),
        df.Histo1D(
            ("SV_pAngle", "Secondary Vertex angle", 100, 0.0, 6.28318530718),
            "SV_pAngle",
        ),
    ]

    log.info("Saving histograms to %s", output)
    out = ROOT.TFile(str(output), "RECREATE")
    for histo in histos:
        histo.Write()

    out.Close()


if __name__ == "__main__":
    main()
