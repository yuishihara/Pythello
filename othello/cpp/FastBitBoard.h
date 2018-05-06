#ifndef __FAST_BIT_BOARD_H__
#define __FAST_BIT_BOARD_H__

#include <cstdint>
#include <string>
#include <tuple>

class FastBitBoard {
public:
    FastBitBoard(const uint16_t rows, const uint16_t columns, const uint64_t blackBitBoard, const uint64_t whiteBitBoard);
    ~FastBitBoard();
    bool isValidMove(const std::tuple<utint16_t, uint16_t>& move, const std::string& const std::string& playerColor);
    bool applyNewMove(const std::tuple<utint16_t, uint16_t>& move, const std::string& const std::string& playerColor);
    bool hasValidMove(const std::string& const std::string& playerColor);
    bool isEndState();
    bool isEmptyPosition(const std::tuple<utint16_t, uint16_t>& position);
    bool listAllValidMoves(const std::string& const std::string& playerColor);
    bool listAllEmptyPositions();
    bool listAllNextStates(const std::string& const std::string& playerColor);
    bool nextBoardState(const std::tuple<utint16_t, uint16_t>& move, const std::string& const std::string& playerColor);
    bool asNumpyMatrix();

protected:
private:
    uint16_t mRows;
    uint16_t mColumns;
    uint64_t mBlackBitBoard;
    uint64_t mWhiteBitBoard;

    uint64_t generateInitialBoard(const uint16_t rows, const uint16_t columns);
    uint64_t boardWithStoneAt(const std::tuple<utint16_t, uint16_t>& position);
    uint64_t generateFlipPattern(const std::tuple<utint16_t, uint16_t>& move, const std::string& const std::string& playerColor);
    uint64_t flipPatternVerticallyUp(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternVerticallyDown(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternHorizontallyLeft(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternHorizontallyRight(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyUpLeft(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonnalyUpRight(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyDownLeft(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternDiagonallyDownRight(const uint64_t& board, const std::string& playerColor);
    uint64_t flipPatternForShifterDirection(const uint64_t& board, const std::string& playerColor,
        const std::function<uint64_t(const uint64_t&)> shifter, const uint64_t& mask);
};

#endif