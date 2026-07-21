#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"

int area(int);
int area(int, int);

TEST_CASE("testing are square overfload") {
    CHECK(area(1) == 1);
    CHECK(area(12) == 144);
    CHECK(area(73) == 5329);
    CHECK(area(10000) == 100000000);
    CHECK(area(46340) == 2147395600);
}

TEST_CASE("testing are rectangle overfload") {
    CHECK(area(1, 2) == 2);
    CHECK(area(46340, 46340) == 2147395600);
    CHECK(area(11, 31) == 341);
}
