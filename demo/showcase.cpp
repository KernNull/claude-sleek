// A small ring buffer, used to show off C++ colors.
#include <array>
#include <cstddef>
#include <iostream>

#define CAPACITY 8
#ifndef DEBUG_LOG
#define DEBUG_LOG 0
#endif

namespace demo {

template <typename T, std::size_t N = CAPACITY>
class Ring {
public:
    bool push(const T& item) {
        if (count_ == N) return false;
        data_[(head_ + count_++) % N] = item;
        return true;
    }

    T pop() {
        T item = data_[head_];
        head_ = (head_ + 1) % N;
        --count_;
        return item;
    }

private:
    std::array<T, N> data_{};
    std::size_t head_ = 0, count_ = 0;
};

}  // namespace demo

int main() {
    demo::Ring<int> r;
    for (int i = 0; i < 10; ++i) {
        if (!r.push(i * 2)) std::cout << "full at " << i << '\n';
    }
    return 0;
}
