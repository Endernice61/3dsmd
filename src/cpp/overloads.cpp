#include <cstdlib>
using std::string_literals::operator""s;

std::string operator*(std::string lhs, int times) {
	std::string out = "";
	for (;times > 0;--times) { out += lhs; }
	return out;
}
