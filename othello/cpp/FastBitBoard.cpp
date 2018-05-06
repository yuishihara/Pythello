#include "FastBitBoard.h"
#include <bitset>
#include <cassert>
#include <iostream>
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
namespace py = pybind11;

void printBitSet(const std::string& title, const uint64_t& pattern) {
   std::cout << title << ". Bit set: " << std::bitset<64>(pattern) << std::endl;
}

PYBIND11_MODULE(libfastbb, m)
{
    m.doc() = "libfastbb pybind11 fastbb plugin";

    py::class_<FastBitBoard>(m, "FastBitBoard")
        .def(py::init<>())
        .def(py::init<const int, const int>())
        .def("apply_new_move", &FastBitBoard::applyNewMove)
        .def("is_valid_move", &FastBitBoard::isValidMove)
        .def("has_valid_move", &FastBitBoard::hasValidMove)
        .def("is_end_state", &FastBitBoard::isEndState)
        .def("is_empty_position", &FastBitBoard::isEmptyPosition)
        .def("list_all_valid_moves", &FastBitBoard::listAllValidMoves)
        .def("list_all_empty_positions", &FastBitBoard::listAllEmptyPositions)
        .def("list_all_next_states", &FastBitBoard::listAllNextStates)
        .def("next_board_state", &FastBitBoard::nextBoardState)
        .def("as_numpy_matrix", &FastBitBoard::asNumpyMatrix);
}

namespace
{
    const std::string COLOR_BLACK = "black";
    const std::string COLOR_WHITE = "white";
    const uint64_t UP_DOWN_MASK = 0x00ffffffffffff00;
    const uint64_t LEFT_RIGHT_MASK = 0x7e7e7e7e7e7e7e7e;
    const uint64_t DIAGONAL_MASK = UP_DOWN_MASK & LEFT_RIGHT_MASK;
}

FastBitBoard::FastBitBoard() : FastBitBoard(8, 8)
{
}

FastBitBoard::FastBitBoard(const int rows, const int columns)
    : mRows(rows), 
      mColumns(columns) {
        mBlackBitBoard = generateInitialBoard(rows, columns, COLOR_BLACK);
        mWhiteBitBoard = generateInitialBoard(rows, columns, COLOR_WHITE);
}

FastBitBoard::FastBitBoard(const int rows, const int columns, const uint64_t blackBitBoard, const uint64_t whiteBitBoard)
    : mRows(rows), 
    mColumns(columns),
    mBlackBitBoard(blackBitBoard), 
    mWhiteBitBoard(whiteBitBoard) {
}

FastBitBoard::~FastBitBoard() {}

bool FastBitBoard::isValidMove(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor)
{
    if (!isEmptyPosition(move)) {
        return false;
    }
    return generateFlipPattern(move, playerColor) != 0;
}

void FastBitBoard::applyNewMove(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor)
{
    uint64_t flipPattern = generateFlipPattern(move, playerColor);
    if (flipPattern == 0) {
        return;
    }
    uint64_t moveBitBoard = boardWithStoneAt(move);
    if (playerColor == COLOR_BLACK) {
        mBlackBitBoard ^= (moveBitBoard | flipPattern);
        mWhiteBitBoard ^= flipPattern;
    } else {
        mWhiteBitBoard ^= (moveBitBoard | flipPattern);
        mBlackBitBoard ^= flipPattern;
    }
}

bool FastBitBoard::hasValidMove(const std::string& playerColor)
{
    return listAllValidMoves(playerColor).size() != 0;
}

bool FastBitBoard::isEndState()
{
    return (!hasValidMove(COLOR_BLACK) && !hasValidMove(COLOR_WHITE));
}

bool FastBitBoard::isEmptyPosition(const std::tuple<uint16_t, uint16_t>& position)
{
    uint64_t positionBitBoard = boardWithStoneAt(position);
    return (positionBitBoard & (mBlackBitBoard | mWhiteBitBoard)) == 0;
}

std::vector<std::tuple<uint64_t, uint64_t> > FastBitBoard::listAllValidMoves(const std::string& playerColor)
{
    std::vector<std::tuple<uint64_t, uint64_t> > moves;
    for (uint8_t row = 0; row < mRows; ++row) {
        for (uint8_t column = 0; column < mColumns; ++column) {
            std::tuple<uint64_t, uint64_t> move = std::make_tuple<uint64_t, uint64_t>(row, column);
            if (isValidMove(move, playerColor)) {
                moves.push_back(move);
            }
        }
    }
    return moves;
}

std::vector<std::tuple<uint64_t, uint64_t> > FastBitBoard::listAllEmptyPositions()
{
    std::vector<std::tuple<uint64_t, uint64_t> > positions;
    for (uint8_t row = 0; row < mRows; ++row) {
        for (uint8_t column = 0; column < mColumns; ++column) {
            std::tuple<uint64_t, uint64_t> position = std::make_tuple<uint64_t, uint64_t>(row, column);
            if (isEmptyPosition(position)) {
                positions.push_back(position);
            }
        }
    }
    return positions;
}

std::vector<FastBitBoard> FastBitBoard::listAllNextStates(const std::string& playerColor)
{
    std::vector<FastBitBoard> nextStates;
    for (uint8_t row = 0; row < mRows; ++row) {
        for (uint8_t column = 0; column < mColumns; ++column) {
            std::tuple<uint64_t, uint64_t> move = std::make_tuple<uint64_t, uint64_t>(row, column);
            if (!isEmptyPosition(move)) {
                continue;
            }
            FastBitBoard nextState = nextBoardState(move, playerColor);
            if (isSameBoardState(nextState)) {
                continue;
            }
            nextStates.push_back(nextState);
        }
    }
    return nextStates;
}

