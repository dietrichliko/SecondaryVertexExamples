#!/usr/bin/env python

import logging
import sys
import pathlib

import click
import ROOT
import ROOT.std as std

logging.basicConfig(
    format="%(asctime)s - %(levelname)8s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

log = logging.getLogger(__name__)

GEN_PART_VARS = [
    "GenPart_genPartIdxMother",
    "GenPart_pdgId",
    # "GenPart_pt",
    # "GenPart_eta",
    # "GenPart_phi",
    # "GenPart_mass",
    # "GenPart_status",
    # "GenPart_statusFlags",
]


@click.command
@click.argument("url")
@click.option("--tree", default="Events", help="Name of ROOT TTree")
@click.option("-f", "--first", default=0, help="First event to print")
@click.option("-l", "--last", default=10, help="Last event to print")
@click.option("-d", "--debug", is_flag=True)
def main(url: str, tree: str, first: int, last: int, debug: bool) -> None:
    "Pretty print the GenPart of NanoAOD"
    if debug:
        log.setLevel(logging.DEBUG)

    log.info("Pretty Print GenPart of NanoAOD")

    # load C++ routines
    log.debug("Loading C++ ...")
    ROOT.gInterpreter.AddIncludePath(str(pathlib.Path(__file__).parent))
    ROOT.gROOT.ProcessLine('#include "PrintGenPart_inc.hxx"')

    log.debug("Opening %s", url)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    input = ROOT.TFile.Open(url)
    ROOT.gErrorIgnoreLevel = -1
    t = input.Get(tree)
    if t is None:
        log.fatal("Could not find tree %s", tree)
        sys.exit()

    df = ROOT.RDataFrame(t)
    df = df.Range(first, last)

    log.debug("DefinePrintGenPart")
    ROOT.DefinePrintGenPart(df)


#    df.Define("dummy", f'PrintGenPart({",".join(GEN_PART_VARS)})')


if __name__ == "__main__":
    main()
