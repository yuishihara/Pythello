#include "FastBitBoard.h"
#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;
using namespace std;

PYBIND11_MODULE(libfastbb, m) {
    m.doc() = "libfastbb pybind11 fastbb plugin";

    py::class_<FastBitBoard>(m, "FastBitBoard")
        .def(py::init<>())
        .def("is_valid_move", &FastBitBoard::isValidMove);
}

FastBitBoard::FastBitBoard() : mBlackBitBoard(0), mWhiteBitBoard(0) { }

FastBitBoard::~FastBitBoard() { }

bool FastBitBoard::isValidMove(const tuple<int, int>& move, const string& playerColor) {
    cout << "Move[0]: " << get<0>(move) << endl;
    cout << "Color: " << playerColor << endl;
    return true;
}