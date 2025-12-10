#include <iostream>
#include <cstdlib>
#include <string>
#define DEBUG 0

class Buffer {
	public:
		Buffer() {}

		Buffer& operator<<(char byte) {
			str += byte;
			#if DEBUG
			std::cout << flush();
			#endif
			return *this;
		}

		Buffer& operator<<(Buffer other) {
			str += other.getStr();
			#if DEBUG
			std::cout << flush();
			#endif
			return *this;
		}

		Buffer& operator<<(std::string other) {
			str += other;
			#if DEBUG
			std::cout << flush();
			#endif
			return *this;
		}

		Buffer& operator<<(int other) {
			str += std::to_string(other);
			#if DEBUG
			std::cout << flush();
			#endif
			return *this;
		}

		Buffer& operator<<(float other) {
			str += std::to_string(other);
			#if DEBUG
			std::cout << flush();
			#endif
			return *this;
		}

		std::string getStr() { return str; }

		std::string flush() {
			std::string temp = str;
			str = "";
			return temp;
		}
	private:
		std::string str = "";
};