FastBitBoard FastBitBoard::nextBoardState(const std::tuple<uint16_t, uint16_t>& move, const std::string& playerColor)
{
    FastBitBoard nextBoard = FastBitBoard(mRows, mColumns, mBlackBitBoard, mWhiteBitBoard);
    nextBoard.applyNewMove(move, playerColor);
    return nextBoard;
}

bool FastBitBoard::isSameBoardState(const FastBitBoard& target) {
    return (mBlackBitBoard == target.mBlackBitBoard) && (mWhiteBitBoard == target.mWhiteBitBoard);
}

pybind11::array_t<int64_t> FastBitBoard::asNumpyMatrix()
{
    pybind11::array_t<int64_t> matrix(std::vector<ptrdiff_t>{8, 8}, new int64_t[mRows * mColumns]());
    for (uint8_t x = 0; x < mRows; ++x) {
        for (uint8_t y = 0; y < mColumns; ++y) {
            std::tuple<uint16_t, uint16_t> position = std::make_tuple(x, y);
            matrix.mutable_data()[x * mRows + y] = colorOf(position);
        }
    }
    return matrix;
}

int64_t FastBitBoard::colorOf(std::tuple<uint16_t, uint16_t>& position) {
    uint64_t mask = boardWithStoneAt(position);
    if ((mask & mBlackBitBoard) != 0) {
        return -1;
    } else if ((mask & mWhiteBitBoard) != 0) {
        return 1;
    } else {
        return 0;
    }
}

uint64_t FastBitBoard::generateInitialBoard(const uint16_t rows, const uint16_t columns, const std::string& color)
{
    uint16_t centerX = rows / 2;
    uint16_t centerY = columns / 2;
    if (color == COLOR_BLACK) {
        return boardWithStoneAt(std::make_tuple(centerX, centerY - 1)) 
            | boardWithStoneAt(std::make_tuple(centerX - 1, centerY));
    } else if (color == COLOR_WHITE) {
        return boardWithStoneAt(std::make_tuple(centerX, centerY)) 
            | boardWithStoneAt(std::make_tuple(centerX - 1, centerY - 1));
    } else {
        throw -1;
    }
}

uint64_t FastBitBoard::boardWithStoneAt(const std::tuple<uint16_t, uint16_t>& position)
{
    uint16_t row = std::get<0>(position);
    uint16_t column = std::get<1>(position);
    assert(row < mRows && column < mColumns);

    // Must cast to uint64_t or will be treated as 32bit(environment dependent)
    return ((uint64_t)1 << ((mRows - row - 1) * mRows + (mColumns - column - 1)));
}

uint64_t FastBitBoard::generateFlipPattern(const std::tuple<std::uint16_t, uint16_t>& move, const std::string& playerColor)
{
    uint64_t flipPattern = 0;
    if (!isEmptyPosition(move)) {
        return flipPattern;
    }

    uint64_t moveBitBoard = boardWithStoneAt(move);
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
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board << (this->mColumns);
    }, UP_DOWN_MASK);
}

uint64_t FastBitBoard::flipPatternVerticallyDown(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board >> (this->mColumns);
    }, UP_DOWN_MASK);
}

uint64_t FastBitBoard::flipPatternHorizontallyLeft(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board << (1);
    }, LEFT_RIGHT_MASK);
}

uint64_t FastBitBoard::flipPatternHorizontallyRight(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board >> (1);
    }, LEFT_RIGHT_MASK);
}

uint64_t FastBitBoard::flipPatternDiagonallyUpLeft(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board << (this->mColumns + 1);
    }, DIAGONAL_MASK);
}

uint64_t FastBitBoard::flipPatternDiagonnalyUpRight(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board << (this->mColumns - 1);
    }, DIAGONAL_MASK);
}

uint64_t FastBitBoard::flipPatternDiagonallyDownLeft(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board >> (this->mColumns - 1);
    }, DIAGONAL_MASK);
}

uint64_t FastBitBoard::flipPatternDiagonallyDownRight(const uint64_t& board, const std::string& playerColor)
{
    return flipPatternForShifterDirection(board, playerColor, [this](const uint64_t& board) -> uint64_t {
        return board >> (this->mColumns + 1);
    }, DIAGONAL_MASK);
}

uint64_t FastBitBoard::flipPatternForShifterDirection(const uint64_t& board, const std::string& playerColor,
    const std::function<uint64_t(const uint64_t&)> shifter, const uint64_t& mask)
{
    uint64_t flipPattern = 0;
    uint64_t shiftedMove = shifter(board);
    const std::tuple<uint64_t, uint64_t> boards = playersAndOpponentsBoard(playerColor);
    const uint64_t playerBoard = std::get<0>(boards);
    const uint64_t opponentBoard = std::get<1>(boards);
    const uint64_t maskedOpponentBoard = mask & opponentBoard;
    while ((shiftedMove != 0) && ((shiftedMove & maskedOpponentBoard) != 0)) {
        flipPattern |= shiftedMove;
        shiftedMove = shifter(shiftedMove);
    }
    if ((playerBoard & shiftedMove) == 0) {
        return 0;
    } else {
        return flipPattern;
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

