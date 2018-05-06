#ifndef __FAST_BIT_BOARD_H__
#define __FAST_BIT_BOARD_H__

#include <cstdint>
#include <string>
#include <tuple>

class FastBitBoard {
public:
    FastBitBoard();
    ~FastBitBoard();
    bool isValidMove(const std::tuple<int, int>& move, const std::string& playerColor);
protected:
private:
    uint64_t mBlackBitBoard;
    uint64_t mWhiteBitBoard;
};

#endif