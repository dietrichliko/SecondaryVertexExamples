#ifndef FIND_STOPS_INC_HXX
#define FIND_STOPS_INC_HXX

#include "ROOT/RVec.hxx"

using namespace ROOT;

RVecB FindSTopToLSP(const RVecI &idxMother, const RVecI &pdg)
{
    std::size_t nr = idxMother.size();
    RVecB mask(nr, false);
    // Find the stops that have decayed in neutralinos
    for (std::size_t i = 0; i < nr; ++i)
    {
        if (pdg[i] == 1000022)
        {
            std::size_t j = idxMother[i];
            mask[j] = true;
            // std::cout << "Stop at " << j << std::endl;
        };
    };
    //    std::cout << "Nr stops: " << stop_idx.size() << std::endl;
    return mask;
};

RVecF STopDecayLen(const RVecF &vx, const RVecF &vy, const RVecF &vz, const float px, const float py, const float pz)
{
    RVecF dx = vx - px;
    RVecF dy = vy - py;
    RVecF dz = vz - pz;
    return sqrt(dx * dx + dy * dy + dz * dz);
};

RVecF STopDecayTau(const RVecF &pt, const RVecF &eta, const RVecF &mass, const RVecF &dlen)
{
    RVecF p = pt * cosh(eta);

    // beta = p / E
    // gamma = E / m
    // tau = l / ( beta * gamma * c)

    return dlen * mass / (p * 2.998e10);
}

RVecI STopMatchSV(const RVecF &gen_x, const RVecF &gen_y, const RVecF &gen_z, const RVecF &sv_x, const RVecF &sv_y, const RVecF &sv_z)
{
    const float kDistMax = 0.02;
    RVecI idx;
    std::size_t gen_n = gen_x.size();
    std::size_t sv_n = sv_x.size();
    // std::cout << "Nr Gen: " << gen_n << ", Nr SV: " << sv_n << std::endl;
    for (std::size_t i = 0; i < gen_n; ++i)
    {
        float min_d2 = kDistMax * kDistMax;
        int min_idx = -1;
        // std::cout << "Gen  " << i << ": " << gen_x[i] << " : " << gen_y[i] << " : " << gen_z[i] << std::endl;
        for (std::size_t j = 0; j < sv_n; ++j)
        {
            float d_x = gen_x[i] - sv_x[j];
            float d_y = gen_y[i] - sv_y[j];
            float d_z = gen_z[i] - sv_z[j];
            // std::cout << "SV  " << j << ": " << sv_x[j] << " : " << sv_y[j] << " : " << sv_z[j] << std::endl;

            if (abs(d_x) < kDistMax && abs(d_y) < kDistMax && abs(d_z) < kDistMax)
            {
                float d2 = d_x * d_x + d_y * d_y + d_z * d_z;
                if (d2 < min_d2)
                {
                    // std::cout << "Match " << i << " - " << j << " : " << min_d2 << std::endl;
                    min_d2 = d2;
                    min_idx = j;
                }
            }
        }
        // std::cout << "Gen " << i << ": " << min_idx << std::endl;
        if (std::find(idx.begin(), idx.end(), min_idx) == idx.end())
        {
            idx.push_back(min_idx);
        }
        else
        {
            idx.push_back(-1);
        }
    }
    int nr = 0;
    for (int i = 0; i < idx.size(); ++i)
    {
        if (idx[i] >= 0)
            ++nr;
    }
    std::cout << "Matches " << nr << std::endl;
    return idx;
}

#endif