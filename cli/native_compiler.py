#!/usr/bin/env python3
"""
Untold Lang - Native Compiler (C Backend)
Generates optimized C code from Untold source
"""


class NativeCompiler:
    def __init__(self, output_path="output.c"):
        self.output_path = output_path
        self.code = []

    def generate_header(self):
        self.code.append("""/**
 * Untold Lang - Generated C Code
 * For maximum performance
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define UNTOLD_VERSION "2.1.1"

// Built-in types
typedef enum { UT_NUM, UT_TEXT, UT_BOOL, UT_LIST, UT_MAP, UT_NULL } UtType;
typedef struct { UtType type; void *value; } UtValue;
typedef struct { UtType type; int size; void *data; } UtList;
typedef struct { int size; char **keys; void **values; } UtMap;

// Memory management
void *ut_malloc(size_t size) {
    void *ptr = malloc(size);
    if (!ptr) {
        fprintf(stderr, "[Untold] Out of memory\\n");
        exit(1);
    }
    return ptr;
}

// Built-in functions
void ut_say(UtValue v) {
    switch (v.type) {
        case UT_TEXT: printf("%s", (char*)v.value); break;
        case UT_NUM: printf("%g", *(double*)v.value); break;
        case UT_BOOL: printf("%s", *(bool*)v.value ? "true" : "false"); break;
        case UT_NULL: printf("null"); break;
        default: printf("<value>"); break;
    }
    printf("\\n");
}

long long ut_len(UtValue v) {
    switch (v.type) {
        case UT_TEXT: return strlen((char*)v.value);
        case UT_LIST: return ((UtList*)v.value)->size;
        default: return 0;
    }
}

// Constant-time comparison (for security)
bool ut_secure_compare(const char *a, const char *b) {
    if (!a || !b) return false;
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    if (len_a != len_b) return false;

    unsigned char diff = 0;
    for (size_t i = 0; i < len_a; i++) {
        diff |= a[i] ^ b[i];
    }
    return diff == 0;
}

int main(int argc, char *argv[]) {
    printf("Untold Lang v%s - Native Compilation\\n", UNTOLD_VERSION);
    return 0;
}
""")

    def compile(self, source_file):
        self.generate_header()
        with open(self.output_path, "w") as f:
            f.write("\n".join(self.code))
        print(f"[untold] C code written to {self.output_path}")
        print("[untold] To compile: gcc -O2 -o program output.c -lm")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python native_compiler.py <input.ut> [output.c]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.c"

    compiler = NativeCompiler(output_file)
    compiler.compile(input_file)