#ifndef PRINT_GEN_INC_HXX
#define PRINT_GEN_INC_HXX

#include "ROOT/RVec.hxx"
#include <iostream>

using namespace ROOT;

void PrintGenPart(const RVecI &genPartIdxMother,
                  const RVecI &pdgId,
                  const RVecF &pt,
                  const RVecF &eta,
                  const RVecF &phi,
                  const RVecF &mass,
                  const RVecF &vx,
                  const RVecF &vy,
                  const RVecF &vz,
                  const RVecI &status,
                  const RVecI &statusFlags)
{

    std::cout << std::string(113, '-') << std::endl;
    std::cout << "!  Idx ! Mth !     PDG !  St !  Flags !        pt !       eta !   phi !   mass !       vx !       vy !       vz !" << std::endl;
    std::cout << std::string(113, '-') << std::endl;
    for (unsigned int i = 0; i < genPartIdxMother.size(); ++i)
    {
        std::cout << "! " << std::setw(3) << i << " ! ";
        if (genPartIdxMother[i] >= 0)
        {
            std::cout << std::setw(3) << genPartIdxMother[i] << " ! ";
        }
        else
        {
            std::cout << "    ! ";
        }
        std::cout << std::setw(8) << pdgId[i] << " ! ";
        std::cout << std::setw(3) << status[i] << " ! ";
        std::cout << "0x" << std::setw(4) << std::setfill('0') << std::hex << std::uppercase << statusFlags[i] << std::dec << std::setfill(' ') << " ! ";
        std::cout << std::setw(9) << std::fixed << std::setprecision(2) << pt[i] << " ! ";
        std::cout << std::setw(9) << eta[i] << " ! ";
        std::cout << std::setw(5) << phi[i] << " ! ";
        std::cout << std::setw(6) << mass[i] << " ! ";
        std::cout << std::setw(8) << std::setprecision(4) << vx[i] << " ! ";
        std::cout << std::setw(8) << vy[i] << " ! ";
        std::cout << std::setw(8) << vz[i] << " !" << std::endl;
    };
    std::cout << std::string(113, '-') << std::endl;
};

template <class T>
void ForeachPrintGenPart(T &df)
{
    df.Foreach(PrintGenPart,
               {"GenPart_genPartIdxMother",
                "GenPart_pdgId",
                "GenPart_pt",
                "GenPart_eta",
                "GenPart_phi",
                "GenPart_mass",
                "GenPart_vx",
                "GenPart_vy",
                "GenPart_vz",
                "GenPart_status",
                "GenPart_statusFlags"});
};
#endif