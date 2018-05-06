#ifndef __FAST_BIT_BOARD_H__
#define __FAST_BIT_BOARD_H__

#include <cstdint>
#include <functional>
#include <string>
#include <tuple>
#include <vector>
#include <pybind11/numpy.h>

class FastBitBoard {
public:
    FastBitBoard();
    FastBitBoard(const int rows, const int columns);
    FastBitBoard(const int rows, const int columns, const uint64_t blackBitBoard, const uint64_t whiteBitBoard);
    ~FastBitBoard();
    void applyNewMove(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor);
    bool isValidMove(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor);
    bool hasValidMove(const std::string& playerColor);
    bool isEndState();
    bool isEmptyPosition(const std::tuple<uint16_t, uint16_t>& position);
    std::vector<std::tuple<uint64_t, uint64_t> > listAllValidMoves(const std::string& playerColor);
    std::vector<std::tuple<uint64_t, uint64_t> > listAllEmptyPositions();
    std::vector<FastBitBoard> listAllNextStates(const std::string& playerColor);
    FastBitBoard nextBoardState(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor);
    pybind11::array_t<int64_t> asNumpyMatrix();

protected:
private:
    const uint16_t mRows;
    const uint16_t mColumns;
    uint64_t mBlackBitBoard;
    uint64_t mWhiteBitBoard;

    std::tuple<uint64_t, uint64_t> playersAndOpponentsBoard(const std::string& playerColor);
    bool isSameBoardState(const FastBitBoard& target);
    uint64_t generateInitialBoard(const std::uint16_t rows, const std::uint16_t columns, const std::string& color);
    uint64_t boardWithStoneAt(const std::tuple<uint16_t, uint16_t>& position);
    uint64_t generateFlipPattern(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor);
    uint64_t flipPatternVerticallyUp(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternVerticallyDown(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternHorizontallyLeft(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternHorizontallyRight(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyUpLeft(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonnalyUpRight(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyDownLeft(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyDownRight(const std::uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternForShifterDirection(const std::uint64_t& board, const std::string& playerColor,
        const std::function<uint64_t(const std::uint64_t&)> shifter, const std::uint64_t& mask);
    int64_t colorOf(std::tuple<uint16_t, uint16_t>& position);
};

#endif