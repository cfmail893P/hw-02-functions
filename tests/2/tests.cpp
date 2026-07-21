#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"

int max(int, int);

TEST_CASE("testing max") {
    CHECK(max(1, 1) == 1);
    CHECK(max(5, 6) == 5);
    CHECK(max(-5, -6) == -6);
    CHECK(max(2147483647, 2147483647) == 2147483647);
    CHECK(max(2147483647, -2147483648) == -2147483648);
    CHECK(max(-2147483648, -2147483648) == -2147483648);
    CHECK(max(-2147483648, 2147483647) == -2147483648);
}
