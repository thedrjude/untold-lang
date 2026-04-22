package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func greet(name, greeting string) string {
    return fmt.Sprintf("%s, %s!", greeting, name)
}

func main() {
    result := add(5, 3)
    fmt.Printf("5 + 3 = %d\n", result)

    greeting := greet("Untold", "Hello")
    fmt.Println(greeting)

    square := func(x int) int { return x * x }
    fmt.Printf("Square of 7: %d\n", square(7))
}