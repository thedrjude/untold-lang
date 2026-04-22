#!/bin/bash
# Untold Lang Native Compiler (C Backend)
# Generates optimized C code from Untold source

set -e

usage() {
    echo "Usage: untold compile-c <input.ut> [output]"
    echo "  Compiles Untold to C for native performance"
    exit 1
}

[ -z "$1" ] && usage

INPUT="$1"
OUTPUT="${2:-${INPUT%.ut}.c}"

echo "[untold] Generating C code from $INPUT..."

# Generate C code header
cat > "$OUTPUT" << 'CHEADER'
/**
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
        fprintf(stderr, "[Untold] Out of memory\n");
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
    printf("\n");
}

long long ut_len(UtValue v) {
    switch (v.type) {
        case UT_TEXT: return strlen((char*)v.value);
        case UT_LIST: return ((UtList*)v.value)->size;
        default: return 0;
    }
}

// Hash functions
const char *ut_sha256(const char *data) {
    static char result[65];
    // Simplified - in production use OpenSSL
    snprintf(result, 65, "hash_%s", data);
    return result;
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
CHEADER

echo "[untold] C header generated"

# Extract program structure and generate main function
echo "" >> "$OUTPUT"
echo "// Program entry point" >> "$OUTPUT"
echo "int main(int argc, char *argv[]) {" >> "$OUTPUT"

# Parse and emit C code for each line
while IFS= read -r line; do
    # Skip comments
    [[ "$line" =~ ^[[:space:]]*// ]] && continue
    
    # start main() -> main
    if [[ "$line" =~ start\ main\(\)\ *\{ ]]; then
        echo "    // Program starts here" >> "$OUTPUT"
        continue
    fi
    
    # say("...")
    if [[ "$line" =~ say\("([^"]+)"\) ]]; then
        echo "    printf(\"${BASH_REMATCH[1]}\\n\");" >> "$OUTPUT"
    fi
    
    # let var = value
    if [[ "$line" =~ let\ ([a-zA-Z_][a-zA-Z0-9_]*)\ =\ (.+) ]]; then
        echo "    // Variable: ${BASH_REMATCH[1]} = ${BASH_REMATCH[2]}" >> "$OUTPUT"
    fi
    
    # lock CONST = value
    if [[ "$line" =~ lock\ ([A-Z_][A-Z0-9_]*)\ =\ (.+) ]]; then
        echo "    const char *${BASH_REMATCH[1]} = \"${BASH_REMATCH[2]}\";" >> "$OUTPUT"
    fi
    
    # fn name() -> type { ... }
    if [[ "$line" =~ fn\ ([a-zA-Z_][a-zA-Z0-9_]*)\(.+\)\ -\> ]]; then
        echo "    // Function: ${BASH_REMATCH[1]}" >> "$OUTPUT"
    fi
    
    # loop i in 0..N
    if [[ "$line" =~ loop\ ([a-zA-Z_][a-zA-Z0-9_]*)\ in\ ([0-9]+)\.\.([0-9]+) ]]; then
        echo "    for (int ${BASH_REMATCH[1]} = ${BASH_REMATCH[2]}; ${BASH_REMATCH[1]} < ${BASH_REMATCH[3]}; ${BASH_REMATCH[1]}++) {" >> "$OUTPUT"
    fi
    
    # Closing braces
    if [[ "$line" =~ ^[[:space:]]*\} ]]; then
        echo "    }" >> "$OUTPUT"
    fi
    
    # if conditions
    if [[ "$line" =~ if\ (.+)\ \{ ]]; then
        echo "    if (${BASH_REMATCH[1]}) {" >> "$OUTPUT"
    fi
    
    # return
    if [[ "$line" =~ return\ (.+) ]]; then
        echo "    return ${BASH_REMATCH[1]};" >> "$OUTPUT"
    fi
    
done < "$INPUT"

echo "    return 0;" >> "$OUTPUT"
echo "}" >> "$OUTPUT"

echo "[untold] C code written to $OUTPUT"
echo "[untold] To compile: gcc -O2 -o program $OUTPUT -lm"