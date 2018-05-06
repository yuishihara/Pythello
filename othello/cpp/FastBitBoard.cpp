#include "FastBitBoard.h"
#include <cassert>
#include <iostream>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

PYBIND11_MODULE(libfastbb, m)
{
    m.doc() = "libfastbb pybind11 fastbb plugin";

    py::class_<FastBitBoard>(m, "FastBitBoard")
        .def(py::init<>())
        .def("is_valid_move", &FastBitBoard::isValidMove);
}

static
{
    static const string COLOR_BLACK = "black";
    static const string COLOR_WHITE = "white";
    static const uint64_t UP_DOWN_MASK = 0x00ffffffffffff00;
    static const uint64_t LEFT_RIGHT_MASK = 0x7e7e7e7e7e7e7e7e;
    static const uint64_t DIAGONAL_MASK = UP_DOWN_MASK & LEFT_RIGHT_MASK;
}

FastBitBoard::FastBitBoard(const uint16_t rows, const uint16_t columns, const uint64_t blackBitBoard, const uint64_t whiteBitBoard)
    : mRows(rows)
    , mColumns(columns)
    , mBlackBitBoard(blackBitBoard)
    , mWhiteBitBoard(whiteBitBoard)
{
}

FastBitBoard::~FastBitBoard() {}

bool FastBitBoard::isValidMove(const tuple<uint16_t, uint16_t>& move, const string& playerColor)
{
    cout << "Move[0]: " << get<0>(move) << endl;
    cout << "Color: " << playerColor << endl;
    return true;
}

bool FastBitBoard::applyNewMove(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor)
{
    uint64_t FastBitBoard::flipPattern = generateFlipPattern(move, playerColor);
}

bool FastBitBoard::hasValidMove(const std::string& playerColor)
{
}

bool FastBitBoard::isEndState()
{
}

bool FastBitBoard::isEmptyPosition(const std::tuple<uint16_t, uint16_t>& position)
{
}

bool FastBitBoard::listAllValidMoves(const std::string& playerColor)
{
}

bool FastBitBoard::listAllEmptyPositions()
{
}

bool FastBitBoard::listAllNextStates(const std::string& playerColor)
{
}

bool FastBitBoard::nextBoardState(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor)
{
}
bool FastBitBoard::asNumpyMatrix()
{
}

uint64_t FastBitBoard::generateInitialBoard(const uint16_t rows, const uint16_t columns, const std::string& playerColor)
{
    uint16_t centerX = rows / 2;
    uint16_t centerY = columns / 2;
    if (playerColor == COLOR_BLACK) {
        return boardWithStoneAt(centerX, centerY - 1) | boardWithStoneAt(centerX - 1, centerY)
    } else if (playerColor == COLOR_WHITE) {
        return boardWithStoneAt(centerX, centerY) | boardWithStoneAt(centerX - 1, centerY - 1)
    } else {
        throw - 1
    }
}

uint64_t FastBitBoard::boardWithStoneAt(const std::tuple<uint16_t, uint16_t>& position)
{
    uint16_t row = get<0>(position);
    uint16_t column = get<1>(position);
    assert(row < mRows && column < mColumns)

    return 1 << ((mRows - row - 1) * mRows + (mColumns - column - 1)));
}

uint64_t generateFlipPattern(const std::tuple<utint16_t, uint16_t>& move, const std::string& playerColor)
{
    uint64_t FastBitBoard::flipPattern = 0;
    if (!isEmptyPosition(move)) {
        return flipPattern;
    }

    moveBitBoard = boardWithStoneAt(move);
    flipPattern = flipPatternVerticallyUp(moveBitBoard, playerColor)
        | flipPatternVerticallyDown(moveBitBoard, playerColor)
        | flipPatternHorizontallyLeft(moveBitBoard, playerColor)
        | flipPatternHorizontallyRight(moveBitBoard, playerColor)
        | flipPatternDiagonallyUpLeft(moveBitBoard, playerColor)
        | flipPatternDiagonnalyUpRight(moveBitBoard, playerColor)
        | flipPatternDiagonallyDownLeft(moveBitBoard, playerColor)
        | flipPatternDiagonallyDownRight(moveBitBoard, playerColor);
    return flipPattern;
}

uint64_t FastBitBoard::flipPatternVerticallyUp(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternVerticallyDown(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternHorizontallyLeft(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternHorizontallyRight(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternDiagonallyUpLeft(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternDiagonnalyUpRight(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternDiagonallyDownLeft(const uint64_t& board, const std::string& playerColor)
{
}

uint64_t FastBitBoard::flipPatternDiagonallyDownRight(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(const uint64_t board, const std::string& playerColor, [](const uint64_t& board) -> uint64_t {
        return board >> (mColumns + 1);
    });
}

uint64_t FastBitBoard::flipPatternForShifterDirection(const uint64_t& board, const std::string& playerColor,
    const std::function<uint64_t(const uint64_t&)> shifter, const uint64_t& mask)
{
    uint64_t flipPattern = 0;
    uint64_t shiftedMove = shifter(board);
    std::tuple<uint64_t, uint64_t> boards = playersAndOpponentsBoard(playerColor);
    uint64_t playerBoard = get<0>(boards);
    uint64_t opponentBoard = get<1>(boards);
    uint64_t maskedOpponentBoard = mask & opponentBoard;
    while ((shiftedMove != 0) && (shiftedMove & maskedOpponentBoard != 0)) {
        flipPattern |= shiftedMove;
        shiftedMovve = shifter(shiftedMove);
    }
    if ((playerBoard & shiftedMove) == 0) {
        return 0;
    } else {
        return flipPattern
    }
}

std::tuple<uint64_t, uint64_t> FastBitBoard::playersAndOpponentsBoard(const std::string& playerColor)
{
    if (playerColor == COLOR_BLACK) {
        return std::make_tuple(mBlackBitBoard, mWhiteBitBoard);
    } else {
        return std::make_tuple(mWhiteBitBoard, mBlackBitBoard);
    }
}
